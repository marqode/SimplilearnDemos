package logcleaner.model;

public record Report(
        int filesProcessed,
        int totalLines,
        int parsedEvents,
        int errorCount
) {
    public String toJson() {
        // Minimal JSON to avoid dependencies for the course demo
        return "{\n" +
                "  \"filesProcessed\": " + filesProcessed + ",\n" +
                "  \"totalLines\": " + totalLines + ",\n" +
                "  \"parsedEvents\": " + parsedEvents + ",\n" +
                "  \"errorCount\": " + errorCount + "\n" +
                "}\n";
    }
}