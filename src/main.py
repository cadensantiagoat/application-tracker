import streamlit as st
import gspread

# Authentication
gc = gspread.service_account(filename='client_secret.json')

# Opening Google sheet
sheet = gc.open('Job Applications').sheet1

st.title('Job Application Manager')

# View current Jobs
st.subheader('Current Jobs')
data = sheet.get_all_records()

if data:
    st.dataframe(data, width='stretch')
else:
    st.info("No jobs added yet. Add you first job below.")

    st.divider()

    # New job form
    st.subheader('Add New Job')

with st.form("add_job_form", clear_on_submit=True):
    position = st.text_input('Position')
    company = st.text_input('Company')
    link = st.text_input('Link')
    status = st.selectbox('Status', ['Plan to Apply ', 'Applied', 'Waiting for Response', 'Interview Scheduled', 'Rejected', 'Offered'])

    submitted = st.form_submit_button('Submit Job')

    if submitted:
        if position and company:
            new_row= [position, company, link, status]

            sheet.append_row(new_row)
            st.success(f'Successfully added {position} at {company}')

            st.rerun()
        else: 
            st.error("Please fill out at least the Position and Company fields.")

st.divider() 
st.subheader('Update Job Status')

if data:
    # Create a clean list of jobs for the dropdown (e.g., "Software Engineer at Intuit")
    job_options = [f"{row['Position']} at {row['Company']}" for row in data]
    
    with st.form("update_status_form"):
        selected_job = st.selectbox("Select a Job to Update", job_options)
        new_status = st.selectbox("New Status", ['Plan to Apply', 'Applied', 'Waiting for Response', 'Offered', 'Declined'])
        
        update_submitted = st.form_submit_button('Update Status')
        
        if update_submitted:
            # Figure out which row this job is in. 
            # We add 2 because Python lists start at 0, and Google Sheets Row 1 is your headers.
            row_index = job_options.index(selected_job) + 2 
            
            # Update column 4 (Status) of that specific row
            sheet.update_cell(row_index, 4, new_status)
            
            st.success(f"Status updated to '{new_status}'!")
            st.rerun()
else:
    st.info("Add some jobs above before you can update statuses!")