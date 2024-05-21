#!/usr/bin/python

import sys
import json
import re
from pprint import pprint


def main():
    makefile_graph = parse_make_p(sys.stdin)
    # pprint(makefile_graph)
    json.dump(makefile_graph, sys.stdout)


def parse_make_p(fp, graphs=None):
    if graphs is None:
        graphs = []
    for l in fp:
        if l.startswith('# Make data base, printed on '):
            graphs.append(_parse_db(fp))
    if not graphs:
        raise ValueError("{} seems not connected to `LANG=C make -p`".format(fp))
    return graphs


def _parse_db(fp):
    for l in fp:
        if l.startswith('# Files'):
            fp.readline() # skip the first empty line
            entries = _parse_entries(fp)
            for key in entries:
                entries[key] = list(set(entries[key]))
            return entries
    return {}

def _parse_entries(fp):
    deps_graph = {}
    for l in fp:
        if l.startswith('# files hash-table stats:'):
            return deps_graph
        elif l.startswith('# Not a target:'):
            _skip_until_next_entry(fp)
        elif l.startswith("# makefile (from '") or l.startswith("# 'override' directive"):
            fp.readline() # skip information on target specific variable value
        else:
            _parse_entry(l, deps_graph)
            _skip_until_next_entry(fp)
    return deps_graph

TARGET_SPLIT_REGEX = re.compile(r':{1,2} *')
def _parse_entry(l, deps_graph):
    target, deps = TARGET_SPLIT_REGEX.split(l, 1)
    deps_graph[target] = [dep for dep in deps.split() if dep != '|']

def _skip_until_next_entry(fp):
    for l in fp:
        if _is_new_entry(l):
            return

def _is_new_entry(s):
    return s.startswith('\n')

if __name__ == '__main__':
    main()
