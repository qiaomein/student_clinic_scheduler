import streamlit as st
import pandas as pd
import io

from SCS import Student, Slots, logout, scheduleResponses



def load_csv(uploaded_file, haha = 'infer'):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file, header=haha)
    return None


def main():
    st.set_page_config(layout="wide")

    st.title("Student Clinic Scheduler")
    st.text("Ronald Shaju, Volunteer Coordinator 2024-2025")
    st.markdown("""
    **Email:** [ronald.shaju01@utrgv.edu](mailto:ronald.shaju01@utrgv.edu), [ronaldshaju@gmail.com](mailto:ronaldshaju@gmail.com), (956) 605-4202
    """)
    
    slots = Slots()
    slots.display_slots()
    
    col1,col2 = st.columns(2)
    
    with col1:
        url = "https://forms.gle/UAvQuLgE1Gz5NL7b7"
        st.header("Upload Responses File")

        responses_file = st.file_uploader("You must upload your responses file exported as a .csv file here.",type=["csv"], key="responses")
    
    with col2:
        st.header("Upload Attendance File")
        attendance_file = st.file_uploader("Upload attendance tracker file. If not, an empty attendance file, tracker.csv, will be generated for you.", type=["csv"], key="attendance")
    
    responses_df = load_csv(responses_file)
    attendance_df = load_csv(attendance_file)
    
    try:
        if "@" in str(attendance_df.columns[0]) or len(attendance_df.columns) != 3:
            st.error("[ERROR] Make sure uploaded attendance file has headers in order of [email, attendance, signups].")
            raise ValueError
        if len(list(responses_df.columns)) != 6:
            st.error("[ERROR] Make sure the responses are directly exported from Google Forms with the headers ['Timestamp', 'Name', 'UTRGV Email', 'Time Slot(s)', 'Year', 'Spanish?']")
            raise ValueError
    except AttributeError:
        pass
    
    
    
    if responses_df is not None:
        with col1:
            st.subheader("Responses Preview")
            st.dataframe(responses_df,height = 200)
    else:
        with col1:
            st.warning("Please upload responses as a csv file.")
    
    if attendance_df is not None:
        with col2:
            st.subheader("Attendance Preview")
            st.dataframe(attendance_df, height = 200)
    
    scheduleout = ""
    leftout = ""
    
    
    
    if responses_df is not None: # only show the buttons if responses are uploaded
        goButton = st.button("Shuffle!")
        #reshuffleButton = st.button("Reshuffle!")
        
    
        if goButton: ############# MAIN SORTING FEATURE
            # now schedule from responses_df
            finalSlots, students_left,updated_tracker = scheduleResponses(slots,responses_df,attendance_df)
            
            
            # print('\n-----------------------------------\n')
            
            scheduleout += str(finalSlots)
            leftout +=('Students left out:\n')
            leftout +=('\n'.join([str(s) for s in students_left]))
            
            
            #log_output+= ("\n----------------------------------- DONE ---------------------------------------------")
            
    
    if scheduleout:
        col1,col2 = st.columns(2)
        with col1:
            st.subheader("Generated Schedule")
            st.text_area("Console Log", scheduleout, height=250)
            selected_chain = ';'.join([s.email for sl in finalSlots.curr_slots for s in sl])
            st.text_area("Copy and paste", selected_chain, height=70)
        with col2:
            st.subheader("Unscheduled Students")
            st.text_area("Console Log", leftout, height=250)
            left_chain = ';'.join([s.email for s in students_left])
            st.text_area("Copy and paste", left_chain, height=70)
        
        
    
    # now, update the counts and attendance of selected students and download the updated tracker
    
        
        st.download_button(
            label="Download Updated Attendance CSV!",
            data=updated_tracker.to_csv(index = False),
            file_name="tracker.csv",
            mime="text/csv"
        )
        with col1:
            st.subheader("Updated Tracker Preview")
            st.dataframe(updated_tracker)
        with col2:
            st.subheader("Previous Tracker Preview [Comparison]")
            st.dataframe(attendance_df)
    
if __name__ == "__main__":
    main()
