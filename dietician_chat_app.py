import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load API key
load_dotenv()
client = OpenAI()

# Set Streamlit page configuration
st.set_page_config(page_title="🩺 AI Health Coach", layout="centered")

# Welcome title
st.title("🩺 Your Personal AI Health Coach")

# Friendly intro
st.markdown("""
Hi there! 👋 Welcome to your personal AI health coaching session.  
I'm here to guide you toward healthier habits, smarter eating, and feeling your best — all based on trustworthy sources like the **Canadian Food Guide** 🇨🇦.

💬 I'll ask you some simple questions about your lifestyle and goals.  
📅 When you're ready, just type **"generate my plan"** and I'll create your personalized health plan!

Let's get started! 😊
""")

# 💬 Step 1: User inputs their name
user_name = st.text_input("First, what name would you like me to call you? ✨", placeholder="Enter your name here...")

# 💬 Step 2: Choose Support Level
st.markdown("### 💬 Choose Your Support Level:")

support_level = st.radio(
    "How supportive would you like your health coach to be?",
    ("Normal Support 🧠", "High Support 💛", "Ultra Support 🫶")
)

# Set custom system message based on support level
if support_level == "Normal Support 🧠":
    system_personality = f"You are a friendly and knowledgeable AI health coach talking to {user_name}. Base all advice primarily on the Canadian Food Guide. Be supportive and practical."
elif support_level == "High Support 💛":
    system_personality = f"You are an extra gentle, warm, and encouraging AI health coach helping {user_name}. Always provide supportive, uplifting advice. Base your advice on the Canadian Food Guide."
elif support_level == "Ultra Support 🫶":
    system_personality = f"You are a very sensitive, therapeutic AI health coach guiding {user_name}. Speak with extreme kindness, patience, and emotional sensitivity. Be as uplifting and compassionate as possible while still basing health advice on the Canadian Food Guide."

# Initialize chat history if not already done
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": system_personality},
        {"role": "assistant", "content": f"Hi {user_name}! 👋 I'm excited to work with you today. What is your main health or fitness goal right now?"}
    ]

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])
    elif msg["role"] == "user":
        st.chat_message("user").write(msg["content"])

# Get user input
user_input = st.chat_input("Type your reply...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # GPT generates next assistant reply based on chat history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.chat_history,
        temperature=0.7
    )

    assistant_reply = response.choices[0].message.content.strip()
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})

    # Display assistant reply immediately
    st.chat_message("assistant").write(assistant_reply)

# Watch for "generate my plan" keyword to create final plan
if any("generate my plan" in m["content"].lower() for m in st.session_state.chat_history if m["role"] == "user"):
    with st.spinner("Creating your personalized plan..."):
        # Compile all user responses
        user_context = "\n".join(m["content"] for m in st.session_state.chat_history if m["role"] == "user")

        plan_prompt = (
            f"Based on this information about {user_name}:\n\n{user_context}\n\n"
            "Generate a personalized health improvement plan. Include:\n"
            "- 3 beginner-friendly first steps aligned with the Canadian Food Guide\n"
            "- 1 healthy, balanced meal suggestion following the Canadian Food Guide principles\n"
            "- A 7-day health plan (Day 1 to Day 7)\n"
            "Format it nicely with headings for each section."
        )

        plan_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a professional AI health coach specializing in recommendations based on the Canadian Food Guide, speaking supportively to {user_name}."},
                {"role": "user", "content": plan_prompt}
            ],
            temperature=0.7
        )

        final_plan = plan_response.choices[0].message.content.strip()

        st.markdown("---")
        st.subheader(f"🧠 {user_name}'s Full Personalized Plan")
        st.markdown(final_plan)

        # Download button
        st.download_button(
            label="📥 Download Your Plan",
            data=final_plan,
            file_name=f"{user_name}_health_plan.txt",
            mime="text/plain"
        )

# Cute Footer
st.markdown("""
<hr style="margin-top: 50px;">
<p style="text-align: center; font-size: 0.9em; color: gray;">
Made with ❤️ by Rachel Wolf | Powered by GPT-3.5
</p>
""", unsafe_allow_html=True)