import sys
import os
import json
from pprint import pprint

def main():
    json_data = json.loads(input())
    display_welcome(json_data)

    sys.stdin = open('/dev/tty')

    nodes = json_data.keys()

    node = ""
    hierarchy_list = []
    while True:
        order = input()

        if len(hierarchy_list) == 0 and order not in nodes:
            print("no such a node")
            continue
        if len(hierarchy_list) != 0:
            if node not in nodes:
                if order != '..':
                    continue
            elif order not in json_data[node] and order != '..':
                print("no such a node")
                continue

        clear_console()

        if order == '..':
            hierarchy_list.pop()
            if len(hierarchy_list) != 0:
                node = hierarchy_list[-1]
            else:
                node = ''
        else:
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
    buff = "  " * indent_level + "..\n"
    if parent_node == '':
        display_welcome(graph)
        return
    if parent_node not in graph:
        print("## here is end node. ##")
    else:
        for node in graph[parent_node]:
            buff += "  " * indent_level + node + "\n"
    print(buff)

def display_welcome(graph):
    print("## select start node ##")
    pprint(graph)

if __name__ == '__main__':
    main()