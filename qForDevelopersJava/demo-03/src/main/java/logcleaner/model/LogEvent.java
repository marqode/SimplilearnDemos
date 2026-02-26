package logcleaner.model;

public record LogEvent(
        String source,
        String timestamp,
        String level,
        String component,
        String message
) {}