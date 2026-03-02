📊 Instagram Unfollow Checker

A simple web-based analytics tool built with Python (Flask) to analyze exported JSON data from Instagram and identify accounts that do not follow back.

This project is designed for learning backend development, JSON parsing, and web-based data processing using Flask.

🚀 Features

Upload followers_1.json

Upload following.json

Parse Instagram exported JSON data

Compare followers and following

Display:

Total Followers

Total Following

Total Non-Followers

List of accounts that do not follow back

Simple and clean web interface

Error handling for invalid JSON files

🛠 Tech Stack

Python 3

Flask

Bootstrap (CDN)

HTML5

📂 Project Structure
instagram-unfollow-checker/
│
├── app.py
├── requirements.txt
├── Procfile (optional for deployment)
├── templates/
│   └── index.html
└── static/
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/instagram-unfollow-checker.git
cd instagram-unfollow-checker
2️⃣ Create virtual environment (recommended)
python -m venv venv

Activate it:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
▶️ Run the Application
python app.py

Open your browser and visit:

http://127.0.0.1:5000
📥 How to Use

Go to your Instagram account settings.

Download your account data.

Extract the ZIP file.

Locate:

followers_1.json

following.json

Upload both files into the web app.

Click Analyze.

View the list of accounts that do not follow you back.

⚠️ Privacy Notice

This application:

Does NOT store user data

Does NOT save uploaded files

Processes data temporarily in memory only

Is intended for personal and educational use

🌱 Future Improvements

Download results as CSV

Add mutual followers detection

Add dashboard statistics

Add user authentication

Deploy with custom domain

👨‍💻 Author

Rivael Saputra
Informatics Student | Web Developer | Tech Enthusiast
