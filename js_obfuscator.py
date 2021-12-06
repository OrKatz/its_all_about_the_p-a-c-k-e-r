import hashlib
import os
import requests
from bs4 import BeautifulSoup
from pyjsparser import parse
import packers_signatures
import features_collection
import config


def errors_prints(log_type, log):
    """writing errors to log file"""
    errors_file.write(str("{}: {} \n").format(log_type, log))


def detection_print(url, log):
    """Printing detections"""
    print("The detection for url/file {} is:".format(url))
    for i in log:
        if log[i] != 'no_obfuscation':
            print("{} - True".format(i))


def check_file(url, body):
    """Going over file to collect features and execute obfuscation detection"""
    'contains the info for all JS codes features in a single file (i.e. - An HTML file can contains many JS codes)'
    list_file_js_features = []
    soup = BeautifulSoup(body, features="html.parser")

    'extracting all JS codes from file'
    if url.endswith(".js"):
        js_code = [body]
    else:
        js_code = soup.find_all("script")

    'Adding URL'
    list_file_js_features.append(url)
    'Adding number of JS codes'
    list_file_js_features.append(len(js_code))

    'Going over all file JS codes'
    for i in js_code:
        try:
            'All features for a single JS code (one file can contains numerous codes of JS)'
            list_js_features = []
            'When file is HTML need to remove the <script> tags'
            if url.endswith(".js"):
                parsed_js = parse(i)
            else:
                parsed_js = parse(features_collection.remove_html_tags(i))
            'store JS hash value'
            list_js_features.append(hashlib.sha256(i.encode('utf-8')).hexdigest())
            'collect all vars and func names'
            func_var_names_list = features_collection.collect_func_var_names(parsed_js)
            'collect hash of the AST declaration'
            declarations_list = features_collection.js_blocks_declarations(parsed_js)
            'store hash of the AST declaration'
            list_js_features.append(hashlib.sha256('_'.join(declarations_list).encode('utf-8')).hexdigest())
            'collect unique vars and func names (identifiers)'
            identifiers = features_collection.list_unique_identifiers(func_var_names_list)
            'push number of unique vars and func names (identifiers)'
            list_js_features.append(len(identifiers))
            'push number of identifiers starting with _0x'
            list_js_features.append(features_collection.number_of_0x_identifier(identifiers))
            'push number of identifiers hex value'
            list_js_features.append(features_collection.number_of_hex_identifier(identifiers))
            'collect Array elements'
            js_var_values = features_collection.var_values_extract(parsed_js)
            'push number of elements in Array'
            list_js_features.append(len(js_var_values))
            'push number of Array elements that starts with _0x'
            list_js_features.append(features_collection.number_of_0x_var(js_var_values))
            'push number of Array elements that are hex value'
            list_js_features.append(features_collection.number_of_hex_var(js_var_values))

            'detection of push-shift packer'
            is_obfuscation = packers_signatures.detect_push_shift_obfuscation_func(parsed_js)
            list_js_features.append(is_obfuscation)
            'detection of kaktys packer'
            is_kaktys = packers_signatures.detect_kaktys_encode(parsed_js)
            list_js_features.append(is_kaktys)
            'detection of munger packer'
            is_munger = packers_signatures.detect_munger_packer(parsed_js)
            list_js_features.append(is_munger)
            'detection of aes-ctr packer'
            is_aes_ctr = packers_signatures.detect_aes_ctr_decrypt(parsed_js)
            list_js_features.append(is_aes_ctr)
            'detection of eval(unescape packer'
            is_eval_unescape = packers_signatures.detect_eval_unescape(parsed_js)
            list_js_features.append(is_eval_unescape)

            list_file_js_features.append(list_js_features)
            if (is_aes_ctr != "no_obfuscation") or (is_eval_unescape != "no_obfuscation") or (is_munger != "no_obfuscation") or (
                    is_kaktys != "no_obfuscation") or (is_obfuscation != "no_obfuscation"):
                detection_print(url, {'is_aes_ctr': is_aes_ctr, 'is_eval_unescape': is_eval_unescape, 'is_munger': is_munger, 'is_kaktys': is_kaktys,
                                      'is_obfuscation': is_obfuscation})

        except Exception as e:
            errors_prints(config.ERROR_TYPES['error'], e)
            pass
    return list_file_js_features


def urls_file_scan(path, results_file):
    """Scanning urls and sending to check_file for obfuscation detection"""
    file_urls = open(path, 'r').readlines()
    urls_scan(file_urls, results_file)


def urls_scan(file_urls, results_file):
    """scan list of urls (it can also be activated with list with one item (single url)"""
    results = open(results_file, 'w')
    url_numerator = 0
    for url in file_urls:
        try:
            url_numerator = url_numerator + 1
            url = url.strip('\n')
            r = requests.get(url)
            file_content = r.text
            results.write(str(check_file(url, file_content)) + "\n")

        except Exception as e:  # except KeyError:
            errors_prints(str(url_numerator) + " " + config.ERROR_TYPES['url'], url)
            errors_prints(config.ERROR_TYPES['message'], "error on scan return value")
            errors_prints(config.ERROR_TYPES['error'], e)
            results.write("[{}, \"error_in_scan\"]\n".format(url))
            pass


def scan_files(file_path, results_file):
    """scanning local files for obfuscation detection"""
    file_numerator = 0
    try:
        file_numerator = file_numerator + 1
        results = open(results_file, 'w')
        files_list = []
        for filename in os.listdir(file_path):
            if filename.endswith('.js'):
                files_list.append(filename)

        print(files_list)
        for file_name in files_list:
            if os.path.isfile(os.path.join(file_path, file_name)):
                file_data = open(os.path.join(file_path, file_name), 'r').read()
                results.write(str(check_file(os.path.join(file_path, file_name), file_data)) + "\n")

    except Exception as e:  # except KeyError:
        errors_prints(str(file_numerator) + " " + config.ERROR_TYPES['url'], filename)
        errors_prints(config.ERROR_TYPES['message'], "error on scan return value")
        errors_prints(config.ERROR_TYPES['error'], e)
        pass


def main(mode, files_scan_path="", results_file=""):
    """Main"""
    if mode == 'urls_scan':
        urls_file_scan(files_scan_path, results_file)
    elif mode == 'local_scan':
        scan_files(files_scan_path, results_file)
    elif mode == 'single_url_scan':
        # since the input is single url files_scan_path is being rapped by list
        urls_scan([files_scan_path], results_file)
    else:
        print("unknown mode!!!")
        exit(0)


if __name__ == "__main__":
    errors_file = open(config.ERRORS_FILE, 'w')
    args = config.arguments_config()
    if args.mode[0] == 'urls_scan':
        if os.path.exists(args.files[0]):
            main(args.mode[0], args.files[0], args.results[0])
        else:
            print('The file with urls path specified does not exist')
    elif args.mode[0] == 'local_scan':
        if os.path.isdir(args.files[0]):
            main(args.mode[0], args.files[0], args.results[0])
        else:
            print('The files path specified does not exist')
    elif args.mode[0] == 'single_url_scan':

        main(args.mode[0], args.files[0], args.results[0])
