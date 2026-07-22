"""
Resume Processor - Main Entry Point
Combines Resume Parser + Question Generator
Author: Adarsh

MAIN FUNCTIONS:
    1. parse_resume(pdf_path) → dict
    2. generate_questions(skills) → list
    3. process_resume_pipeline(pdf_path) → complete result
"""

from .resume_parser import ResumeParser
from .question_generator import QuestionGenerator

# Initialize once
parser = ResumeParser()
question_gen = QuestionGenerator()


def parse_resume(pdf_path):
    """
    Parse a resume PDF and extract structured information

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        dict: {
            'name': str,
            'email': str,
            'phone': str,
            'linkedin': str,
            'github': str,
            'skills': list,
            'education': list,
            'experience': dict,
            'status': str
        }

    Example:
        data = parse_resume("resume.pdf")
        print(data['skills'])  # ['Python', 'React', 'AWS']
    """
    return parser.parse(pdf_path)


def generate_questions(skills, num_questions=5, difficulty=None):
    """
    Generate interview questions based on skills

    Args:
        skills (list): List of skills from resume
        num_questions (int): Number of questions (default: 5)
        difficulty (str): 'easy', 'medium', 'hard', or None for mix

    Returns:
        list: [
            {
                'id': int,
                'question': str,
                'skill': str,
                'type': str,
                'difficulty': str
            }
        ]

    Example:
        questions = generate_questions(['Python', 'React'])
        for q in questions:
            print(q['question'])
    """
    if difficulty:
        return question_gen.generate_by_difficulty(skills, difficulty, num_questions)
    return question_gen.generate(skills, num_questions)


def generate_questions_for_skill(skill, num_questions=3):
    """
    Generate questions for ONE specific skill

    Args:
        skill (str): Single skill name
        num_questions (int): Number of questions

    Returns:
        list: Questions focused on that skill
    """
    return question_gen.generate_for_skill(skill, num_questions)


def process_resume_pipeline(pdf_path, num_questions=5, difficulty=None):
    """
    COMPLETE PIPELINE: Parse resume + Generate questions

    This is the main function Akash should call from the backend.

    Args:
        pdf_path (str): Path to resume PDF
        num_questions (int): Number of questions to generate
        difficulty (str): 'easy', 'medium', 'hard', or None

    Returns:
        dict: {
            'candidate': {name, email, phone, linkedin, github},
            'profile': {skills, education, experience},
            'interview_questions': [...],
            'metadata': {total_skills, total_questions},
            'status': str
        }

    Example:
        result = process_resume_pipeline("resume.pdf", num_questions=5)
        # Send result to frontend as JSON
    """
    # Step 1: Parse resume
    resume_data = parse_resume(pdf_path)

    if resume_data.get('status') == 'failed':
        return {
            'error': resume_data.get('error', 'Failed to parse resume'),
            'status': 'failed'
        }

    # Step 2: Generate questions
    skills = resume_data.get('skills', [])
    questions = generate_questions(skills, num_questions, difficulty)

    # Step 3: Build final response
    result = {
        'candidate': {
            'name': resume_data.get('name', 'Unknown'),
            'email': resume_data.get('email'),
            'phone': resume_data.get('phone'),
            'linkedin': resume_data.get('linkedin'),
            'github': resume_data.get('github'),
        },
        'profile': {
            'skills': resume_data.get('skills', []),
            'education': resume_data.get('education', []),
            'experience': resume_data.get('experience', {}),
        },
        'interview_questions': questions,
        'metadata': {
            'total_skills_found': len(skills),
            'total_questions_generated': len(questions),
            'difficulty_level': difficulty or 'mixed',
        },
        'status': 'success'
    }

    return result