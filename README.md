# 🎯 AI Virtual Interview Coach

An AI-powered web application that helps job seekers prepare for interviews by parsing their resume, generating custom interview questions, evaluating their answers, and providing personalized performance reports.

## 🚀 Features

- 📄 **Resume Parsing** — Extracts skills, experience, and education from uploaded resumes
- ❓ **Smart Question Generation** — Creates custom interview questions based on the candidate's profile
- 🤖 **AI-Powered Answer Evaluation** — Scores answers (1-10) with detailed feedback
- 📊 **Performance Reports** — Generates comprehensive reports with strengths, weaknesses, and improvement tips
- 🎨 **Interactive Web Interface** — Clean, user-friendly Streamlit UI

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI/LLM:** Google Gemini API
- **NLP:** spaCy, Hugging Face Transformers
- **Backend:** Python 3.10+
- **Version Control:** Git & GitHub

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<username>/ai-interview-coach.git
   cd ai-interview-coach
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate       # Windows
   source venv/bin/activate    # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root folder:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   Get your free key from: https://aistudio.google.com/apikey

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
ai-interview-coach/
    ├── app.py                  # Main Streamlit application
    ├── nlp_module/             # Resume parsing & question generation
    ├── evaluator/              # Answer evaluation & report generation
    ├── requirements.txt        # Python dependencies
    ├── .env                    
    ├── .gitignore
    └── README.md
```

## 👥 Team

This is a collaborative project built by a team of 3 developers:

- **Adarsh** — NLP & Data Engineer (Resume Parsing, Question Generation)
- **Prateek** — Generative AI & Analytics Engineer (Answer Evaluation, Report Generation)
- **Akash** — Full Stack Engineer (Streamlit UI, Integration, Deployment)

## 🎯 How It Works

1. User uploads their resume (PDF)
2. NLP module extracts skills and experience
3. AI generates 5 custom interview questions
4. User types their answers
5. Each answer is evaluated with score and feedback
6. Final report is generated with actionable insights

## 🔮 Future Enhancements

- 🎙️ Voice input with sentiment analysis
- 📈 Progress tracking over multiple sessions
- 🌐 Multi-language support
- 📄 Downloadable PDF reports

## 📄 License

This project is for educational purposes.

---

Built with ❤️ by Adarsh, Prateek & Akash
