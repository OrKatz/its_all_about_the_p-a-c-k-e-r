import re
import dpath.util
import hashlib
import js_obfuscator
import config

COLLECT_VARS_AND_FUNC_REGEX = "'type':\s+u?'([^']+)', 'name':\su?'([^']+)'"
CHECK_IDENTIFIER_HEX_REGEX = r'(\\_x[0-9a-z][0-9a-z]){4,}'


def unique_identifiers(parsed_js):
    try:
        js_identifiers = []
        for i in collect_func_var_names(parsed_js):
            js_identifiers.append(i)
        return set(js_identifiers)
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        pass


def num_unique_identifiers(js_identifiers):
    return len(js_identifiers)


def num_unique_var_values(js_var_values):
    return len(js_var_values)


def check_identifier_0x(x):
    if x.startswith('_0x'):
        return True
    return False



def check_identifier_hex(x):
    try:
        hex_encoded_identifiers = re.search(CHECK_IDENTIFIER_HEX_REGEX, str(x))
        if hex_encoded_identifiers:
            return True
        return False
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        pass


def collect_func_var_names(parsed_js):
    try:
        x = re.findall(COLLECT_VARS_AND_FUNC_REGEX, str(parsed_js), re.DOTALL)
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        return None
    return x


def var_values_extract(parsed_js):
    try:
        values = []
        if dpath.util.values(parsed_js, 'body/*/declarations/*/init/elements/*/raw'):
            values = [x.strip('\'') for x in dpath.util.values(parsed_js, 'body/*/declarations/*/init/elements/*/raw')]
        elif dpath.util.values(parsed_js, 'body/*/body/body/*/declarations/*/init/elements/*/raw'):
            #also pulling array being placed in a function
            values = [x.strip('\'') for x in dpath.util.values(parsed_js, 'body/*/body/body/*/declarations/*/init/elements/*/raw')]
        return(values)

    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        pass


def number_of_0x_identifier(identifiers):
    try:
        number_of_0x_identifiers = 0
        for id in identifiers:
            if check_identifier_0x(id[1]):
                number_of_0x_identifiers += 1
        return number_of_0x_identifiers
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        return None


def number_of_hex_identifier(identifiers):
    try:
        number_of_hex_identifiers = 0
        for id in identifiers:
            if check_identifier_hex(id[1]):
                number_of_hex_identifiers += 1
        return number_of_hex_identifiers
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        return None


def number_of_0x_var(js_var_values):
    try:
        number_of_0x_var_values = 0
        for v_value in list(js_var_values):
            if check_identifier_0x(v_value):
                number_of_0x_var_values += 1
        return number_of_0x_var_values
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        return None


def number_of_hex_var(js_var_values):
    try:
        number_of_hex_var_values = 0
        for v_value in js_var_values:
            if check_identifier_hex(v_value):
                number_of_hex_var_values += 1
        return number_of_hex_var_values
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        return None


def js_blocks_declarations(parsed_js):
    try:
        return dpath.util.values(parsed_js, 'body/*/type')

    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        pass


def remove_html_tags(text):
    """Remove html tags from a string"""
    try:
        clean = re.compile('<.*?>')
        return re.sub(clean, '', str(text))
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        pass


def js_hash(js_code_block):
    """return hash value of js code block"""
    try:
        return hashlib.sha256(js_code_block.encode('utf-8')).hexdigest()
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        pass


def declarations_hash(parsed_js):
    """return hash value of js declarations"""
    try:
        return hashlib.sha256('_'.join(js_blocks_declarations(parsed_js)).encode('utf-8')).hexdigest()
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        pass
