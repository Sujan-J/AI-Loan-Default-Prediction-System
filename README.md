# 💳 AI Loan Default Prediction System

An intelligent web-based application that predicts loan default risk using Machine Learning. The system uses a Decision Tree Classifier to classify loan applicants into **Low Risk** and **High Risk** categories based on their financial and personal details.

Built using Python, Flask, Scikit-learn, HTML, CSS, Bootstrap, and SQLite.

## 🚀 Project Overview

The AI Loan Default Prediction System helps demonstrate how machine learning can support loan risk assessment.

Users can register, log in, enter applicant details, receive a risk prediction with a confidence score, and view their prediction history. Administrators can monitor users and prediction statistics through an admin dashboard.

## ✨ Key Features

- **User Authentication:** Registration and secure login.
- **Loan Risk Prediction:** Predicts Low Risk or High Risk.
- **Machine Learning:** Decision Tree classification algorithm.
- **Confidence Score:** Displays the model's prediction confidence.
- **Prediction History:** Stores and displays previous predictions.
- **Admin Dashboard:** Displays user statistics and prediction records.
- **Responsive Interface:** Built with HTML, CSS and Bootstrap.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Flask | Backend web framework |
| Scikit-learn | Machine Learning |
| Decision Tree | Classification algorithm |
| Pandas & NumPy | Data processing |
| HTML & CSS | Frontend |
| Bootstrap | Responsive UI |
| JavaScript | Frontend functionality |
| SQLite | Local database |
| MySQL | Database schema design |

## 🧠 Machine Learning Workflow

1. Generate/load applicant data.
2. Preprocess numerical and categorical features.
3. Encode categorical attributes.
4. Split data into training and testing sets.
5. Train a Decision Tree Classifier.
6. Generate predictions and confidence scores.
7. Save the trained model as `loan_model.pkl`.

## 📋 Applicant Details

The system accepts the following inputs:

- Age
- Annual Income
- Employment Type
- Education
- Marital Status
- Number of Dependents
- Loan Amount
- Loan Term
- Credit Score
- Existing Debt
- Loan Purpose

## 📂 Project Structure

```text
AI-Loan-Default-Prediction-System/
│
├── app.py
├── db.py
├── train_model.py
├── requirements.txt
├── schema_mysql.sql
├── README.md
├── .gitignore
│
├── models/
│   └── .gitkeep
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── predict.html
│   ├── result.html
│   ├── history.html
│   └── admin.html
│
└── static/
    └── style.css
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Loan-Default-Prediction-System.git
```

### 2. Navigate to the project folder

```bash
cd AI-Loan-Default-Prediction-System
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Train the machine learning model

```bash
python train_model.py
```

This generates the trained model at:

```text
models/loan_model.pkl
```

### 6. Run the Flask application

```bash
python app.py
```

### 7. Open in your browser

```text
http://127.0.0.1:5000
```

Register an account and start using the application.

## 👨‍💻 Admin Access

For local demonstration, register a user account and promote it to administrator using SQLite:

```sql
UPDATE users
SET role = 'admin'
WHERE email = 'your-email@example.com';
```

Log out and log in again to refresh your session.

## 📸 Application Screenshots

Add your actual application screenshots here after uploading them to a `screenshots/` folder.

Suggested screenshots:

- Login Page
- User Dashboard
- Loan Prediction Form
- Prediction Result
- Prediction History
- Admin Dashboard

Example:

```markdown
![Login Page](screenshots/login.png)
![Prediction Result](screenshots/result.png)
![Admin Dashboard](screenshots/admin.png)
```

## ⚠️ Important Disclaimer

This repository is an academic demonstration project.

The original training dataset was not recovered. The included training script generates synthetic sample data for demonstration and testing.

Therefore:
- Model predictions are not validated for real-world lending.
- Confidence scores are not proof of actual prediction accuracy.
- Do not use this application to approve or reject real loan applications.

## 🔮 Future Enhancements

- Integration with a verified real-world loan dataset.
- Comparison of multiple machine learning algorithms.
- Improved model evaluation and performance metrics.
- MySQL database integration.
- Loan analytics and visual reports.
- Deployment to a cloud platform.

## 👨‍🎓 Developer

**J Sujan**  
Computer Science and Engineering  
Navodaya Institute of Technology, Raichur  
Graduation: 2027

## ⭐ Support

If you find this project interesting, consider giving the repository a ⭐ on GitHub!
