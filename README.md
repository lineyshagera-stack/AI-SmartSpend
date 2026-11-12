# AI-SmartSpend
# AI SmartSpend 💰

### AI-Powered Personal Spending Tracker

AI SmartSpend is a personal finance application that combines PayPal payment integration with Artificial Intelligence to help users track their transactions, understand their spending habits, and make smarter financial decisions.

The project uses AI to generate personalised spending insights and practical budgeting recommendations based on transaction data.

## 🚀 Features

- **PayPal Integration:** Process payments using the PayPal Sandbox environment.
- **Transaction Tracking:** Store and manage payment information using an SQLite database.
- **AI Spending Insights:** Generate AI-powered recommendations using the Groq API.
- **Spending Categories:** Organise transactions into categories such as groceries and other expenses.
- **Dashboard:** View transaction information and spending insights in one place.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| SQLite | Transaction database |
| PayPal Sandbox API | Payment integration and testing |
| Groq API | AI-powered spending insights |
| Git & GitHub | Version control |

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/lineyshagera-stack/AI-SmartSpend.git
```

Navigate into the project directory:

```bash
cd AI-SmartSpend
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project directory.

Add your own PayPal Sandbox and Groq API credentials using the variable names required by the application.

**Important:** Never upload your `.env` file or expose API keys and secret credentials on GitHub.

### 5. Run the application

```bash
python3 app.py
```

Open your browser and visit:

http://127.0.0.1:5000

## 💳 PayPal Sandbox Testing

AI SmartSpend integrates with PayPal Sandbox to test payment functionality without using real money.

The application supports:
- Sandbox payment approval.
- Payment capture.
- Transaction storage in SQLite.

A PayPal Sandbox buyer account can be used to test payments.

## 🤖 AI Spending Insights

The application uses the Groq API to generate AI-powered spending recommendations.

Based on transaction information, AI SmartSpend can provide:
- Spending observations.
- Category-based recommendations.
- Practical budgeting suggestions.
- Ideas for managing expenses more effectively.

## 📁 Project Structure

```text
AI-SmartSpend/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── smartspend.db
│
├── static/
│   └── style.css
│
└── templates/
    └── index.html
```

## 🔒 Security

- API credentials are stored in environment variables.
- The `.env` file should not be committed to GitHub.
- PayPal Sandbox is used for development and testing.

## 🧪 Testing

The following functionality has been tested:

- PayPal Sandbox payment approval.
- Successful payment capture.
- Transaction storage in SQLite.
- Transaction display on the dashboard.
- AI-generated grocery spending insights.

## 🎯 Project Objective

The objective of AI SmartSpend is to make personal expense management more accessible by combining secure payment integration, transaction tracking, and Artificial Intelligence.

The project demonstrates how Python, APIs, databases, and AI can work together to create a practical financial technology application.

## 👩‍💻 Author

Developed as an individual project for the PayPal AI Hackathon.
## Demonstration Video

Watch the AI SmartSpend demonstration video:

https://drive.google.com/file/d/1nuAzScM_Zbmi6g03p9P8kjPCtnwhym3G/view?usp=sharing
---

**AI SmartSpend — Spend Smarter. Save Better.**
