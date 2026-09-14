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