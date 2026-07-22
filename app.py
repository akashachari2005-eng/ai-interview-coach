import streamlit as st
import pandas as pd
import tempfile
import os

# Import Adarsh's function
from nlp_module.resume_processor import process_resume_pipeline

# Import Prateek's functions
from evaluator.evaluator import evaluate_answer, generate_report


# ===== PAGE SETUP =====
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="centered"
)

# ===== SESSION STATE =====
if "page" not in st.session_state:
    st.session_state.page = "home"
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "candidate" not in st.session_state:
    st.session_state.candidate = {}


# ===== PAGE 1: HOME =====
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


# ===== PAGE 2: UPLOAD RESUME =====
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
        
        if st.button("➡️ Continue to Questions", use_container_width=True, type="primary"):
            with st.spinner("🤖 Analyzing your resume and generating questions..."):
                # Save uploaded file to temp location (Adarsh's function needs a file path)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                try:
                    # Call Adarsh's pipeline
                    result = process_resume_pipeline(tmp_path, num_questions=5)
                    
                    if result.get("status") == "success":
                        # Extract just the question text strings
                        questions_data = result["interview_questions"]
                        questions_text = [q["question"] for q in questions_data]
                        
                        st.session_state.questions = questions_text
                        st.session_state.candidate = result["candidate"]
                        st.session_state.current_question = 0
                        st.session_state.answers = []
                        st.session_state.page = "questions"
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Failed to parse resume')}")
                finally:
                    # Cleanup temp file
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
    else:
        st.warning("⚠️ Please upload a PDF file to continue.")
    
    st.write("")
    st.write("")
    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ===== PAGE 3: QUESTIONS =====
def questions_page():
    st.title("❓ Interview Questions")
    
    # Show candidate name if available
    candidate_name = st.session_state.candidate.get("name", "")
    if candidate_name and candidate_name != "Unknown":
        st.caption(f"👤 Interviewing: **{candidate_name}**")
    
    questions = st.session_state.questions
    current = st.session_state.current_question
    total = len(questions)
    
    progress = (current + 1) / total
    st.progress(progress)
    st.write(f"**Question {current + 1} of {total}**")
    st.write("")
    st.info(f"**Q{current + 1}:** {questions[current]}")
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


# ===== PAGE 4: REPORT =====
def report_page():
    st.title("📊 Your Performance Report")
    
    questions = st.session_state.questions
    answers = st.session_state.answers
    
    # ===== EVALUATE EACH ANSWER =====
    with st.spinner("🤖 AI is evaluating your answers... (this takes 10-20 seconds)"):
        evaluations = []
        progress_bar = st.progress(0)
        
        for i, (q, a) in enumerate(zip(questions, answers)):
            result = evaluate_answer(q, a)
            if result["success"]:
                evaluations.append({
                    "question": q,
                    "answer": a,
                    "score": result["data"]["score"],
                    "strengths": result["data"]["strengths"],
                    "weaknesses": result["data"]["weaknesses"],
                    "better_answer": result["data"]["better_answer"]
                })
            progress_bar.progress((i + 1) / len(questions))
        
        progress_bar.empty()
    
    if not evaluations:
        st.error("❌ Failed to evaluate answers. Please try again.")
        return
    
    # ===== GENERATE FINAL REPORT =====
    with st.spinner("📊 Generating your personalized report..."):
        report_result = generate_report(evaluations)
    
    if not report_result["success"]:
        st.error(f"❌ Error: {report_result['error']}")
        return
    
    report = report_result["data"]
    st.balloons()
    
    # ===== OVERALL SCORE =====
    st.subheader("🏆 Overall Score")
    overall_score = report["overall_score"]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if overall_score >= 8:
            st.success(f"# 🌟 {overall_score} / 10")
            st.success(f"**{report['performance_level']}**")
        elif overall_score >= 6:
            st.info(f"# 👍 {overall_score} / 10")
            st.info(f"**{report['performance_level']}**")
        else:
            st.warning(f"# 💪 {overall_score} / 10")
            st.warning(f"**{report['performance_level']}**")
    
    st.write("")
    
    # ===== SCORE CHART =====
    st.subheader("📈 Question-wise Scores")
    scores = [e["score"] for e in evaluations]
    chart_data = pd.DataFrame({
        "Question": [f"Q{i+1}" for i in range(len(evaluations))],
        "Score": scores
    }).set_index("Question")
    st.bar_chart(chart_data, color="#FF6B6B")
    st.write("")
    
    # ===== QUESTION-BY-QUESTION =====
    st.subheader("📝 Question-by-Question Analysis")
    for i, eval_item in enumerate(evaluations):
        with st.expander(f"**Q{i+1}: {eval_item['question']}** — Score: {eval_item['score']}/10"):
            st.write("**📝 Your Answer:**")
            st.write(f"_{eval_item['answer']}_")
            st.write("")
            st.success(f"**✅ Strengths:** {eval_item['strengths']}")
            st.warning(f"**⚠️ Weaknesses:** {eval_item['weaknesses']}")
            st.info(f"**💡 Better Answer:** {eval_item['better_answer']}")
    
    st.write("")
    
    # ===== TOP STRENGTHS =====
    st.subheader("💪 Your Top Strengths")
    for s in report["top_strengths"]:
        st.success(f"✅ {s}")
    
    # ===== TOP WEAKNESSES =====
    st.subheader("⚠️ Areas to Improve")
    for w in report["top_weaknesses"]:
        st.warning(f"📌 {w}")
    
    # ===== IMPROVEMENT TIPS =====
    st.subheader("💡 Personalized Tips")
    for tip in report["improvement_tips"]:
        st.info(f"🎯 {tip}")
    
    # ===== FINAL VERDICT =====
    st.subheader("📝 Final Verdict")
    st.write(report["final_verdict"])
    
    st.write("")
    st.write("")
    
    # ===== ACTION BUTTONS =====
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Try Again", use_container_width=True, type="primary"):
            st.session_state.page = "home"
            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.questions = []
            st.session_state.candidate = {}
            st.rerun()
    with col2:
        if st.button("📥 Download Report (Coming Soon)", use_container_width=True):
            st.info("💡 Report download feature will be added soon!")


# ===== ROUTER =====
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