import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load API key from .env
load_dotenv()
client = OpenAI()

# GPT Agents

def tips_agent(user_info):
    prompt = (
        f"This person is trying to lose weight and improve their health:\n\n"
        f"{user_info}\n\n"
        "Suggest three specific, beginner-friendly first steps they can start taking today to build better habits. "
        "Format them clearly as Tip 1, Tip 2, and Tip 3."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a supportive and practical health coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def meal_agent(user_info):
    prompt = (
        f"This person is trying to lose weight and eat healthier:\n\n"
        f"{user_info}\n\n"
        "Suggest one healthy, balanced meal they could eat today. "
        "Make sure it includes protein, vegetables, and fiber. "
        "Format as a full meal idea like you're recommending it to a friend."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a registered dietician who gives friendly and realistic meal suggestions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def weekly_plan_agent(user_info):
    prompt = (
        f"This person is trying to lose weight and improve their health:\n\n"
        f"{user_info}\n\n"
        "Create a motivational 7-day health plan. Each day should include one small, realistic action "
        "to help them build healthy habits and lose weight. Format like: Day 1: ..., Day 2: ..., etc."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly and supportive health coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def generate_health_plan(user_info):
    tips = tips_agent(user_info)
    meal = meal_agent(user_info)
    plan = weekly_plan_agent(user_info)
    return tips, meal, plan

# Streamlit UI
st.set_page_config(page_title="🩺 Your Personal AI Dietician", layout="centered")

st.markdown("## 🩺 Your Personal AI Dietician")
st.markdown("Enter your health background and goal to get a custom plan:")

user_input = st.text_area("Your Health Info", height=200, placeholder="Example: I'm a 23-year-old woman...")

if st.button("Generate My Plan"):
    if user_input.strip() == "":
        st.warning("Please enter your health background.")
    else:
        with st.spinner("Creating your personalized plan..."):
            tips, meal, plan = generate_health_plan(user_input)

        st.markdown("---")
        st.markdown("## 🧠 Here's your personalized plan:")

        st.markdown("### ✅ First Steps")
        st.markdown(f"""
        <div style="background-color: #f0fff4; padding: 15px; border-radius: 10px;">
        {tips.replace('Tip', '**Tip') + '**'}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🥗 Meal Suggestion")
        st.markdown(f"""
        <div style="background-color: #fffaf0; padding: 15px; border-radius: 10px;">
        {meal}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📅 Weekly Healthy Living Plan")
        st.markdown(f"""
        <div style="background-color: #f0f4ff; padding: 15px; border-radius: 10px;">
        {plan.replace('Day', '**Day') + '**'}
        </div>
        """, unsafe_allow_html=True)
        # Create full downloadable output
        final_output = f"""
        🧠 Personalized Health Plan

        ✅ First Steps:
        {tips}

        🥗 Meal Suggestion:
        {meal}

        📅 Weekly Healthy Living Plan:
        {plan}
        """

        # Display download button
        st.download_button(
            label="📥 Download Your Plan",
            data=final_output,
            file_name="my_health_plan.txt",
            mime="text/plain"
        )

# Optional footer
st.markdown("""
<hr style="margin-top: 50px;">
<p style="text-align: center; font-size: 0.9em; color: gray;">
Made with ❤️ by Rachel Wolf | Powered by GPT-3.5
</p>
""", unsafe_allow_html=True)