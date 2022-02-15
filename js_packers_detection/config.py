import argparse

MODES_LOCAL = 'local_scan'
MODES_LOCAL_SINGLE = 'single_local_scan'
MODES_URLS = 'urls_scan'
MODES_URL_SINGLE = 'single_url_scan'
DEFAULT_RESULTS_FILE = 'its_all_about_the_packer_results.txt'
DEFAULT_FILES_SCAN_PATH = '~/'
LIST_OF_SIGNATURES = ['detect_push_shift_obfuscation_func', 'detect_push_shift_v2_obfuscation_func', 'detect_kaktys_encode', 'detect_munger_packer', 'detect_aes_ctr_decrypt', 'detect_eval_unescape']
LIST_OF_JS_CODE_FEATURES = ['js_hash']
LIST_OF_JS_AST_CODE_FEATURES = ['declarations_hash', 'num_unique_identifiers']
LIST_OF_JS_IDENTIFIERS_FEATURES = ['number_of_0x_identifier', 'number_of_hex_identifier']
LIST_OF_JS_VAR_VALUES_FEATURES = ['num_unique_var_values', 'number_of_0x_var', 'number_of_hex_var']
LIST_OF_FEATURES = {'LIST_OF_JS_CODE_FEATURES': 'js_code_block', 'LIST_OF_JS_AST_CODE_FEATURES': 'parsed_js', 'LIST_OF_JS_IDENTIFIERS_FEATURES': 'identifiers', 'LIST_OF_JS_VAR_VALUES_FEATURES': 'js_var_values'}

def arguments_config():
    parser = argparse.ArgumentParser(description='Javascript Obfuscation Detector')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--mode', metavar='M', type=str,
                               help='Javascript obfuscator mode is required options are - local_scan/urls_scan/single_url_scan', required=True)
    requiredNamed.add_argument('--results', metavar='R', type=str,
                               help='results file path is required', required=True)
    requiredNamed.add_argument('--files', metavar='F', type=str,
                               help='path for scanned files is required (location of files or location of urls.txt file)', required=True)

    args = parser.parse_args()
    return args


