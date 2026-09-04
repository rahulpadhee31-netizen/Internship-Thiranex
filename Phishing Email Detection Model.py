import pandas as pd
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


# Load dataset
data = pd.read_csv("emails.csv")

# Separate input and output
X = data["text"]
y = data["label"]

# Extract URL feature
def count_urls(text):
    return len(re.findall(r"https?://\S+|www\.\S+", text))

data["url_count"] = data["text"].apply(count_urls)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Convert email text into numerical features
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("Phishing Email Detection Model")
print("--------------------------------")
print("Accuracy:", round(accuracy * 100, 2), "%")

# Confusion Matrix
cm = confusion_matrix(
    y_test,
    predictions,
    labels=["Safe", "Phishing"]
)

plt.figure(figsize=(6, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    xticklabels=["Safe", "Phishing"],
    yticklabels=["Safe", "Phishing"]
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.show()


# Test your own email
email = input("\nEnter an email to check: ")

email_vector = vectorizer.transform([email])
result = model.predict(email_vector)[0]

print("\nResult:", result)
