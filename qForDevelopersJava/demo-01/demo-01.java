import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Demo: Setup + Explain + Debug + Refactor
 *
 * Mirrors a common "fetch order -> compute total -> flag -> return results" flow.
 */
public class OrderProcessorDemo {

    // ---- "S3-like" Object Store ----
    interface ObjectStore {
        Optional<Order> fetchOrder(String bucket, String key);
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
        public Optional<Order> fetchOrder(String bucket, String key) {
            return Optional.ofNullable(data.get(bucket + "/" + key));
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

    private double calculateOrderTotal(Order order) {
        return order.items().stream()
                .mapToDouble(item -> item.price() * item.quantity())
                .sum();
    }

    private ProcessResult processRecord(EventRecord record) {
        return store.fetchOrder(record.bucket(), record.key())
                .map(order -> {
                    double total = calculateOrderTotal(order);
                    String status = total > 1000.0 ? "FLAGGED" : "OK";
                    return new ProcessResult(record.orderId(), status, total);
                })
                .orElseGet(() -> {
                    System.out.println("Order not found: " + record.orderId());
                    return new ProcessResult(record.orderId(), "ERROR", 0.0);
                });
    }

    public List<ProcessResult> processOrders(List<EventRecord> records) {
        return records.stream()
                .map(this::processRecord)
                .toList();
    }

    // ---- Demo runner ----
    public static void main(String[] args) {
        FakeObjectStore store = new FakeObjectStore();

        // Two sample orders with independent totals:
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