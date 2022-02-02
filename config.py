import argparse

DEFAULT_MODE = 'local_scan'
DEFAULT_RESULTS_FILE = 'its_all_about_the_packer_results.txt'
DEFAULT_FILES_SCAN_PATH = '~/'
ERRORS_FILE = 'errors.txt'
ERROR_TYPES = {'url': "URL",
               'error': "ERROR",
               'warning': "WARNING",
               'message': "MESSAGE"}
LIST_OF_SIGNATURES = ['detect_push_shift_obfuscation_func', 'detect_push_shift_v2_obfuscation_func', 'detect_kaktys_encode', 'detect_munger_packer', 'detect_aes_ctr_decrypt', 'detect_eval_unescape']

def arguments_config():
    parser = argparse.ArgumentParser(description='Javascript Obfuscation Detector')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--mode', metavar='M', type=str, nargs='+',
                               help='Javascript obfuscator mode is required options are - local_scan/urls_scan/single_url_scan', required=True)
    requiredNamed.add_argument('--results', metavar='R', type=str, nargs='+',
                               help='results file path is required', required=True)
    requiredNamed.add_argument('--files', metavar='F', type=str, nargs='+',
                               help='path for scanned files is required (location of files or location of urls.txt file)', required=True)

    args = parser.parse_args()
    return args
