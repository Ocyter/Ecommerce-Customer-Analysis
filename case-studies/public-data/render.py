"""Render both study pages from checked aggregates; no JavaScript, APIs or tracking."""
from pathlib import Path
import csv,json
from decimal import Decimal as D
from datetime import datetime as DT
from html import escape
H=Path(__file__).resolve().parent
REPO='https://github.com/Ocyter/Ecommerce-Customer-Analysis/tree/main/case-studies/public-data'
def get(folder,name):
    with (H/folder/name).open() as f:return list(csv.DictReader(f))
def check(f):return json.loads((H/f/'checks.json').read_text())
def link(url,s):return f'<a href="{url}">{s}</a>'
def sec(label,title,body):return f'<section><p class="eyebrow">{label}</p><h2>{title}</h2>{body}</section>'
def table(head,rows,caption):
    return '<div class="table-wrap"><table><caption>'+caption+'</caption><thead><tr>'+''.join(f'<th scope="col">{i}</th>' for i in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{i}</td>' for i in r)+'</tr>' for r in rows)+'</tbody></table></div>'
def page(folder,title,kicker,lead,scope,brief,body,credit,doi,filename):
    short='Retail' if folder=='retail' else 'Bikeshare'
    source=sec('SOURCE &amp; REPRODUCTION','Check the evidence',f'<p class="source">{credit} UCI Machine Learning Repository. <a href="https://doi.org/{doi}">Dataset record and download</a>. Data licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. The analysis groups and transforms the published data. Built with AI assistance as a public-data portfolio study; no employer commissioned it.</p><div class="src">'+link(filename,'Download the aggregate CSV')+link('checks.json','Inspect the audit totals')+link(REPO,'Reproduce the analysis')+link('../../../downloads/Public_Data_Decision_Workbook.xlsx','Download the Excel workbook')+'</div>')
    (H/folder/'index.html').write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{short} case study | Osita Nwaigwe</title><meta name="description" content="{escape(lead,quote=True)}"><link rel="stylesheet" href="../../../home.css"><link rel="stylesheet" href="../studies.css"></head><body>
<a class="skip" href="#main">Skip to study</a><header class="navigation wrap"><a class="identity" href="../../../">Osita Nwaigwe<span>Data Analyst</span></a><nav aria-label="Portfolio"><a href="../../../index.html#work">Case studies</a><a href="../../../resume.html">CV</a></nav></header>
<main class="wrap study" id="main"><p class="breadcrumb"><a href="../../../index.html#work">← Back to my work</a></p><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lead">{lead}</p><p class="meta">{scope}</p><aside class="brief"><p><strong>Decision:</strong> {brief}</p></aside>{body}{source}<footer><a href="../../../index.html#work">Explore other case studies →</a></footer></main></body></html>''')
def retail():
    folder='retail';rows=get(folder,'monthly-bridge.csv');ck=check(folder);t=ck['totals']
    gross,credits,other,net=[D(t[i]) for i in ('positive_gbp','credit_gbp','other_gbp','signed_total_gbp')]
    pct=lambda a,b:100*a/b
    bridge=table(['Posting group','Invoice lines','Signed value (£)'],[[k,f'{n:,}',f'{v:,.2f}'] for k,n,v in [
        ('Positive, non-cancellation lines',t['positive_lines'],gross),('C-coded negative postings',t['credit_lines'],credits),('Other postings',t['other_lines'],other),('All postings',ck['lines'],net)]],'From positive lines to the signed total')
    shares=[pct(-D(r['credit_gbp']),D(r['positive_gbp'])) for r in rows]
    bars=''.join(f'<div class="bar {"partial" if r==rows[-1] else ""}"><span>{DT.strptime(r["month"],"%Y-%m"):%b %Y}{"*" if r==rows[-1] else ""}</span><span class="track" aria-hidden="true"><i class="fill" style="width:{v/35*100:.3f}%"></i></span><b>{v:.1f}%</b></div>' for r,v in zip(rows,shares))
    body=sec('01 / RECONCILIATION','What a positive-only report leaves out',bridge+'<p>Each line contributes quantity × unit price in sterling. The grouping preserves every line, including adjustments. The workbook keeps sub-penny precision through aggregation; displayed totals are rounded. This is invoice posting value, not profit, cash received or audited revenue.</p>')
    largest=D(ck['largest_credit_invoice_gbp'])
    body+=sec('02 / EXCEPTION REVIEW','A small number of large postings can move the KPI',f'<figure><div class="bars">{bars}</div><figcaption>Absolute value of C-coded negative lines ÷ positive non-cancellation value in the same calendar month. Denominators differ. *December 2011 stops on 9 December and cannot be compared as a full month.</figcaption></figure><p>One credit invoice totalled £{largest:,.2f}, or {pct(largest,-credits):.1f}% of the credit value across the extract. A sensitivity check holding positive value fixed and removing only that credit lowers the overall ratio from {pct(-credits,gross):.2f}% to {pct(-credits-largest,gross):.2f}%. That is a diagnostic, not a reason to delete a valid invoice.</p>')
    dup=ck['repeat_contributions_gbp']; nodup=pct(-(credits-D(dup['credit'])),gross-D(dup['positive']))
    body+=sec('03 / DATA QUALITY','Why all 541,909 lines stayed in scope',f'<p>{ck["missing_fields"]["customer_id"]:,} lines lack a customer ID. Dropping them would change a posting-level KPI that does not need customer identity. The workbook also contains {ck["exact_repeat_lines_after_first"]:,} exact repeats beyond the first occurrence across all eight fields. There is no authoritative line ID, so the baseline retains them. Removing repeats changes the overall credit ratio to {nodup:.2f}%.</p><p><strong>Before acting:</strong> ask finance to match the highest-value credits to original invoices, posting reasons and settlement dates. Measure matched value and investigate unresolved exceptions. A C-coded credit is not evidence of a returned item, an unhappy customer or a lost sale. The monthly ratio compares postings in the same month, not matched order cohorts.</p>')
    page(folder,'How much do credits change the sales picture?','COMMERCIAL REPORTING / UK ONLINE RETAIL',f'Positive invoice lines totalled £{gross/1000000:.2f}m. After credits and other adjustments, the same file totalled £{net/1000000:.2f}m. A single number on a sales dashboard would hide that difference.','UK non-store retailer · 1 Dec 2010 to 9 Dec 2011 · 541,909 invoice lines','Show positive value, credits and other adjustments side by side. Prioritise the largest credits for reconciliation before drawing conclusions about customer returns.',body,'Daqing Chen (2015), Online Retail.','10.24432/C5BW33','monthly-bridge.csv')
def bike():
    folder='bikeshare';rows=get(folder,'hourly-profile.csv');ck=check(folder)
    def series(y,d):return sorted([r for r in rows if r['year']==y and r['day_type']==d],key=lambda r:int(r['hour']))
    def peak(rs):return max(rs,key=lambda r:float(r['rides_per_observed_hour']))
    def val(r):return float(r['rides_per_observed_hour'])
    work='Working day';off='Weekend or holiday'; w,h=series('All',work),series('All',off)
    # Constant y scale for both groups; no smoothing of hourly observations.
    x=lambda hr:42+hr*22
    y=lambda n:194-n*.285
    svg='<svg class="plot" viewBox="0 0 585 232" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">Rentals per observed hour by day type</title><desc id="chart-desc">Working days have morning and evening peaks. Weekends and holidays rise towards an early afternoon maximum. Full values follow in a table.</desc>'
    for n in range(0,601,150):svg+=f'<path d="M42 {y(n)} H548" stroke="#d1d8cf"/><text x="35" y="{y(n)+4}" text-anchor="end" font-size="13">{n}</text>'
    for hr in [0,4,8,12,16,20,23]:svg+=f'<text x="{x(hr)}" y="218" text-anchor="middle" font-size="13">{hr:02}:00</text>'
    for rs,col,pattern in [(w,'#235b4c',''),(h,'#a44c29','7 4')]:
        pts=' '.join(f'{x(int(r["hour"]))},{y(val(r)):.2f}' for r in rs)
        svg+=f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3.5" stroke-dasharray="{pattern or "none"}"/>'
    svg+='</svg>'
    wp,hp=peak(w),peak(h)
    body=sec('01 / DEMAND PROFILE','One staffing schedule would miss one of the peaks',f'<figure><div class="legend"><b>Solid: working days</b><b>Dashed: weekends and holidays</b></div>{svg}<figcaption>Average system-wide rentals per observed hour, by local clock hour. Totals are divided by the number of available hour records in each group, not by trips or riders.</figcaption></figure><p>Working days also show a morning peak: {val(w[8]):.0f} rentals per observed 08:00 hour. At 17:00, registered riders accounted for {100*int(wp["registered"])/int(wp["rides"]):.1f}% of rentals; at the weekend/holiday peak their share was {100*int(hp["registered"])/int(hp["rides"]):.1f}%. Registration is recorded; trip purpose is not.</p>')
    body+='<details><summary>Read the hourly values behind the chart</summary>'+table(['Hour','Working day','Weekend / holiday'],[(f'{i:02}:00',f'{val(a):.1f}',f'{val(b):.1f}') for i,(a,b) in enumerate(zip(w,h))],'Rentals per observed hour, 2011 and 2012 combined')+'</details>'
    peaks=[]
    for yr in ['2011','2012']:
        pair=[peak(series(yr,d)) for d in [work,off]]
        peaks.append([yr]+[f'{int(r["hour"]):02}:00 ({val(r):.0f})' for r in pair])
    body+=sec('02 / VALIDATION','The peak hours hold in both years',table(['Year','Working-day peak','Weekend / holiday peak'],peaks,'Peak clock hour (average rentals per observed hour)')+f'<p>All {ck["observed_hours"]:,} hourly records have unique date/hour keys. Casual and registered counts add to the recorded total on every row; all {ck["calendar_days"]} daily sums match the separate daily file. A nominal 24-hour grid has {ck["nominal_24h_slots_without_row"]} more slots than recorded rows. Unrecorded hours were not imputed as zero.</p>')
    body+=sec('03 / OPERATIONS DECISION','Check stations before moving bikes','<p>For a historical staffing review, examine working-day coverage before 08:00 and 17:00, and weekend or holiday coverage before 13:00. System-wide trips show when bikes were rented, not where demand went unmet.</p><p>For a present-day pilot, first obtain recent station-level departures, arrivals, capacity and minutes empty or full. Select comparable stations and track empty/full minutes per service hour alongside rebalancing cost. Those measures would test whether a schedule change actually helped.</p>')
    page(folder,'When should a bike-share operator check capacity?','OPERATIONS ANALYTICS / CAPITAL BIKESHARE',f'Working-day rental demand peaked at 17:00, averaging {val(wp):.0f} rides per observed hour. On weekends and holidays the peak shifted four hours earlier, to 13:00 ({val(hp):.0f} rides).','Washington, DC area · Jan 2011 to Dec 2012 · 3,292,679 recorded rentals','Review availability before the clock-hour peaks, using different windows for working days and days off. Station-level evidence is needed before assigning bikes or staff.',body,'Hadi Fanaee-T (2013), Bike Sharing.','10.24432/C5W894','hourly-profile.csv')
if __name__=='__main__': retail();bike()
