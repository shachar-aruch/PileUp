from src.clean import clean_text


def test_already_clean_text_is_unchanged():
    text = "This is a clean sentence.\nAnd another one."
    assert clean_text(text) == text


def test_strips_leading_and_trailing_whitespace():
    text = "  \n\nHello world.\n\n  "
    assert clean_text(text) == "Hello world."


def test_collapses_multiple_blank_lines():
    text = "First paragraph.\n\n\n\nSecond paragraph."
    assert clean_text(text) == "First paragraph.\n\nSecond paragraph."


def test_removes_symbol_only_lines():
    text = "Good content.\n---\nMore content."
    result = clean_text(text)
    assert "---" not in result
    assert "Good content." in result
    assert "More content." in result


def test_fixes_broken_encoding():
    broken = "It\xe2\x80\x99s a caf\xc3\xa9."
    result = clean_text(broken)
    assert "It’s" in result or "It's" in result
    assert "caf\xe9" in result or "café" in result
