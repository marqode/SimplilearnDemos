package logcleaner;

import logcleaner.model.LogEvent;

import java.util.Optional;

public final class Parsing {
    private Parsing() {}

    /**
     * Parse a log line like:
     * 2026-02-15T10:12:30Z INFO auth User logged in
     *
     * Returns Optional.empty() if the line is malformed.
     */
    public static Optional<LogEvent> parseLine(String sourceFile, String line) {
        if (line == null || line.isBlank()) return Optional.empty();

        // Split into at most 3 parts: timestamp, level, and "rest"
        String[] parts = line.trim().split("\\s+", 3);
        if (parts.length < 3) return Optional.empty();

        String timestamp = parts[0];
        String level = parts[1];
        String rest = parts[2];

        String component = rest;     
        String message = "";         

        return Optional.of(new LogEvent(sourceFile, timestamp, level, component, message));
    }
}