import re

SCRIPT_PATH = 'multi_indicator_alerts.pine'


def read_lines():
    with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
        return f.readlines()


def test_mfi_two_arguments():
    lines = [ln for ln in read_lines() if 'ta.mfi' in ln and not ln.strip().startswith('//')]
    assert lines, 'ta.mfi calls not found'
    for ln in lines:
        # there should be exactly one comma inside the call
        inside = ln.split('ta.mfi', 1)[1]
        # Extract content between parentheses
        m = re.search(r'\(([^\)]*)\)', inside)
        assert m, 'missing parentheses'
        assert m.group(1).count(',') == 1, f'expected two arguments in ta.mfi call: {ln.strip()}'


def test_request_financial_period_param():
    lines = [ln for ln in read_lines() if 'request.financial' in ln]
    assert lines, 'request.financial calls not found'
    for ln in lines:
        assert 'period=' in ln, f'period parameter missing in: {ln.strip()}'


def test_dynamic_alerts_present():
    text = ''.join(read_lines())
    assert 'alert(' in text, 'expected runtime alert() calls for dynamic messages'


def test_no_str_format():
    text = ''.join(read_lines())
    assert 'str.format' not in text, 'str.format should not be used with series values'


def test_rating_not_compared_to_strings():
    text = ''.join(read_lines())
    assert 'rating == "' not in text and 'rating != "' not in text, 'rating compared to string literal'


def test_watchlist_parsing():
    text = ''.join(read_lines())
    assert 'input.string' in text and 'str.split' in text, 'watchlist input not parsed with str.split'


def test_version_is_5():
    lines = read_lines()
    assert lines[0].strip() == '//@version=5', 'script should declare Pine Script v5'
