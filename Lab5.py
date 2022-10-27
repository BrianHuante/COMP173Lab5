# Programmer: Brian Huante Lopez
# Assignment: Lab 5
# Class: COMP 173
# Date: 25 Oct, 2022

import sys


def fcfs(p, p_dict):
    fcfs_dict = {}
    counter = 0
    for i in range(p):
        lowestStartProcess = p_dict.keys()[0]
        for process, valueArr in p_dict.items():
            if counter == i:
                continue

            if valueArr[0] == p_dict[lowestStartProcess][0]:
                if process < lowestStartProcess:
                    lowestStartProcess = process
            elif valueArr[0] < p_dict[lowestStartProcess][0]:
                lowestStartProcess = process

        fcfs_dict[lowestStartProcess] = p_dict[lowestStartProcess]
        p_dict.pop(lowestStartProcess)
        counter += 1

    print('FCFC:\n')
    print('\t\tPID\tArrival\tStart Time\tEnd Time\tRunning\tWaiting')


n = len(sys.argv)
if n < 3:
    sys.exit("Not enough values in command line.")

processDict = {}

with open('filename') as f:
    lines = [line.rstrip('\n') for line in f]
numProcesses = int(lines[0])
lines.pop(0)

for line in lines:
    processDict[int(line.split()[0])] = [int(line.split()[1]), int(line.split()[2])]

fcfs(numProcesses, processDict)
