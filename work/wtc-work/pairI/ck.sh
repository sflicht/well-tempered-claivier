python3 build.py piece f.json >/dev/null && python3 chk.py f.json -v | grep -E "unprep|m2/M7_clash_list|^parallel_5ths_8ves\(eighth|par16_list|crossing_list|xrel_list"
