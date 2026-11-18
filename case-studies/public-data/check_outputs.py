"""Independent SQL controls on what actually reaches the published reports."""
from pathlib import Path
from decimal import Decimal
import csv,sqlite3
H=Path(__file__).resolve().parent
db=sqlite3.connect(':memory:')
def read(path):
    with (H/path).open() as f:return list(csv.DictReader(f))
r=read('retail/monthly-bridge.csv'); b=read('bikeshare/hourly-profile.csv')
db.execute('CREATE TABLE retail(month TEXT PRIMARY KEY,positive_lines INT,credit_lines INT,other_lines INT,positive_mills INT,credit_mills INT,other_mills INT,signed_mills INT)')
def mills(n):
    m=Decimal(n)*1000;assert int(m)==m;return int(m)
db.executemany('INSERT INTO retail VALUES(?,?,?,?,?,?,?,?)',[(v['month'],*[int(v[k+'_lines']) for k in ['positive','credit','other']],*[mills(v[k+'_gbp']) for k in ['positive','credit','other','signed_total']]) for v in r])
db.execute('CREATE TABLE bike(year TEXT,day_type TEXT,hour INT,hours INT,casual INT,registered INT,rides INT,PRIMARY KEY(year,day_type,hour))')
db.executemany('INSERT INTO bike VALUES(?,?,?,?,?,?,?)',[(v['year'],v['day_type'],*[int(v[k]) for k in ['hour','hours','casual','registered','rides']]) for v in b])
db.executescript((H/'review.sql').read_text())
assert db.execute('SELECT * FROM reporting_control').fetchone()==(10666684544,-896812490,-22124120,9747747934,0,541909)
assert db.execute('SELECT COUNT(*) FROM retail WHERE positive_mills+credit_mills+other_mills!=signed_mills').fetchone()==(0,)
assert db.execute("SELECT sum(hours),sum(rides) FROM bike WHERE year='All'").fetchone()==(17379,3292679)
assert db.execute('SELECT count(*) FROM bike WHERE casual+registered != rides').fetchone()==(0,)
peaks=list(db.execute('SELECT year,day_type,hour FROM profile_rank WHERE peak_rank=1'))
assert len(peaks)==6 and all(h==(17 if d=='Working day' else 13) for _,d,h in peaks)
print('Verified retail signed-amount bridge, monthly reconciliation, file counts, rider splits and all six peak rankings.')
