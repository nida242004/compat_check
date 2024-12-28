import streamlit as st
import pandas as pd
import random
import string
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Simulate storage using session state
if "responses" not in st.session_state:
    st.session_state.responses = {}

# Function to generate a unique session ID
def generate_session_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Define Questions
questions = [
    {"type": "dropdown", "question": "Your ideal vacation spot?", "options": ["🏖️ Beach", "🏞️ Mountains", "🏙️ City", "🏕️ Camping"]},
    {"type": "slider", "question": "How much do you enjoy trying new cuisines? (1: Hate it, 10: Love it)", "min": 1, "max": 10},
    {"type": "radio", "question": "Favorite weekend activity?", "options": ["🎉 Partying", "📚 Reading", "🚴 Exploring", "💤 Relaxing"]},
    {"type": "text", "question": "Describe your dream date in one sentence:"},
    {"type": "radio", "question": "How important is communication in a relationship?", "options": ["🔑 Extremely Important", "🙂 Somewhat Important", "🤐 Not Important"]},
    {"type": "slider", "question": "Rate your love for surprises (1: Hate them, 10: Love them):", "min": 1, "max": 10},
    {"type": "dropdown", "question": "How do you handle stress?", "options": ["😌 Stay calm", "😰 Get anxious", "🫂 Need support"]},
    {"type": "radio", "question": "How do you feel about pets?", "options": ["🐶 Love them", "😐 Neutral", "🙅 Dislike them"]},
    {"type": "slider", "question": "How important are shared hobbies? (1: Not at all, 10: Very important)", "min": 1, "max": 10},
    {"type": "text", "question": "What’s one thing you’d like your partner to always remember about you?"}
]

# App Title
st.markdown("<h1 style='text-align: center; color: #ffffff;'>💖 Remote Couples Compatibility Quiz 💖</h1>", unsafe_allow_html=True)

# Step 1: Create or Join a Session
st.sidebar.title("Session Details")
session_id = st.sidebar.text_input("Enter a session name (e.g., Couple2024):", key="session_name")

if session_id:
    st.sidebar.success(f"You're in session: {session_id}")

    # Step 2: Partner Selection
    st.sidebar.title("Your Role")
    role = st.sidebar.radio("Select your role:", ["Partner 1", "Partner 2"])

    if role == "Partner 1":
        st.markdown("<h2 style='color: #6a0dad;'>🎉 Partner 1: Answer the Questions 🎉</h2>", unsafe_allow_html=True)
        partner1_responses = {}

        for idx, q in enumerate(questions):
            st.markdown(f"### {idx + 1}. {q['question']}")
            if q["type"] == "dropdown":
                partner1_responses[q["question"]] = st.selectbox("", q["options"], key=f"p1_q{idx}")
            elif q["type"] == "slider":
                partner1_responses[q["question"]] = st.slider("", q["min"], q["max"], key=f"p1_q{idx}")
            elif q["type"] == "radio":
                partner1_responses[q["question"]] = st.radio("", q["options"], key=f"p1_q{idx}")
            elif q["type"] == "text":
                partner1_responses[q["question"]] = st.text_input("", key=f"p1_q{idx}")

        if st.button("Submit Partner 1's Answers"):
            # Check if all fields are filled
            if all(v != "" for v in partner1_responses.values()):
                st.session_state.responses[session_id] = {"partner1": partner1_responses}
                st.success(f"Partner 1's answers saved! Share this session name ({session_id}) with Partner 2.")
            else:
                st.warning("Please answer all the questions.")

    elif role == "Partner 2":
        if session_id in st.session_state.responses and "partner1" in st.session_state.responses[session_id]:
            st.markdown("<h2 style='color: #6a0dad;'>🎉 Partner 2: Answer the Questions 🎉</h2>", unsafe_allow_html=True)
            partner2_responses = {}

            for idx, q in enumerate(questions):
                st.markdown(f"### {idx + 1}. {q['question']}")
                if q["type"] == "dropdown":
                    partner2_responses[q["question"]] = st.selectbox("", q["options"], key=f"p2_q{idx}")
                elif q["type"] == "slider":
                    partner2_responses[q["question"]] = st.slider("", q["min"], q["max"], key=f"p2_q{idx}")
                elif q["type"] == "radio":
                    partner2_responses[q["question"]] = st.radio("", q["options"], key=f"p2_q{idx}")
                elif q["type"] == "text":
                    partner2_responses[q["question"]] = st.text_input("", key=f"p2_q{idx}")

            if st.button("Submit Partner 2's Answers"):
                # Check if all fields are filled
                if all(v != "" for v in partner2_responses.values()):
                    st.session_state.responses[session_id]["partner2"] = partner2_responses
                    st.success("Partner 2's answers saved! Results are now available.")

                    # Show Compatibility Results
                    st.markdown("<h2 style='color: #ff66b3;'>💖 Compatibility Results 💖</h2>", unsafe_allow_html=True)
                    partner1 = st.session_state.responses[session_id]["partner1"]
                    partner2 = partner2_responses

                    # Compatibility Calculation using Linear Regression
                    compatibility_data = []
                    label_encoder = LabelEncoder()

                    # Encode categorical values
                    for q in questions:
                        if q["type"] != "text":
                            p1_answer = partner1[q["question"]]
                            p2_answer = partner2[q["question"]]
                            p1_encoded = label_encoder.fit_transform([p1_answer])[0]
                            p2_encoded = label_encoder.fit_transform([p2_answer])[0]
                            compatibility_data.append((p1_encoded, p2_encoded))

                    # Convert to DataFrame
                    df = pd.DataFrame(compatibility_data, columns=["Partner 1", "Partner 2"])

                    # Prepare the features and target
                    X = df["Partner 1"].values.reshape(-1, 1)
                    y = df["Partner 2"].values

                    # Fit the model
                    try:
                        model = LinearRegression()
                        model.fit(X, y)
                        predictions = model.predict(X)
                        compatibility = np.mean(np.abs(predictions - y))  # Lower error means higher compatibility

                        # Display Results
                        st.subheader(f"Your Compatibility Score: {100 - compatibility:.2f}%")
                        st.progress((100 - compatibility) / 100)
                        if 100 - compatibility > 80:
                            st.success("You are a match made in heaven! 💞")
                        elif 100 - compatibility > 50:
                            st.info("There's potential here! Keep exploring. ✨")
                        else:
                            st.warning("Opposites attract? Maybe! 😅")
                    except Exception as e:
                        st.error(f"An error occurred while fitting the model: {e}")
                else:
                    st.warning("Please answer all the questions.")
        else:
            st.warning("Waiting for Partner 1 to complete their answers. Please try again later.")
