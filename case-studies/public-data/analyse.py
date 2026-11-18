"""Rebuild published aggregates from two pinned UCI archives. Python 3.10+, openpyxl."""
from pathlib import Path
from collections import Counter, defaultdict
from decimal import Decimal as D
from datetime import date
from urllib.request import urlopen
import hashlib, zipfile, io, csv, argparse, json
from openpyxl import load_workbook

HERE=Path(__file__).resolve().parent
SOURCES={
    'bike':('275/bike+sharing+dataset','b70182d0d0508e9abbb79306ce5c0cec34869000f8220175ac83d11dbe845401'),
    'retail':('352/online+retail','f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b')}
def archive(name,cache):
    url,sha=SOURCES[name]
    path=cache/(name+'.zip')
    if not path.exists():
        path.write_bytes(urlopen('https://archive.ics.uci.edu/static/public/'+url+'.zip',timeout=120).read())
    assert hashlib.sha256(path.read_bytes()).hexdigest()==sha, f'{name}: source changed; review new archive'
    return zipfile.ZipFile(path)
def output(folder,name,rows):
    with (HERE/folder/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n'); w.writeheader(); w.writerows(rows)
def metrics(folder,d):
    (HERE/folder/'checks.json').write_text(json.dumps(d,indent=2,sort_keys=True,default=str)+'\n')

def bike(z):
    def read(name):
        return list(csv.DictReader(io.TextIOWrapper(z.open(name),encoding='utf-8-sig')))
    hours,days=read('hour.csv'),read('day.csv')
    by_date=defaultdict(Counter); series=defaultdict(Counter); keys=set()
    for r in hours:
        d,hr,work=r['dteday'],int(r['hr']),int(r['workingday'])
        assert (d,hr) not in keys and 0<=hr<=23 and work in (0,1); keys.add((d,hr))
        c,m,t=[int(r[k]) for k in ('casual','registered','cnt')]
        assert c>=0 and m>=0 and c+m==t
        for year in ['All',d[:4]]:
            series[year,work,hr].update(hours=1,casual=c,registered=m,rides=t)
        by_date[d].update(casual=c,registered=m,cnt=t)
    dates={r['dteday'] for r in days}
    assert len(dates)==len(days)==731 and set(by_date)==dates
    first,last=min(dates),max(dates)
    assert (date.fromisoformat(last)-date.fromisoformat(first)).days+1==len(dates)
    for r in days:
        assert all(by_date[r['dteday']][k]==int(r[k]) for k in ['casual','registered','cnt'])
    result=[]
    for (year,work,hr),vals in sorted(series.items()):
        result.append(dict(year=year,day_type='Working day' if work else 'Weekend or holiday',hour=hr,**vals,rides_per_observed_hour=round(vals['rides']/vals['hours'],4)))
    output('bikeshare','hourly-profile.csv',result)
    metrics('bikeshare',dict(first=first,last=last,observed_hours=len(hours),calendar_days=len(days),
        nominal_24h_slots_without_row=24*len(days)-len(hours),rentals=sum(int(r['cnt']) for r in days),
        replicated_daily_totals=len(days),duplicate_date_hour_keys=len(hours)-len(keys),
        hourly_csv_sha256=hashlib.sha256(z.read('hour.csv')).hexdigest(),daily_csv_sha256=hashlib.sha256(z.read('day.csv')).hexdigest()))
def retail(z):
    data=z.read('Online Retail.xlsx')
    wb=load_workbook(io.BytesIO(data),read_only=True,data_only=True)
    rows=iter(wb.active.values)
    assert tuple(next(rows))==('InvoiceNo','StockCode','Description','Quantity','InvoiceDate','UnitPrice','CustomerID','Country')
    buckets=defaultdict(Counter); raw=Counter(); credits=Counter(); seen=set(); copies=0;missing=Counter();dup_adjust=Counter()
    n=0; first=last=None
    for invoice,sku,descr,qty,dt,price,customer,country in rows:
        n+=1; inv=str(invoice); p=D(str(price)); assert int(qty)==qty
        amount=D(qty)*p # full-precision GBP; round only for display
        key=(inv,str(sku),descr,qty,dt,p,customer,country)
        duplicate=key in seen; copies+=int(duplicate); seen.add(key)
        assert invoice is not None and dt is not None
        first=min(first or dt,dt); last=max(last or dt,dt)
        is_c=inv.upper().startswith('C')
        if is_c and amount<0: route='credit'
        elif not is_c and qty>0 and p>0: route='positive'
        else: route='other'
        if duplicate:dup_adjust[route]+=amount
        missing['customer_id']+=customer is None; missing['description']+=descr is None
        b=buckets[dt.strftime('%Y-%m')]
        b[route+'_gbp']+=amount; b[route+'_lines']+=1; raw['gbp']+=amount
        if route=='credit': credits[inv]-=amount
    wb.close()
    result=[]
    for month,b in sorted(buckets.items()):
        result.append(dict(month=month,**{k:b[k] for k in ['positive_lines','credit_lines','other_lines','positive_gbp','credit_gbp','other_gbp']},
            signed_total_gbp=sum(b[k+'_gbp'] for k in ['positive','credit','other'])))
    output('retail','monthly-bridge.csv',result)
    totals={k:sum(r[k] for r in result) for k in result[0] if k!='month'}
    assert n==541909==sum(totals[k+'_lines'] for k in ['positive','credit','other'])
    assert raw['gbp']==totals['signed_total_gbp'] and sum(credits.values())==-totals['credit_gbp']
    metrics('retail',dict(first=str(first),last=str(last),lines=n,totals=totals,missing_fields=dict(missing),
        exact_repeat_lines_after_first=copies,repeat_contributions_gbp=dict(dup_adjust),
        credit_invoices=len(credits),largest_credit_invoice_gbp=max(credits.values()),workbook_sha256=hashlib.sha256(data).hexdigest()))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',type=Path,required=True);args=p.parse_args()
    args.cache.mkdir(parents=True,exist_ok=True)
    for name,fn in [('bike',bike),('retail',retail)]:
        with archive(name,args.cache) as z: fn(z)
