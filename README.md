# Job Application Manager

A cross-platform Streamlit app that uses Google Sheets to track job applications.

## Setup Instructions
1. Install dependencies: `python -m pip install streamlit gspread`
2. Ensure your `client_secret.json` is in the root directory.
3. Run the app: `python -m streamlit run main.py`

## Bookmarklet 
To easily scrape jobs from the web, create a new browser bookmark, name it "📌 Save Job", and paste the following code into the URL section:

```javascript
javascript:(function(){let t=document.title.split(/\s+[-|]\s+|\s+at\s+/i);let p=t[0]?t[0].trim():'';let c=t[1]?t[1].trim():'';let url='http://localhost:8501/?position='+encodeURIComponent(p)+'&company='+encodeURIComponent(c)+'&link='+encodeURIComponent(window.location.href);window.open(url,'JobTrackerApp');})();