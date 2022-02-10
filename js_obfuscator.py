import os
import requests
from bs4 import BeautifulSoup
from pyjsparser import parse
import packers_signatures
import features_collection
import config
import sys


def print_exception_context():
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno

    config.ERRORS_FILE.write(str("{}: {} {}\n").format(config.ERROR_TYPES['error'], "Exception type: ", exception_type))
    config.ERRORS_FILE.write(str("{}: {} {}\n").format(config.ERROR_TYPES['error'], "File name: ", filename))
    config.ERRORS_FILE.write(str("{}: {} {}\n").format(config.ERROR_TYPES['error'], "Line number: ", line_number))


def errors_prints(log_type, log):
    """writing errors to log file"""
    config.ERRORS_FILE.write(str("{}: {} \n").format(log_type, log))
    print_exception_context()
    config.ERRORS_FILE.write("#######################################\n")


def detection_print(url, log):
    """Printing detections"""
    print("The detection for url/file {} is:".format(url))
    for i in log:
        if log[i] != 'no_obfuscation':
            print("{} - True".format(i))


def signatures_execution(list_js_features, parsed_js, url):
    """Executing all packers signature def and print results"""
    try:
        detection_print_values = {}
        for detection_def in config.LIST_OF_SIGNATURES:
            detection_value = getattr(packers_signatures, detection_def)(parsed_js)
            detection_print_values[detection_def] = detection_value
            list_js_features.append(detection_value)

        detection_print(url, detection_print_values)
        return list_js_features

    except Exception as e:
        errors_prints(config.ERROR_TYPES['error'], e)
        pass


def features_collection_execution(list_js_features, js_code_block, parsed_js, identifiers, js_var_values):
    """Executing all file features collection def"""
    try:
        for feature_type in config.LIST_OF_FEATURES:
            for feature_def in eval('config.'+feature_type):
                feature_value = getattr(features_collection, feature_def)(eval(config.LIST_OF_FEATURES[feature_type]))
                list_js_features.append(feature_value)

        return list_js_features

    except Exception as e:
        errors_prints(config.ERROR_TYPES['error'], e)
        pass


def features_collection_signatures_names_header():
    """Executing all file features collection name and packers signatures names for result file header """
    try:
        features_names = []
        for feature_type in config.LIST_OF_FEATURES:
            for feature_def in eval('config.'+feature_type):
                features_names.append(feature_def)

        for signature_name in config.LIST_OF_SIGNATURES:
            features_names.append(signature_name)

        return features_names

    except Exception as e:
        errors_prints(config.ERROR_TYPES['error'], e)
        pass


def check_file(url, body):
    """Going over file to collect features and execute obfuscation detection"""
    #contains the info for all JS codes features in a single file (i.e. - An HTML file can contains many JS codes)
    list_file_js_features = []
    soup = BeautifulSoup(body, features="html.parser")

    #extracting all JS codes from file
    if url.endswith(".js"):
        js_code = [body]
    else:
        js_code = soup.find_all("script")

    #Adding URL
    list_file_js_features.append(url)
    #Adding number of JS codes
    list_file_js_features.append(len(js_code))

    #Going over all file JS code blocks in given file
    for js_code_block in js_code:
        try:
            #All features for a single JS code (one file can contains numerous codes of JS)
            list_js_features = []
            #When file is HTML need to remove the <script> tags
            if url.endswith(".js"):
                parsed_js = parse(js_code_block)
            else:
                parsed_js = parse(features_collection.remove_html_tags(i))
            #Collect func/var values
            identifiers = features_collection.unique_identifiers(parsed_js)
            #collect Array elements
            js_var_values = features_collection.var_values_extract(parsed_js)
            #collecting all features from different JS parsed data including the JS code, the ASP code representation, the collected identifiers and Array values
            list_js_features = features_collection_execution(list_js_features, js_code_block, parsed_js, identifiers, js_var_values)
            #executing the packers signatures
            list_js_features = signatures_execution(list_js_features, parsed_js, url)
            #adding all JS code features to the file features strcture
            list_file_js_features.append(list_js_features)

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
    # writing the output header field names
    results.write('url' + 'number_of_js_code_blocks' + str(features_collection_signatures_names_header()) + "\n")
    for url in file_urls:
        try:
            url_numerator = url_numerator + 1
            url = url.strip('\n')
            r = requests.get(url, timeout=1)
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
        results.write('url, ' + 'number_of_js_code_blocks, ' + str(features_collection_signatures_names_header()) + "\n")
        for filename in os.listdir(file_path):
            if filename.endswith('.js') or filename.endswith('.txt'):
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
    args = config.arguments_config()
    if args.mode == 'urls_scan':
        if os.path.exists(args.files):
            main(args.mode, args.files, args.results)
        else:
            print('The file with urls path specified does not exist')
    elif args.mode == 'local_scan':
        if os.path.isdir(args.files):
            main(args.mode, args.files, args.results)
        else:
            print('The files path specified does not exist')
    elif args.mode == 'single_url_scan':
        main(args.mode, args.files, args.results)
    else:
        print("unknown mode type was used")
