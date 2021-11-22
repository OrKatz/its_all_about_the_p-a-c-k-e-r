import argparse

default_mode = 'local_scan'
default_results_file = 'its_all_about_the_packer_results.txt'
default_files_scan_path = '~/'
errors_file = 'errors.txt'
error_types = {'url': "URL",
               'error': "ERROR",
               'warning': "WARNING",
               'message': "MESSAGE"}

def arguments_config():

    parser = argparse.ArgumentParser(description='Javascript Obfuscation Detector')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--mode', metavar='M', type=str, nargs='+',
                        help='Javascript obfuscator mode is required options are - local_scan/urls_scan', required=True)
    requiredNamed.add_argument('--results', metavar='R', type=str, nargs='+',
                        help='results file path is required', required=True)
    requiredNamed.add_argument('--files', metavar='F', type=str, nargs='+',
                        help='path for scanned files is required (location of files or location of urls.txt file)', required=True)

    args = parser.parse_args()
    return args
