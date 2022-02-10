import pytest
import js_obfuscator


@pytest.fixture
def ast_input():
    return open('examples/push_shift_example_phishing_2.js', 'r').read()


def test_check_file_validation(ast_input):
    assert js_obfuscator.check_file('push_shift_example_phishing_2.js', ast_input)[0] == "push_shift_example_phishing_2.js", "test succeeded"
    assert js_obfuscator.check_file('push_shift_example_phishing_2.js', ast_input)[2][0] == "7f1180e4423878983914cbc32321293e3ec7c5daecc7ced2d8d4cdfc6dc00e84", "test succeeded"
    assert js_obfuscator.check_file('push_shift_example_phishing_2.js', ast_input)[2][1] == "835977b02ec3c1891b7314e2da3c7424916f274ef4cc0ac7e5a7e3bd4a6b3171", "test succeeded"
    assert js_obfuscator.check_file('push_shift_example_phishing_2.js', ast_input)[2][8] == "shift_push_obfuscation_func", "test succeeded"
