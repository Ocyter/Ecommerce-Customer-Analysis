"""Rebuild the self-contained, synthetic Order Review Power BI project; no external services."""
import base64
import csv
import io
import json
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent
OUT = HERE / "project"
REPORT = OUT / "OrderReview.Report"
MODEL = OUT / "OrderReview.SemanticModel"
DEFINITION = REPORT / "definition"
S = "https://developer.microsoft.com/json-schemas/fabric/"
R = S + "item/report/definition/"


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def schema(uri, **data):
    return {"$schema": uri + "/schema.json", **data}


def read_csv(path):
    return list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8"))))


# Each Power Query import is a literal snapshot of the same source CSV.
# The small fixture stays portable: no local paths, internet, accounts or credentials.
inputs = {"Customers":"outputs/customers_clean.csv", "Orders":"outputs/reporting_fact.csv",
          "Quarantine":"outputs/quarantine.csv", "Reconciliation":"outputs/reconciliation.csv",
          "RawOrders":"data/orders.csv"}
numbers = {"amount_ngn", "order_row", "rows", "known_amount_ngn", "missing_amount_rows"}
measures = {
    "Orders":{
        "Completed Orders":'COALESCE(CALCULATE(COUNTROWS(Orders), KEEPFILTERS(Orders[order_status] = "completed")), 0)',
        "Reported Amount NGN":'COALESCE(CALCULATE(SUM(Orders[amount_ngn]), KEEPFILTERS(Orders[order_status] = "completed")), 0)'},
    "RawOrders":{
        "Input Rows":"COUNTROWS(RawOrders)",
        "Missing Amount Rows":"COUNTBLANK(RawOrders[amount_ngn])",
        "Raw Known Amount NGN":"SUM(RawOrders[amount_ngn])"},
    "Quarantine":{"Rejected Rows":"COUNTROWS(Quarantine)"},
    "Reconciliation":{
        "Routed Rows":"SUM(Reconciliation[rows])",
        "Routed Known Amount NGN":"SUM(Reconciliation[known_amount_ngn])",
        "Row Difference":"[Input Rows] - CALCULATE([Routed Rows], REMOVEFILTERS(Reconciliation))",
        "Known Amount Difference NGN":"[Raw Known Amount NGN] - CALCULATE([Routed Known Amount NGN], REMOVEFILTERS(Reconciliation))"}}

def model_table(name, src):
    source = SOURCE / src
    fields = list(read_csv(source)[0])
    encoded = base64.b64encode(source.read_bytes()).decode("ascii")
    mtypes = ", ".join('{"%s", %s}' % (f, "Int64.Type" if f in numbers else "type text") for f in fields)
    # Missing numeric values must remain null; empty text conversion is explicit.
    m = ["let", f'    Csv = Csv.Document(Binary.FromText("{encoded}", BinaryEncoding.Base64), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
         '    Headers = Table.PromoteHeaders(Csv, [PromoteAllScalars=true]),']
    numeric = ', '.join(json.dumps(f) for f in fields if f in numbers)
    m += [f'    Blanks = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, {{{numeric}}}),' if numeric else '    Blanks = Headers,',
          f'    Typed = Table.TransformColumnTypes(Blanks, {{{mtypes}}}, "en-US")', 'in', '    Typed']
    return {"name":name,"columns":[{"name":f,"dataType":"int64" if f in numbers else "string","sourceColumn":f,
            "summarizeBy":"none"} for f in fields],
            "partitions":[{"name":name,"mode":"import","source":{"type":"m","expression":m}}],
            **({"measures":[{"name":k,"expression":v,"formatString":"#,0;(#,0);0"} for k,v in measures[name].items()]} if name in measures else {})}

def projection(kind, entity, field):
    return {"field":{kind:{"Expression":{"SourceRef":{"Entity":entity}},"Property":field}},"queryRef":entity+"."+field}

def literal(v):
    return {"expr":{"Literal":{"Value":v}}}

def visual(page, name, kind, title, pos, **roles):
    x,y,w,h,order=pos
    cfg={"visualType":kind, "query":{"queryState":{r:{"projections":[projection(*arg) for arg in args]} for r,args in roles.items()}},
         "visualContainerObjects":{"title":[{"properties":{"show":literal("true"),"text":literal("'"+title+"'")}}]}}
    write(DEFINITION/"pages"/page/"visuals"/name/"visual.json",schema(R+"visualContainer/1.0.0",name=name,
          position={"x":x,"y":y,"width":w,"height":h,"z":order,"tabOrder":order},visual=cfg))

def check_fixture():
    data={k:read_csv(SOURCE/v) for k,v in inputs.items()}
    raw=data["RawOrders"]; fact=data["Orders"]; keys={r["customer_id"]:r["region"] for r in data["Customers"]}
    comp=[r for r in fact if r["order_status"]=="completed"]
    assert len(keys)==len(data["Customers"])==4 and len(fact)==5 and len(comp)==3
    assert all(r["customer_id"] in keys for r in fact)
    assert [(reg,sum(keys[r["customer_id"]]==reg for r in comp),sum(int(r["amount_ngn"]) for r in comp if keys[r["customer_id"]]==reg))
            for reg in sorted(set(keys.values()))]==[("North",2,28000),("South",0,0),("West",1,24000)]
    assert len(raw)==sum(int(r["rows"]) for r in data["Reconciliation"])==12
    assert sum(int(r["amount_ngn"] or 0) for r in raw)==sum(int(r["known_amount_ngn"]) for r in data["Reconciliation"])==122500
    assert sum(r["amount_ngn"]=="" for r in raw)==1 and len(data["Quarantine"])==7
    assert sorted((r["disposition"], int(r["rows"])) for r in data["Reconciliation"])==[("outside_reporting_scope",2),("quarantined",7),("reported",3)]

def build():
    check_fixture()
    (HERE/"measures.dax").write_text("// Report model measures by table. DAX engine execution requires Power BI Desktop.\n" +
        "\n".join(f"\n// {table}\n" + "\n\n".join(f"{name} = {expr}" for name,expr in group.items())
                    for table,group in measures.items()) + "\n", encoding="utf-8")
    write(OUT/"OrderReview.pbip",schema(S+"pbip/pbipProperties/1.0.0",version="1.0",artifacts=[{"report":{"path":"OrderReview.Report"}}],
          settings={"enableAutoRecovery":True}))
    write(REPORT/"definition.pbir",schema(S+"item/report/definitionProperties/2.0.0",version="4.0",datasetReference={"byPath":{"path":"../OrderReview.SemanticModel"}}))
    write(MODEL/"definition.pbism",schema(S+"item/semanticModel/definitionProperties/1.0.0",version="1.0",settings={}))
    write(MODEL/"model.bim",{"compatibilityLevel":1567,"name":"OrderReview","model":{"culture":"en-US","sourceQueryCulture":"en-US",
        "defaultPowerBIDataSourceVersion":"powerBI_V3","tables":[model_table(k,v) for k,v in inputs.items()],
        "relationships":[{"name":"d14f555a-0031-471f-be43-11c389fe245e","fromTable":"Orders","fromColumn":"customer_id",
        "toTable":"Customers","toColumn":"customer_id","fromCardinality":"many","toCardinality":"one","crossFilteringBehavior":"oneDirection"}]}})
    write(DEFINITION/"version.json",schema(R+"versionMetadata/1.0.0",version="2.0.0"))
    write(DEFINITION/"report.json",schema(R+"report/1.0.0",themeCollection={},layoutOptimization="None"))
    pages=[("reported","Completed orders | synthetic"),("quality","Data quality | full extract")]
    write(DEFINITION/"pages"/"pages.json",schema(R+"pagesMetadata/1.0.0",pageOrder=[p for p,t in pages],activePageName="reported"))
    for page,title in pages:
        write(DEFINITION/"pages"/page/"page.json",schema(R+"page/1.0.0",name=page, displayName=title, width=1040,height=640,displayOption="FitToPage"))
    col=lambda t,f:("Column",t,f)
    m=lambda t,f:("Measure",t,f)
    visual("reported","region","slicer","Filter by customer region",(20,20,240,285,0),Values=[col("Customers","region")])
    visual("reported","value","clusteredBarChart","Completed order value by region (NGN)",(280,20,730,285,1),
           Category=[col("Customers","region")],Y=[m("Orders","Reported Amount NGN")])
    visual("reported","summary","tableEx","Completed orders and value | excludes pending and cancelled",(20,330,990,270,2),
           Values=[col("Customers","region"),m("Orders","Completed Orders"),m("Orders","Reported Amount NGN")])
    visual("quality","source","tableEx","Raw input | checks against all routed rows",(20,20,1000,145,0),
        Values=[m("RawOrders","Input Rows"),m("RawOrders","Missing Amount Rows"),m("Reconciliation","Row Difference"),m("Reconciliation","Known Amount Difference NGN")])
    visual("quality","routes","tableEx","Where the input went | full extract",(20,190,535,420,1),
        Values=[col("Reconciliation","disposition"),m("Reconciliation","Routed Rows"),m("Reconciliation","Routed Known Amount NGN")])
    visual("quality","defects","tableEx","Quarantined rows by primary issue",(570,190,450,420,2),
        Values=[col("Quarantine","issue"),m("Quarantine","Rejected Rows")])
    # Ensure every visual binding resolves to an actual model field of the declared kind.
    model=json.loads((MODEL/"model.bim").read_text())["model"]
    fields={(t["name"],k,i["name"]) for t in model["tables"] for k,group in [("Column","columns"),("Measure","measures")] for i in t.get(group,[])}
    for f in DEFINITION.rglob("visual.json"):
        vis=json.loads(f.read_text())["visual"]
        for role in vis["query"]["queryState"].values():
            for binding in role["projections"]:
                kind,field=next(iter(binding["field"].items()))
                assert (field["Expression"]["SourceRef"]["Entity"],kind,field["Property"]) in fields
    # The download is built in Pages CI; run the same command locally for an identical archive.
    with zipfile.ZipFile(HERE/"OrderReview-PowerBI.zip","w") as z:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():
                meta=zipfile.ZipInfo(str(p.relative_to(OUT)),(2020,1,1,0,0,0))
                z.writestr(meta,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED)
        z.writestr(zipfile.ZipInfo("README.md",(2020,1,1,0,0,0)),(HERE/"README.md").read_bytes(),compress_type=zipfile.ZIP_DEFLATED)
    print("Built two report pages and six visuals; all data bindings and fixture controls passed.")

if __name__=="__main__":
    build()
