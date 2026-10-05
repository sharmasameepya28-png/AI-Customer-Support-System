from ml_classifier import predict_category


def classify_ticket(problem):

    # ================================================
    # ML CATEGORY CLASSIFICATION
    # ================================================

    ml_result = predict_category(problem)

    category = ml_result["category"]

    confidence = ml_result["confidence"]


    # ================================================
    # HUMAN REVIEW DECISION
    # ================================================

    if confidence < 0.75:

        needs_human_review = True

    else:

        needs_human_review = False


    # ================================================
    # PRIORITY
    # ================================================

    problem_lower = problem.lower()

    if any(word in problem_lower for word in [
        "urgent",
        "immediately",
        "emergency",
        "critical",
        "as soon as possible"
    ]):

        priority = "High"

    elif any(word in problem_lower for word in [
        "soon",
        "important",
        "quickly"
    ]):

        priority = "Medium"

    else:

        priority = "Low"


    # ================================================
    # SENTIMENT
    # ================================================

    if any(word in problem_lower for word in [
        "angry",
        "terrible",
        "frustrated",
        "hate",
        "worst",
        "disappointed",
        "not working"
    ]):

        sentiment = "Negative"

    elif any(word in problem_lower for word in [
        "thank",
        "thanks",
        "great",
        "happy",
        "excellent"
    ]):

        sentiment = "Positive"

    else:

        sentiment = "Neutral"


    # ================================================
    # SUGGESTED RESPONSE
    # ================================================

    if category == "Payment":

        suggested_response = (
            "We are sorry for the payment issue. "
            "Our support team will verify the transaction "
            "and help resolve the issue as soon as possible."
        )

    elif category == "Account":

        suggested_response = (
            "We are sorry you are having trouble with your account. "
            "Please verify your login details and try resetting "
            "your password. Our support team can assist you "
            "if the issue continues."
        )

    elif category == "Learning":

        suggested_response = (
            "Thank you for contacting us. "
            "We will review your learning-related issue "
            "and help you resolve it as soon as possible."
        )

    elif category == "Technical":

        suggested_response = (
            "We are sorry you are experiencing a technical issue. "
            "Our support team will investigate the problem "
            "and assist you shortly."
        )

    else:

        suggested_response = (
            "Thank you for contacting customer support. "
            "We have received your request and our team "
            "will review it shortly."
        )


    # ================================================
    # RETURN RESULT
    # ================================================

    return {

        "category": category,

        "confidence": confidence,

        "needs_human_review": needs_human_review,

        "priority": priority,

        "sentiment": sentiment,

        "suggested_response": suggested_response

    }


# ================================================
# TEST
# ================================================

if __name__ == "__main__":

    problem = (
        "I paid for my course but the payment is still pending. "
        "This is urgent and very frustrating."
    )

    result = classify_ticket(problem)

    print(result)