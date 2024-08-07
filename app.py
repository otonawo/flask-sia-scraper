from flask import Flask, jsonify, request
from scraper import scrape_student_data, scrape_schedule

app = Flask(__name__)

def extract_and_validate_request_data():
    try:
        data = request.get_json()
        nim = data.get('nim')
        password = data.get('password')
        if not nim or not password:
            raise ValueError('NIM and password are required')
        return nim, password, None
    except (TypeError, ValueError) as e:
        return None, None, str(e)

@app.route('/getStudentData', methods=['POST'])
def get_student_data():
    nim, password, error = extract_and_validate_request_data()
    if error:
        return jsonify({'error': error}), 400

    student_data = scrape_student_data(nim, password)
    return jsonify(student_data)

@app.route('/getSchedule', methods=['POST'])
def get_schedule():
    nim, password, error = extract_and_validate_request_data()
    if error:
        return jsonify({'error': error}), 400

    schedule = scrape_schedule(nim, password)
    return jsonify(schedule)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)