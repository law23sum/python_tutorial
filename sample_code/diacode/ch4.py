#############chapter 4


cabinet = [1, 2, 3, 3, 4, 6, 8, 12]

to_insert = 5

check_location = len(cabinet) - 1

insert_location = 0

if to_insert > cabinet[check_location]:
    insert_location = check_location + 1

cabinet.insert(insert_location, to_insert)


def insert_cabinet(cabinet, to_insert):
    check_location = len(cabinet) - 1
    insert_location = 0
    while (check_location >= 0):
        if to_insert > cabinet[check_location]:
            insert_location = check_location + 1
            check_location = - 1
        check_location = check_location - 1
    cabinet.insert(insert_location, to_insert)
    return (cabinet)


cabinet = [1, 2, 3, 3, 4, 6, 8, 12]
newcabinet = insert_cabinet(cabinet, 5)
print(newcabinet)

cabinet = [8, 4, 6, 1, 2, 5, 3, 7]
newcabinet = []

to_insert = cabinet.pop(0)
newcabinet = insert_cabinet(newcabinet, to_insert)

cabinet = [8, 4, 6, 1, 2, 5, 3, 7]


def insertion_sort(cabinet):
    newcabinet = []
    while len(cabinet) > 0:
        to_insert = cabinet.pop(0)
        newcabinet = insert_cabinet(newcabinet, to_insert)
    return (newcabinet)


sortedcabinet = insertion_sort(cabinet)
print(sortedcabinet)

from timeit import default_timer as timer

start = timer()
cabinet = [8, 4, 6, 1, 2, 5, 3, 7]
sortedcabinet = insertion_sort(cabinet)
end = timer()
print(end - start)


def insert_cabinet(cabinet, to_insert):
    check_location = len(cabinet) - 1
    insert_location = 0
    global stepcounter
    while (check_location >= 0):
        stepcounter += 1
        if to_insert > cabinet[check_location]:
            insert_location = check_location + 1
            check_location = - 1
        check_location = check_location - 1
    stepcounter += 1
    cabinet.insert(insert_location, to_insert)
    return (cabinet)


def insertion_sort(cabinet):
    newcabinet = []
    global stepcounter
    while len(cabinet) > 0:
        stepcounter += 1
        to_insert = cabinet.pop(0)
        newcabinet = insert_cabinet(newcabinet, to_insert)
    return (newcabinet)


cabinet = [8, 4, 6, 1, 2, 5, 3, 7]
stepcounter = 0
sortedcabinet = insertion_sort(cabinet)
print(stepcounter)

import random

size_of_cabinet = 10
cabinet = [int(1000 * random.random()) for i in range(size_of_cabinet)]


def check_steps(size_of_cabinet):
    cabinet = [int(1000 * random.random()) for i in range(size_of_cabinet)]
    global stepcounter
    stepcounter = 0
    sortedcabinet = insertion_sort(cabinet)
    return (stepcounter)


random.seed(5040)
xs = list(range(1, 100))
ys = [check_steps(x) for x in xs]
print(ys)

import matplotlib.pyplot as plt

plt.plot(xs, ys)
plt.title('Steps Required for Insertion Sort for Random Cabinets')
plt.xlabel('Number of Files in Random Cabinet')
plt.ylabel('Steps Required to Sort Cabinet by Insertion Sort')
plt.show()

import math
import numpy as np

random.seed(5040)
xs = list(range(1, 100))
ys = [check_steps(x) for x in xs]
ys_exp = [math.exp(x) for x in xs]
plt.plot(xs, ys)
axes = plt.gca()
axes.set_ylim([np.min(ys), np.max(ys) + 140])
plt.plot(xs, ys_exp)
plt.title('Comparing Insertion Sort to the Exponential Function')
plt.xlabel('Number of Files in Random Cabinet')
plt.ylabel('Steps Required to Sort Cabinet')
plt.show()

random.seed(5040)
xs = list(range(1, 100))
ys = [check_steps(x) for x in xs]
xs_exp = [math.exp(x) for x in xs]
Sorting and Searching
61
xs_squared = [x ** 2 for x in xs]
xs_threehalves = [x ** 1.5 for x in xs]
xs_cubed = [x ** 3 for x in xs]
plt.plot(xs, ys)
axes = plt.gca()
axes.set_ylim([np.min(ys), np.max(ys) + 140])
plt.plot(xs, xs_exp)
plt.plot(xs, xs)
plt.plot(xs, xs_squared)
plt.plot(xs, xs_cubed)
plt.plot(xs, xs_threehalves)
plt.title('Comparing Insertion Sort to Other Growth Rates')
plt.xlabel('Number of Files in Random Cabinet')
plt.ylabel('Steps Required to Sort Cabinet')
plt.show()

newcabinet = []

left = [1, 3, 4, 4, 5, 7, 8, 9]
right = [2, 4, 6, 7, 8, 8, 10, 12, 13, 14]

if left[0] > right[0]:
    to_insert = right.pop(0)
    newcabinet.append(to_insert)
elif left[0] <= right[0]:
    to_insert = left.pop(0)
    newcabinet.append(to_insert)

while (min(len(left), len(right)) > 0):
    if left[0] > right[0]:
        to_insert = right.pop(0)
        newcabinet.append(to_insert)
    elif left[0] <= right[0]:
        to_insert = left.pop(0)
        newcabinet.append(to_insert)


def merging(left, right):
    newcabinet = []
    while (min(len(left), len(right)) > 0):
        if left[0] > right[0]:
            to_insert = right.pop(0)
            newcabinet.append(to_insert)
        elif left[0] <= right[0]:
            to_insert = left.pop(0)
            newcabinet.append(to_insert)
    if (len(left) > 0):
        for i in left:
            newcabinet.append(i)
    if (len(right) > 0):
        for i in right:
            newcabinet.append(i)
    return (newcabinet)


left = [1, 3, 4, 4, 5, 7, 8, 9]
right = [2, 4, 6, 7, 8, 8, 10, 12, 13, 14]
newcab = merging(left, right)


def mergesort_two_elements(cabinet):
    newcabinet = []
    if (len(cabinet) == 1):
        newcabinet = cabinet
    else:
        left = cabinet[:math.floor(len(cabinet) / 2)]
        right = cabinet[math.floor(len(cabinet) / 2):]
        newcabinet = merging(left, right)
    return (newcabinet)


def mergesort_four_elements(cabinet):
    newcabinet = []
    if (len(cabinet) == 1):
        newcabinet = cabinet
    else:
        left = mergesort_two_elements(cabinet[:math.floor(len(cabinet) / 2)])
        right = mergesort_two_elements(cabinet[math.floor(len(cabinet) / 2):])
        newcabinet = merging(left, right)
    return (newcabinet)


cabinet = [2, 6, 4, 1]
newcabinet = mergesort_four_elements(cabinet)


def mergesort(cabinet):
    newcabinet = []
    if (len(cabinet) == 1):
        newcabinet = cabinet
    else:
        left = mergesort(cabinet[:math.floor(len(cabinet) / 2)])
        right = mergesort(cabinet[math.floor(len(cabinet) / 2):])
        newcabinet = merging(left, right)
    return (newcabinet)


cabinet = [4, 1, 3, 2, 6, 3, 18, 2, 9, 7, 3, 1, 2.5, -9]
newcabinet = mergesort(cabinet)
print(newcabinet)


def merging(left, right):
    newcabinet = []
    while (min(len(left), len(right)) > 0):
        if left[0] > right[0]:
            to_insert = right.pop(0)
            newcabinet.append(to_insert)
        elif left[0] <= right[0]:
            to_insert = left.pop(0)
            newcabinet.append(to_insert)
    if (len(left) > 0):
        for i in left:
            newcabinet.append(i)
    if (len(right) > 0):
        for i in right:
            newcabinet.append(i)
    return (newcabinet)


def mergesort(cabinet):
    newcabinet = []
    if (len(cabinet) == 1):
        newcabinet = cabinet
    else:
        left = mergesort(cabinet[:math.floor(len(cabinet) / 2)])
        right = mergesort(cabinet[math.floor(len(cabinet) / 2):])
        newcabinet = merging(left, right)
    return (newcabinet)


cabinet = [4, 1, 3, 2, 6, 3, 18, 2, 9, 7, 3, 1, 2.5, -9]
newcabinet = mergesort(cabinet)

print(sorted(cabinet))

import threading
from time import sleep


def sleep_sort(i):
    sleep(i)
    global sortedlist
    sortedlist.append(i)
    return (i)


items = [2, 4, 5, 2, 1, 7]
sortedlist = []
ignore_result = [threading.Thread(target=sleep_sort, args=(i,)).start() \
                 for i in items]

sorted_cabinet = [1, 2, 3, 4, 5]
upperbound = len(sorted_cabinet)
lowerbound = 0

import math

guess = math.floor(len(sorted_cabinet) / 2)

looking_for = 3
if (sorted_cabinet[guess] > looking_for):
    upperbound = guess
    guess = math.floor((guess + lowerbound) / 2)

if (sorted_cabinet[guess] < looking_for):
    lowerbound = guess
    guess = math.floor((guess + upperbound) / 2)

import math

sortedcabinet = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def binarysearch(sorted_cabinet, looking_for):
    guess = math.floor(len(sorted_cabinet) / 2)
    upperbound = len(sorted_cabinet)
    lowerbound = 0
    while (abs(sorted_cabinet[guess] - looking_for) > 0.0001):
        if (sorted_cabinet[guess] > looking_for):
            upperbound = guess
            guess = math.floor((guess + lowerbound) / 2)
        if (sorted_cabinet[guess] < looking_for):
            lowerbound = guess
            guess = math.floor((guess + upperbound) / 2)
    return (guess)


print(binarysearch(sortedcabinet, 8))


def inverse_sin(number):
    domain = [x * math.pi / 10000 - math.pi / 2 for x in list(range(0, 10000))]
    the_range = [math.sin(x) for x in domain]
    result = domain[binarysearch(the_range, number)]
    return (result)
