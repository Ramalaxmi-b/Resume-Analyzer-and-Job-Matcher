import os
from flask import request, jsonify, Blueprint
from parsers.text_extractor import extract_text_from_pdf, extract_text_from_docx
from utils.preprocess import clean_text

resume_parser_bp = Blueprint('resume_parser', __name__)

@resume_parser_bp.route('/parse_resume', methods=['POST'])
def parse_resume():
    data = request.json
    file_path = data.get('file_path')

    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 400

    ext = file_path.lower().split('.')[-1]
    try:
        if ext == "pdf":
            text, _ = extract_text_from_pdf(file_path)
        elif ext == "docx":
            text, _ = extract_text_from_docx(file_path)
        elif ext == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            return jsonify({'error': 'Unsupported file format'}), 400

        if not text or "Error" in text:
            return jsonify({'error': 'Failed to extract text from resume'}), 500

        text_cleaned = clean_text(text)
        return jsonify({'resume_text': text_cleaned}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
