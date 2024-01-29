#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:44:25 2024

@author: qiaomein
"""

import csv, random, os



class Student(object):
    def __init__(self, l, count = 0):
        self.time, self.name, self.email, self.raw_time_slot, self.year, self.spanish = l
        self.year = int(self.year[-1])
        self.count = count
        self.time_slot = self.raw_time_slot.split(",")
        if len(self.time_slot) == 2:
            self.time_slot = 'b'
        else:
            if self.time_slot[0][0] == '9':
                self.time_slot = 'm'
            elif self.time_slot[0][0] == '1':
                self.time_slot = 'a'
                
        if self.spanish == "Yes":
            self.spanish = True
        else:
            self.spanish = False
            
    def __eq__(self, o):
        return self.email == o.email
    
    def __str__(self):
        return f"- {self.name} [{self.count}] (MS{self.year}, {self.spanish}) requesting for {self.raw_time_slot}."

class Slots(object):
    def __init__(self):
        self.n = 10 # n total slots
        self.slot_names = ["Morning MS1","Morning MS2","Morning MS3/4","Morning Spanish MS1/2","Morning Spanish MS3/4","Afternoon MS1","Afternoon MS2","Afternoon MS3/4","Afternoon Spanish MS1/2","Afternoon Spanish MS3/4",]
        self.ms1mc, self.ms2mc, self.ms34mc, self.spanish12mc, self.spanish34mc, self.ms1ac, self.ms2ac, self.ms34ac, self.spanish12ac, self.spanish34ac = [3,3,3,2,2,3,3,4,2,2]
        self.ms1m, self.ms2m, self.ms34m, self.spanish12m, self.spanish34m, self.ms1a, self.ms2a, self.ms34a, self.spanish12a, self.spanish34a = [],[],[],[],[],[],[],[],[],[]

        
    def cleanup(self):
        self.all_slots = [self.ms1m, self.ms2m, self.ms34m, self.spanish12m, self.spanish34m, self.ms1a, self.ms2a, self.ms34a, self.spanish12a, self.spanish34a]
        self.slot_max = [self.ms1mc, self.ms2mc, self.ms34mc, self.spanish12mc, self.spanish34mc, self.ms1ac, self.ms2ac, self.ms34ac, self.spanish12ac, self.spanish34ac]

        for i in range(self.n):
            k = list(set([str(x) for x in self.all_slots[i]]))
            names = '\n'.join(k)
            if len(self.all_slots[i]) == 0:
                names = "- None available"
            print(f"{self.slot_names[i]}: \n{names}")
            print("\n##################################################################\n")
        
        return self.all_slots
            
def removeStudent(student, student_set):
    for s in student_set:
        if student.email == s.email:
            student_set.remove(s)
            break
    return student_set
            
        
    
if __name__ == "__main__":
    students_dict = dict()
    
    
    filename = "responses.csv"
    countname = "attendance.csv"
    
    
    try:
        with open(filename, mode="r") as file:
            data = csv.DictReader(file)
        
            for d in data:
                
                entry = list(d.values())
                s = Student(entry)
        
                students_dict[s.email] = s
    except FileNotFoundError:
        print(f"ERROR: Please ensure {filename} is in same directory as this program.")
        raise
            
    
    
    if countname not in os.listdir():
        print(f"LOG: attendance data file {countname} NOT detected. Creating an empty one...")
        with open(countname,'w') as f:
            for email in students_dict.keys():
                f.write(f"{email},0\n")
    else:
        print(f"LOG: attendance data file {countname} DETECTED. Loading...")
        with open(countname,'r') as f:
            c = f.readlines()
            tempd = dict()
            for item in c:
                k,v = item.split(',')
                v = v.strip()
                tempd[k] = int(v)
        for email in filter(lambda x: x in list(tempd.keys()), students_dict.keys()):
            count = tempd[email]
            students_dict[email].count = count
        
        
    students = list(students_dict.values())
    max_count = int(max([x.count for x in students])) + 1
    clist = [0] * max_count
    
    
    for c in range(0,max_count):
        temp = list(filter(lambda x: int(x.count) == c, students))
        clist[c] = temp
        #print(f"{c}: {[str(x) for x in temp]}")
        
    print("\n##################################################################\n")
    
    # clist contains students with c count at clist[c]
    
    
    slots = Slots()
    
    students_left = []
    
    for c in range(0,max_count): # loop through all students (sorted by count)
    
        student_set = clist[c]
        random.shuffle(student_set) # randomize 
        
        student_set_spanish = list(filter(lambda x: x.spanish, student_set))
        
        student_set_both_spanish = list(filter(lambda x: x.time_slot == 'b', student_set_spanish))
        student_set_morning_spanish = list(filter(lambda x: x.time_slot == 'm', student_set_spanish)) + student_set_both_spanish
        student_set_afternoon_spanish = list(filter(lambda x: x.time_slot == 'a', student_set_spanish))
        
        
        ## now sort students with count c based on their time slot
        
        for student in student_set_morning_spanish:
    
            if student.year > 2:
                if len(slots.spanish34m) < slots.spanish34mc:
                    slots.spanish34m.append(student)
                    student_set = removeStudent(student,student_set)
            else:
                if len(slots.spanish12m) < slots.spanish12mc:
                    slots.spanish12m.append(student)
                    student_set = removeStudent(student,student_set)
        
        # takes people in both time slots not chosen before into next one
            
        for student in student_set_afternoon_spanish + list(filter(lambda x: x.spanish, student_set)): 
            if student.year > 2:
                if len(slots.spanish34a) < slots.spanish34ac:
                    slots.spanish34a.append(student)
                    student_set = removeStudent(student,student_set)
            else:
                if len(slots.spanish12a) < slots.spanish12ac:
                    slots.spanish12a.append(student)
                    student_set = removeStudent(student,student_set)
    
        
        student_set_both = list(filter(lambda x: x.time_slot == 'b', student_set))
        student_set_morning = list(filter(lambda x: x.time_slot == 'm', student_set)) + student_set_both
        student_set_afternoon = list(filter(lambda x: x.time_slot == 'a', student_set))
        
    
        
        for student in student_set_morning:
    
            if student.year > 2 and len(slots.ms34m) < slots.ms34mc:
                slots.ms34m.append(student)
                student_set = removeStudent(student,student_set)
            elif student.year == 2 and len(slots.ms2m) < slots.ms2mc:
                slots.ms2m.append(student)
                student_set = removeStudent(student,student_set)
            elif student.year == 1 and len(slots.ms1m) < slots.ms1mc:
                slots.ms1m.append(student)
                student_set = removeStudent(student,student_set)
        
        for student in student_set_afternoon + student_set:
    
            if student.year > 2 and len(slots.ms34a) < slots.ms34ac:
                slots.ms34a.append(student)
                student_set = removeStudent(student,student_set)
            elif student.year == 2 and len(slots.ms2a) < slots.ms2ac:
                slots.ms2a.append(student)
                student_set = removeStudent(student,student_set)
            elif student.year == 1 and len(slots.ms1a) < slots.ms1ac:
                slots.ms1a.append(student)
                student_set = removeStudent(student,student_set)
        
        students_left.extend(student_set)
    
    
                
    final = slots.cleanup()
    
    leftout = '\n'.join([str(s) for s in students_left])
    print(f"Students left out:\n{leftout}")
    
    print("\n\n")
    
    r = None
    while r not in ['Y','n']:
        r = input("[LOG]: Would you like to finalize these slots? [Y/n]\n")
        
    if r == 'Y':
        # increment the attendance in the attendance file
        #os.remove(countname)
        with open(countname,'w') as f:
            for email,s in list(students_dict.items()):
                if s not in students_left:
                    c = s.count + 1
                    f.write(f"{email},{c}\n")

        print("[LOG]: Attendance logged!")
    else:
        print("[LOG]: Canceled and attendance is NOT logged.")
        
        
    
    
        
    