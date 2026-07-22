"""
Flask API for AI Interview Coach
This is the backend that Akash's frontend will talk to
Author: Adarsh
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_module import parse_resume, generate_questions, process_resume_pipeline
import os
import json
import uuid

app = Flask(__name__)
CORS(app)  # Allow frontend to connect
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB max file size

# Upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'message': 'AI Interview Coach API is running!',
        'endpoints': {
            '/upload': 'POST - Upload resume PDF',
            '/parse': 'POST - Parse resume and get data',
            '/questions': 'POST - Get interview questions',
            '/pipeline': 'POST - Complete pipeline (parse + questions)',
        },
        'status': 'active'
    })


@app.route('/upload', methods=['POST'])
def upload_resume():
    """Upload a resume PDF file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    # Save file with unique name
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(filepath)

    return jsonify({
        'message': 'File uploaded successfully',
        'filename': unique_filename,
        'filepath': filepath
    })


@app.route('/parse', methods=['POST'])
def parse_resume_endpoint():
    """Parse an uploaded resume"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files allowed'}), 400

    # Save with unique name
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

    try:
        file.save(filepath)
        result = parse_resume(filepath)
        return jsonify(result)
    finally:
        # Delete after processing
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass


@app.route('/questions', methods=['POST'])
def get_questions():
    """Generate questions from skills list"""
    data = request.get_json()

    if not data or 'skills' not in data:
        return jsonify({'error': 'Send skills list in JSON body'}), 400

    skills = data['skills']
    num_questions = data.get('num_questions', 5)
    difficulty = data.get('difficulty', None)

    questions = generate_questions(skills, num_questions, difficulty)

    return jsonify({
        'questions': questions,
        'total': len(questions)
    })


@app.route('/pipeline', methods=['POST'])
def full_pipeline():
    """
    Complete pipeline: Upload PDF → Parse → Generate Questions
    This is the MAIN endpoint Akash should use
    
    Improvements:
    - Unique filenames (no conflicts between users)
    - Auto-delete files after processing (save disk space)
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files allowed'}), 400

    # Create unique filename to prevent conflicts between users
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

    try:
        # Save file with unique name
        file.save(filepath)

        # Get parameters
        num_questions = int(request.form.get('num_questions', 5))
        difficulty = request.form.get('difficulty', None)

        # Run pipeline
        result = process_resume_pipeline(filepath, num_questions, difficulty)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 500

    finally:
        # Auto-delete file after processing (save disk space)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass


@app.errorhandler(413)
def file_too_large(e):
    """Handle file too large error"""
    return jsonify({
        'error': 'File too large. Maximum size is 5MB.',
        'status': 'failed'
    }), 413


if __name__ == '__main__':
    print("\n🚀 AI Interview Coach API is starting...")
    print("📍 URL: http://localhost:5000")
    print("📍 Endpoints:")
    print("   GET  / → Health check")
    print("   POST /upload → Upload resume")
    print("   POST /parse → Parse resume")
    print("   POST /questions → Generate questions")
    print("   POST /pipeline → Complete pipeline")
    print("\n")
    app.run(debug=True, port=5000)