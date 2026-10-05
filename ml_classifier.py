from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# --------------------------------------------------
# TRAINING DATA
# --------------------------------------------------

training_texts = [

    # PAYMENT
    "I made a payment but it is still pending",
    "My payment failed",
    "I was charged twice",
    "I need a refund",
    "Money was deducted from my account",
    "My transaction failed",
    "I paid for the course but cannot access it",
    "There is a problem with my billing",
    "Payment is not going through",
    "I was charged but did not receive the course",

    # ACCOUNT
    "I cannot login to my account",
    "I forgot my password",
    "I cannot sign in",
    "My account is locked",
    "I want to reset my password",
    "I cannot access my account",
    "My login is not working",
    "I forgot my account password",
    "I am unable to login",
    "Please help me recover my account",

    # LEARNING
    "I cannot access my course",
    "The lesson is not opening",
    "I have a problem with my assignment",
    "My class is not available",
    "I cannot watch the course lesson",
    "The LMS is not showing my course",
    "I need help with my assignment",
    "My learning material is missing",
    "I cannot access my learning content",
    "My course progress is not updating",

    # TECHNICAL
    "The website is not working",
    "The application keeps crashing",
    "I found a bug",
    "The app shows an error",
    "The website is very slow",
    "The application is not responding",
    "I cannot open the website",
    "There is a technical problem",
    "The app stopped working",
    "I am getting an error message",

    # GENERAL
    "I need more information",
    "I have a question",
    "Please help me",
    "I need assistance",
    "Can someone help me",
    "I want to know more",
    "I have a general query",
    "I need support",
    "Can you provide information",
    "I have a question about your service"
]


training_labels = [

    # PAYMENT
    "Payment",
    "Payment",
    "Payment",
    "Payment",
    "Payment",
    "Payment",
    "Payment",
    "Payment",
    "Payment",
    "Payment",

    # ACCOUNT
    "Account",
    "Account",
    "Account",
    "Account",
    "Account",
    "Account",
    "Account",
    "Account",
    "Account",
    "Account",

    # LEARNING
    "Learning",
    "Learning",
    "Learning",
    "Learning",
    "Learning",
    "Learning",
    "Learning",
    "Learning",
    "Learning",
    "Learning",

    # TECHNICAL
    "Technical",
    "Technical",
    "Technical",
    "Technical",
    "Technical",
    "Technical",
    "Technical",
    "Technical",
    "Technical",
    "Technical",

    # GENERAL
    "General",
    "General",
    "General",
    "General",
    "General",
    "General",
    "General",
    "General",
    "General",
    "General"
]


# --------------------------------------------------
# TF-IDF
# --------------------------------------------------

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(training_texts)


# --------------------------------------------------
# MACHINE LEARNING MODEL
# --------------------------------------------------

model = LogisticRegression(
    max_iter=1000
)

model.fit(X, training_labels)


# --------------------------------------------------
# PREDICTION FUNCTION
# --------------------------------------------------

def predict_category(problem):

    problem_vector = vectorizer.transform([problem])

    prediction = model.predict(problem_vector)

    probabilities = model.predict_proba(problem_vector)

    confidence = max(probabilities[0])

    return {
        "category": prediction[0],
        "confidence": round(float(confidence), 2)
    }


# --------------------------------------------------
# TEST MODEL
# --------------------------------------------------

if __name__ == "__main__":

    test_problems = [

        "I paid for my course but my payment is still pending",

        "I forgot my password and cannot login",

        "My lesson is not opening",

        "The website keeps showing an error",

        "I need some information about your service"
    ]

    for problem in test_problems:

        result = predict_category(problem)

        print("\nProblem:")
        print(problem)

        print("Prediction:")
        print(result)