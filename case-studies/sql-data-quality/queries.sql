-- SQLite SQL. Synthetic practice only, not client or employer records.
-- Keep raw rows and reject ambiguous keys instead of silently deduplicating.
CREATE TABLE raw_customers (
    customer_row INTEGER PRIMARY KEY,
    customer_id TEXT,
    region TEXT
);
CREATE TABLE raw_orders (
    order_row INTEGER PRIMARY KEY,
    order_id TEXT,
    customer_id TEXT,
    order_status TEXT,
    amount_ngn INTEGER
);

-- Aggregate the dimension first; a duplicate key must not multiply the join.
CREATE VIEW customer_keys AS
SELECT customer_id,
       COUNT(*) AS key_rows,
       MAX(region) AS region,
       SUM(CASE WHEN region IS NULL OR TRIM(region) = '' THEN 1 ELSE 0 END) AS missing_regions
FROM raw_customers
GROUP BY customer_id;

CREATE VIEW orders_checked AS
WITH joined AS (
    SELECT o.*, c.key_rows, c.region, c.missing_regions,
           COUNT(*) OVER (PARTITION BY o.order_id) AS order_key_rows
    FROM raw_orders o
    LEFT JOIN customer_keys c ON c.customer_id = o.customer_id
)
SELECT *, CASE
    WHEN order_id IS NULL OR TRIM(order_id) = '' THEN 'missing_order_id'
    WHEN order_key_rows > 1 THEN 'duplicate_order_id'
    WHEN customer_id IS NULL OR TRIM(customer_id) = '' THEN 'missing_customer_id'
    WHEN key_rows IS NULL THEN 'unknown_customer'
    WHEN key_rows > 1 THEN 'ambiguous_customer_id'
    WHEN missing_regions > 0 THEN 'missing_customer_region'
    WHEN amount_ngn IS NULL THEN 'missing_amount'
    WHEN amount_ngn < 0 THEN 'negative_amount'
    WHEN order_status IS NULL OR order_status NOT IN ('completed','pending','cancelled')
        THEN 'invalid_status'
    ELSE NULL
END AS issue
FROM joined;

-- One primary issue per row, in the CASE precedence above.
-- Valid cancelled/pending orders are outside this completed-order report.
CREATE VIEW orders_routed AS
SELECT *, CASE
    WHEN issue IS NOT NULL THEN 'quarantined'
    WHEN order_status <> 'completed' THEN 'outside_reporting_scope'
    ELSE 'reported'
END AS disposition
FROM orders_checked;

CREATE VIEW reconciliation AS
SELECT disposition, COUNT(*) AS rows,
       COALESCE(SUM(amount_ngn), 0) AS known_amount_ngn,
       SUM(CASE WHEN amount_ngn IS NULL THEN 1 ELSE 0 END) AS missing_amount_rows
FROM orders_routed
GROUP BY disposition;

CREATE VIEW customers_clean AS
SELECT customer_id, region
FROM customer_keys
WHERE key_rows = 1 AND missing_regions = 0
  AND customer_id IS NOT NULL AND TRIM(customer_id) <> '';

CREATE VIEW reporting_fact AS
SELECT order_row, order_id, customer_id, order_status, amount_ngn
FROM orders_routed
WHERE issue IS NULL;

CREATE VIEW reported_by_region AS
SELECT c.region, COUNT(*) AS completed_orders, SUM(o.amount_ngn) AS reported_amount_ngn
FROM reporting_fact o
JOIN customers_clean c ON c.customer_id = o.customer_id
WHERE o.order_status = 'completed'
GROUP BY c.region;

-- SELECT * FROM orders_routed ORDER BY order_row;
-- SELECT * FROM reconciliation ORDER BY disposition;
-- SELECT * FROM reported_by_region ORDER BY region;
