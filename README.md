{\rtf1\ansi\ansicpg1252\cocoartf2759
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww30040\viewh18900\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 THIS DOCUMENT COVERS:\
1. how to import data from google form at: https://forms.gle/UAvQuLgE1Gz5NL7b7\
2. how to manually change attendance data\
3. how to use the program\
\
1. After responses are filled on the form, simply save the file as a CSV file and rename it to \'93responses.csv\'94 in the same directory as the \'93main.py\'94 file (this is the main program). You may manually change the free response answers such as name and email in case of typos.\
2. The program assumes everyone person is identified with their email. The program will search for a file called \'93attendance.csv\'94 that tracks everyone\'92s attendance. If no file is detected, it will create a new \'93attendance.csv\'94 file with all attendances set to 0 based on the emails in the \'93responses.csv\'94.\
3. To use the program, set the folder on your Desktop. This way, saving \'93responses.csv\'94 and \'93attendance.csv\'94 are readily accessible. Open terminal and navigate to the directory with \'93cd Desktop/student_clinic_scheduler\'94. Run the python file \'93main.py\'94 once \'93responses.csv\'94 is ready.\
After the program outputs a randomized optimal set of filled time slots, you are asked to confirm the slots by the program log. Type \'93Y\'94 and hit enter to confirm, which updates \'93attendance.csv\'94 with updated attendance counts. Type \'93n\'94 to cancel the operation and no data is modified. }