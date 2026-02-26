import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Demo: Setup + Explain + Debug + Refactor
 *
 * Mirrors a common "fetch order -> compute total -> flag -> return results" flow.
 */
public class OrderProcessorDemo {

    // ---- "S3-like" Object Store ----
    interface ObjectStore {
        Order fetchOrder(String bucket, String key);
    }

    /**
     * A fake in-memory store to avoid AWS SDK/credentials overhead in a beginner demo.
     * Keys are stored as "bucket/key" to keep the call site similar to S3.
     */
    static class FakeObjectStore implements ObjectStore {
        private final Map<String, Order> data = new HashMap<>();

        public void put(String bucket, String key, Order order) {
            data.put(bucket + "/" + key, order);
        }

        @Override
        public Order fetchOrder(String bucket, String key) {
            Order order = data.get(bucket + "/" + key);
            if (order == null) {
                throw new IllegalArgumentException("Order not found for bucket=" + bucket + ", key=" + key);
            }
            return order;
        }
    }

    // ---- Domain model ----
    record LineItem(String name, double price, int quantity) {}
    record Order(List<LineItem> items) {}
    record EventRecord(String orderId, String bucket, String key) {}
    record ProcessResult(String orderId, String status, double total) {}

    // ---- Business logic (mirrors your Python functions) ----
    private final ObjectStore store;

    public OrderProcessorDemo(ObjectStore store) {
        this.store = store;
    }

    public Order fetchOrderFromStore(String bucket, String key) {
        return store.fetchOrder(bucket, key);
    }

    public double calculateOrderTotal(Order order) {
        double total = 0.0;
        for (LineItem item : order.items()) {
            total += item.price() * item.quantity();
        }
        return total;
    }

    public List<ProcessResult> processOrders(List<EventRecord> records) {
        List<ProcessResult> results = new ArrayList<>();

        double runningTotal = 0.0; // <-- BUG: should not be shared across orders

        for (EventRecord record : records) {
            try {
                Order order = fetchOrderFromStore(record.bucket(), record.key());

                // BUG: total should be calculated per order, but we keep accumulating into runningTotal
                runningTotal += calculateOrderTotal(order);

                String status = (runningTotal > 1000.0) ? "FLAGGED" : "OK";

                results.add(new ProcessResult(
                        record.orderId(),
                        status,
                        runningTotal
                ));
            } catch (Exception e) {
                System.out.println("Error processing order " + record.orderId() + ": " + e.getMessage());
            }
        }

        return results;
    }

    // ---- Demo runner ----
    public static void main(String[] args) {
        FakeObjectStore store = new FakeObjectStore();

        // Two sample orders; totals should be independent:
        // - order-001 total = 420.00
        // - order-002 total = 700.00
        store.put("demo-bucket", "orders/order-001.json",
                new Order(List.of(
                        new LineItem("Keyboard", 70.00, 2),
                        new LineItem("Monitor", 140.00, 2)
                )));

        store.put("demo-bucket", "orders/order-002.json",
                new Order(List.of(
                        new LineItem("Laptop", 700.00, 1)
                )));

        List<EventRecord> event = List.of(
                new EventRecord("order-001", "demo-bucket", "orders/order-001.json"),
                new EventRecord("order-002", "demo-bucket", "orders/order-002.json")
        );

        OrderProcessorDemo processor = new OrderProcessorDemo(store);
        List<ProcessResult> results = processor.processOrders(event);

        System.out.println("Results:");
        for (ProcessResult r : results) {
            System.out.printf("order_id=%s status=%s total=%.2f%n", r.orderId(), r.status(), r.total());
        }
    }
}