from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect("subscriptions.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            plan TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# CREATE - Add a subscription
@app.route("/subscriptions", methods=["POST"])
def add_subscription():
    data = request.get_json()

    name = data["name"]
    plan = data["plan"]
    price = data["price"]

    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO subscriptions (name, plan, price) VALUES (?, ?, ?)",
        (name, plan, price)
    )
    conn.commit()

    subscription_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Subscription added successfully",
        "id": subscription_id
    }), 201


# READ - View all subscriptions
@app.route("/subscriptions", methods=["GET"])
def get_subscriptions():
    conn = get_db_connection()
    subscriptions = conn.execute(
        "SELECT * FROM subscriptions"
    ).fetchall()
    conn.close()

    return jsonify([dict(subscription) for subscription in subscriptions])


# READ - View one subscription
@app.route("/subscriptions/<int:id>", methods=["GET"])
def get_subscription(id):
    conn = get_db_connection()
    subscription = conn.execute(
        "SELECT * FROM subscriptions WHERE id = ?", (id,)
    ).fetchone()
    conn.close()

    if subscription is None:
        return jsonify({"message": "Subscription not found"}), 404

    return jsonify(dict(subscription))


# UPDATE - Update a subscription
@app.route("/subscriptions/<int:id>", methods=["PUT"])
def update_subscription(id):
    data = request.get_json()

    name = data["name"]
    plan = data["plan"]
    price = data["price"]

    conn = get_db_connection()

    cursor = conn.execute(
        """
        UPDATE subscriptions
        SET name = ?, plan = ?, price = ?
        WHERE id = ?
        """,
        (name, plan, price, id)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"message": "Subscription not found"}), 404

    return jsonify({
        "message": "Subscription updated successfully"
    })


# DELETE - Delete a subscription
@app.route("/subscriptions/<int:id>", methods=["DELETE"])
def delete_subscription(id):
    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM subscriptions WHERE id = ?", (id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"message": "Subscription not found"}), 404

    return jsonify({
        "message": "Subscription deleted successfully"
    })

# Create subscription table
def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            plan TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    app.run(debug=True)