#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:44:25 2024

@author: qiaomein
"""

import random, re
import streamlit as st
import pandas as pd

def logout(*s): print(f"[LOG]: {s}")

class Student(object): # pass in a line (l) from the csv file as a list
    def __init__(self, l, count = 0, attempts = 0):
        
        if l is None: # nameless student
            return
        
    
        self.slot = None # should start with no slot; this is index corresponding to order listed in Slots class
        try:
            self.time, self.name, self.email, self.raw_time_slot, self.year, self.spanish = l
        except:
            logout("[WARNING] Nameless student created due to improper construction.")
        
        self.year = int(self.year[-1])
        self.count = count
        self.attempts = attempts
        
        # time_slot should be from set ['m','a','m/a']
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
                
        if self.spanish.lower() == "yes":
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

    def __lt__(self,other):
        return self.email < other.email

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
    slot_year = slot_name.split("MS")[-1].split('/')
    slot_time_slot = slot_name[0].lower()
    slot_spanish = "[S]" in slot_name
    
    eligible_year = str(student.year) in slot_year
    eligible_timeslot = slot_time_slot in student.time_slot.split('/')
    eligible_spanish = not (not student.spanish and slot_spanish)
    
    if eligible_year and eligible_timeslot and eligible_spanish:
        return True
    else:
        #print(f"VERIFY INELIGIBILITY: {student}, FOR {slot_name}")
        return False          

def check_all(slots, leftovers, all_students, prevstudents, updatedtracker): # checks that output satisfies all constraints
    # slots is slotsobject so that slots.curr_slots is the schedule
    # leftovers is a list of unselected students
    # all_students is a list of ALL students (from attendance sheet and responses)
    # updated tracker: list of dictionaries of 'email':value, 'attendance':value, 'signups':value
    
    def ensureNoDupes(selected_students):
        return (sorted(list(set(selected_students))) == sorted(selected_students))
    
    # check that all_students = leftovers + slots.curr_slots
    selected_students = []
    for l in slots.curr_slots:
        selected_students.extend(l)
    
    assert sorted((selected_students + leftovers + prevstudents)) == sorted(all_students) # we know that all students been ac
    
    # no need to check if everyone is eligible for the slot they're in
    
    # check no  list has duplicates
    assert ensureNoDupes(selected_students)
    assert ensureNoDupes(leftovers)
    assert ensureNoDupes(prevstudents)
    assert ensureNoDupes(all_students)
    
    # now check updated tracker: list of dicts
    ut_emails = [list(s.values())[0] for s in updatedtracker]
    # ut_vals = [list(s.values())[1:] for s in updatedtracker]
    for s in all_students:
        if s.email in ut_emails:
            ut_emails.remove(s.email)
    
    assert ut_emails == [] # everyone accounted for in the updated tracker
    

    print("[LOG]: TESTS ALL PASSED.")

def scheduleResponses(slots, responses_df, attendance_df):
    # this takes in a Slots object, slots, a pandas df responses_df, and attendance_df
    # returns:
    # outputs a Slots.curr_slots populated with students and another list of students left out
    
    # first construct a pool of students from responses_df
    all_responders = [Student(row) for row in responses_df.itertuples(index = False)] # this only includes responders
    prev_students = [] # keep track of previous students (from attendance file)
    ## load in data from attendance_df
    if attendance_df is not None: 
        all_emails = [s.email for s in all_responders] # emails of all requesting students
        # email, attendance, attempts
        # take all rows with the @ symbol in the first column;
        filtereddf = attendance_df[attendance_df.iloc[:, 0].str.contains("@", na=False)]
        student_dict = filtereddf.set_index(filtereddf.columns[0]).apply(tuple, axis=1).to_dict()
        # print('here',student_dict) # never using pandas again lmfao
        for email,d in student_dict.items(): # storing the data from attendance form
            if email not in all_emails:
                s = Student(None)
                s.email = email
                s.count, s.attempts = [int(q) for q in d]
                prev_students.append(s)
        
        for s in all_responders: # update the previous attendance of the responding students
            if s.email in student_dict.keys():
                d = student_dict[s.email]
                s.count = int(d[0])
                s.attempts = int(d[1])
                
            else: # new email in the responses!
                pass
        
        
    complete_students = all_responders + prev_students
    
    random.shuffle(all_responders) # randomize 
    #all_responders.sort(key = lambda x: -x.attempts/(x.count+1)) # sort by attendance; orignal random order is preserved (stable sorting)
    all_responders.sort(key = lambda x: x.count) 
    ## now we just loop through each time slot, and go down the all_responders list and pop it if eligible
    for i in range(slots.n-1,-1,-1): # loop through each time slot
        slot_name = slots.slot_names[i]
        for s in all_responders[:]:  # Iterate over a copy to avoid modifying while looping
            eligibility = isEligible(s, slots, i)
            ncurrslot = len(slots.curr_slots[i])
            maxsize = slots.slot_max[i]

            if ncurrslot < maxsize:
                if eligibility:
                    slots.curr_slots[i].append(s)
                    all_responders = removeStudent(s, all_responders)  # Safe to remove since iterating over a copy
            else:
                break  # Exit early if slot is full
    students_left = all_responders

    # now we update the attendance; updated_tracker is a list of all students to be logged into the updated tracker
    updated_tracker = [] 
    for s in complete_students:
        d = dict()
        d['email'] = s.email
        if s in students_left: # remember, all_students are just studnets left out
            d['attendance'] = s.count
            d['signups'] = s.attempts + 1
        elif s in prev_students:
            d['attendance'] = s.count 
            d['signups'] = s.attempts
        else: # selected studnet!
            d['attendance'] = s.count + 1
            d['signups'] = s.attempts + 1
        updated_tracker.append(d)
    
    check_all(slots,students_left,complete_students,prev_students, updated_tracker) 
    

    return slots, students_left, pd.DataFrame(updated_tracker) # by now, all_students is just students left