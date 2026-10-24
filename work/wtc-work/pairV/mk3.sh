cd /workspace/wtc-work/pairV
source mkfun.sh; mk >/dev/null; cat meta6.py >> fugue_v6_bars.py
( cat fugue_v6_bars.py; cat adds7.py ) > fugue_v7_bars.py
sed -i "s/Fugue V in D major - v2/Fugue V in D major - v3/; s/'edition':'v2'/'edition':'v3'/; s/composition v2/composition v3/" build_fugue6.py.v3 2>/dev/null
../venv/bin/python build_fugue7.py fugue-v_v3.json fugue_v7_bars >/dev/null || exit 1
../venv/bin/python chk.py fugue-v_v3.json -v > chk7.out
grep -E "both_attack|clash_list|par16_list|^parallel_5ths_8ves\(eighth|crossing_list|xrel_list" chk7.out | cut -c1-900
../venv/bin/python vact.py fugue-v_v3.json | tail -2
