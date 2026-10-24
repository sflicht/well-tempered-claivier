#!/bin/bash
cd /workspace/wtc-work/pairV
../venv/bin/python build_prelude5.py prelude-v_v1.json ${1:-prelude_v1_bars} >/dev/null || exit 1
../venv/bin/python chk.py prelude-v_v1.json -v | grep -E "both_att|clash_list|par16_list|par_list|xrel_list|crossing_list|identical|^parallel_5ths|one_held_list" | cut -c1-2500
echo ---implied; ../venv/bin/python implied.py prelude-v_v1.json | cut -c1-3000
