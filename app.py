import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# OpenRouter Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="ML Tutor Pro",
    layout="wide"
)

# ---------------- HEADER ---------------- #

st.title("ML Tutor Pro")
st.subheader("Your Personal Machine Learning Tutor")

st.info("""
👋 **Welcome to ML Tutor Pro!**

I am your personal **Machine Learning Tutor** designed to help you understand ML concepts in a simple and interactive way.

###  I can help you with:

Machine Learning Fundamentals

Supervised Learning

Unsupervised Learning

Regression & Classification

Decision Trees & Random Forest

KNN, SVM, Naive Bayes

Data Preprocessing

Feature Engineering

Model Evaluation

Scikit-learn

Python for Machine Learning

### Domain Restriction

I answer **only Machine Learning-related questions**.
Questions outside the Machine Learning domain will be politely declined.
""")

# ---------------- SIDEBAR ---------------- #

st.sidebar.title(" ML Tutor Pro")

st.sidebar.success("Machine Learning Learning Assistant")

st.sidebar.markdown("---")

# Prompt Engineering Technique
prompt_type = st.sidebar.selectbox(
    " Prompt Engineering Technique",
    [
        "Zero-Shot",
        "One-Shot",
        "Few-Shot",
        "Role Prompting",
        "Step-by-Step Tutor"
    ],
    key="prompt_type"
)

# Difficulty Level
difficulty = st.sidebar.selectbox(
    " Difficulty Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ],
    key="difficulty_level"
)
# User Role
user_role = st.sidebar.selectbox(
    " Select User",
    [
        "Student",
        "Teacher"
    ],
    key="user_role"
)

st.sidebar.markdown("---")

st.sidebar.info(f" **Current Technique:** {prompt_type}")
st.sidebar.info(f" **Difficulty:** {difficulty}")

st.sidebar.markdown("---")

st.sidebar.markdown("### 💡 Suggested Questions")

st.sidebar.markdown("""
- What is Machine Learning?
- Explain Random Forest.
- Difference between Regression and Classification.
- What is Overfitting?
- Explain Cross Validation.
""")

st.sidebar.markdown("---")

if st.sidebar.button(" Clear Chat"):
    st.session_state.messages = []
    st.rerun()
# ---------------- SESSION ---------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# ---------------- ROLE PROMPT ---------------- #

if user_role == "Student":

    role_prompt = """
You are ML Tutor Pro, an expert Machine Learning Tutor.

Your role is to TEACH students.

Rules:
- Explain concepts in detail.
- Use beginner-friendly language.
- Explain step by step.
- Give real-world examples.
- Provide Python (Scikit-learn) code whenever appropriate.
- Give practical tips.
- End every answer with a short summary.
"""

else:

    role_prompt = """
You are ML Tutor Pro, an experienced Machine Learning Professor and Examiner.

Your role is to HELP TEACHERS create assessments.

When a teacher asks a topic:

Generate:
1. 5 Multiple Choice Questions (with correct answers)
2. 5 Short Questions
3. 3 Long Questions
4. 5 Viva Questions
5. 5 Interview Questions

If the teacher asks for an explanation, first give a short explanation, then generate the questions.

Keep everything strictly related to Machine Learning.
Never answer non-Machine Learning questions.
"""
# ---------------- SYSTEM PROMPT ---------------- #

if prompt_type == "Zero-Shot":

    system_prompt = f"""
{role_prompt}

You are ML Tutor Pro, a Machine Learning tutor.

Teach at {difficulty} level.

Rules:
- Answer ONLY Machine Learning questions.
- Explain concepts in simple language.
- Use real-world examples.
- Provide Python (Scikit-learn) code whenever appropriate.
- If the question is outside Machine Learning, reply:
"I'm ML Tutor Pro. I only answer Machine Learning-related questions."
"""

elif prompt_type == "One-Shot":

    system_prompt = f"""
{role_prompt}

You are ML Tutor Pro.

Teach at {difficulty} level.

Example:

User:
What is Supervised Learning?

Assistant:
Supervised Learning is a Machine Learning technique where a model learns from labeled data.

Example:
Email Spam Detection.

Now answer the user's question in the same teaching style.

Rules:
- Answer ONLY Machine Learning questions.
- Use simple explanations and examples.
"""

elif prompt_type == "Few-Shot":

    system_prompt = f"""
{role_prompt}

You are ML Tutor Pro.

Teach at {difficulty} level.

Examples:

User:
What is Machine Learning?

Assistant:
Machine Learning enables computers to learn patterns from data without explicit programming.

User:
What is Classification?

Assistant:
Classification predicts categories.

Example:
Spam vs Not Spam.

User:
What is Overfitting?

Assistant:
Overfitting occurs when a model memorizes training data instead of learning patterns.

Now answer the user's question similarly.

Rules:
- Answer ONLY Machine Learning questions.
- Use beginner-friendly explanations.
"""

elif prompt_type == "Role Prompting":

    system_prompt = f"""
{role_prompt}

You are an experienced Machine Learning professor.

Teach students at {difficulty} level.

Always explain:

1. Definition
2. Real-world example
3. Python example
4. Interview tip
5. Summary

Only answer Machine Learning questions.
"""

else:   # Step-by-Step Tutor

    system_prompt = f"""
{role_prompt}

You are ML Tutor Pro.

Teach every concept step by step.

Difficulty Level:
{difficulty}

Structure every answer like this:

1. Definition
2. Why it is important
3. Real-world example
4. Python implementation
5. Advantages
6. Limitations
7. Interview Tip
8. Summary

Only answer Machine Learning questions.
"""

# ---------------- CHAT HISTORY ---------------- #

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ---------------- #

user_input = st.chat_input(" Ask a Machine Learning question...")

if user_input:

    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:

        with st.spinner("ML Tutor is thinking..."):

            response = client.chat.completions.create(
                model="meta-llama/llama-3.1-8b-instruct",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages
                ],
                temperature=0.4,
                max_tokens=800
            )

            answer = response.choices[0].message.content

    except Exception as e:
        answer = f"Error: {str(e)}"

    # Store assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.caption(
    " ML Tutor Pro | Powered by Streamlit + OpenRouter + Meta Llama 3.1"
)
