import dpath.util
import js_obfuscator
import config


def detect_push_shift_obfuscation_func(parsed_js):
    '''Push-shift packer signature ver 1'''
    try:
        if 'BlockStatement' in dpath.util.values(parsed_js, 'body/*/expression/callee/body/type'):
            if 'push' in dpath.util.values(parsed_js, 'body/*/expression/callee/body/body/*/declarations/*/init/body/body/*/body/body/*/expression/callee/property/value'):
                if 'shift' in dpath.util.values(parsed_js, 'body/*/expression/callee/body/body/*/declarations/*/init/body/body/*/body/body/*/expression/arguments/*/callee/property/value'):
                    return 'shift_push_obfuscation_func'
        return 'no_obfuscation'
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        return 'no_obfuscation'
        pass

def detect_push_shift_v2_obfuscation_func(parsed_js):
    '''Push-shift packer signature ver2'''
    try:
        #print(json.dumps(parsed_js, indent=4, sort_keys=True))
        if 'BlockStatement' in dpath.util.values(parsed_js, 'body/*/expression/callee/body/type'):
            if 'push' in dpath.util.values(parsed_js,'body/*/expression/callee/body/body/*/body/body/*/block/body/*/alternate/body/*/expression/callee/property/value'):
                if 'shift' in dpath.util.values(parsed_js,'body/*/expression/callee/body/body/*/body/body/*/block/body/*/alternate/body/*/expression/arguments/*/callee/property/value'):
                    return 'shift_push_v2_obfuscation_func'
        return 'no_obfuscation'
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        return 'no_obfuscation'
        pass



def detect_kaktys_encode(parsed_js):
    '''kaktys packer signature'''
    try:
        if 'FunctionDeclaration' in dpath.util.values(parsed_js, 'body/*/type'):
            if 'decodeURIComponent' in dpath.util.values(parsed_js, 'body/*/body/body/*/argument/callee/name'):
                if dpath.util.get(parsed_js, 'body/*/body/body/*/argument/arguments/*/callee/object/callee/object/object/object/name') == 'Array':
                    if dpath.util.get(parsed_js, 'body/*/body/body/*/argument/arguments/*/callee/object/arguments/*/callee/name') == 'atob':
                        return 'kaktys_encode_match_' + str(dpath.util.get(parsed_js, 'body/*/id/name'))
        return 'no_obfuscation'
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        return 'no_obfuscation'
        pass


def detect_munger_packer(parsed_js):
    '''munger packer signature'''
    try:
        if 'ExpressionStatement' in dpath.util.values(parsed_js, 'body/*/type'):
            if 'eval' in dpath.util.values(parsed_js, 'body/*/expression/callee/name'):
                if len(dpath.util.values(parsed_js, 'body/*/expression/arguments/*/callee/params/*/name')) == 6:
                    return  'munger_packer_match_' + "".join(dpath.util.values(parsed_js, 'body/*/expression/arguments/*/callee/params/*/name'))
                if 'replace' in dpath.util.values(parsed_js, 'body/*/expression/arguments/*/callee/body/body/*/body/body/*/consequent/body/*/expression/right/callee/property/name'):
                    if 'RegExp' in dpath.util.values(parsed_js, 'body/*/expression/arguments/*/callee/body/body/*/body/body/*/consequent/body/*/expression/right/arguments/*/callee/name'):
                        return 'munger_packer_match_'
        return 'no_obfuscation'
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        return 'no_obfuscation'
        pass


def detect_eval_unescape(parsed_js):
    '''eval_unescape packer signature'''
    try:
        if 'ExpressionStatement' in dpath.util.values(parsed_js, 'body/*/type'):
            if 'eval' in dpath.util.values(parsed_js, 'body/*/expression/callee/name'):
                if 'unescape' in dpath.util.values(parsed_js, 'body/*/expression/arguments/*/callee/name'):
                    return "eval_unescape_packer_match"
        return 'no_obfuscation'
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        return 'no_obfuscation'
        pass


def detect_aes_ctr_decrypt(parsed_js):
    '''aes_ctr packer signature'''
    try:
        if 'VariableDeclaration' in dpath.util.values(parsed_js, 'body/*/type'):
            if 'Aes' in dpath.util.values(parsed_js, 'body/*/declarations/*/init/callee/object/object/name') and \
                    'Ctr' in dpath.util.values(parsed_js, 'body/*/declarations/*/init/callee/object/property/name') and \
                    'decrypt' in dpath.util.values(parsed_js, 'body/*/declarations/*/init/callee/property/name'):
                return "aes_ctr_decrypt_packer_match"
        return 'no_obfuscation'
    except Exception as e:
        js_obfuscator.errors_prints(config.ERROR_TYPES['error'], e)
        return 'no_obfuscation'
        pass
