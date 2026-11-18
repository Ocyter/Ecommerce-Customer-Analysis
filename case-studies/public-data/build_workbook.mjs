// Run in a Node environment with @oai/artifact-tool, passing the public-data folder
// and output directory: node build_workbook.mjs ./case-studies/public-data ./downloads
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
const [input, outputDir]=process.argv.slice(2);
if(!input||!outputDir) throw Error('Pass the public-data folder and output directory.');
const read=async p=>await fs.readFile(path.join(input,p),'utf8');
// These two repository-produced aggregates contain no comma or quote in any text field.
const csv=async p=>(await read(p)).trim().split(/\r?\n/).slice(1).map(line=>line.split(','));
const monthly=await csv('retail/monthly-bridge.csv'), hourly=(await csv('bikeshare/hourly-profile.csv')).filter(row=>row[0]!=='All');
const ret=JSON.parse(await read('retail/checks.json')),bike=JSON.parse(await read('bikeshare/checks.json'));
const w=Workbook.create(), r=w.worksheets.add('Invoice postings'), b=w.worksheets.add('Rental peaks'), h=w.worksheets.add('Hourly inputs');
const ink='#153745', teal='#006F72', light='#DCEDEC',muted='#45616A',accent='#B45B32',alt='#F3F7F6';
const gbp='"£"#,##0;("£"#,##0);"£"0',num='#,##0',pct='0.00%';
const rg=(s,a)=>s.getRange(a), val=(s,a,x)=>rg(s,a).values=[[x]],formula=(s,a,x)=>rg(s,a).formulas=[[x]];
function band(s,a,text,bg,fg,size,bold=true){const z=rg(s,a);z.merge();z.values=[[text]];z.format.fill=bg;z.format.font={name:'Calibri',size,bold,color:fg};z.format.verticalAlignment='center';z.format.rowHeight=size>15?36:23;}
function table(s,a,heads){const z=rg(s,a);z.values=[heads];z.format.fill=teal;z.format.font={name:'Calibri',bold:true,color:'#FFFFFF',size:11};z.format.rowHeight=34;z.format.wrapText=true;z.format.verticalAlignment='center';}
function base(s,range,widths){s.showGridLines=false;s.tabColor=teal;const z=rg(s,range);z.format.font={name:'Calibri',size:11,color:ink};z.format.rowHeight=18;for(const [col,width] of Object.entries(widths))rg(s,col+'1').format.columnWidth=width;}
function note(s,a,t){band(s,a,t,alt,muted,11,false);}
base(r,'A1:H32',{A:18,B:22,C:21,D:21,E:22,F:20,G:20,H:18});
band(r,'A1:H1','01    RETAIL OPERATIONS',ink,'#FFFFFF',11);
band(r,'A2:H2','How much do credits change the sales picture?',ink,'#FFFFFF',22);
note(r,'A3:H3','UK online retailer, 1 Dec 2010 to 9 Dec 2011. Invoice posting value in sterling; the final month covers nine days.');
note(r,'A4:H4','Reconcile all posting types before using the KPI. Keep the largest credit in the baseline and review its underlying documentation.');
band(r,'A6:H6','Full extract and one-invoice sensitivity',light,ink,14);
table(r,'A7:H7',['Positive value','Credit value','Other value','Signed value','Credit / positive','Largest credit¹','Excluding largest¹','Source lines']);
for(const [c,f] of Object.entries({A:'=SUM(B13:B25)',B:'=SUM(C13:C25)',C:'=SUM(D13:D25)',D:'=SUM(E13:E25)',E:'=-B8/A8',G:'=(-B8-F8)/A8',H:'=SUM(H13:H25)'}))formula(r,c+'8',f);
val(r,'F8',Number(ret.largest_credit_invoice_gbp));rg(r,'A8:D8').setNumberFormat(gbp);rg(r,'F8').setNumberFormat(gbp);rg(r,'E8').setNumberFormat(pct);rg(r,'G8').setNumberFormat(pct);rg(r,'H8').setNumberFormat(num);
note(r,'A9:H9','¹ Sensitivity holds positive value fixed and removes only the single largest credit. It does not estimate the share of customers returning goods.');
band(r,'A11:H11','Monthly postings and reconciliation',light,ink,14);
table(r,'A12:H12',['Month','Positive value','Credit value','Other value','Calculated signed','Source signed','Difference (£)','Source lines']);
for(let i=0;i<monthly.length;i++){const m=monthly[i],row=13+i;const dt=new Date(m[0]+'-01T00:00:00Z');
rg(r,'A'+row+':D'+row).values=[[dt,Number(m[4]),Number(m[5]),Number(m[6])]];val(r,'F'+row,Number(m[7]));val(r,'H'+row,Number(m[1])+Number(m[2])+Number(m[3]));formula(r,'E'+row,'=SUM(B'+row+':D'+row+')');formula(r,'G'+row,'=ROUND(E'+row+'-F'+row+',3)');if(i%2===0)rg(r,'A'+row+':H'+row).format.fill=alt;}
rg(r,'A13:A25').setNumberFormat('mmm yyyy');rg(r,'B13:F25').setNumberFormat(gbp);rg(r,'G13:G25').setNumberFormat('0.000');rg(r,'H13:H25').setNumberFormat(num);
note(r,'A27:H27','Source: Daqing Chen, Online Retail (UCI), CC BY 4.0. https://doi.org/10.24432/C5BW33');
note(r,'A28:H28','Monthly signed values reconcile at £0.001 precision. Displayed amounts are rounded; signed postings do not measure profit or cash collected.');
note(r,'A29:H29','Aggregates: retail/monthly-bridge.csv and retail/checks.json. AI-assisted public-data portfolio study.');
base(h,'A1:G104',{A:14,B:28,C:15,D:20,E:22,F:22,G:20});
band(h,'A1:G1','SOURCE DATA     /     CAPITAL BIKESHARE',ink,'#FFFFFF',11);
band(h,'A2:G2','Observed rental hours',ink,'#FFFFFF',20);
note(h,'A3:G3','Source: Hadi Fanaee-T, Bike Sharing (UCI), CC BY 4.0. https://doi.org/10.24432/C5W894');
note(h,'A4:G4','Year rows only. Pooled rows in bikeshare/hourly-profile.csv are excluded to avoid counting each rental twice.');
table(h,'A6:G6',['Year','Day type','Hour (0–23)','Observed hours','Casual rentals','Registered rentals','All rentals']);
rg(h,'A7:G102').values=hourly.map(m=>[+m[0],m[1],...m.slice(2,7).map(Number)]);rg(h,'D7:G102').setNumberFormat(num);h.freezePanes.freezeRows(6);
base(b,'A1:H42',{A:18,B:22,C:22,D:20,E:18,F:18,G:18,H:18});
band(b,'A1:H1','02    MOBILITY OPERATIONS',ink,'#FFFFFF',11);
band(b,'A2:H2','When should operators check capacity?',ink,'#FFFFFF',22);
note(b,'A3:H3','Capital Bikeshare, 2011–2012. Rates divide total rentals by recorded hours in each hour and day type; missing slots are not treated as zero.');
note(b,'A4:H4','Use the peak times to choose station checks. A staffing or rebalancing plan also needs current arrivals, departures and stockouts.');
table(b,'A6:D6',['Day type','Peak hour (0–23)','Rentals per observed hour','Registered at peak']);
val(b,'A7','Working day');val(b,'A8','Weekend or holiday');
for(const [row,col] of [[7,'B'],[8,'C']]){formula(b,'C'+row,'=MAX('+col+'12:'+col+'35)');formula(b,'B'+row,'=INDEX(A12:A35,MATCH(C'+row+','+col+'12:'+col+'35,0))');
const crit="'Hourly inputs'!$B$7:$B$102,$A"+row+",'Hourly inputs'!$C$7:$C$102,$B"+row;
formula(b,'D'+row,"=SUMIFS('Hourly inputs'!$F$7:$F$102,"+crit+")/SUMIFS('Hourly inputs'!$G$7:$G$102,"+crit+")");}
rg(b,'C7:C8').setNumberFormat('0.0');rg(b,'D7:D8').setNumberFormat('0.0%');
table(b,'A11:C11',['Hour (0–23)','Working day','Weekend or holiday']);
for(let i=0;i<24;i++){const row=12+i;val(b,'A'+row,i);for(const c of ['B','C']){const crit="'Hourly inputs'!$B$7:$B$102,"+c+"$11,'Hourly inputs'!$C$7:$C$102,$A"+row;formula(b,c+row,"=SUMIFS('Hourly inputs'!$G$7:$G$102,"+crit+")/SUMIFS('Hourly inputs'!$D$7:$D$102,"+crit+")");}if(i%2===0)rg(b,'A'+row+':C'+row).format.fill=alt;}rg(b,'B12:C35').setNumberFormat('0.0');
const ch=b.charts.add('line',rg(b,'A11:C35'));ch.title='Rentals per observed hour';ch.setPosition('D11','H29');ch.legend={position:'bottom'};ch.series.items[0].fill=teal;ch.series.items[1].fill=accent;ch.xAxis={axisType:'textAxis',tickLabelInterval:3};ch.yAxis={numberFormatCode:'#,##0',numberFormatSourceLinked:false};
note(b,'A37:H37','All hourly inputs reconcile to 731 daily totals in the upstream audit. The hourly profiles use observed hours, not scheduled hours.');
w.recalculate();
const readCell=(s,a)=>rg(s,a).values[0][0], near=(v,n)=>assert.ok(Math.abs(v-n)<1e-6,'Expected '+n+'; got '+v);
near(readCell(r,'D8'),Number(ret.totals.signed_total_gbp));near(readCell(r,'H8'),ret.lines);for(let j=13;j<=25;j++)near(readCell(r,'G'+j),0);
assert.equal(readCell(b,'B7'),17);assert.equal(readCell(b,'B8'),13);assert.equal(hourly.reduce((a,m)=>a+(+m[6]),0),bike.rentals);
for(const [row,type] of [[7,'Working day'],[8,'Weekend or holiday']]){const h0=readCell(b,'B'+row), part=hourly.filter(m=>m[1]===type&&+m[2]===h0);const sum=k=>part.reduce((a,m)=>a+Number(m[k]),0);near(readCell(b,'C'+row),sum(6)/sum(3));near(readCell(b,'D'+row),sum(5)/sum(6));}
const checked=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:12}});console.log(checked.ndjson);
await fs.mkdir(outputDir,{recursive:true});
for(const [s,range,slug] of [[r,'A1:H29','retail'],[b,'A1:H37','rentals'],[h,'A1:G18','inputs']]){const prev=await w.render({sheetName:s.name,range,scale:0.84});await fs.writeFile(path.join(outputDir,slug+'.png'),new Uint8Array(await prev.arrayBuffer()));}
await (await SpreadsheetFile.exportXlsx(w)).save(path.join(outputDir,'Public_Data_Decision_Workbook.xlsx'));
