#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:44:25 2024

@author: qiaomein
"""

import csv, random, os, re



class Student(object):
    def __init__(self, l, count = 0, attempts = 0):
        self.time, self.name, self.email, self.raw_time_slot, self.year, self.spanish = l
        self.year = int(self.year[-1])
        self.count = count
        self.attempts = attempts
        self.time_slot = re.split(";|,", self.raw_time_slot)
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
        return f"- {self.name} [{self.count}] (MS{self.year}, {self.spanish}) requesting for {self.raw_time_slot} [{self.time_slot}]."

    def __hash__(self):
        return hash(self.email)

class Slots(object):
    def __init__(self):
        self.n = 10 # n total slots
        self.slot_names = ["Morning MS1","Morning MS2","Morning MS3/4","Morning Spanish MS1/2","Morning Spanish MS3/4","Afternoon MS1","Afternoon MS2","Afternoon MS3/4","Afternoon Spanish MS1/2","Afternoon Spanish MS3/4",]
        self.ms1mc, self.ms2mc, self.ms34mc, self.spanish12mc, self.spanish34mc, self.ms1ac, self.ms2ac, self.ms34ac, self.spanish12ac, self.spanish34ac = [3,3,3,2,2,3,3,4,2,2]
        self.ms1m, self.ms2m, self.ms34m, self.spanish12m, self.spanish34m, self.ms1a, self.ms2a, self.ms34a, self.spanish12a, self.spanish34a = [],[],[],[],[],[],[],[],[],[]

        
    def cleanup(self):
        self.all_slots = [self.ms1m, self.ms2m, self.ms34m, self.spanish12m, self.spanish34m, self.ms1a, self.ms2a, self.ms34a, self.spanish12a, self.spanish34a]
        self.slot_max = [self.ms1mc, self.ms2mc, self.ms34mc, self.spanish12mc, self.spanish34mc, self.ms1ac, self.ms2ac, self.ms34ac, self.spanish12ac, self.spanish34ac]



        for i in range(self.n): # loop through all the time slots
            k = list(set([str(x) for x in self.all_slots[i]])) #rids duplicates
            kl = len(k)
            names = '\n'.join(k)
            full_condition = ''
            if kl == 0:
                names = "- None available"
            elif kl == self.slot_max[i]:
                full_condition = " [FULL]"
            print(f"{self.slot_names[i]}{full_condition}: \n{names}")
            print("\n##################################################################\n")
        
        return self.all_slots
            
def removeStudent(student, student_set):
    for s in student_set:
        if student.email == s.email:
            student_set.remove(s)
            break
    return student_set
          
def isEligible(student, slots, i): # true if student can be slotted into slots.all_slots[i]
    slot_name = slots.slot_names[i]
    year = slot_name.split("MS")[-1].split('/')
    time_slot = slot_name[0].lower()
    spanish = "Spanish" in slot_name
    if str(student.year) in year and student.time_slot == time_slot and student.spanish == spanish:
        return True
    else:
        return False
            


def check_all(out, slots, all_students, students_left): # checks that output satisfies all constraints
    # out is final scheduling of students such that out[i] is the students in the ith time slot
    # slots is the final Slots object 
    # students_left is a list of all students not selected
    # all_students is a list of all students
    
    N = len(set(all_students)) 
    
    selected_students = []
    for s in out:
        selected_students.extend(s)
    
    all_slots = slots.all_slots
    
    
    # assert that students_left is subset of all_students
    assert set(students_left).issubset(set(all_students))
    
    
    # assert no duplicates in students left nor in all_students
    assert len(set(students_left)) == len(students_left) and N == len(all_students)
    
    # assert that none of the students_left are in the final output
    assert (set(students_left) & set(selected_students)) == set()
    
    # assert that no one is filled in different slots at same time
    assert len(selected_students) == len(set(selected_students))
    
    # assert that none of the students left can be slotted in
    for s in students_left:
        for i in range(slots.n):
            slot = all_slots[i]
            if len(slot) < slots.slot_max[i]: # if the slot isn't full, check if student left can be fit in
                assert not isEligible(s, slots, i)
                
    # assert that every student is in correct time slot
    for i in range(slots.n): # checking morning slots
        for student in out[i]:
            if i < 5:
                assert student.time_slot in ['m','b']
            else:
                assert student.time_slot in ['a','b']
        
        
        
                
            
    
    print("[LOG]: TESTS ALL PASSED.")
    
    
if __name__ == "__main__":
    
    
    students_dict = dict() # initialize database of all students
    
    
    filename = "responses 3.csv"
    countname = "tracker.csv"
    
    # load in responses
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
            
    
    # load in any attendance files; create one if doesn't exist
    
    print("LOG: Tracker is formatted as \n\n email | attendance | attempts \n")
    
    if countname not in os.listdir():
        print(f"LOG: attendance data file {countname} NOT detected. Creating an empty one...")
        with open(countname,'w') as f:
            for email in students_dict.keys():
                f.write(f"{email},0,0\n") # format is email: attendance, attempts to sign up
    else:
        print(f"LOG: attendance data file {countname} DETECTED. Loading...")
        with open(countname,'r') as f:
            c = f.readlines()
            tempd = dict()
            for item in c:
                k,v,attempts = item.split(',')
                v = v.strip()
                attempts = attempts.strip()
                tempd[k] = [int(v),int(attempts)]
        for email in filter(lambda x: x in list(tempd.keys()), students_dict.keys()): # update existing responses
            count,attempts = tempd[email]
            students_dict[email].count = count
            students_dict[email].attempts = attempts
        
        
        
    ############# initialize    
        
    students = list(students_dict.values()) 
    all_students = [str(s) for s in students]
    max_count = int(max([x.count for x in students])) + 1 # find max attendance of any student
    max_attempts = int(max([x.attempts for x in students])) + 1
    clist = [0] * max_count # count list; clist[i] stores the students with attendance i
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
        student_set.sort(key = lambda x: -x.attempts) # sort by attempts after shuffling
        
        student_set_spanish = list(filter(lambda x: x.spanish, student_set))
        student_set_both_spanish = list(filter(lambda x: x.time_slot == 'b', student_set_spanish))
        student_set_morning_spanish = list(filter(lambda x: x.time_slot == 'm', student_set_spanish)) 
        student_set_afternoon_spanish = list(filter(lambda x: x.time_slot == 'a', student_set_spanish))
        
        
        ## now sort students with count c based on their time slot
        
        for student in student_set_morning_spanish + student_set_both_spanish:
    
            if student.year > 2:
                if len(slots.spanish34m) < slots.spanish34mc:
                    slots.spanish34m.append(student)
                    student_set = removeStudent(student,student_set)
                    student_set_both_spanish = removeStudent(student, student_set_both_spanish)
            else:
                if len(slots.spanish12m) < slots.spanish12mc:
                    slots.spanish12m.append(student)
                    student_set = removeStudent(student,student_set)
                    student_set_both_spanish = removeStudent(student, student_set_both_spanish)
        
        # takes people in both time slots not chosen before into next one
            
        for s in student_set_afternoon_spanish + student_set_both_spanish: 
            if s.year > 2:
                if len(slots.spanish34a) < slots.spanish34ac:
                    slots.spanish34a.append(s)
                    student_set = removeStudent(s,student_set)
            else:
                if len(slots.spanish12a) < slots.spanish12ac:
                    slots.spanish12a.append(s)
                    student_set = removeStudent(s,student_set)
    
        
        student_set_both = list(filter(lambda x: x.time_slot == 'b', student_set))
        student_set_morning = list(filter(lambda x: x.time_slot == 'm', student_set))
        
        student_set_afternoon = list(filter(lambda x: x.time_slot == 'a', student_set))
        
    
        
        for student in student_set_morning + student_set_both:
    
            if student.year > 2 and len(slots.ms34m) < slots.ms34mc:
                slots.ms34m.append(student)
                student_set = removeStudent(student,student_set)
                student_set_both = removeStudent(student,student_set_both)
            elif student.year == 2 and len(slots.ms2m) < slots.ms2mc:
                slots.ms2m.append(student)
                student_set = removeStudent(student,student_set)
                student_set_both = removeStudent(student,student_set_both)
            elif student.year == 1 and len(slots.ms1m) < slots.ms1mc:
                slots.ms1m.append(student)
                student_set = removeStudent(student,student_set)
                student_set_both = removeStudent(student,student_set_both)
        
        for student in student_set_afternoon + student_set_both:
    
            if student.year > 2 and len(slots.ms34a) < slots.ms34ac:
                slots.ms34a.append(student)
                student_set = removeStudent(student,student_set)
            elif student.year == 2 and len(slots.ms2a) < slots.ms2ac:
                slots.ms2a.append(student)
                student_set = removeStudent(student,student_set)
            elif student.year == 1 and len(slots.ms1a) < slots.ms1ac:
                slots.ms1a.append(student)
                student_set = removeStudent(student,student_set)
        
        students_left.extend(student_set) # add any leftover students to students_left
    
    
                
    final = slots.cleanup() # post process to finalize all slots
    
    
    
    
    leftout = '\n'.join([str(s) for s in students_left])
    print(f"Students left out:\n{leftout}")
    
    print("\n\n")
    
    
    
    check_all(final, slots, students, students_left) 
    
    r = None
    while r not in ['Y','n']:
        r = input("[LOG]: Would you like to finalize these slots? [Y/n]\nEnter here: ")
        
    if r == 'Y':
        # increment the attendance in the attendance file
        #os.remove(countname)
        with open(countname,'w') as f:
            for s in students:
                s.attempts += 1
                if s not in students_left: # only increment if student has been selected
                    s.count += 1
                    #print(s)
                
                f.write(f"{s.email},{s.count},{s.attempts}\n")

        print("[LOG]: Attendance logged!")
    else:
        print("[LOG]: Canceled and attendance is NOT logged.")
        
    print("\n\nEmails of students selected:\n")
    print(','.join([s.email for s in filter(lambda x: x not in students_left , students)]))
    print("\n\nEmails of students NOT selected:\n")
    print(','.join([s.email for s in students_left]))
    
        
        
    
    
        
    