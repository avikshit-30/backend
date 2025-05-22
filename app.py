from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Read and clean CSV
data = pd.read_csv('students.csv')
data['ID NO'] = data['ID NO'].astype(str).str.strip()  # Remove extra spaces in IDs

@app.route('/')
def home():
    return '''
        <form action="/result" method="post">
            Enter Student ID: <input type="text" name="id">
            <input type="submit">
        </form>
    '''

@app.route('/result', methods=['POST'])
def result():
    student_id = request.form['id'].strip()  # Clean up input
    app.logger.info(f"📝 HTML Form Request: Student ID = {student_id}, from IP = {request.remote_addr}")

    # Match after stripping spaces
    student = data[data['ID NO'] == student_id]

    if student.empty:
        return "Student not found"

    student_dict = student.to_dict(orient='records')[0]
    return render_template('result.html', student=student_dict)

@app.route('/api/student/<student_id>', methods=['GET'])
def get_student_data(student_id):
    student_id = student_id.strip()
    app.logger.info(f"📡 API Request for Student ID = {student_id}, from IP = {request.remote_addr}")

    student = data[data['ID NO'] == student_id]

    if student.empty:
        return jsonify({'error': 'Student not found'}), 404

    return jsonify(student.to_dict(orient='records')[0])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # default to 5000 if not set
    app.run(host='0.0.0.0', port=port, debug=True)
