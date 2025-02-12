#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:44:25 2024

@author: qiaomein
"""

import csv, random, os, re
import streamlit as st
import pandas as pd

def logout(*s): print(f"[LOG]: {s}")

class Student(object): # pass in a line (l) from the csv file as a list
    def __init__(self, l, count = 0, attempts = 0):
        # TODO: handle if l goes wrong
        if l is None: # nameless student
            return
        
    
        self.slot = None # should start with no slot; this is index corresponding to order listed in Slots class
        try:
            self.time, self.name, self.email, self.raw_time_slot, self.year, self.spanish = l
        except:
            raise IndexError
        
        self.year = int(self.year[-1])
        self.count = count
        self.attempts = attempts
        self.time_slot = re.split(";|,", self.raw_time_slot)
        if len(self.time_slot) == 2:
            self.time_slot = "m/a"
        else:
            rawstring = self.time_slot[0]
            rawstring = re.findall(r'\d{1,2}:\d{2}', rawstring)
            assert len(rawstring) == 2
            
            if int(rawstring[0].split(':')[0]) < int(rawstring[1].split(':')[0]):
                self.time_slot = 'm'
            else:
                self.time_slot = 'a'
                
        if self.spanish == "Yes":
            self.spanish = True
        else:
            self.spanish = False
            
    def __eq__(self, o):
        return self.email == o.email
    
    def __str__(self):
        sptext = "E"
        if self.spanish:
            sptext = "E/S"
        return f"- {self.name} [{self.count}/{self.attempts}] (MS{self.year}, {sptext}) for time slots {self.raw_time_slot} [{self.time_slot}]."

    def __hash__(self):
        return hash(self.email)
    
    def __repr__(self):
        return f"{self.email}"

class Slots: # indices correspond to slot names
    def __init__(self):
        self.n = 10
        self.slot_names = [
            "Morning MS1", "Morning MS2", "Morning MS3/4", "Morning [S] MS1/2", "Morning [S] MS3/4",
            "Afternoon MS1", "Afternoon MS2", "Afternoon MS3/4", "Afternoon [S] MS1/2", "Afternoon [S] MS3/4"
        ]
        self.slot_max = [3, 3, 3, 2, 2, 3, 3, 4, 2, 2]
        self.curr_slots = [[] for _ in range(self.n)] #stores list of list of students; curr_slots[i] returns all students slotted in the ith time slot
    
    def display_slots(self): # this is for gui streamlit display; updates the max cap of a slot
        st.subheader("Adjust Time Slot Max Capacities")
        
        num_cols = 5  # Number of columns in a row
        cols = st.columns(num_cols)  # Create columns
        
        for i in range(self.n):
            with cols[i % num_cols]:  # Distribute inputs evenly across columns
                self.slot_max[i] = st.number_input(f"{self.slot_names[i]}", min_value=0, max_value=100, value=self.slot_max[i], key=f"slot_{i}")
    
    def __str__(self):
        s = "##################################################################\n"
        
        for i in range(self.n):
            sn = self.slot_names[i]
            slist = self.curr_slots[i]
            k = [str(s) for s in slist]
            kl = len(slist)
            
            names = '\n'.join(k)
            full_condition = ''
            if kl == 0:
                names = "- None available"
            elif kl == self.slot_max[i]:
                full_condition = " [FULL]"
            s += f"{self.slot_names[i]} [{kl}/{self.slot_max[i]}] {full_condition}: \n{names}"
            s += "\n##################################################################\n"
        
        return s
            
            

            
def removeStudent(student, student_set): # simply removes student from a student_set
    for s in student_set:
        if student.email == s.email:
            student_set.remove(s)
            break
    return student_set
          
def isEligible(student, slots, i): # true if student can be slotted into slots.all_slots[i]
    slot_name = slots.slot_names[i]
    year = slot_name.split("MS")[-1].split('/')
    time_slot = slot_name[0].lower()
    spanish = "[S]" in slot_name
    if str(student.year) in year and (time_slot in student.time_slot.split('/')) and not (not student.spanish and spanish):
        
        #print(f"CHECK ELIGIBILITY: {student}, FOR {slot_name}")
        return True
    else:
        #print(f"VERIFY INELIGIBILITY: {student}, FOR {slot_name}")
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
    print("[LOG]: No conflicting.")
    
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

def scheduleResponses(slots, responses_df, attendance_df):
    # this takes in a Slots object, slots, a pandas df responses_df, and attendance_df
    # returns:
    # outputs a Slots.curr_slots populated with students and another list of students left out
    
    # first construct a pool of students from responses_df
    all_students = [Student(row) for row in responses_df.itertuples(index = False)] # this only includes responders
    prev_students = [] # keep track of previous students (from attendance file)
    ## load in data from attendance_df
    if attendance_df is not None: 
        all_emails = [s.email for s in all_students] # emails of all requesting students
        # email, attendance, attempts
        # take all rows with the @ symbol in the first column;
        filtereddf = attendance_df[attendance_df.iloc[:, 0].str.contains("@", na=False)]
        student_dict = filtereddf.set_index(filtereddf.columns[0]).apply(tuple, axis=1).to_dict()
        print('here',student_dict) # never using pandas again lmfao
        for email,d in student_dict.items(): # storing the data from attendance form
            if email not in all_emails:
                s = Student(None)
                s.email = email
                s.count, s.attempts = [int(q) for q in d]
                #print('her#####################e2', s.count, s.attempts)
                prev_students.append(s)
        
        for s in all_students: # update the previous attendance of the responding students
            if s.email in student_dict.keys():
                d = student_dict[s.email]
                s.count = int(d[0])
                s.attempts = int(d[1])
                
            else: # new email in the responses!
                pass
        
        
    complete_students = all_students + prev_students
    
    random.shuffle(all_students) # randomize 
    all_students.sort(key = lambda x: x.count) # sort by attendance; orignal random order is preserved (stable sorting)
    ## now we just loop through each time slot, and go down the all_students list and pop it if eligible
    
    for i in range(slots.n-1,-1,-1): # loop through each time slot
        slot_name = slots.slot_names[i]
        #print("SLOT NAME: ",slot_name,len(slots.curr_slots[i]), slots.curr_slots)
        for s in all_students[:]:  # Iterate over a copy to avoid modifying while looping
            eligibility = isEligible(s, slots, i)
            ncurrslot = len(slots.curr_slots[i])
            maxsize = slots.slot_max[i]

            if ncurrslot < maxsize:
                if eligibility:
                    slots.curr_slots[i].append(s)
                    all_students = removeStudent(s, all_students)  # Safe to remove since iterating over a copy
            else:
                #print(f"SIZE ISSUE {slot_name}: N,MAX {[ncurrslot, maxsize]}")
                break  # Exit early if slot is full


    # now we update the attendance; updated_tracker is a list of all students to be logged into the updated tracker
    updated_tracker = []
    
    
    for s in complete_students:
        d = dict()
        d['email'] = s.email
        if s in all_students: # remember, all_students are just studnets left out
            d['attendance'] = s.count
            d['signups'] = s.attempts + 1
        elif s in prev_students:
            #print("not in response but in attendance history",s.email)
            d['attendance'] = s.count 
            d['signups'] = s.attempts
        else: # selected studnet!
            d['attendance'] = s.count + 1
            d['signups'] = s.attempts + 1
        updated_tracker.append(d)
    
    

    return slots, all_students, pd.DataFrame(updated_tracker) # by now, all_students is just students left