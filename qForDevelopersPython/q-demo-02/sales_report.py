import csv
import sys
from collections import defaultdict
from rich.console import Console
from rich.table import Table

def load_rows(path):
    with open(path, "r") as f:
        rows = []
        reader = csv.DictReader(f)
        for r in reader:
            # keep as strings, convert later
            rows.append(r)
    return rows

def money(x):
    """Format a numeric value as a currency string with dollar sign and 2 decimal places."""
    return f"${x:.2f}"

def main():
    if len(sys.argv) < 2:
        print("usage: python sales_report.py <csv_path>")
        return 1

    path = sys.argv[1]
    rows = load_rows(path)

    region_totals = defaultdict(float)
    customer_totals = defaultdict(float)
    invalid_counts = defaultdict(int)

    for r in rows:
        try:
            qty = int(r["qty"])
            price = float(r["unit_price_usd"])
            region = r.get("region", "").strip()
            customer = r.get("customer", "").strip()
            
            # validate: reject negative prices or negative quantities
            if price < 0 or qty < 0:
                invalid_counts["negative_price_or_qty"] += 1
                continue
            
            # validate: reject missing region or customer
            if not region or not customer:
                invalid_counts["missing_region_or_customer"] += 1
                continue
            
            total = qty * price

            # track totals (qty=0 is valid, contributes $0)
            region_totals[region] += total
            customer_totals[customer] += total

        except (ValueError, KeyError) as e:
            if "qty" in str(e) or "unit_price_usd" in str(e):
                invalid_counts["missing_or_invalid_numeric"] += 1
            else:
                invalid_counts["other_error"] += 1

    # print report
    console = Console()
    console.print("\n[bold cyan]SALES REPORT[/bold cyan]\n")
    
    region_table = Table(title="Region Totals")
    region_table.add_column("Region", style="cyan")
    region_table.add_column("Total", justify="right", style="green")
    for region, total in sorted(region_totals.items(), key=lambda x: x[1], reverse=True):
        region_table.add_row(region, money(total))
    console.print(region_table)

    customer_table = Table(title="\nTop Customers")
    customer_table.add_column("Customer", style="cyan")
    customer_table.add_column("Total", justify="right", style="green")
    for customer, total in sorted(customer_totals.items(), key=lambda x: x[1], reverse=True):
        customer_table.add_row(customer, money(total))
    console.print(customer_table)

    console.print(f"\n[yellow]Invalid rows:[/yellow] {sum(invalid_counts.values())}")
    if invalid_counts:
        for reason, count in sorted(invalid_counts.items()):
            console.print(f"  • {reason.replace('_', ' ')}: {count}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
