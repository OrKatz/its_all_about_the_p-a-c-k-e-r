# its_all_about_the_p-a-c-k-e-r
Javascript obfuscation packers detection
In order to test detection use python with the following attributes:  
```python js_obfuscator.py --mode local_scan --files test/ --results results.txt```


required named arguments:

--mode M [M ...]     Javascript obfuscator mode is required options are -
                     local_scan/urls_scan/single_url_scan/single_local_scan

--results R [R ...]  results file path is required

--files F [F ...]    path for scanned files or file with list of URLs is required (depends on the usage mode, "local_scan" will require folder path, "urls_scan" will require file with list of URLs and "single_url_scan" will include URL as an input)
 
