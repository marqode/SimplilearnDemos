package logcleaner.integration;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

public class CliIT {

    @TempDir
    Path tmp;

    @Test
    void cli_writesReportJson_withExpectedErrorCount() throws Exception {
        Path inputDir = Path.of("sample_data");
        Path outFile = tmp.resolve("report.json");

        // Run the CLI main method in-process (no network)
        logcleaner.Cli.main(new String[]{
                inputDir.toString(),
                "--out", outFile.toString()
        });

        assertTrue(Files.exists(outFile), "report.json should be created");

        String json = Files.readString(outFile);

        // Expect 2 ERROR lines across the sample logs:
        // app1.log: ERROR db Connection failed
        // app2.log: ERROR payments Charge failed: insufficient funds
        assertTrue(json.contains("\"errorCount\": 2"), "report should include errorCount=2, got:\n" + json);
    }
}