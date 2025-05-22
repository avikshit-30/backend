from flask import Flask, request, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)
data = pd.read_csv('students.csv')

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
    student_id = request.form['id'].strip() 
    print(student_id) # Remove extra spaces
    student = data[data['ID NO'].str.strip() == student_id]
    print(student)
    if student.empty:
        return "Student not found"
    student_dict = student.to_dict(orient='records')[0]
    return render_template('result.html', student=student_dict)

@app.route('/api/student/<student_id>', methods=['GET'])
def get_student_data(student_id):
    student = data[data['ID NO'].str.strip() == student_id.strip()]
    if student.empty:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student.to_dict(orient='records')[0])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # default to 5000 if not in Render
    app.run(host='0.0.0.0', port=port, debug=True)