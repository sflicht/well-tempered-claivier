#!/bin/bash
cd /workspace/wtc-work/pairV
../venv/bin/python build_fugue6.py fugue-v_v1.json ${1:-fugue_v5_bars} >/dev/null || exit 1
../venv/bin/python chk.py fugue-v_v1.json -v | grep -E "^bars|both_attack|clash_list|par16_list|^parallel_5ths_8ves\(eighth|crossing_list|xrel_list|bar_pairs|longest_identical" | cut -c1-1400
