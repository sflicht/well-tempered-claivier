mk () 
{ 
    ( sed -n 1,38p fugue_v5_bars.py;
    cat expo6.py;
    echo;
    sed -n '/Episode 1 (b13/,/^# ---- metadata/p' fugue_v5_bars.py | sed '$d';
    cat adds6.py;
    sed -n '/^# ---- metadata/,$p' fugue_v5_bars.py ) > fugue_v6_bars.py && ./mkf6.sh | sed -n 2,7p
}
mk2 () 
{ 
    mk > /dev/null;
    cat meta6.py >> fugue_v6_bars.py;
    ./mkf6.sh | sed -n 2,7p
}
