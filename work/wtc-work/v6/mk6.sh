#!/bin/bash
# usage: mk6.sh  -> builds fugue_v6 and prints check summary
../venv/bin/python build_fugue.py fugue-iv_v6.json fugue_v6_bars >/dev/null || exit 1
../venv/bin/python chk.py fugue-iv_v6.json -v | grep -E "^bars|both_attack|clash_list|par16_list|^parallel_5ths_8ves\(eighth|crossing_list|xrel_list|bar_pairs|longest_identical" | cut -c1-900
