#!/bin/bash
cd /workspace/wtc-work/pairV
../venv/bin/python build_fugue6.py fugue-v_v2.json ${1:-fugue_v6_bars} >/dev/null || exit 1
../venv/bin/python chk.py fugue-v_v2.json -v > chk6.out
grep -E "^bars|both_attack|clash_list|par16_list|^parallel_5ths_8ves\(eighth|crossing_list|xrel_list|longest_identical" chk6.out | cut -c1-${2:-1500}
../venv/bin/python vact.py fugue-v_v2.json | tail -2
