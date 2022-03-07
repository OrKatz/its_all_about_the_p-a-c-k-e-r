import pytest
from js_packers_detection import packers_signatures
from pyjsparser import parse

@pytest.fixture
def push_shift_input_file():
    return parse(open('../examples/push_shift_example_phishing_2.js', 'r').read())


@pytest.fixture
def push_shift_ver_2_input_file():
    return parse(open('../examples/push_shift_new_version.js', 'r').read())


@pytest.fixture
def mungar_input_file():
    return parse(open('../examples/mungar_example_with_params_packed_value.js', 'r').read())


@pytest.fixture
def kaktys_input_file():
    return parse(open('../examples/kaktys_example.js', 'r').read())

@pytest.fixture
def eval_unescape_input_file():
    return parse(open('../examples/eval_unescape_example.js', 'r').read())


@pytest.fixture
def aes_ctr_input_file():
    return parse(open('../examples/aes_ctr_example.js', 'r').read())


def test_detect_push_shift_obfuscation_func_validation(push_shift_input_file, aes_ctr_input_file):
    assert packers_signatures.detect_push_shift_obfuscation_func(push_shift_input_file) == 'shift_push_obfuscation_func', "test succeeded"
    assert packers_signatures.detect_push_shift_obfuscation_func(aes_ctr_input_file) == 'no_obfuscation', "test succeeded"


def test_detect_push_shift_v2_obfuscation_func_validation(push_shift_ver_2_input_file, push_shift_input_file):
    assert packers_signatures.detect_push_shift_v2_obfuscation_func(push_shift_ver_2_input_file) == 'shift_push_v2_obfuscation_func', "test succeeded"
    assert packers_signatures.detect_push_shift_v2_obfuscation_func(push_shift_input_file) == 'no_obfuscation', "test succeeded"


def test_detect_kaktys_encode_validation(kaktys_input_file, push_shift_ver_2_input_file):
    assert packers_signatures.detect_kaktys_encode(kaktys_input_file) == 'kaktys_encode_match__kaktys_encode', "test succeeded"
    assert packers_signatures.detect_kaktys_encode(push_shift_ver_2_input_file) == 'no_obfuscation', "test succeeded"


def test_detect_munger_packer_validation(mungar_input_file, kaktys_input_file):
    assert packers_signatures.detect_munger_packer(mungar_input_file) == 'munger_packer_match_packed', "test succeeded"
    assert packers_signatures.detect_munger_packer(kaktys_input_file) == 'no_obfuscation', "test succeeded"


def test_detect_eval_unescape_validation(eval_unescape_input_file, mungar_input_file):
    assert packers_signatures.detect_eval_unescape(eval_unescape_input_file) == 'eval_unescape_packer_match', "test succeeded"
    assert packers_signatures.detect_eval_unescape(mungar_input_file) == 'no_obfuscation', "test succeeded"


def test_detect_aes_ctr_decrypt_validation(aes_ctr_input_file, eval_unescape_input_file):
    assert packers_signatures.detect_aes_ctr_decrypt(aes_ctr_input_file) == 'aes_ctr_decrypt_packer_match', "test succeeded"
    assert packers_signatures.detect_aes_ctr_decrypt(eval_unescape_input_file) == 'no_obfuscation', "test succeeded"