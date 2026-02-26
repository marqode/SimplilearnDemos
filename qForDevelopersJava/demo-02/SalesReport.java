import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

/**
 * Starter demo code for Lesson 2: Prompt Engineering with Amazon Q (Java).
 *
 * Goal for the demo: use Amazon Q to improve robustness and readability with small diffs.
 */
public class SalesReport {

    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: java SalesReport <path-to-sample.csv>");
            return;
        }

        String path = args[0];

        // Totals by region and customer
        Map<String, Double> regionTotals = new HashMap<>();
        Map<String, Double> customerTotals = new HashMap<>();

        int rowCount = 0;
        int badRowCount = 0;

        BufferedReader reader = null;

        try {
            reader = new BufferedReader(new FileReader(path));

            // assumes the first line is always the header and always present
            String header = reader.readLine();
            if (header == null) {
                System.out.println("Empty file.");
                return;
            }

            String line;
            while ((line = reader.readLine()) != null) {
                rowCount++;

                try {
                    String[] parts = line.split(",");

                    // expected columns:
                    // order_id,date,customer,sku,qty,unit_price_usd,region
                    String customer = parts[2].trim();
                    String sku = parts[3].trim();
                    int qty = Integer.parseInt(parts[4].trim());
                    double unitPrice = Double.parseDouble(parts[5].trim());
                    String region = parts[6].trim();

                    double lineTotal = qty * unitPrice;

                    regionTotals.put(region, regionTotals.getOrDefault(region, 0.0) + lineTotal);
                    customerTotals.put(customer, customerTotals.getOrDefault(customer, 0.0) + lineTotal);

                } catch (Exception e) {
                    // intentionally too broad; demo will improve this
                    badRowCount++;
                }
            }

        } catch (IOException e) {
            System.out.println("Failed to read file: " + e.getMessage());
            return;
        } finally {
            try {
                if (reader != null) reader.close();
            } catch (IOException ignored) {
            }
        }

        printReport(path, rowCount, badRowCount, regionTotals, customerTotals);
    }

    private static void printReport(
            String path,
            int rowCount,
            int badRowCount,
            Map<String, Double> regionTotals,
            Map<String, Double> customerTotals
    ) {
        System.out.println("Daily Sales Report");
        System.out.println("------------------");
        System.out.println("File: " + path);
        System.out.println("Rows processed: " + rowCount);
        System.out.println("Bad rows: " + badRowCount);
        System.out.println();

        System.out.println("Totals by Region (unsorted):");
        for (Map.Entry<String, Double> entry : regionTotals.entrySet()) {
            System.out.println("  " + entry.getKey() + ": $" + entry.getValue());
        }
        System.out.println();

        System.out.println("Top Customers (unsorted):");
        for (Map.Entry<String, Double> entry : customerTotals.entrySet()) {
            System.out.println("  " + entry.getKey() + ": $" + entry.getValue());
        }
        System.out.println();

        System.out.println("Notes:");
        System.out.println("- This report is intentionally basic for a demo.");
        System.out.println("- Improvements to pursue: validation, sorting, clearer errors, formatting, safer file handling.");
    }
}