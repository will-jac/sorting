## simple python script to do simple sorts

import random
import copy
import math
import time
from datetime import timedelta

## data source
def random_data(size, bound=1000):
    data = []
    for i in range(0,size):
        data.append(int(random.uniform(0,bound)))
    return data

def copy_data(data):
    d = []
    for i in range(0,len(data)):
        d.append(data[i])
    return d


class Sorter:
    name = "Sorter Name"

    def __init__(self, data):
        self.data = copy_data(data)
        self.start = time.monotonic()
        self.data = self.sort(self.data)
        self.end = time.monotonic()
        self.time = self.end - self.start

    def sort(self, data):
        return data

    def print(self):
        print(self.name + " : " + str(timedelta(seconds=self.time)))

## insertion sort
## [5,1,2,3,4,6]
## [1,5,...]
## [1,2,5,...]
class Insertion(Sorter):
    name = "Insertion Sort"
    def sort(self, data):
        for i in range(1, len(data)):
            d = data[i]
            ## insert d into correct location in the array
            j = i - 1
            while j >= 0 and data[j] > d:
                data[j+1] = data[j] # move the number forward, ie create a hole for d
                j = j - 1
                data[j+1] = d           # insert the number
        return data

class MergeTop(Sorter):
    name = "Merge Sort"

    def sort(self, data):

        def split_and_merge(data):
            length = len(data)
            if length == 1:
                return data
            middle = length // 2
            left = split_and_merge(data[:middle])
            right = split_and_merge(data[middle:])
            return merge(left, right)

        def merge(left, right):
            if left is None:
                return right
            elif right is None:
                return left

            l_len = len(left)
            r_len = len(right)

            l_i = 0
            r_i = 0
            merged = []
            while len(merged) < (l_len + r_len):
                if left[l_i] <= right[r_i]:
                    merged.append(left[l_i])
                    l_i += 1
                else:
                    merged.append(right[r_i])
                    r_i += 1

                if l_i == l_len:
                    while r_i < r_len:
                        merged.append(right[r_i])
                        r_i += 1
                    break
                elif r_i == r_len:
                    while l_i < l_len:
                        merged.append(left[l_i])
                        l_i += 1
                    break
            return merged

        return split_and_merge(data)

class MergeBottom(Sorter):
    name = "Merge Bottom"

    def sort(self, data):
        result = copy.deepcopy(data)
        part_size = 1

        while part_size < len(data) * 2:
            for i in range(0, len(data), part_size*2):
                MergeBottom.do_merge(data, i, i + part_size, part_size, result)
            # swap result and data to avoid needing to copy result -> data
            temp = data
            data = result
            result = temp
            part_size *= 2
        return result

    def do_merge(data, left, right, part_size, result):
        middle = right
        j = left

        if right >= len(data): # case where right does not exist
            while left < min(middle, len(data)):
                result[j] = data[left]
                j += 1
                left += 1
            return

        end = min(len(data), right + part_size)

        while j < end:
            if data[left] <= data[right]:
                result[j] = data[left]
                left += 1
            else:
                result[j] = data[right]
                right += 1
            j += 1
            if left >= middle:
                while right < end:
                    result[j] = data[right]
                    j += 1
                    right += 1
                return
            elif right >= end:
                while left < middle:
                    result[j] = data[left]
                    j += 1
                    left += 1
                return

class Shell(Sorter):
    name = "Shell Sort"

    def sort(self, data):

        def gap_seq(n):
            seq = []
            s = 0
            i = 1
            while s <= math.ceil(n / 3):
                s = math.ceil((1/5)*(9*(9/4)**(i - 1) - 4))
                seq.append(s)
                i += 1
            return seq

        def shell_sort(data, n):
            #for i in range(0, n):
            for i in range(1, len(data)):
                d = data[i]
                ## insert d into correct location in the array
                j = i - n
                while j >= 0 and data[j] > d:
                    data[j+n] = data[j] # move the number forward, ie create a hole for d
                    j = j - n
                data[j+n] = d           # insert the number
            return data

        seq = gap_seq(len(data))
        for i in range(len(seq) - 1, -1, -1):
            shell_sort(data, seq[i])

        return data

class Quick(Sorter):
    name = "Quick Sort"
    def sort(self, data):

        def quicksort(data, lo, hi):
            if lo < hi:
                l, r = partition(data, lo, hi)
                quicksort(data, lo, l)
                quicksort(data, r, hi)

        def partition(data, lo, hi):
            i, j = lo, hi
            #pivot = data[random.randint(i, j)]
            pivot = data[lo + (hi - lo) // 2]
            while i <= j:
                while data[i] < pivot:
                    i += 1
                while data[j] > pivot:
                    j -= 1
                if i <= j:
                    data[i], data[j] = data[j], data[i]
                    i += 1
                    j -= 1
            return j, i

        quicksort(data, 0, len(data) - 1)
        return data

class Python(Sorter):
    name="Python Sort"
    def sort(self, data):
        data.sort()
        return(data)

size = 17
print("sorting " + str(size) + " numbers")
print("assuming 1000000 operations / sec")
print("n^2 of this is    : " + str(size*size / 1000000) + " seconds")
print("n lg n of this is : " + str( size * math.log(size, 2) / 1000000) + " seconds")
data = random_data(size, 20)
#print(data)
sorted = []
#sorted.append(Insertion(copy.deepcopy(data)))
sorted.append(MergeTop(copy.deepcopy(data)))
sorted.append(MergeBottom(copy.deepcopy(data)))
sorted.append(Shell(copy.deepcopy(data)))
sorted.append(Quick(copy.deepcopy(data)))
sorted.append(Python(data))
data.sort()
#print(data)
for s in sorted:
    s.print()
    for i in range(0, len(data)):
        if data[i] != s.data[i]:
            print(s.name + " is not sorted correctly! Bad element was ["+str(s.data[i])+"], expected ["+str(data[i])+"], at pos ["+str(i)+"]")
