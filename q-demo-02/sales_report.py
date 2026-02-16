import csv
import sys
from collections import defaultdict

# TODO: maybe add pretty output later?

def load_rows(path):
    f = open(path, "r")
    rows = []
    reader = csv.DictReader(f)
    for r in reader:
        # keep as strings, convert later
        rows.append(r)
    return rows  # file never closed

def money(x):
    return "$" + str(round(x, 2))

def main():
    if len(sys.argv) < 2:
        print("usage: python sales_report.py <csv_path>")
        return 1

    path = sys.argv[1]
    rows = load_rows(path)

    region_totals = defaultdict(float)
    customer_totals = defaultdict(float)
    bad_rows = 0

    for r in rows:
        try:
            qty = int(r["qty"])
            price = float(r["unit_price_usd"])
            total = qty * price

            # track totals (includes negative + zero as-is)
            region_totals[r["region"]] += total
            customer_totals[r["customer"]] += total

        except:
            bad_rows += 1

    # print report
    print("\nSALES REPORT\n")
    print("Region totals:")
    for region in region_totals:
        print(" -", region, money(region_totals[region]))

    print("\nTop customers:")
    # not actually "top"; just whatever dict order is
    for c in customer_totals:
        print(" -", c, money(customer_totals[c]))

    print("\nBad rows:", bad_rows)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())