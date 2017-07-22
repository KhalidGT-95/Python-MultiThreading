# -*- coding: utf-8 -*-
"""
Created on Fri Tue 18 10:43:06 2017

@author: Khalid
"""

from threading import Thread
import threading
import random
import time
import numpy as npy
import math
import time

Vector_X = []        # Vector to be used as a dataset
Vector_Y = []        # Used for Vector addition
Result_vector = []   # Third vector to store the results in

size_of_vectors_n = [int(math.pow(10,5)),int(math.pow(10,7)),int(math.pow(10,8))] #Three different size of vectors, user can choose one of these

choice = 0      # selected choice of the user
thread_size = 0 # Number of threads to be used in the program

write_lock = threading.Lock()   # Lock to be used to synchronize 

Final_min_value_of_vector = 100     # Initialized to be some random value 

Total_average = 0       # contains average returned by each chunk of the thread

################## Input taken from the user ###################
def Input_for_vector_size():
    global thread_size
    global choice
    choice = int(input("Enter 1 for 10^5 size vector , Enter 2 for 10^7 size vector , Enter 3 for 10^8 size vector : "))
    thread_size = int(input("Enter the number of threads : "))

################### Initialize the vectors to some random value between 1 and 100 ###################
def Initialize_Vectors():
    for i in range(0,size_of_vectors_n[choice-1]):
        Vector_X.append(random.randint(1,100))
        Vector_Y.append(random.randint(1,100))

################### Summation of two vectors ###################
def Sum_two_vectors(start_index,terminating_index):
    for iterator in range(start_index,terminating_index):
        Result_vector.append(Vector_X[iterator] + Vector_Y[iterator]) # Assign the result to the result vector
            
################### Finds the minimum value in each chunk of the vector ###################
def Find_minimum_in_a_vector(start_index,terminating_index):
    min_num = min(Vector_X[start_index:terminating_index])
    return min_num

################### Finds the average value of each chunk of the vector ###################
def Find_average_of_numbers_in_a_vector(start_index,terminating_index):
    return npy.average(Result_vector[start_index:terminating_index])

################### This function is called by each thread to perform summation ###################
def Base_function_for_sum(name,start_index,terminating_index):
    Sum_two_vectors(start_index,terminating_index)
    
################### This function is called by each thread to find average in the chunk ###################
def Base_function_for_avg(name,start_index,terminating_index):
    global Total_average
    Total_average += Find_average_of_numbers_in_a_vector(start_index,terminating_index) # Add all the averages

################### This function is called by each thread to find minimum value in the chunk ###################
def Base_function_for_min(name,start_index,terminating_index):
    global Final_min_value_of_vector
    temp_min_value_in_chunk = Find_minimum_in_a_vector(start_index,terminating_index)

    write_lock.acquire()    # Lock required because we are assigning the mimimum value, If it is smaller than the current value then update it.
    if Final_min_value_of_vector > temp_min_value_in_chunk:     # If final minimum value is greater than the value found in this chunk, update it 
        Final_min_value_of_vector = temp_min_value_in_chunk
    write_lock.release()   # Release the lock

################### Called by the Main thread to print the average value found by each thread ###################
def Print_final_average():
    Final_average = Total_average / thread_size     # Average value found by dividing sum of average by number of threads
    print("The final average of Resulting Vector is " + str(Final_average))

################### Called by Main thread to print the minimum value in X ###################
def Print_min_value_in_vector():
    print("The min value in Vector_X is : " + str(Final_min_value_of_vector))

################### Invoked by Main thread to fork threads which perform summation in parallel ###################
def Thread_function_for_sum():
    thread_handle = []
    for j in range(0,thread_size):
        # Passed two parameters to the function, the start index and the ending index so that the thread accesses only a specific portion of the vector
        t = Thread(target = Base_function_for_sum, args=(str(j) , int((size_of_vectors_n[choice-1]/thread_size) * j),int((size_of_vectors_n[choice-1]/thread_size) * (j+1))))
        thread_handle.append(t)
        t.start()
    
    for j in range(0,thread_size):
        thread_handle[j].join()

################### Invoked by Main thread to fork threads which find average in parallel ###################
def Thread_function_for_average():
    thread_handle = []

    for j in range(0,thread_size):
        # Passed two parameters to the function, the start index and the ending index so that the thread accesses only a specific portion of the vector
        t = Thread(target = Base_function_for_avg, args=(str(j) , int((size_of_vectors_n[choice-1]/thread_size) * j),int((size_of_vectors_n[choice-1]/thread_size) * (j+1))))
        thread_handle.append(t)
        t.start()
        
    for j in range(0,thread_size):
        thread_handle[j].join()

################### Invoked by Main thread to fork threads which find average in parallel ###################
def Thread_function_for_min():
    thread_handle = []

    for j in range(0,thread_size):
        # Passed two parameters to the function, the start index and the ending index so that the thread accesses only a specific portion of the vector
        t = Thread(target = Base_function_for_min, args=(str(j) , int((size_of_vectors_n[choice-1]/thread_size) * j),int((size_of_vectors_n[choice-1]/thread_size) * (j+1))))
        thread_handle.append(t)
        t.start()
        
    for j in range(0,thread_size):
        thread_handle[j].join()

if __name__=="__main__":
    
    Input_for_vector_size()
    
    start_time_main = time.time()
    Initialize_Vectors()
    start_time_end = time.time()
    print("\nTime taken to initialize the array with random numbers is " + str(start_time_end - start_time_main))
    
    start_time = time.time()
    Thread_function_for_sum()
    end_time = time.time()
    print("\nTotal time taken when summing array of size " + str(size_of_vectors_n[choice-1]) + " is " + str(end_time - start_time))
    
    start_time = time.time()
    Thread_function_for_average()
    end_time = time.time()
    Print_final_average()
    
    print("\nTotal time taken when finding average of size " + str(size_of_vectors_n[choice-1]) + " is " + str(end_time - start_time))
    
    start_time = time.time()
    Thread_function_for_min()
    end_time = time.time()
    Print_min_value_in_vector()
    
    print("\nTotal time taken when finding minimum of size " + str(size_of_vectors_n[choice-1]) + " is " + str(end_time - start_time))   
    
    print("\nTotal time taken by the program (including time for initialization) is " + str(time.time() - start_time_main))