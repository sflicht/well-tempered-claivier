python3 -c "
import build,sys
build.build('fug2','f2.json','Fugue I in C minor - v2 (two voices, wedge subject)','v2')" && python3 chk.py f2.json -v | grep -E "unprep|m2/M7_clash_list|^parallel_5ths_8ves\(eighth|par16_list|crossing_list|xrel_list" ; python3 implied.py f2.json | grep -E "par_|leap"
