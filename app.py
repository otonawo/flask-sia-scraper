import os
from flask import Flask, jsonify, request
from scraper import scrape_student_data, scrape_schedule
from functools import wraps

app = Flask(__name__)
API_KEY = os.getenv('API_KEY')

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

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key != API_KEY:
            return jsonify({"message": "Forbidden"}), 403
        return func(*args, **kwargs)
    return wrapper

@app.route('/getStudentData', methods=['POST'])
@require_api_key
def get_student_data():
    nim, password, error = extract_and_validate_request_data()
    if error:
        return jsonify({'error': error}), 400

    student_data = scrape_student_data(nim, password)
    return jsonify(student_data)

@app.route('/getSchedule', methods=['POST'])
@require_api_key
def get_schedule():
    nim, password, error = extract_and_validate_request_data()
    if error:
        return jsonify({'error': error}), 400

    schedule = scrape_schedule(nim, password)
    return jsonify(schedule)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)