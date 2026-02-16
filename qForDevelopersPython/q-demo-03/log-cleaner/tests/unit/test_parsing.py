from logcleaner.parsing import parse_line


def test_parse_line_extracts_component_and_message():
    src = "sample_data/app1.log"
    line = "2026-02-15T10:12:30Z INFO auth User logged in"
    evt = parse_line(src, line)

    assert evt is not None
    assert evt.timestamp == "2026-02-15T10:12:30Z"
    assert evt.level == "INFO"
    # This is expected to FAIL initially until parsing.py is fixed:
    assert evt.component == "auth"
    assert evt.message == "User logged in"