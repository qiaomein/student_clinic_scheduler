## THIS DOCUMENT COVERS:

1. how to import data from google form at: https://forms.gle/UAvQuLgE1Gz5NL7b7

After responses are filled on the form, simply save the file as a CSV file and rename it to "responses.csv" in the same directory as the "main.py" file (this is the main program). You may manually change the free response answers such as name and email in case of typos.

2. how to manually change attendance data

The program assumes everyone person is identified with their email. The program will search for a file called "attendance.csv" that tracks everyone's attendance. If no file is detected, it will create a new "attendance.csv" file with all attendances set to 0 based on the emails in the "responses.csv".

3. how to use the program

To use the program, set the folder on your Desktop. This way, saving "responses.csv" and "attendance.csv" are readily accessible. Open terminal and navigate to the directory with "cd Desktop/student_clinic_scheduler". Run the python file "main.py" once "responses.csv" is ready.
After the program outputs a randomized optimal set of filled time slots, you are asked to confirm the slots by the program log. Type "Y" and hit enter to confirm, which updates "attendance.csv" with updated attendance counts. Type "n" to cancel the operation and no data is modified. 
