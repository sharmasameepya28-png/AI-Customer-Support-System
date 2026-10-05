from ml_classifier import predict_category


# ==================================================
# TEST CASES
# ==================================================

test_cases = [

    # PAYMENT
    "I was charged twice for my course",

    "My payment failed and money was deducted",

    "I need a refund for my purchase",

    # ACCOUNT
    "I forgot my password and cannot login",

    "My account is locked and I cannot sign in",

    "I cannot access my account",

    # LEARNING
    "My course lesson is not opening",

    "I cannot access my assignment",

    "My LMS is not showing my course",

    # TECHNICAL
    "The website keeps crashing",

    "The application shows an error",

    "The app is not working properly",

    # GENERAL
    "I need more information about your service",

    "Can someone help me with a question?",

    "I need assistance with something"

]


# ==================================================
# RUN TESTS
# ==================================================

print("=" * 70)

print("AI CUSTOMER SUPPORT - ML CLASSIFICATION TEST")

print("=" * 70)


for number, problem in enumerate(test_cases, start=1):

    result = predict_category(problem)

    category = result["category"]

    confidence = result["confidence"]


    print()

    print(f"Test {number}")

    print("-" * 70)

    print("Customer Problem:")
    print(problem)

    print()

    print("Predicted Category:")
    print(category)

    print()

    print("Model Confidence:")
    print(f"{confidence * 100:.2f}%")

    print("-" * 70)


print()

print("Testing completed successfully!")