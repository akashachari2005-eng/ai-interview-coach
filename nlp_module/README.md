#  AI Interview Coach - NLP Module

**Author:** Adarsh (NLP & Data Engineer)  
**Project:** AI Virtual Interview Coach

##  What This Does
- Reads resume PDFs and extracts skills, education, experience
- Generates custom interview questions based on extracted skills
- Provides a Flask API for frontend integration

##  Quick Setup

```bash
# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run tests
python -m tests.test_module

# Start API server
python app.py