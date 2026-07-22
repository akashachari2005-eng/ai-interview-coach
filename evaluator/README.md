# 🎯 Interview Evaluator Module

An AI-powered interview evaluation system that scores candidate answers and generates personalized performance reports using Google Gemini.

## 🚀 Features

- ✅ Evaluate individual interview answers with scoring and feedback
- ✅ Generate comprehensive performance reports from multiple evaluations
- ✅ AI-powered insights for strengths, weaknesses, and improvement tips
- ✅ Production-ready error handling

## 📦 Installation

1. Clone the repository

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate       # Windows
   source venv/bin/activate    # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root folder:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   Get your free key from: https://aistudio.google.com/apikey

## 💡 Usage

### 1. Evaluate a Single Answer

```python
from evaluator import evaluate_answer

result = evaluate_answer(
    question="What is Python?",
    answer="Python is a high-level programming language."
)

if result["success"]:
    data = result["data"]
    print(f"Score: {data['score']}/10")
    print(f"Strengths: {data['strengths']}")
    print(f"Weaknesses: {data['weaknesses']}")
    print(f"Better Answer: {data['better_answer']}")
else:
    print(f"Error: {result['error']}")
```

**Returns:**
```python
{
    "success": True,
    "data": {
        "score": 7,
        "strengths": "Clear definition...",
        "weaknesses": "Lacks examples...",
        "better_answer": "Python is a versatile..."
    }
}
```

### 2. Generate Final Report

```python
from evaluator import generate_report

evaluations = [
    {
        "question": "What is Python?",
        "answer": "...",
        "score": 7,
        "strengths": "...",
        "weaknesses": "..."
    },
    # ... more evaluations
]

report = generate_report(evaluations)

if report["success"]:
    data = report["data"]
    print(f"Overall Score: {data['overall_score']}/10")
    print(f"Performance: {data['performance_level']}")
    print(f"Tips: {data['improvement_tips']}")
```

**Returns:**
```python
{
    "success": True,
    "data": {
        "overall_score": 6.5,
        "performance_level": "Good 👍",
        "total_questions": 3,
        "strong_answers": 1,
        "weak_answers": 1,
        "top_strengths": [...],
        "top_weaknesses": [...],
        "improvement_tips": [...],
        "final_verdict": "..."
    }
}
```

## ⚠️ Error Handling

All functions return a consistent format:
- `success: True` → data is in `result["data"]`
- `success: False` → error message is in `result["error"]`

Always check `result["success"]` before accessing data.

## 🛠️ Tech Stack

- **Python 3.10+**
- **Google Gemini API** (gemini-2.5-flash)
- **python-dotenv** for secure key management

## 👨‍💻 Author

Built by **Prateek** as part of the AI Virtual Interview Coach project.