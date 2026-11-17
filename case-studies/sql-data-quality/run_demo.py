"""Reproduce the synthetic SQL exercise with Python's standard library."""
from pathlib import Path
import csv
import hashlib
import json
import sqlite3

ROOT = Path(__file__).resolve().parent

def read_csv(name):
    with (ROOT / 'data' / name).open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))

def export_csv(conn, filename, query):
    cursor = conn.execute(query)
    with (ROOT / 'outputs' / filename).open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle, lineterminator='\n')
        writer.writerow([c[0] for c in cursor.description])
        writer.writerows(cursor.fetchall())

def main():
    conn = sqlite3.connect(':memory:')
    conn.executescript((ROOT / 'queries.sql').read_text(encoding='utf-8'))
    customers, orders = read_csv('customers.csv'), read_csv('orders.csv')
    conn.executemany('INSERT INTO raw_customers VALUES (?, ?, ?)', [
        (int(r['customer_row']), r['customer_id'], r['region'] or None) for r in customers
    ])
    conn.executemany('INSERT INTO raw_orders VALUES (?, ?, ?, ?, ?)', [
        (int(r['order_row']), r['order_id'], r['customer_id'], r['order_status'],
         int(r['amount_ngn']) if r['amount_ngn'] else None) for r in orders
    ])
    raw_rows = conn.execute('SELECT COUNT(*) FROM raw_orders').fetchone()[0]
    expected_issues = {
        2: 'duplicate_order_id', 3: 'duplicate_order_id',
        4: 'ambiguous_customer_id', 5: 'missing_customer_region',
        7: 'unknown_customer', 9: 'negative_amount', 10: 'missing_amount'
    }
    issues = dict(conn.execute('SELECT order_row, issue FROM orders_checked WHERE issue IS NOT NULL'))
    assert issues == expected_issues, issues
    routes = dict(conn.execute('SELECT disposition, rows FROM reconciliation'))
    assert routes == {'reported': 3, 'quarantined': 7, 'outside_reporting_scope': 2}, routes
    assert sum(routes.values()) == raw_rows == 12
    assert conn.execute('SELECT COUNT(*) FROM orders_checked').fetchone()[0] == raw_rows, 'Join multiplied rows'
    assert conn.execute('SELECT COUNT(*) FROM customers_clean').fetchone()[0] == 4
    assert conn.execute('SELECT COUNT(*) FROM reporting_fact').fetchone()[0] == 5
    assert conn.execute('SELECT COUNT(*) FROM reporting_fact WHERE amount_ngn IS NULL OR amount_ngn < 0').fetchone()[0] == 0
    region = conn.execute('SELECT * FROM reported_by_region ORDER BY region').fetchall()
    assert region == [('North', 2, 28000), ('West', 1, 24000)], region
    reported_amount = sum(r[2] for r in region)
    assert reported_amount == 52000
    raw_known = conn.execute('SELECT SUM(amount_ngn) FROM raw_orders').fetchone()[0]
    routed_known = conn.execute('SELECT SUM(known_amount_ngn) FROM reconciliation').fetchone()[0]
    assert raw_known == routed_known == 122500
    assert conn.execute('SELECT SUM(missing_amount_rows) FROM reconciliation').fetchone()[0] == 1
    assert len(set(issues.values())) == 6
    (ROOT / 'outputs').mkdir(exist_ok=True)
    exports = {
        'orders_checked.csv': 'SELECT order_row, order_id, customer_id, order_status, amount_ngn, region, issue, disposition FROM orders_routed ORDER BY order_row',
        'quarantine.csv': 'SELECT order_row, order_id, customer_id, order_status, amount_ngn, issue FROM orders_routed WHERE issue IS NOT NULL ORDER BY order_row',
        'reconciliation.csv': 'SELECT * FROM reconciliation ORDER BY disposition',
        'customers_clean.csv': 'SELECT * FROM customers_clean ORDER BY customer_id',
        'reporting_fact.csv': 'SELECT * FROM reporting_fact ORDER BY order_row',
        'reported_by_region.csv': 'SELECT * FROM reported_by_region ORDER BY region'
    }
    for filename, query in exports.items():
        export_csv(conn, filename, query)
    result = {
        'data_type': 'synthetic practice fixture, not employer or client data',
        'raw_order_rows': raw_rows, 'raw_customer_rows': len(customers),
        'quarantined_order_rows': routes['quarantined'],
        'outside_reporting_scope_rows': routes['outside_reporting_scope'],
        'reported_order_rows': routes['reported'], 'reported_amount_ngn': reported_amount,
        'row_reconciliation_difference': raw_rows - sum(routes.values()),
        'known_amount_reconciliation_difference_ngn': raw_known - routed_known,
        'missing_amount_rows': 1,
        'checks': 'passed: expected defects, row conservation, join cardinality, valid reporting rows, regional totals and known-amount reconciliation',
        'input_sha256': {name: hashlib.sha256((ROOT / 'data' / name).read_bytes()).hexdigest()
                         for name in ['customers.csv', 'orders.csv']},
        'scope_limit': 'Tests cover this small fixture. They do not establish a production system, universal validation coverage or business impact.'
    }
    (ROOT / 'outputs' / 'verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
