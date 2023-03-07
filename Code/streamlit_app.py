import streamlit as st
import pandas as pd

st.set_page_config(layout="wide",page_title='Blend360 Timesheets')

import datetime

col1, col2, col3 = st.columns([1,3,1])
with col1:
    st.image("Blend360logo.png")
with col2:
    st.markdown("<h1 style='text-align: center; color: Black;'>AllStars Cohort10 Timesheets</h1>", unsafe_allow_html=True)
    # st.title("AllStars Cohort10 Timesheets")
    # st.subheader("")
with col3:
    st.image("Blend360logo.png")


Employees_Names = ['Udheep', 'Sagar', 'Brunda', 'Ismail']
Task_Names = ["Assignments", "Client Work", "Trainings", "Coding Challenge", "Others"]

col1, col2 = st.columns([3,2])
with col1:
    emp_name = st.selectbox('Select the Employee Name',Employees_Names)
with col2:
    inputdate = st.date_input("Timesheet Date",datetime.date(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day))

timesheets_fulldata = pd.DataFrame(pd.read_csv("Timesheets_FullData.csv"))
timesheets_search = timesheets_fulldata[(timesheets_fulldata['Name']==emp_name) & (timesheets_fulldata['Date']==str(inputdate))]

if timesheets_search.shape[0]==0:
    df_dummy = {'Date': '', 'Name': '', 'Task': '', 'TimeSpent' : '', 'Details' : ""}
    timesheets_search = timesheets_search.append(df_dummy, ignore_index = True)
    timesheets_search.reset_index(drop=True, inplace=True)
else:
    timesheets_search.reset_index(drop=True, inplace=True)

timesheets_search["Task"] = (timesheets_search["Task"].astype("category").cat.add_categories([col for col in Task_Names if col not in timesheets_search['Task'].unique().tolist()]))
edited_timesheet = st.experimental_data_editor(timesheets_search[['Task', 'TimeSpent', 'Details']], use_container_width=True, num_rows="dynamic")

if inputdate>=datetime.date.today():
    submit = st.button("Submit")
    if submit:
        edited_timesheet.insert(0,'Date',inputdate)
        edited_timesheet.insert(1,'Name',emp_name)

        indexdrop = timesheets_fulldata[ (timesheets_fulldata['Name'] == emp_name) & (timesheets_fulldata['Date'] == str(inputdate)) ].index
        timesheets_fulldata.drop(indexdrop , inplace=True)
        timesheets_fulldata.reset_index(drop=True, inplace=True)

        timesheets_fulldata = pd.concat([timesheets_fulldata,edited_timesheet], ignore_index=True)
        timesheets_fulldata.reset_index(drop=True, inplace=True)
        timesheets_fulldata.to_csv("Timesheets_FullData.csv", index=False)

else:
    st.markdown("<h3 style='text-align: center; color: Black;'>You cannot edit historical timesheets</h1>", unsafe_allow_html=True)
