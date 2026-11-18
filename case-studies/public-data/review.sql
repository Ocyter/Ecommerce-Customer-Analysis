-- Independent review on the published aggregates. SQLite 3.25+.
-- Exclude the All rows when comparing years. They overlap, not another cohort.
CREATE TEMP VIEW profile_rank AS
SELECT year, day_type, hour, rides, hours,
       1.0 * rides / hours AS rate,
       DENSE_RANK() OVER (
          PARTITION BY year, day_type ORDER BY 1.0 * rides / hours DESC
       ) AS peak_rank
FROM bike;

-- Work in integer thousandths of a pound to preserve the source precision.
-- Each monthly row stores the signed credit contribution (not its absolute value).
CREATE TEMP VIEW reporting_control AS
SELECT SUM(positive_mills) AS positive, SUM(credit_mills) AS credits,
       SUM(other_mills) AS other, SUM(signed_mills) AS signed_total,
       SUM(positive_mills + credit_mills + other_mills - signed_mills) AS delta,
       SUM(positive_lines+credit_lines+other_lines) AS line_count
FROM retail;
