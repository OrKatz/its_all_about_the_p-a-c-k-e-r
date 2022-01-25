import re
import dpath.util

COLLECT_VARS_AND_FUNC = "'type':\s+u'([^']+)', 'name':\su'([^']+)'"

def list_unique_identifiers(identifiers):
    js_identifiers = []
    for i in identifiers:
        js_identifiers.append(i)
    return set(js_identifiers)


def check_identifier_0x(x):
    if x.startswith('_0x'):
        return True
    return False


def check_identifier_hex(x):
    hex_encoded_identifiers = re.search(r'(\\_x[0-9a-z][0-9a-z]){4,}', str(x))
    if hex_encoded_identifiers:
        return True
    return False


def collect_func_var_names(parsed_js):
    try:
        x = re.findall(COLLECT_VARS_AND_FUNC, str(parsed_js), re.DOTALL)
    except Exception as e:
        print(e)
        return None
    return x


def var_values_extract(parsed_js):

    try:
        return dpath.util.values(parsed_js, 'body/*/declarations/*/init/elements/*/raw')

    except Exception as e:
        print(e)
        pass


def number_of_0x_identifier(identifiers):
    try:
        number_of_0x_identifiers = 0
        for id in identifiers:
            if check_identifier_0x(id[1]):
                number_of_0x_identifiers += 1
        return number_of_0x_identifiers
    except Exception as e:
        print(e)
        return None


def number_of_hex_identifier(identifiers):
    try:
        number_of_hex_identifiers = 0
        for id in identifiers:
            if check_identifier_hex(id[1]):
                number_of_hex_identifiers += 1
        return number_of_hex_identifiers
    except Exception as e:
        print(e)
        return None


def number_of_0x_var(js_var_values):
    try:
        number_of_0x_var_values = 0
        for v_value in js_var_values:
            if check_identifier_0x(v_value):
                number_of_0x_var_values += 1
        return number_of_0x_var_values
    except Exception as e:
        print(e)
        return None


def number_of_hex_var(js_var_values):
    try:
        number_of_hex_var_values = 0
        for v_value in js_var_values:
            if check_identifier_hex(v_value):
                number_of_hex_var_values += 1
        return number_of_hex_var_values
    except Exception as e:
        print(e)
        return None


def js_blocks_declarations(parsed_js):
    declarations_list = []
    for key1 in parsed_js:
        if key1 == 'body':
            for key2 in parsed_js[key1]:
                for key3 in key2:
                    if key3 == 'type':
                        declarations_list.append(key2[key3])
    return declarations_list


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', str(text))
