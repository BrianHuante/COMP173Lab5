# Programmer: Brian Huante Lopez
# Assignment: Lab 5
# Class: COMP 173
# Date: 25 Oct, 2022

import sys


def average(lst):
    return sum(lst) / len(lst)


def fcfs(p, p_dict):
    fcfs_dict = {}
    counter = 0
    for i in range(p):
        lowestStartProcess = list(p_dict.keys())[0]
        for process, valueArr in p_dict.items():
            if counter == i:
                counter += 1
                continue
            if valueArr[0] == p_dict[lowestStartProcess][0]:
                if process < lowestStartProcess:
                    lowestStartProcess = process
            elif valueArr[0] < p_dict[lowestStartProcess][0]:
                lowestStartProcess = process
            counter += 1

        fcfs_dict[lowestStartProcess] = p_dict[lowestStartProcess]
        p_dict.pop(lowestStartProcess)
        counter = i + 1

    print('FCFC:\n')
    print('\t\tPID\tArrival\t\tStart Time\tEnd Time\tRunning\tWaiting')
    print('\t\t\t\tTime\t\t\t\t\tTime\tTime\n')
    counter = 0
    start_time = 0
    ordered_p = list(fcfs_dict.keys())
    wait_arr = []
    while True:
        if fcfs_dict[ordered_p[0]][1] == counter:
            waiting_time = counter - fcfs_dict[ordered_p[0]][1]
            running_time = counter - start_time
            wait_arr.append(waiting_time)
            print("\t\t"+ordered_p[0]+"\t"+fcfs_dict[ordered_p[0]][0]+"\t\t"+start_time+"\t"+counter+"\t"+running_time
                  +"\t"+waiting_time+"\n")
            start_time = counter
            ordered_p.pop(0)
        counter += 1
        if not ordered_p:
            break
    average_wait = average(wait_arr)
    print("Average Waiting Time: ", round(average_wait, 2))


n = len(sys.argv)
if n < 3:
    sys.exit("Not enough values in command line.")

processDict = {}
with open(sys.argv[1]) as f:
    lines = [line.rstrip('\n') for line in f]
numProcesses = int(lines[0])
lines.pop(0)
for line in lines:
    processDict[int(line.split()[0])] = [int(line.split()[1]), int(line.split()[2])]

fcfs(numProcesses, processDict)
