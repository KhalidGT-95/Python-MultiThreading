# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 12:54:22 2017

@author: Khalid
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 18:02:50 2017

@author: Khalid
"""
from threading import Thread
import math
import numpy as np
import time
import threading

Training_data = []
Testing_data = []

least_distance = 0
class_index = None

matrix_dimensions_row = None
matrix_dimensions_column = None

cosine_similarity_index = 0
num_of_threads = 0

Final_minimum_distance_and_index = {"min_dist":0,"min_index":0}

write_lock = threading.Lock()

def Take_input():
    global matrix_dimensions_row
    global matrix_dimensions_column
    global num_of_threads
    
    matrix_dimensions_row = int(input("Enter the number of rows N : "))
    matrix_dimensions_column = int(input("Enter the number of column M : "))
    num_of_threads = int(input("Enter the number of threads : "))
    print("Generating a 1xM Vector for Testing data")

def Generate_matrix():
    global X
    global random_point
    global Training_data
    global Testing_data
    global matrix_dimensions_row
    global matrix_dimensions_column
    
    Training_data = np.random.random((matrix_dimensions_row,matrix_dimensions_column))
    Testing_data = np.random.random((matrix_dimensions_column))
    
    Training_data = Training_data * 5
    Training_data = Training_data.astype(int)
    
    Testing_data = Testing_data * 5
    Testing_data = Testing_data.astype(int)
     
def Calculate_kNN_Parallel(start_index,terminating_index):
    
    global least_distance
    global class_index
    global matrix_dimensions_column
    
    for i in range(start_index,terminating_index):
        temp = 0
        sqrt_result = 1
        TrainingData_temp = 0
        TestingData_temp = 0
        
        for j in range(matrix_dimensions_column):  # Calculate the dot product
            temp += (Training_data[i][j] * Testing_data[j])
            TrainingData_temp += math.pow(Training_data[i][j],2)
            TestingData_temp += math.pow(Testing_data[j],2)
        
        a = math.sqrt(TrainingData_temp)
           
        b = math.sqrt(TestingData_temp)
       
        sqrt_result = a * b
       
        cos_theta = temp / sqrt_result
        
        if cos_theta > least_distance:
            least_distance = cos_theta
            class_index = i
    
    write_lock.acquire()
    if Final_minimum_distance_and_index["min_dist"] < cos_theta:
        Final_minimum_distance_and_index["min_dist"] = cos_theta
        Final_minimum_distance_and_index["min_index"] = class_index
    write_lock.release()
                
def Thread_function():    
    global num_of_threads
    global matrix_dimensions_row
    thread_handle = []
    
    
    for j in range(0,num_of_threads):
        t = Thread(target = Calculate_kNN_Parallel, args=(int((matrix_dimensions_row/num_of_threads) * j),int((matrix_dimensions_row/num_of_threads) * (j+1))))
        
        thread_handle.append(t)
        
        t.start()
        
    for k in range(0,num_of_threads):
        thread_handle[k].join()
        
        
Take_input()
Generate_matrix()
print("\nCalculating . . .\n")
before = time.time()

Thread_function()

after = time.time()

print("\n\n" + str(least_distance) + " and the point which is closest to it has index : " + str(class_index))

print("And the time taken is : " + str(after-before) + " seconds")