# its_all_about_the_p-a-c-k-e-r
Javascript obfuscation packers detection
In order to test detection use python with the following attributes:  
```python js_obfuscator.py --mode local_scan --files test/ --results results.txt```


required named arguments:

--mode M [M ...]     Javascript obfuscator mode is required options are -
                     local_scan/urls_scan/single_url_scan/single_local_scan

--results R [R ...]  results file path is required

--files F [F ...]    path for scanned files or file with list of URLs is required (depends on the usage mode, "local_scan" will require folder path, "urls_scan" will require file with list of URLs and "single_url_scan" will include URL as an input)

For running the tool at imported python module use the following code:
<code>
from js_packers_detection import js_obfuscator

js_obfuscator.main('single_local_scan', 'examples/push_shift_example_phishing_2.js', 'result.csv')
</code>

The returned value will be list of detection features with the following values:
url,number_of_js_code_blocks,[js_hash, declarations_hash, num_unique_identifiers, number_of_0x_identifier, number_of_hex_identifier, num_unique_var_values, number_of_0x_var, number_of_hex_var, detect_push_shift_obfuscation_func, detect_push_shift_v2_obfuscation_func, detect_kaktys_encode, detect_munger_packer, detect_aes_ctr_decrypt, detect_eval_unescape]

As same file might contains number of javascript blocks, each will have a list of features in output.
