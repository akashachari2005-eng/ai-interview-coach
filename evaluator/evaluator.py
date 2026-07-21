from google import genai
from dotenv import load_dotenv
import os
import json

# Load API key when file is imported
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def evaluate_answer(question: str, answer: str) -> dict:
    """
    Evaluates a candidate's answer to an interview question using Gemini AI.
    
    Args:
        question (str): The interview question asked
        answer (str): The candidate's answer
    
    Returns:
        dict: Contains 'success' (bool) and either the evaluation data or an error message
    """
    
    # ============================
    # STEP 1: Input Validation
    # ============================
    if not question or not question.strip():
        return {
            "success": False,
            "error": "Question cannot be empty."
        }
    
    if not answer or not answer.strip():
        return {
            "success": False,
            "error": "Answer cannot be empty. Please provide a response."
        }
    
    if len(answer.strip()) < 5:
        return {
            "success": False,
            "error": "Answer is too short. Please provide a meaningful response."
        }
    
    # ============================
    # STEP 2: Build the Prompt
    # ============================
    prompt = f"""
    You are an expert technical interviewer evaluating a candidate's answer.

    Question: {question}
    Candidate's Answer: {answer}

    Please evaluate this answer and provide:
    1. A score from 1 to 10
    2. What was good about the answer (strengths)
    3. What needs improvement (weaknesses)
    4. A better example answer

    Respond ONLY in this JSON format, with no extra text or markdown:
    {{
        "score": <number>,
        "strengths": "<text>",
        "weaknesses": "<text>",
        "better_answer": "<text>"
    }}
    """
    
    # ============================
    # STEP 3: Call Gemini (with safety net)
    # ============================
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to connect to Gemini: {str(e)}"
        }
    
    # ============================
    # STEP 4: Parse the response (with safety net)
    # ============================
    try:
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        result = json.loads(cleaned_text)
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "AI returned an invalid response. Please try again."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }
    
    # ============================
    # STEP 5: Return the successful result
    # ============================
    return {
        "success": True,
        "data": result
    }

def generate_report(evaluations: list) -> dict:
    """
    Generates a final interview report from multiple Q&A evaluations.
    Uses Python for math and Gemini for smart insights.
    
    Args:
        evaluations (list): List of evaluation dictionaries from evaluate_answer()
    
    Returns:
        dict: Contains 'success' (bool) and either report data or error message
    """
    
    # ============================
    # STEP 1: Input Validation
    # ============================
    if not evaluations or not isinstance(evaluations, list):
        return {
            "success": False,
            "error": "Evaluations must be a non-empty list."
        }
    
    if len(evaluations) == 0:
        return {
            "success": False,
            "error": "No evaluations provided to generate report."
        }
    
    # ============================
    # STEP 2: Do the Math (Python)
    # ============================
    total_questions = len(evaluations)
    
    total_score = 0
    for eval_item in evaluations:
        total_score += eval_item.get("score", 0)
    
    average_score = round(total_score / total_questions, 2)
    
    # Determine performance level
    if average_score >= 8:
        performance_level = "Excellent 🌟"
    elif average_score >= 6:
        performance_level = "Good 👍"
    elif average_score >= 4:
        performance_level = "Average 📊"
    else:
        performance_level = "Needs Improvement 📚"
    
    # Count strong and weak answers
    strong_answers = 0
    weak_answers = 0
    for eval_item in evaluations:
        score = eval_item.get("score", 0)
        if score >= 7:
            strong_answers += 1
        elif score <= 4:
            weak_answers += 1
    
    # ============================
    # STEP 3: Collect Strengths & Weaknesses
    # ============================
    all_strengths = []
    all_weaknesses = []
    
    for eval_item in evaluations:
        strength = eval_item.get("strengths", "")
        weakness = eval_item.get("weaknesses", "")
        if strength:
            all_strengths.append(strength)
        if weakness:
            all_weaknesses.append(weakness)
    
    # Convert lists into readable text for Gemini
    strengths_text = "\n- " + "\n- ".join(all_strengths)
    weaknesses_text = "\n- " + "\n- ".join(all_weaknesses)
    
    # ============================
    # STEP 4: Build Smart Prompt for Gemini
    # ============================
    prompt = f"""
    You are an expert interview coach analyzing a candidate's performance.

    The candidate answered {total_questions} questions.
    Their average score was {average_score}/10 ({performance_level}).

    STRENGTHS observed across all answers:{strengths_text}

    WEAKNESSES observed across all answers:{weaknesses_text}

    Based on these patterns, provide:
    1. Top 3 recurring strengths (as short phrases)
    2. Top 3 recurring weaknesses (as short phrases)
    3. Top 3 actionable improvement tips (specific and practical)
    4. A personalized final verdict (2-3 sentences motivating the candidate)

    Respond ONLY in this JSON format, with no extra text or markdown:
    {{
        "top_strengths": ["strength 1", "strength 2", "strength 3"],
        "top_weaknesses": ["weakness 1", "weakness 2", "weakness 3"],
        "improvement_tips": ["tip 1", "tip 2", "tip 3"],
        "final_verdict": "<motivational paragraph>"
    }}
    """
    
    # ============================
    # STEP 5: Call Gemini
    # ============================
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to connect to Gemini: {str(e)}"
        }
    
    # ============================
    # STEP 6: Parse Gemini's Response
    # ============================
    try:
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        ai_insights = json.loads(cleaned_text)
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "AI returned an invalid report format. Please try again."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }
    
    # ============================
    # STEP 7: Combine Math + AI into Final Report
    # ============================
    final_report = {
        "overall_score": average_score,
        "performance_level": performance_level,
        "total_questions": total_questions,
        "strong_answers": strong_answers,
        "weak_answers": weak_answers,
        "top_strengths": ai_insights.get("top_strengths", []),
        "top_weaknesses": ai_insights.get("top_weaknesses", []),
        "improvement_tips": ai_insights.get("improvement_tips", []),
        "final_verdict": ai_insights.get("final_verdict", "")
    }
    
    return {
        "success": True,
        "data": final_report
    }


if __name__ == "__main__":
    
    # Simulate 3 evaluated answers
    fake_evaluations = [
        {
            "question": "What is Python?",
            "answer": "Python is a language",
            "score": 6,
            "strengths": "Correct basic definition",
            "weaknesses": "Lacks depth and examples"
        },
        {
            "question": "What is React?",
            "answer": "React is a JavaScript library for building UIs",
            "score": 8,
            "strengths": "Clear and accurate answer",
            "weaknesses": "Could mention virtual DOM"
        },
        {
            "question": "Explain OOP",
            "answer": "OOP is programming with objects",
            "score": 4,
            "strengths": "Basic idea correct",
            "weaknesses": "No mention of encapsulation, inheritance, or examples"
        }
    ]
    
    print("\n📊 GENERATING SMART REPORT...\n")
    print("=" * 60)
    
    result = generate_report(fake_evaluations)
    
    if result["success"]:
        report = result["data"]
        
        print(f"\n📌 Total Questions: {report['total_questions']}")
        print(f"📊 Overall Score: {report['overall_score']}/10")
        print(f"🏆 Performance: {report['performance_level']}")
        print(f"✅ Strong Answers: {report['strong_answers']}")
        print(f"⚠️  Weak Answers: {report['weak_answers']}")
        
        print("\n🌟 TOP STRENGTHS:")
        for s in report['top_strengths']:
            print(f"  • {s}")
        
        print("\n⚠️  TOP WEAKNESSES:")
        for w in report['top_weaknesses']:
            print(f"  • {w}")
        
        print("\n💡 IMPROVEMENT TIPS:")
        for t in report['improvement_tips']:
            print(f"  • {t}")
        
        print(f"\n📝 FINAL VERDICT:\n{report['final_verdict']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "=" * 60)
    
    
        