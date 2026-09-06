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
    