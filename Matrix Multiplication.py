# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 17:37:57 2017

@author: Khalid
"""

from threading import Thread
import random
import math
import numpy as np
import threading
import time

Matrix_A = []
Matrix_B = []
Matrix_C = []

size_of_vectors_n = [int(math.pow(10,2)),int(math.pow(10,3)),int(math.pow(10,4))]

dimension_N = 2 # Default to a 2x2 matrix

num_of_threads = 1
def Input_for_matrix_dimensions():
    global dimension_N
    global num_of_threads
    
    dimension_N = int(input("Enter the number N to generate NxN matrix : "))
    num_of_threads = int(input("Enter the number of threads : "))
    
def Initialize_Matrix():
    global Matrix_A
    global Matrix_B
    global Matrix_C
    #for i in range(0,dimension_N):
    #    Matrix_A.append([random.randint(1,5) for i in range(0,dimension_N)])
    #print(Matrix_A)

    #Using numpy to generate matrix
    Matrix_A = np.random.random((dimension_N,dimension_N))
    Matrix_A = Matrix_A * 10
    Matrix_A = Matrix_A.astype(int)
    
    Matrix_B = np.random.random((dimension_N,dimension_N))
    Matrix_B = Matrix_B * 10
    Matrix_B = Matrix_B.astype(int)
    
    Matrix_C = np.zeros((dimension_N,dimension_N))
    Matrix_C = Matrix_C.astype(int)

def Matrix_multiply_parallel(start,end):
    for i in range(start,end):
        for j in range(dimension_N):
            for k in range(dimension_N):
                Matrix_C[i][j] += int(Matrix_A[i][k] * Matrix_B[k][j])
    
def Thread_function():
    global num_of_threads
    thread_handle = []

    for j in range(0,num_of_threads):
        t = Thread(target = Matrix_multiply_parallel, args=(int((dimension_N/num_of_threads) * j),int((dimension_N/num_of_threads) * (j+1))))
        thread_handle.append(t)
        t.start()   
        
    for j in range(0,num_of_threads):
        thread_handle[j].join()
            
if __name__=="__main__":
    
    Input_for_matrix_dimensions()
    Initialize_Matrix()
    
    start_time = time.time()
    Thread_function()
    end_time = time.time()
    
    print("Time taken to multiply two matrices in parallel comes out to be : " + str(end_time - start_time))
 