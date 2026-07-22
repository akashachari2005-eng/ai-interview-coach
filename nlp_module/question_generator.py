"""
Question Generator
Generates interview questions based on extracted skills
Author: Adarsh
"""

import random
from .skills_database import QUESTION_TEMPLATES


class QuestionGenerator:
    """Class to generate interview questions"""

    def __init__(self):
        self.templates = QUESTION_TEMPLATES

    def generate_technical_questions(self, skills, num_questions=3):
        """Generate technical questions based on skills"""
        questions = []

        if not skills:
            return questions

        selected_skills = random.sample(skills, min(len(skills), num_questions))

        for skill in selected_skills:
            # Randomly pick difficulty
            difficulty = random.choice(['easy', 'medium', 'hard'])

            # Pick template based on difficulty
            if difficulty == 'easy':
                template = random.choice(self.templates['technical_easy'])
            elif difficulty == 'medium':
                template = random.choice(self.templates['technical_medium'])
            else:
                template = random.choice(self.templates['technical_hard'])

            question_text = template.format(skill=skill)

            questions.append({
                'question': question_text,
                'skill': skill,
                'type': 'technical',
                'difficulty': difficulty
            })

        return questions

    def generate_behavioral_questions(self, skills, num_questions=1):
        """Generate behavioral questions"""
        questions = []

        if not skills:
            return questions

        selected_skills = random.sample(skills, min(len(skills), num_questions))

        for skill in selected_skills:
            template = random.choice(self.templates['behavioral'])
            question_text = template.format(skill=skill)

            questions.append({
                'question': question_text,
                'skill': skill,
                'type': 'behavioral',
                'difficulty': 'medium'
            })

        return questions

    def generate_general_questions(self, num_questions=1):
        """Generate general interview questions"""
        selected = random.sample(
            self.templates['general'],
            min(len(self.templates['general']), num_questions)
        )

        questions = []
        for q in selected:
            questions.append({
                'question': q,
                'skill': 'general',
                'type': 'general',
                'difficulty': 'easy'
            })

        return questions

    def generate(self, skills, num_questions=5):
        """
        MAIN METHOD: Generate a mix of interview questions

        Args:
            skills (list): Skills extracted from resume
            num_questions (int): Total questions to generate

        Returns:
            list: Questions with metadata
        """
        all_questions = []

        if not skills:
            # If no skills found, return all general questions
            all_questions = self.generate_general_questions(num_questions)
        else:
            # Split: 3 technical + 1 behavioral + 1 general
            num_technical = max(1, num_questions - 2)
            num_behavioral = 1
            num_general = 1

            # Adjust if num_questions is small
            if num_questions <= 2:
                num_technical = num_questions
                num_behavioral = 0
                num_general = 0
            elif num_questions <= 4:
                num_technical = num_questions - 1
                num_behavioral = 1
                num_general = 0

            all_questions.extend(
                self.generate_technical_questions(skills, num_technical)
            )
            all_questions.extend(
                self.generate_behavioral_questions(skills, num_behavioral)
            )
            all_questions.extend(
                self.generate_general_questions(num_general)
            )

        # Add IDs
        for i, q in enumerate(all_questions, 1):
            q['id'] = i

        return all_questions

    def generate_by_difficulty(self, skills, difficulty='medium', num_questions=5):
        """
        Generate questions of specific difficulty

        Args:
            skills: list of skills
            difficulty: 'easy', 'medium', or 'hard'
            num_questions: how many
        """
        questions = []

        if not skills:
            return self.generate_general_questions(num_questions)

        selected_skills = random.sample(skills, min(len(skills), num_questions))

        template_key = f'technical_{difficulty}'
        if template_key not in self.templates:
            template_key = 'technical_medium'

        for i, skill in enumerate(selected_skills, 1):
            template = random.choice(self.templates[template_key])
            questions.append({
                'id': i,
                'question': template.format(skill=skill),
                'skill': skill,
                'type': 'technical',
                'difficulty': difficulty
            })

        return questions

    def generate_for_skill(self, skill, num_questions=3):
        """
        Generate multiple questions for ONE specific skill

        Useful when user wants to practice one topic deeply
        """
        questions = []
        all_templates = (
            self.templates['technical_easy'] +
            self.templates['technical_medium'] +
            self.templates['technical_hard']
        )

        selected_templates = random.sample(
            all_templates,
            min(len(all_templates), num_questions)
        )

        difficulties = ['easy', 'medium', 'hard']

        for i, template in enumerate(selected_templates, 1):
            questions.append({
                'id': i,
                'question': template.format(skill=skill),
                'skill': skill,
                'type': 'technical',
                'difficulty': difficulties[i % 3]
            })

        return questions