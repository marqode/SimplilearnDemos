package logcleaner.unit;

import logcleaner.Parsing;
import logcleaner.model.LogEvent;
import org.junit.jupiter.api.Test;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

public class ParsingTest {

    @Test
    void parseLine_extractsComponentAndMessage() {
        String src = "app1.log";
        String line = "2026-02-15T10:12:30Z INFO auth User logged in";

        Optional<LogEvent> maybe = Parsing.parseLine(src, line);
        assertTrue(maybe.isPresent());

        LogEvent evt = maybe.get();
        assertEquals("2026-02-15T10:12:30Z", evt.timestamp());
        assertEquals("INFO", evt.level());

        // Expected to FAIL initially until Parsing.parseLine is fixed:
        assertEquals("auth", evt.component());
        assertEquals("User logged in", evt.message());
    }
}