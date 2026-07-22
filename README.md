# 🎯 AI Virtual Interview Coach

An AI-powered web application that helps job seekers prepare for interviews by parsing their resume, generating personalized interview questions, evaluating their answers, and providing detailed performance reports — all powered by Google Gemini.

## 🚀 Features

- 📄 **Smart Resume Parsing** — Extracts skills, education, experience, and contact info from PDF resumes
- ❓ **Personalized Question Generation** — Creates custom interview questions based on your skills
- 🤖 **AI-Powered Answer Evaluation** — Scores answers (1-10) with detailed feedback and model answers
- 📊 **Comprehensive Performance Reports** — Overall score, top strengths, weaknesses, and personalized improvement tips
- 🎨 **Clean Interactive UI** — Built with Streamlit for a smooth user experience

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI/LLM:** Google Gemini API (gemini-2.5-flash)
- **NLP:** spaCy, PyPDF2, pdfplumber
- **Backend:** Python 3.10+
- **Version Control:** Git & GitHub

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/akashachari2005-eng/ai-interview-coach.git
cd ai-interview-coach
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download spaCy language model
```bash
python -m spacy download en_core_web_sm
```

### 5. Set up environment variables
Create a `.env` file in the **root folder**:
```
GEMINI_API_KEY=your_api_key_here
```
Get your free key from: https://aistudio.google.com/apikey

### 6. Run the app 🚀
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

## 📁 Project Structure

```
ai-interview-coach/
    ├── app.py                          # Main Streamlit application
    │
    ├── nlp_module/                     # Resume parsing & question generation
    │   ├── resume_parser.py            # PDF text extraction & info parsing
    │   ├── question_generator.py       # Interview question generation
    │   ├── resume_processor.py         # Main pipeline (parse + questions)
    │   └── skills_database.py          # Skills & question templates
    │
    ├── evaluator/                      # Answer evaluation & report generation
    │   ├── evaluator.py                # Core AI evaluation logic
    │   ├── example_usage.py            # Usage examples
    │   └── README.md                   # Module-specific docs
    │
    ├── requirements.txt                # Python dependencies
    ├── .env                            # API keys (not tracked)
    ├── .gitignore
    └── README.md
```

## 🎯 How It Works

```
1. User uploads resume (PDF)
        ↓
2. NLP module extracts skills, education, experience
        ↓
3. Question generator creates 5 personalized questions
        ↓
4. User answers each question in the browser
        ↓
5. Gemini AI evaluates each answer (score + feedback)
        ↓
6. Final report generated with strengths, weaknesses & tips
```

## 👥 Team

Built by a 3-member team, each owning a core module:

| Member | Role | Contribution |
|--------|------|--------------|
| **Adarsh** | NLP & Data Engineer | Resume parsing, skill extraction, question generation |
| **Prateek** | Generative AI Engineer | Answer evaluation, hybrid report generation using Gemini API |
| **Akash** | Full Stack Engineer | Streamlit UI, integration, deployment |

## 🧪 Usage Example

```python
# For developers who want to use the modules independently:

# 1. Parse a resume
from nlp_module.resume_processor import process_resume_pipeline
result = process_resume_pipeline("path/to/resume.pdf", num_questions=5)

# 2. Evaluate an answer
from evaluator.evaluator import evaluate_answer
evaluation = evaluate_answer("What is Python?", "Python is a language...")

# 3. Generate final report
from evaluator.evaluator import generate_report
report = generate_report(list_of_evaluations)
```

## 🐛 Troubleshooting

**`ModuleNotFoundError: No module named 'nlp_module'`**  
→ Run the app from the **root folder** (`ai-interview-coach/`), not inside a subfolder.

**`spacy model not found`**  
→ Run: `python -m spacy download en_core_web_sm`

**`GEMINI_API_KEY not found`**  
→ Create a `.env` file in the root with your Gemini API key.

**Streamlit not opening in browser**  
→ Manually visit `http://localhost:8501`

## 🔮 Future Enhancements

- 🎙️ Voice input with sentiment analysis (confidence detection)
- 📈 Progress tracking across multiple interview sessions
- 🌐 Multi-language support
- 📄 Downloadable PDF performance reports
- 💾 User accounts & interview history (MongoDB)

## 📄 License

This project is built for educational and portfolio purposes.

---

**Built with ❤️ by Adarsh, Prateek & Akash**
