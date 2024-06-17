#! /bin/bash

set -eu

BASE_DIR=$(cd $(dirname $0); pwd)

LANG=C make -p | python3 $BASE_DIR/make_p_to_json.py > tmp.txt
python3 $BASE_DIR/view_json_graph.py
rm -f tmp.txt