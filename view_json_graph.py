import sys
import os
import json
from pprint import pprint
import curses

def run_program(stdscr, json_data):
    display_welcome(stdscr, json_data)
    curses.echo()
    stdscr.keypad(True)
    node = ""
    hierarchy_list = []

    try:
        while True: # APP
            input_buffer = ""
            while True: # until enter
                try:
                    key = stdscr.getkey()
                except curses.error:
                    continue
                #if key is not pressed, then keep polling
                if key == "KEY_LEFT":
                    input_buffer, node = transition("..", node, json_data, hierarchy_list)
                    input_buffer = ""

                    stdscr.clear()
                    display_hierarchy(stdscr, hierarchy_list)
                    display_children(stdscr, json_data, node, len(hierarchy_list) + 1)
                #when enter key press is detected
                elif key == "\n":
                    input_buffer, node = transition(input_buffer, node, json_data, hierarchy_list)

                    stdscr.clear()
                    display_hierarchy(stdscr, hierarchy_list)
                    display_children(stdscr, json_data, node, len(hierarchy_list) + 1)
                    printline(stdscr, input_buffer)
                #when backspace key press detected
                elif key == "KEY_BACKSPACE":
                    input_buffer = input_buffer[:-1]
                    y,x = stdscr.getyx()
                    stdscr.addstr(y, x, " ")
                    stdscr.addstr(y, x, "")
                elif len(key) != 1:
                    continue
                else:
                    input_buffer += key
                    _,x = stdscr.getyx()
                    x += 1

    except KeyboardInterrupt:
        stdscr.clear()
        stdscr.addstr(1, 0, "KeyboardInterrupt detected! Exiting...")
        stdscr.refresh()
        curses.napms(500)

def transition(order, now_node, json_data, hierarchy_list):
    nodes = json_data.keys()
    if order == '..':
        if len(hierarchy_list) == 0:
            return "", ""
        elif len(hierarchy_list) == 1:
            hierarchy_list.pop()
            return "", ""
        else:
            hierarchy_list.pop()
            now_node = hierarchy_list[-1]
            order = ""
            return order, now_node
    
    if len(hierarchy_list) == 0:
        if order not in nodes:
            return order, now_node
        else:
            now_node = order
            hierarchy_list.append(order)
            order = ""
            return order, now_node
    
    if order not in json_data[now_node]:
        return order, now_node
    else:
        now_node = order
        hierarchy_list.append(order)
        order = ""
        return order, now_node

    # display_hierarchy(stdscr, hierarchy_list)
    # display_children(stdscr, json_data, node, len(hierarchy_list) + 1)

def printline(stdscr, message):
    y,x = stdscr.getyx()
    stdscr.addstr(y+1, 0, message)
    stdscr.refresh()
    
def display_hierarchy(stdscr, hierarchy_list):
    buff = ""
    indent_level = 0
    for node in hierarchy_list:
        buff += "  " * indent_level + node + "\n"
        indent_level += 1
    printline(stdscr, buff)

def display_children(stdscr, graph, parent_node, indent_level):
    buff = "  " * indent_level + "..\n"
    if parent_node == '':
        display_welcome(stdscr, graph)
        return
    if parent_node not in graph:
        print("## here is end node. ##")
    else:
        for node in graph[parent_node]:
            buff += "  " * indent_level + node + "\n"
    printline(stdscr, buff)

def display_welcome(stdscr, graph):
    printline(stdscr, "## select start node ##")
    printline(stdscr, str(graph) + "\n")

def main():
    with open("tmp.txt", "rt") as f:
        json_data = json.loads(f.read())
    curses.wrapper(run_program, json_data)

if __name__ == '__main__':
    main()
