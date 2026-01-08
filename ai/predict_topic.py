import pickle

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("topic_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_topic(text):
    if not text or text.strip() == "":
        return "Other"

    text_vec = vectorizer.transform([text.lower()])
    prediction = model.predict(text_vec)
    return prediction[0]

examples = [
    "New covid variant detected in Europe",
    "Hospitals under pressure due to staff shortage",
    "Healthy nutrition and exercise reduce obesity",
    "Depression among teenagers is increasing"
]

for e in examples:
    print(e, "→", predict_topic(e))
