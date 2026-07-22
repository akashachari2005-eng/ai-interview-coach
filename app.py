import streamlit as st
import pandas as pd
import random

# ===== PAGE SETUP =====
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="centered"
)

# ===== SETUP NAVIGATION (Sticky Notes 📝) =====
if "page" not in st.session_state:
    st.session_state.page = "home"

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "answers" not in st.session_state:
    st.session_state.answers = []


# ===== DUMMY QUESTIONS =====
QUESTIONS = [
    "Tell me about yourself and your background.",
    "What are your key technical skills?",
    "Describe a challenging project you worked on.",
    "Why do you want to work with our company?",
    "Where do you see yourself in 5 years?"
]


# ===== PAGE 1: HOME PAGE =====
def home_page():
    st.title("🎤 AI Virtual Interview Coach")
    st.subheader("Practice interviews. Get instant AI feedback. Land your dream job! 🚀")
    
    st.write("")
    
    st.info(
        """
        👋 **Welcome!**  
        
        Are you preparing for a job interview? 😰  
        Don't worry — we've got you covered! ✨
        
        **Here's how it works:**
        1. 📄 Upload your Resume (PDF)
        2. 🤖 Our AI will generate 5 personalized questions
        3. ✍️ You answer them one by one
        4. 📊 Get a detailed performance report!
        """
    )
    
    st.write("")
    
    if st.button("🚀 Get Started", use_container_width=True):
        st.session_state.page = "upload"
        st.rerun()


# ===== PAGE 2: UPLOAD RESUME PAGE =====
def upload_page():
    st.title("📄 Upload Your Resume")
    st.write("Upload your resume in PDF format so our AI can analyze it.")
    
    st.write("")
    
    uploaded_file = st.file_uploader(
        "📁 Choose your Resume PDF",
        type=["pdf"],
        help="Only PDF files are allowed"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ Successfully uploaded: **{uploaded_file.name}**")
        st.info(f"📦 File size: {round(uploaded_file.size / 1024, 2)} KB")
        
        st.write("")
        
        st.session_state.resume_file = uploaded_file
        
        if st.button("➡️ Continue to Questions", use_container_width=True, type="primary"):
            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.page = "questions"
            st.rerun()
    else:
        st.warning("⚠️ Please upload a PDF file to continue.")
    
    st.write("")
    st.write("")
    
    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ===== PAGE 3: QUESTIONS PAGE =====
def questions_page():
    st.title("❓ Interview Questions")
    
    current = st.session_state.current_question
    total = len(QUESTIONS)
    
    progress = (current + 1) / total
    st.progress(progress)
    st.write(f"**Question {current + 1} of {total}**")
    
    st.write("")
    
    st.info(f"**Q{current + 1}:** {QUESTIONS[current]}")
    
    st.write("")
    
    answer = st.text_area(
        "✍️ Type your answer here:",
        height=200,
        placeholder="Take your time and write a detailed answer...",
        key=f"answer_{current}"
    )
    
    st.write("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔙 Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    
    with col2:
        if current == total - 1:
            if st.button("🏁 Finish Interview", use_container_width=True, type="primary"):
                if answer.strip() == "":
                    st.error("⚠️ Please write an answer before finishing!")
                else:
                    st.session_state.answers.append(answer)
                    st.session_state.page = "report"
                    st.rerun()
        else:
            if st.button("➡️ Next Question", use_container_width=True, type="primary"):
                if answer.strip() == "":
                    st.error("⚠️ Please write an answer before continuing!")
                else:
                    st.session_state.answers.append(answer)
                    st.session_state.current_question += 1
                    st.rerun()


# ===== PAGE 4: REPORT PAGE (THE STAR! ⭐) =====
def report_page():
    # Fake scores for each question (later replaced by AI)
    scores = [random.randint(6, 10) for _ in range(len(QUESTIONS))]
    overall_score = round(sum(scores) / len(scores), 1)
    
    # Big celebration heading
    st.title("📊 Your Performance Report")
    st.balloons()  # 🎈 Balloons for celebration!
    
    st.write("")
    
    # ===== OVERALL SCORE (Big & Bold) =====
    st.subheader("🏆 Overall Score")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Show score in a big colorful way
        if overall_score >= 8:
            st.success(f"# 🌟 {overall_score} / 10")
            st.success("**Excellent Performance!** 🎉")
        elif overall_score >= 6:
            st.info(f"# 👍 {overall_score} / 10")
            st.info("**Good Performance!** Keep practicing!")
        else:
            st.warning(f"# 💪 {overall_score} / 10")
            st.warning("**Needs Improvement.** Don't give up!")
    
    st.write("")
    st.write("")
    
    # ===== SCORE CHART =====
    st.subheader("📈 Question-wise Scores")
    
    # Create data for chart
    chart_data = pd.DataFrame({
        "Question": [f"Q{i+1}" for i in range(len(QUESTIONS))],
        "Score": scores
    })
    chart_data = chart_data.set_index("Question")
    
    st.bar_chart(chart_data, color="#FF6B6B")
    
    st.write("")
    
    # ===== INDIVIDUAL QUESTION RESULTS =====
    st.subheader("📝 Question-by-Question Analysis")
    
    for i, (question, answer, score) in enumerate(zip(QUESTIONS, st.session_state.answers, scores)):
        with st.expander(f"**Q{i+1}: {question}** — Score: {score}/10"):
            st.write("**📝 Your Answer:**")
            st.write(f"_{answer}_")
            st.write("")
            st.write(f"**⭐ Score:** {score}/10")
            
            # Fake feedback based on score
            if score >= 8:
                st.success("✅ Great answer! Clear and confident.")
            elif score >= 6:
                st.info("👍 Good answer, but can be improved with more details.")
            else:
                st.warning("⚠️ Try to add more examples and be more specific.")
    
    st.write("")
    
    # ===== STRENGTHS =====
    st.subheader("💪 Your Strengths")
    st.success(
        """
        ✅ **Clear Communication** — You expressed your thoughts well  
        ✅ **Confident Tone** — Your answers sounded assured  
        ✅ **Relevant Examples** — You backed up your points  
        """
    )
    
    # ===== WEAKNESSES =====
    st.subheader("⚠️ Areas to Improve")
    st.warning(
        """
        📌 **Add More Details** — Some answers were too short  
        📌 **Use STAR Method** — Structure answers (Situation, Task, Action, Result)  
        📌 **Practice More** — Confidence comes with practice  
        """
    )
    
    # ===== TIPS =====
    st.subheader("💡 Tips for Next Time")
    st.info(
        """
        🎯 Research the company before the interview  
        🎯 Prepare 3-5 stories about your past experiences  
        🎯 Practice answers out loud, not just in your head  
        🎯 Ask smart questions at the end of the interview  
        🎯 Maintain good eye contact and body language  
        """
    )
    
    st.write("")
    st.write("")
    
    # ===== ACTION BUTTONS =====
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Try Again", use_container_width=True, type="primary"):
            st.session_state.page = "home"
            st.session_state.current_question = 0
            st.session_state.answers = []
            st.rerun()
    
    with col2:
        if st.button("📥 Download Report (Coming Soon)", use_container_width=True):
            st.info("💡 Report download feature will be added soon!")


# ===== SHOW THE RIGHT PAGE =====
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "upload":
    upload_page()
elif st.session_state.page == "questions":
    questions_page()
elif st.session_state.page == "report":
    report_page()


# ===== FOOTER =====
st.write("")
st.markdown("---")
st.caption("Made with ❤️ by Team AI Interview Coach")