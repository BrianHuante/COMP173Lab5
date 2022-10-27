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
    print('\t\tPID\tArrival\t\tStart Time\tEnd Time\tRunning\t\tWaiting')
    print('\t\t\tTime\t\t\t\tTime\t\tTime\n')
    counter = 0
    start_time = 0
    curr_burst = 0
    ordered_p = list(fcfs_dict.keys())
    wait_arr = []
    while True:
        if fcfs_dict[ordered_p[0]][1] == curr_burst:
            waiting_time = start_time - fcfs_dict[ordered_p[0]][0]
            running_time = counter - start_time
            wait_arr.append(waiting_time)
            print("\t\t"+str(ordered_p[0])+"\t"+str(fcfs_dict[ordered_p[0]][0])+"\t\t"+str(start_time)+"\t\t"+str(counter)+"\t\t"+str(running_time)+"\t\t"+str(waiting_time)+"\n")
            start_time = counter
            ordered_p.pop(0)
        counter += 1
        curr_burst = counter - start_time
        if not ordered_p:
            break
    average_wait = average(wait_arr)
    print("Average Waiting Time: ", round(average_wait, 2))


def rr(p, p_dict, time_inter):
    rr_dict = {}
    final_dict = p_dict
    for process, value in final_dict.items():
        value = [value[0], 0, 0, 0]
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

        rr_dict[lowestStartProcess] = p_dict[lowestStartProcess]
        p_dict.pop(lowestStartProcess)
        counter = i + 1

    print('RR: (Time quantum = '+str(time_inter)+')\n')
    print('\t\tPID\tStart Time\tEnd Time\tRunning')
    print('\t\t\t\t\t\t\t\t\t\t\tTime\n')
    counter = 0
    p_counter = 0
    start_time = 0
    curr_burst = 0
    ordered_p = list(rr_dict.keys())
    wait_arr = []
    while True:
        if (counter + 1) % time_inter == 0 or rr_dict[ordered_p[p_counter]][1] == curr_burst:
            waiting_time = start_time - final_dict[p_counter][0]
            final_dict[p_counter][0] = counter
            running_time = counter - start_time
            final_dict[p_counter][2] += (counter - start_time)
            final_dict[p_counter][3] = counter
            print("\t\t" + str(ordered_p[p_counter]) + "\t" + str(start_time) + "\t\t" + str(counter) + "\t\t" + str(running_time) + "\n")
            start_time = counter
            if rr_dict[ordered_p[p_counter]][1] == curr_burst:
                ordered_p.pop(p_counter)
                final_dict[p_counter][1] += waiting_time
            p_counter = (p_counter + 1) % len(ordered_p)
        counter += 1
        curr_burst = counter - start_time
        if not ordered_p:
            break
    print('\t\tPID\tArrival\t\tRunning\tEnd Time\t\tWaiting')
    print('\t\t\tTime\t\tTime\t\t\tTime\n')
    for process, value in final_dict.items():
        print("\t\t" + str(process) + "\t" + str(rr_dict[ordered_p[0]][0]) + "\t\t" + str(value[2]) + "\t\t" + str(value[3]) + "\t\t" + str(value[1]) + "\n")
        wait_arr.append(value[1])
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

if sys.argv[2] == "fcfs":
    fcfs(numProcesses, processDict)
elif sys.argv[2] == "rr":
    rr(numProcesses, processDict, int(sys.argv[3]))
