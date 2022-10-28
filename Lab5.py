# Programmer: Brian Huante Lopez
# Assignment: Lab 5
# Class: COMP 173
# Date: 25 Oct, 2022

import sys


def average(lst): # This function calculates the average of a list
    return sum(lst) / len(lst)


def sort_pdict(p, p_dict): # This function sorts the processes by arrival time
    return_dict = {} # Initialize the dictionary that will be returned
    counter = 0
    for i in range(p): # Only doing range p because we don't need to sort more
        lowestStartProcess = list(p_dict.keys())[0] # Initialize with arrival time of first process
        for process, valueArr in p_dict.items():
            if counter == i:
                counter += 1
                continue
            if valueArr[0] == p_dict[lowestStartProcess][0]: # If arrival time equal to lowestStartProcess
                if process < lowestStartProcess: # checks PID values and lowest PID becomes new lowestStartProcess
                    lowestStartProcess = process
            elif valueArr[0] < p_dict[lowestStartProcess][0]: # If arrival time lower than lowestStartProcess then become new lowestStartProcess
                lowestStartProcess = process
            counter += 1

        return_dict[lowestStartProcess] = p_dict[lowestStartProcess] # Add new item to return_dict
        p_dict.pop(lowestStartProcess) # pop old lowestStartProcess, so we don't interact with item again
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
        if fcfs_dict[ordered_p[0]][1] == curr_burst: # go through dictionary and only printing when burst time is reached
            waiting_time = start_time - fcfs_dict[ordered_p[0]][0]
            running_time = counter - start_time
            wait_arr.append(waiting_time)
            print("\t\t"+str(ordered_p[0])+"\t"+str(fcfs_dict[ordered_p[0]][0])+"\t\t"+str(start_time)+"\t\t"+str(counter)+"\t\t"+str(running_time)+"\t\t"+str(waiting_time)+"\n")
            start_time = counter
            ordered_p.pop(0) # popping item from dictionary because we don't need it anymore
        counter += 1
        curr_burst = counter - start_time
        if not ordered_p:
            break
    average_wait = average(wait_arr)
    print("Average Waiting Time: ", round(average_wait, 2))


def rr(p, p_dict, time_inter):
    final_dict = p_dict.copy() # Making a copy of p_dict in final_dict
    for process, value in final_dict.items(): # iterating through final_dict
        final_dict[process] = [value[0], 0, 0, 0] # create a new list for each key in final_dict for stop time, end time, total wait time, and total running time

    rr_dict = sort_pdict(p, p_dict) # sort p_dict and put in rr_dict

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
        if p_counter >= len(ordered_p): # if p_counter greater than or equal to length of process left, it means it should go back to the first process
            p_counter = 0
        if start_time >= rr_dict[ordered_p[p_counter]][0]: # can only enter if start time is greater than arrival time
            if (iteration_counter + 1) % (time_inter + 1) == 0 or rr_dict[ordered_p[p_counter]][1] == curr_burst: # can only enter if time quantum is reached or burst time is reached
                iteration_counter = 0
                waiting_time = start_time - final_dict[ordered_p[p_counter]][0]
                final_dict[ordered_p[p_counter]][1] += waiting_time
                final_dict[ordered_p[p_counter]][0] = counter
                running_time = counter - start_time
                final_dict[ordered_p[p_counter]][2] += running_time
                final_dict[ordered_p[p_counter]][3] = counter
                print("\t\t" + str(ordered_p[p_counter]) + "\t" + str(start_time) + "\t\t" + str(counter) + "\t\t" + str(running_time) + "\n")
                start_time = counter
                if rr_dict[ordered_p[p_counter]][1] == curr_burst: # if burst time is reached
                    ordered_p.pop(p_counter) # we don't have to check this process anymore
                    if p_counter >= len(ordered_p): # if out of array set counter back to 0
                        p_counter = 0
                else:
                    rr_dict[ordered_p[p_counter]][1] -= time_inter # else we continue with the next process and save where we left off
                    if len(ordered_p) != 1:
                        p_counter += 1
            counter += 1
            iteration_counter += 1
            curr_burst = counter - start_time
        else:
            p_counter += 1
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
    p_lock = 0 # lock is for so we can stay on the shortest/first process
    p_done = []
    wait_counter = 0
    exit_num = len(list(sjf_dict.keys()))
    start_time = 0
    curr_burst = 0
    wait_arr = []
    sjf_dict[-1] = [-1, -1]
    while True:
        if p_lock == 0: # if lock is not set continue into if statement
            for process, value in sjf_dict.items():
                if process in p_done or process == -1: # if process is marked as done or is process -1 then continue in for loop
                    continue
                if counter >= sjf_dict[process][0]: # if arrival time less than coutner continue
                    if sjf_dict[process][1] < sjf_dict[p_counter][1] or p_counter == -1:
                        p_counter = process # sets as process that we will be using if it is the shortest or the only one
            p_lock = 1 # set lock
        if sjf_dict[p_counter][1] == curr_burst and p_lock == 1: # go into printing when burst time is reached in the locked process
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
        if wait_counter == exit_num: # break from for loop when we have done all the processes
            break
    average_wait = average(wait_arr)
    print("Average Waiting Time: ", round(average_wait, 2))


n = len(sys.argv)
if n < 3: # program will only run if we have a minimum of 3 command line arguements
    sys.exit("Not enough values in command line.")

processDict = {}
with open(sys.argv[1]) as f: # read all contents of the file and put as an array of strings in lines
    lines = [line.rstrip('\n') for line in f]
numProcesses = int(lines[0]) # store the number of processes as an int in numProcesses
lines.pop(0) # pop this element of the list for numProcesses
for line in lines:
    processDict[int(line.split()[0])] = [int(line.split()[1]), int(line.split()[2])] # make the list of processes into a dict

if sys.argv[2] == "fcfs":
    fcfs(numProcesses, processDict)
elif sys.argv[2] == "rr":
    rr(numProcesses, processDict, int(sys.argv[3]))
elif sys.argv[2] == "sjf":
    sjf(numProcesses, processDict)
