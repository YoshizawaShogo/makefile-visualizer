import sys
import os
import json
from pprint import pprint

def main():
    json_data = json.loads(input())
    pprint(json_data)
    sys.stdin = open('/dev/tty')

    node = ""
    hierarchy_list = []
    while True:
        order = input()
        clear_console()
        node = order
        hierarchy_list.append(node)

        display_hierarchy(hierarchy_list)
        display_children(json_data, node, len(hierarchy_list) + 1)

def clear_console():
    os.system('clear')
    
def display_hierarchy(hierarchy_list):
    buff = ""
    indent_level = 0
    for node in hierarchy_list:
        buff += "  " * indent_level + node + "\n"
        indent_level += 1
    print(buff)

def display_children(graph, parent_node, indent_level):
    buff = ""
    for node in graph[parent_node]:
        buff += "  " * indent_level + node + "\n"
    print(buff) 

if __name__ == '__main__':
    main()