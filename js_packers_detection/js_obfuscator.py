import os,sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

import requests
from bs4 import BeautifulSoup
from pyjsparser import parse
from js_packers_detection import config, features_collection, packers_signatures
import logging
import csv


def print_exception_context():
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno

    logging.error(str("{}: {}\n").format("Exception type: ", exception_type))
    logging.error(str("{}: {}\n").format("File name: ", filename))
    logging.error(str("{}: {}\n").format("Line number: ", line_number))


def errors_prints(log):
    """writing errors to log file"""
    try:
        logging.error(str("{}\n").format(log))
        print_exception_context()
        logging.error("#######################################\n")
    except Exception as e:
        print(e)
        pass

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
        errors_prints(e)
        pass


def func2():
    setattr(object, "attribute", "the fun things")


def features_collection_execution(list_js_features, js_code_block, parsed_js, identifiers, js_var_values):
    """Executing all file features collection def. This func will get the list of features and add new collected
    features/signature to be returned at the end of execution. The other variables the func gets are used and
    referenced dynamically in the getattr call as local variables. The getattr is executing all collection and
    signatures functionality by using configuration from config.py. In order to add new signature/feature collection
    one just need to add functionality code and configuration of the name of that func to config code."""
    try:
        for feature_type in config.LIST_OF_FEATURES:
            for feature_def in config.get_config(feature_type):
                feature_value = getattr(features_collection, feature_def)(locals()[config.get_config("LIST_OF_FEATURES")[feature_type]])
                list_js_features.append(feature_value)

        return list_js_features

    except Exception as e:
        errors_prints(e)
        pass


def features_collection_signatures_names_header():
    """Executing all file features collection name and packers signatures names for result file header """
    try:
        features_names = []
        for feature_type in config.LIST_OF_FEATURES:
            for feature_def in config.get_config(feature_type):
                features_names.append(feature_def)

        for signature_name in config.LIST_OF_SIGNATURES:
            features_names.append(signature_name)

        return features_names

    except Exception as e:
        errors_prints(e)
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
                parsed_js = parse(features_collection.remove_html_tags(js_code_block))
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
            errors_prints(e)
            pass
    return list_file_js_features


def urls_file_scan(path, results_file):
    """Scanning urls and sending to check_file for obfuscation detection"""
    file_urls = open(path, 'r').readlines()
    urls_scan(file_urls, results_file)


def urls_scan(file_urls, results_file):
    """scan list of urls (it can also be activated with list with one item (single url)"""
    with open(results_file, 'w') as csv_result_file:
        scanwriter = csv.writer(csv_result_file)
        scanwriter.writerow(['url', 'number_of_js_code_blocks', str(features_collection_signatures_names_header())])
        url_numerator = 0
        result_value = []
        # writing the output header field names
        for url in file_urls:
            try:
                url_numerator = url_numerator + 1
                url = url.strip('\n')
                r = requests.get(url, timeout=1)
                file_content = r.text
                file_result = check_file(url, file_content)
                result_value.append(file_result)
                scanwriter.writerow(file_result)

            except Exception as e:  # except KeyError:
                errors_prints(str(url_numerator) + " " + url)
                errors_prints("error on scan return value")
                errors_prints(e)
                scanwriter.writerow([url, "error_in_scan"])
        return result_value


def scan_files(file_path, results_file, single):
    """scanning local files for obfuscation detection"""
    file_numerator = 0
    result_value = []
    try:
        file_numerator = file_numerator + 1
        with open(results_file, 'w') as csv_result_file:
            scanwriter = csv.writer(csv_result_file)

            files_list = []
            scanwriter.writerow(['url', 'number_of_js_code_blocks', str(features_collection_signatures_names_header())])
            #single is boolean to distinguish scanning of single file path vs. folder with files being scanned
            if single:
                if os.path.isfile(file_path):
                    files_list.append(os.path.basename(file_path))
                    file_path = os.path.dirname(file_path)
                else:
                    print('The file path specified does not exist')
            else:
                if os.path.isdir(file_path):
                    for filename in os.listdir(file_path):
                        if filename.endswith('.js') or filename.endswith('.txt'):
                            files_list.append(filename)
                else:
                    print('The folder path specified does not exist')

            print(files_list)
            for file_name in files_list:
                if os.path.isfile(os.path.join(file_path, file_name)):
                    file_data = open(os.path.join(file_path, file_name), 'r').read()
                    file_result = check_file(os.path.join(file_path, file_name), file_data)
                    result_value.append(file_result)
                    scanwriter.writerow(file_result)
            return result_value
    except Exception as e:  # except KeyError:
        errors_prints(str(file_numerator) + " " + filename)
        errors_prints("error on scan return value")
        errors_prints(e)
        pass


def main(mode, files_scan_path="", results_file=""):
    """Main"""
    if mode == config.MODES_URLS:
        return urls_file_scan(files_scan_path, results_file)
    elif mode == config.MODES_LOCAL:
        return scan_files(files_scan_path, results_file, False)
    elif mode == config.MODES_LOCAL_SINGLE:
        return scan_files(files_scan_path, results_file, True)
    elif mode == config.MODES_URL_SINGLE:
        # since the input is single url files_scan_path is being rapped by list
        return urls_scan([files_scan_path], results_file)
    else:
        print("unknown mode!!!")
        exit(0)


if __name__ == "__main__":
    args = config.arguments_config()
    logging.basicConfig(filename='error.log', filemode='w',)
    main(args.mode, args.files, args.results)
