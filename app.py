from flask import Flask, request, jsonify, render_template
import sqlite3

from ai_classifier import classify_ticket


app = Flask(__name__)


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_database_connection():

    connection = sqlite3.connect("tickets.db")

    connection.row_factory = sqlite3.Row

    return connection


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================================
# SUPPORT DASHBOARD
# ==================================================

@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


# ==================================================
# CREATE TICKET + AI/ML ANALYSIS
# ==================================================

@app.route("/tickets", methods=["POST"])
def create_ticket():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body must contain JSON"
        }), 400


    # ----------------------------------------------
    # GET CUSTOMER DATA
    # ----------------------------------------------

    customer_name = data.get("customer_name")

    email = data.get("email")

    problem = data.get("problem")


    # ----------------------------------------------
    # VALIDATION
    # ----------------------------------------------

    if not customer_name or not email or not problem:

        return jsonify({
            "error": "customer_name, email and problem are required"
        }), 400


    # ----------------------------------------------
    # AI / ML ANALYSIS
    # ----------------------------------------------

    try:

        ai_result = classify_ticket(problem)

    except Exception as error:

        return jsonify({
            "error": "AI classification failed",
            "details": str(error)
        }), 500


    # ----------------------------------------------
    # GET AI RESULTS
    # ----------------------------------------------

    category = ai_result["category"]

    confidence = ai_result["confidence"]

    needs_human_review = ai_result["needs_human_review"]

    priority = ai_result["priority"]

    sentiment = ai_result["sentiment"]

    suggested_response = ai_result["suggested_response"]


    # ----------------------------------------------
    # SAVE TICKET
    # ----------------------------------------------

    connection = get_database_connection()

    cursor = connection.cursor()


    try:

        cursor.execute("""
            INSERT INTO tickets
            (
                customer_name,
                email,
                problem,
                category,
                priority,
                sentiment,
                status,
                suggested_response,
                confidence
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            customer_name,

            email,

            problem,

            category,

            priority,

            sentiment,

            "Open",

            suggested_response,

            confidence

        ))


        connection.commit()

        ticket_id = cursor.lastrowid


    except sqlite3.Error as error:

        connection.close()

        return jsonify({
            "error": "Database error",
            "details": str(error)
        }), 500


    connection.close()


    # ----------------------------------------------
    # RETURN RESULT
    # ----------------------------------------------

    return jsonify({

        "message":
            "Ticket created successfully!",

        "ticket_id":
            ticket_id,

        "ai_analysis": {

            "category":
                category,

            "confidence":
                confidence,

            "confidence_percentage":
                round(confidence * 100, 2),

            "needs_human_review":
                needs_human_review,

            "priority":
                priority,

            "sentiment":
                sentiment,

            "suggested_response":
                suggested_response

        }

    }), 201


# ==================================================
# GET ALL TICKETS
# ==================================================

@app.route("/tickets", methods=["GET"])
def get_tickets():

    connection = get_database_connection()


    tickets = connection.execute(
        """
        SELECT *
        FROM tickets
        ORDER BY id DESC
        """
    ).fetchall()


    connection.close()


    ticket_list = []


    for ticket in tickets:

        ticket_list.append(
            dict(ticket)
        )


    return jsonify(ticket_list)


# ==================================================
# GET ONE TICKET
# ==================================================

@app.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):

    connection = get_database_connection()


    ticket = connection.execute(
        """
        SELECT *
        FROM tickets
        WHERE id = ?
        """,
        (ticket_id,)
    ).fetchone()


    connection.close()


    if ticket is None:

        return jsonify({
            "error": "Ticket not found"
        }), 404


    return jsonify(
        dict(ticket)
    )


# ==================================================
# UPDATE TICKET
# ==================================================

@app.route("/tickets/<int:ticket_id>", methods=["PUT"])
def update_ticket(ticket_id):

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "Request body must contain JSON"
        }), 400


    status = data.get("status")

    priority = data.get("priority")


    # ----------------------------------------------
    # VALIDATE STATUS
    # ----------------------------------------------

    allowed_statuses = [

        "Open",

        "In Progress",

        "Closed"

    ]


    if status not in allowed_statuses:

        return jsonify({

            "error":
                "Invalid status. Use Open, In Progress, or Closed."

        }), 400


    # ----------------------------------------------
    # VALIDATE PRIORITY
    # ----------------------------------------------

    allowed_priorities = [

        "Low",

        "Medium",

        "High"

    ]


    if priority not in allowed_priorities:

        return jsonify({

            "error":
                "Invalid priority. Use Low, Medium, or High."

        }), 400


    # ----------------------------------------------
    # UPDATE DATABASE
    # ----------------------------------------------

    connection = get_database_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        UPDATE tickets

        SET status = ?,
            priority = ?

        WHERE id = ?
        """,

        (
            status,
            priority,
            ticket_id
        )
    )


    connection.commit()


    if cursor.rowcount == 0:

        connection.close()

        return jsonify({

            "error":
                "Ticket not found"

        }), 404


    connection.close()


    return jsonify({

        "message":
            "Ticket updated successfully!",

        "ticket_id":
            ticket_id,

        "status":
            status,

        "priority":
            priority

    })


# ==================================================
# DELETE TICKET
# ==================================================

@app.route("/tickets/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):

    connection = get_database_connection()

    cursor = connection.cursor()


    cursor.execute(

        """
        DELETE FROM tickets
        WHERE id = ?
        """,

        (ticket_id,)

    )


    connection.commit()


    if cursor.rowcount == 0:

        connection.close()

        return jsonify({

            "error":
                "Ticket not found"

        }), 404


    connection.close()


    return jsonify({

        "message":
            "Ticket deleted successfully!",

        "ticket_id":
            ticket_id

    })


# ==================================================
# HEALTH CHECK
# ==================================================

@app.route("/health", methods=["GET"])
def health_check():

    return jsonify({

        "status":
            "running",

        "message":
            "AI Customer Support API is working"

    })


# ==================================================
# START FLASK SERVER
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )