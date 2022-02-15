import pytest
import features_collection
from pyjsparser import parse

@pytest.fixture
def ast_input():
    return parse(open('../examples/push_shift_example_phishing_2.js', 'r').read())


@pytest.fixture
def var_values_input(ast_input):
    return features_collection.var_values_extract(ast_input)

@pytest.fixture
def unique_identifiers_input(ast_input):
    return features_collection.unique_identifiers(ast_input)


def test_num_unique_identifiers_list_validation(unique_identifiers_input):
    assert features_collection.num_unique_identifiers(unique_identifiers_input) == 18, "test succeeded"


def test_num_unique_var_values_validation(var_values_input):
    assert features_collection.num_unique_var_values(var_values_input) == 43, "test succeeded"


def test_check_identifier_0x_match_value():
    assert features_collection.check_identifier_0x('_0xfdfdf') is True, "test succeeded"
    assert features_collection.check_identifier_0x('0xfdfdf') is False, "test succeeded"


def test_check_identifier_hex_match_value():
    assert features_collection.check_identifier_hex('\\xdd\\xdd\\xdd\\xdd') is True, "test succeeded"
    assert features_collection.check_identifier_hex('0xfdfdf') is False, "test succeeded"


def test_number_of_0x_identifier_validation(unique_identifiers_input):
    assert features_collection.number_of_0x_identifier(unique_identifiers_input) == 2, "test succeeded"


def test_number_of_hex_identifier_validation(unique_identifiers_input):
    assert features_collection.number_of_hex_identifier(unique_identifiers_input) == 0, "test succeeded"


def test_number_of_0x_var_validation(var_values_input):
    assert features_collection.number_of_0x_var(var_values_input) == 2, "test succeeded"


def test_number_of_hex_var_validation(var_values_input):
    assert features_collection.number_of_0x_var(var_values_input) == 2, "test succeeded"


def test_declarations_hash_validation(ast_input):
    assert features_collection.declarations_hash(ast_input) == '835977b02ec3c1891b7314e2da3c7424916f274ef4cc0ac7e5a7e3bd4a6b3171', "test succeeded"
