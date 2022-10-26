# Programmer: Brian Huante Lopez
# Assignment: Lab 5
# Class: COMP 173
# Date: 25 Oct, 2022

import sys


def fcfs(p, p_lines):
    fcfs_dict = {}
    for line in p_lines:
        fcfs_dict[int(line.split()[0])] = [int(line.split()[1]), int(line.split()[2])]
    for i in range(p):
        list_of_keys = [key
                        for key, list_of_values in fcfs_dict.items()
                        if i in list_of_values]


n = len(sys.argv)
if n < 3:
    sys.exit("Not enough values in command line.")

with open('filename') as f:
    lines = [line.rstrip('\n') for line in f]
numProcesses = int(lines[0])
lines.pop(0)

fcfs(numProcesses, lines)
