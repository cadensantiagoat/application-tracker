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
    # use_container_width is the correct Streamlit parameter here
    st.dataframe(data, use_container_width=True)
else:
    st.info("No jobs added yet. Add your first job below.")

st.divider() 

st.subheader('Add New Job')

# Grab data from the URL if it exists
default_pos = st.query_params.get("position", "")
default_comp = st.query_params.get("company", "")
default_link = st.query_params.get("link", "")

# Pass the default values into the form inputs
with st.form("add_job_form", clear_on_submit=True):
    position = st.text_input('Position', value=default_pos)
    company = st.text_input('Company', value=default_comp)
    link = st.text_input('Link', value=default_link)
    
    # 'Plan to Apply' is first in the list, so it becomes the default automatically
    status = st.selectbox('Status', ['Plan to Apply', 'Applied', 'Waiting for Response', 'Offered', 'Declined'])
    
    submitted = st.form_submit_button('Submit Job')
    
    if submitted:
        if position and company:
            new_row = [position, company, link, status]
            sheet.append_row(new_row)
            st.success(f'Successfully added {position} at {company}!')
            
            # Clear the URL parameters so the form actually resets on the next run
            st.query_params.clear()
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