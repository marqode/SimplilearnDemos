package logcleaner;

import logcleaner.model.Report;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public final class Cli {

    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: java logcleaner.Cli <inputDir> [--out <outputFile>]");
            System.exit(2);
        }

        Path inputDir = Paths.get(args[0]);
        Path outFile = null;

        for (int i = 1; i < args.length; i++) {
            if ("--out".equals(args[i]) && i + 1 < args.length) {
                outFile = Paths.get(args[i + 1]);
                i++;
            }
        }

        if (outFile == null) {
            outFile = Paths.get("out", "report.json");
        }

        try {
            List<Path> files = IoUtils.listLogFiles(inputDir);

            Report report = Reporting.buildReport(files);

            IoUtils.ensureParentDir(outFile);
            IoUtils.writeString(outFile, report.toJson());

            System.out.println("Wrote report to: " + outFile.toAbsolutePath());
            System.exit(0);

        } catch (Exception e) {
            System.out.println("ERROR: " + e.getMessage());
            System.exit(1);
        }
    }
}