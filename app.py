
import os
import requests
import sqlite3
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = Flask(__name__)
def initialize_database():
    connection = sqlite3.connect("smartspend.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paypal_transaction_id TEXT UNIQUE,
        amount REAL NOT NULL,
        currency TEXT NOT NULL,
        status TEXT NOT NULL,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
    cursor.execute("PRAGMA table_info(transactions)")
    columns = [column[1] for column in cursor.fetchall()]

    if "category" not in columns:
        cursor.execute("""
            ALTER TABLE transactions
            ADD COLUMN category TEXT DEFAULT 'Uncategorised'
        """)

    connection.commit()
    connection.close()


initialize_database()



@app.route("/")
def home():
    connection = sqlite3.connect("smartspend.db")

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        ORDER BY transaction_date DESC
    """)

    transactions = cursor.fetchall()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE status = 'COMPLETED'
    """)

    total_spending = cursor.fetchone()[0]
    monthly_budget = 1000.00
    remaining_budget = monthly_budget - total_spending
    budget_percentage = (total_spending / monthly_budget) * 100 if monthly_budget > 0 else 0
    connection.close()

    return render_template(
        "index.html",
        paypal_client_id=os.getenv("PAYPAL_CLIENT_ID"),
        transactions=transactions,
        total_spending=total_spending,
        monthly_budget=monthly_budget,
        remaining_budget=remaining_budget,
        budget_percentage=budget_percentage
    )


def get_paypal_access_token():
    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")
    base_url = os.getenv("PAYPAL_BASE_URL")

    response = requests.post(
        f"{base_url}/v1/oauth2/token",
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials"},
        headers={"Accept": "application/json"},
        timeout=20
    )

    response.raise_for_status()
    return response.json()["access_token"]

@app.route("/api/orders", methods=["POST"])
def create_order():
    try:
        access_token = get_paypal_access_token()
        base_url = os.getenv("PAYPAL_BASE_URL")

        data = request.get_json() or {}
        category = data.get("category", "Other")

        response = requests.post(
            f"{base_url}/v2/checkout/orders",
            json={
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "EUR",
                            "value": "5.00"
                        },
                        "custom_id": category
                    }
                ]
            },
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            timeout=20
        )

        response.raise_for_status()

        return jsonify(response.json())

    except requests.RequestException as error:
        print("PAYPAL ORDER CREATION ERROR:", error)

        return jsonify({
            "status": "error",
            "message": "Could not create PayPal order."
        }), 502

def generate_spending_insights(spending_data):

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": """
                You are SmartSpend, a personal finance assistant.
                Analyse the user's spending and provide:
                1. Spending observations.
                2. Areas where they could save money.
                3. Three practical budgeting recommendations.

                Keep your response simple and beginner-friendly.
                """
            },
            {
                "role": "user",
                "content": f"Analyse my spending: {spending_data}"
            }
        ]
    )

    return response.choices[0].message.content

@app.route("/paypal-test")
def paypal_test():
    try:
        get_paypal_access_token()

        return jsonify({
            "status": "success",
            "message": "Successfully connected to PayPal Sandbox!"
        })

    except requests.RequestException:
        return jsonify({
            "status": "error",
            "message": "PayPal authentication failed."
        }), 502







@app.route("/api/orders/<order_id>/capture", methods=["POST"])
def capture_order(order_id):
    try:
        access_token = get_paypal_access_token()
        base_url = os.getenv("PAYPAL_BASE_URL")

        response = requests.post(
            f"{base_url}/v2/checkout/orders/{order_id}/capture",
            json={},
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            timeout=20
        )

        response.raise_for_status()

        paypal_result = response.json()

        print("PAYPAL CAPTURE RESPONSE:")
        print(paypal_result)

        if paypal_result["status"] == "COMPLETED":
            category = paypal_result["purchase_units"][0].get("custom_id", "Other")
            capture_details = paypal_result["purchase_units"][0]["payments"]["captures"][0]

            transaction_id = capture_details["id"]
            amount = float(capture_details["amount"]["value"])
            currency = capture_details["amount"]["currency_code"]
            status = capture_details["status"]

            connection = sqlite3.connect("smartspend.db")
            cursor = connection.cursor()

            cursor.execute("""
                INSERT OR IGNORE INTO transactions
                (paypal_transaction_id, amount, currency, status, category)
                VALUES (?, ?, ?, ?, ?)
            """, (transaction_id, amount, currency, status, category))

            connection.commit()
            connection.close()

            print("TRANSACTION SAVED TO DATABASE!")

        return jsonify(paypal_result)

    except requests.RequestException as error:
        print("PAYPAL CAPTURE ERROR:", error)

        return jsonify({
            "status": "error",
            "message": "Could not capture PayPal payment."
        }), 502

@app.route("/api/insights", methods=["GET"])
def ai_insights():

    connection = sqlite3.connect("smartspend.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE status = 'COMPLETED'
        GROUP BY category
    """)

    spending_data = cursor.fetchall()

    connection.close()

    try:
        insights = generate_spending_insights(spending_data)

        return jsonify({
            "status": "success",
            "insights": insights
        })

    except Exception as error:
        print("GROQ ERROR:", error)

        return jsonify({
            "status": "error",
            "message": "Could not generate AI insights."
        }), 500
if __name__ == "__main__":
    print("Starting SmartSpend...")
    app.run(debug=True)