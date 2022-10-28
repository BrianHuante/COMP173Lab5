# Programmer: Brian Huante Lopez
# Assignment: Lab 5
# Class: COMP 173
# Date: 25 Oct, 2022

import sys


def average(lst):
    return sum(lst) / len(lst)


def sort_pdict(p, p_dict):
    return_dict = {}
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

        return_dict[lowestStartProcess] = p_dict[lowestStartProcess]
        p_dict.pop(lowestStartProcess)
        counter = i + 1
    return return_dict


def fcfs(p, p_dict):
    fcfs_dict = sort_pdict(p, p_dict)

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
    final_dict = p_dict.copy()
    for process, value in final_dict.items():
        final_dict[process] = [value[0], 0, 0, 0]

    rr_dict = sort_pdict(p, p_dict)

    print('RR: (Time quantum = '+str(time_inter)+')\n')
    print('\t\tPID\tStart Time\tEnd Time\tRunning')
    print('\t\t\t\t\t\t\tTime\n')
    counter = 0
    iteration_counter = 0
    p_counter = 0
    start_time = 0
    curr_burst = 0
    ordered_p = list(rr_dict.keys())
    wait_arr = []
    while True:
        if (iteration_counter + 1) % (time_inter + 1) == 0 or rr_dict[ordered_p[p_counter]][1] == curr_burst:
            iteration_counter = 0
            waiting_time = start_time - final_dict[ordered_p[p_counter]][0]
            final_dict[ordered_p[p_counter]][1] += waiting_time
            final_dict[ordered_p[p_counter]][0] = counter
            running_time = counter - start_time
            final_dict[ordered_p[p_counter]][2] += running_time
            final_dict[ordered_p[p_counter]][3] = counter
            print("\t\t" + str(ordered_p[p_counter]) + "\t" + str(start_time) + "\t\t" + str(counter) + "\t\t" + str(running_time) + "\n")
            start_time = counter
            if rr_dict[ordered_p[p_counter]][1] == curr_burst:
                ordered_p.pop(p_counter)
                if p_counter >= len(ordered_p):
                    p_counter = 0
            else:
                rr_dict[ordered_p[p_counter]][1] -= time_inter
                if len(ordered_p) != 1:
                    p_counter += 1
        counter += 1
        iteration_counter += 1
        curr_burst = counter - start_time
        if not ordered_p:
            break
    print('\n\n\t\tPID\tArrival\t\tRunning\t\tEnd Time\tWaiting')
    print('\t\t\tTime\t\tTime\t\tTime\n')
    for process, value in final_dict.items():
        print("\t\t" + str(process) + "\t" + str(rr_dict[process][0]) + "\t\t" + str(value[2]) + "\t\t" + str(value[3]) + "\t\t" + str(value[1]) + "\n")
        wait_arr.append(value[1])
    average_wait = average(wait_arr)
    print("Average Waiting Time: ", round(average_wait, 2))


def sjf(p, p_dict):
    sjf_dict = sort_pdict(p, p_dict)

    print('SJF:\n')
    print('\t\tPID\tArrival\t\tStart Time\tEnd Time\tRunning\t\tWaiting')
    print('\t\t\tTime\t\t\t\tTime\t\tTime\n')
    counter = 0
    p_counter = -1
    p_lock = 0
    p_done = []
    wait_counter = 0
    exit_num = len(list(sjf_dict.keys()))
    start_time = 0
    curr_burst = 0
    wait_arr = []
    sjf_dict[-1] = [-1, -1]
    while True:
        if p_lock == 0:
            for process, value in sjf_dict.items():
                if process in p_done or process == -1:
                    continue
                if counter >= sjf_dict[process][0]:
                    if sjf_dict[process][1] < sjf_dict[p_counter][1] or p_counter == -1:
                        p_counter = process
            p_lock = 1
        if sjf_dict[p_counter][1] == curr_burst and p_lock == 1:
            waiting_time = start_time - sjf_dict[p_counter][0]
            running_time = counter - start_time
            wait_arr.append(waiting_time)
            print("\t\t" + str(p_counter) + "\t" + str(sjf_dict[p_counter][0]) + "\t\t" + str(
                start_time) + "\t\t" + str(counter) + "\t\t" + str(running_time) + "\t\t" + str(waiting_time) + "\n")
            start_time = counter
            p_done.append(p_counter)
            p_counter = -1
            wait_counter += 1
            p_lock = 0
        counter += 1
        curr_burst = counter - start_time
        if wait_counter == exit_num:
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

if sys.argv[2] == "fcfs":
    fcfs(numProcesses, processDict)
elif sys.argv[2] == "rr":
    rr(numProcesses, processDict, int(sys.argv[3]))
elif sys.argv[2] == "sjf":
    sjf(numProcesses, processDict)
