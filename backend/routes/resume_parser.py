import PyPDF2

@app.route('/parse_resume', methods=['POST'])
def parse_resume():
    data = request.json
    file_path = data.get('file_path')

    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 400

    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return jsonify({'resume_text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
