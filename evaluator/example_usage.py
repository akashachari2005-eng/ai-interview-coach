"""
Example usage of the evaluator module.
This file demonstrates how to use evaluate_answer() and generate_report().
"""

from evaluator import evaluate_answer, generate_report


def main():
    # ============================
    # STEP 1: Evaluate individual answers
    # ============================
    questions_and_answers = [
        ("What is Python?", "Python is a high-level programming language used for AI and web development."),
        ("What is React?", "React is a library."),
        ("Explain OOP.", "OOP is programming with objects, classes, inheritance, encapsulation, and polymorphism.")
    ]
    
    evaluations = []
    
    for question, answer in questions_and_answers:
        print(f"\n📝 Evaluating: {question}")
        result = evaluate_answer(question, answer)
        
        if result["success"]:
            eval_data = result["data"]
            # Store the evaluation with question and answer for report
            evaluations.append({
                "question": question,
                "answer": answer,
                "score": eval_data["score"],
                "strengths": eval_data["strengths"],
                "weaknesses": eval_data["weaknesses"]
            })
            print(f"   ✅ Score: {eval_data['score']}/10")
        else:
            print(f"   ❌ Error: {result['error']}")
    
    # ============================
    # STEP 2: Generate final report
    # ============================
    print("\n" + "=" * 60)
    print("📊 GENERATING FINAL REPORT")
    print("=" * 60)
    
    report_result = generate_report(evaluations)
    
    if report_result["success"]:
        report = report_result["data"]
        print(f"\n🏆 Performance: {report['performance_level']}")
        print(f"📊 Overall Score: {report['overall_score']}/10")
        print(f"📌 Total Questions: {report['total_questions']}")
        print(f"\n💡 Top Tips:")
        for tip in report['improvement_tips']:
            print(f"   • {tip}")
        print(f"\n📝 Final Verdict:\n{report['final_verdict']}")
    else:
        print(f"❌ Error: {report_result['error']}")


if __name__ == "__main__":
    main()