📧 Email Automation :-

A simple web application that automatically fetches emails from Gmail, stores them in MongoDB, and displays them on a dashboard with categories like Business Leads, Reporting, General and total emails .


## 📌 About the Project

This project is an **Email Automation Dashboard** that connects to your Gmail account and automatically fetches emails.  
The emails are processed, tagged into categories (Business Lead, Reporting, or General), and displayed in a simple web dashboard.  

The goal of this project is to:
- Show real-time email fetching and storage.
- Provide automatic tagging for better organization.
- Give a clear, user-friendly dashboard view.

This project , the  main focus is on:
1. Using APIs (Gmail API).
2. Storing data in a database (MongoDB).
3. Displaying results through a web application (Flask).


## ✨ Features

- **Email Fetching**  
  Connects to Gmail and pulls emails automatically using the Gmail API.

- **Categorization**  
  Emails are tagged into categories:  
  - 📊 Business Lead  
  - 📑 Reporting  
  - 📩 General  

- **Dashboard View**  
  - Total email count.  
  - Count of emails by category.  
  - Interactive chart (Pie Chart) to visualize distribution.  
  - Table listing all emails with sender, subject, date, and snippet.  

- **Filtering**  
  Filter emails by **date range and tag** to focus on specific periods and group.  

- **Responsive Design**  
  Works smoothly on desktops, tablets, and mobile devices.  

## 🛠 Technologies Used

- **Backend:** Python (Flask) – for handling routes, API calls, and rendering the dashboard.
- **Frontend:** HTML, CSS, JavaScript – for user interface and interactions.
- **Charting Library:** Chart.js – to display email distribution in a pie chart.
- **API:** Gmail API – to fetch emails securely from a Gmail account.
- **Authentication:** OAuth 2.0 – for secure login with Gmail.
- **Environment:** Virtualenv – to manage Python dependencies.



## ⚙️ Installation & Setup

Follow these steps to set up and run the project on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/email-dashboard.git
cd email-dashboard

# Create virtual environment
python -m venv venv

# Activate it On Windows
venv\Scripts\activate

# Activate it On macOS/Linux
source venv/bin/activate

**Install all the Dependencies from the requirements.txt**
pip install -r requirements.txt


***Setup MongoDB***

1.This project uses MongoDB to store the emails.
2.Install MongoDB locally on your computer, or
3.Use a free cloud database with MongoDB Atlas.
4.MongoDB should be running before starting the app.
5.Update the MongoDB connection string inside src/mongo_db.py   if needed.


**Set Up Gmail API Credentials**
1.Go to Google Cloud Console
2.Create a new project (or select an existing one).
3.Enable the Gmail API.
4.Configure OAuth 2.0 Client IDs.
5.Download the credentials.json file.
6.Place the credentials.json file inside the src/ folder of the project
7.The first time while  running the project, it will ask  to log in with your Gmail and will create a token.json file automatically.
8.Run the Application- python app.py(in the virtual enviroment only )

**Access the Dashboard**
   1. Open your browser and go to:http://127.0.0.1:5000/

9. ***Stopping the App*** 
Press CTRL + C in the terminal to stop the Flask server.
If  used a virtual environment,it should be deactivated .


## 🔎 How It Works

1. **Email Fetching**  
   - The app connects to your Gmail account using the Gmail API.  
   - It fetches recent emails at regular intervals (every 1 minute ).  

2. **Storage in MongoDB**  
   - All fetched emails are saved in a MongoDB collection (`emails_collection`).  
   - Each email stores details like **sender, subject, body, date, and category tag**.  

3. **Tagging System**  
   - Emails are automatically categorized into:
     - **Business Lead**
     - **Reporting**
     - **General**
   - Tagging is based on simple keyword checks inside the email subject/body.  

4. **Dashboard Display**  
   - A Flask web app serves the dashboard at `http://127.0.0.1:5000/`.  
   - The dashboard shows:
     - Total number of emails.  
     - Count of emails by tag.  
     - Pie chart visualization.  
     - Table with sender, subject, tag, date, and body preview.  

5. **Filtering by Date**  
   - You can filter emails in the table using a start date and end date.  

6. **Scheduler Automation**  
   - A background scheduler (APScheduler) runs automatically.  
   - It keeps fetching and updating emails without manual refresh.  
