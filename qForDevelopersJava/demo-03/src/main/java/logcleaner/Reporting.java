package logcleaner;

import logcleaner.model.LogEvent;
import logcleaner.model.Report;

import java.nio.file.Path;
import java.util.List;
import java.util.Optional;

public final class Reporting {
    private Reporting() {}

    public static Report buildReport(List<Path> files) throws Exception {
        int totalLines = 0;
        int parsedEvents = 0;
        int errorCount = 0;

        for (Path file : files) {
            List<String> lines = IoUtils.readAllLines(file);
            totalLines += lines.size();

            for (String line : lines) {
                Optional<LogEvent> maybe = Parsing.parseLine(file.getFileName().toString(), line);
                if (maybe.isEmpty()) continue;

                parsedEvents++;
                LogEvent evt = maybe.get();

                if ("ERROR".equals(evt.level())) {
                    errorCount++;
                }
            }
        }

        return new Report(files.size(), totalLines, parsedEvents, errorCount);
    }
}