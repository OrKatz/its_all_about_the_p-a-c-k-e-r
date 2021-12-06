# text based detection dictonary
sig_dict = ['createobject', 'wscript', 'shell', 'activexbbject', 'adodb.stream', 'scripting.filesystemobject',
            'msxml2.xmlhttp']

'''Push-shift packer signature'''


def detect_push_shift_obfuscation_func(parsed_js):
    for level1 in parsed_js['body']:
        try:
            if level1['expression']['callee']['body']['type'] == 'BlockStatement':
                for level2 in level1['expression']['callee']['body']['body']:
                    for level3 in level2['declarations']:
                        for level4 in level3['init']['body']['body']:
                            for level5 in level4['body']['body']:
                                if level5['expression']['callee']['property']['value'] == 'push':
                                    for level6 in level5['expression']['arguments']:
                                        if level6['callee']['property']['value'] == 'shift':
                                            return 'shift_push_obfuscation_func'

        except Exception as e:
            pass

    return 'no_obfuscation'


'''kaktys packer signature'''


def detect_kaktys_encode(parsed_js):
    for level1 in parsed_js['body']:
        try:
            match_kaktys = False
            if level1['type'] == 'FunctionDeclaration':
                # print(level1)
                # print (level1['id']['name'])
                for level2 in level1['body']['body']:
                    if level2['argument']['callee']['name'] == 'decodeURIComponent':
                        # print(level2['argument']['callee']['name'])
                        for level3 in level2['argument']['arguments']:
                            if level3['callee']['object']['callee']['object']['object']['object']['name'] == 'Array':
                                for level4 in level3['callee']['object']['arguments']:
                                    if level4['callee']['name'] == 'atob':
                                        # print(level4['callee']['name'])
                                        return 'kaktys_encode_match_' + str(level1['id']['name'])

        except Exception as e:  # except KeyError:
            pass

    return 'no_obfuscation'


'''munger packer signature'''


def detect_munger_packer(parsed_js):
    for level1 in parsed_js['body']:
        try:
            func_vars = []
            if level1['type'] == 'ExpressionStatement':
                if level1['expression']['callee']['name'] == 'eval':
                    # print('eval string match')
                    # print(level1['expression']['callee']['name'])
                    for level2 in level1['expression']['arguments']:
                        # print("Var length - " + str(len(level2['callee']['params'])))
                        for level3 in level2['callee']['params']:
                            func_vars.append(level3['name'])
                        if len(func_vars) == 6:
                            return 'munger_packer_match_' + "".join(func_vars)
                        for level4 in level2['callee']['body']['body']:
                            for level5 in level4['body']['body']:
                                for level6 in level5['consequent']['body']:
                                    if level6['expression']['right']['callee']['property']['name'] == 'replace':
                                        # print('replace string match')
                                        # print(level6['expression']['right']['callee']['property']['name'])
                                        for level7 in level6['expression']['right']['arguments']:
                                            if level7['callee']['name'] == 'RegExp':
                                                # print('regexp string match')
                                                # print(level7['callee']['name'])
                                                return 'munger_packer_match_' + func_vars


        except Exception as e:  # except KeyError:
            pass
            # print(e)

    return 'no_obfuscation'


'''eval_unescape packer signature'''


def detect_eval_unescape(parsed_js):
    for level1 in parsed_js['body']:
        try:
            if level1['type'] == 'ExpressionStatement':
                if level1['expression']['callee']['name'] == 'eval':
                    for level2 in level1['expression']['arguments']:
                        if level2['callee']['name'] == 'unescape':
                            return "eval_unescape_packer_match"
        except Exception as e:  # except KeyError:
            pass
            # print(e)

    return 'no_obfuscation'


'''aes_ctr packer signature'''


def detect_aes_ctr_decrypt(parsed_js):
    for level1 in parsed_js['body']:
        try:
            if level1['type'] == 'VariableDeclaration':
                for level2 in level1['declarations']:
                    if (level2['init']['callee']['object']['object']['name'] == 'Aes') and (
                            level2['init']['callee']['object']['property']['name'] == 'Ctr') and (
                            level2['init']['callee']['property']['name'] == 'decrypt'):
                        return "aes_ctr_decrypt_packer_match"
        except Exception as e:  # except KeyError:
            pass
            # print(e)

    return 'no_obfuscation'
