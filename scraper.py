import requests
from bs4 import BeautifulSoup

# Constants
GATE_URL = 'https://sia.mercubuana.ac.id/gate.php/login'
INFO_URL = 'https://sia.mercubuana.ac.id/akad.php/biomhs/lst'
SCHEDULE_URL = 'https://sia.mercubuana.ac.id/akad.php/biomhs/jadwal'
LOGIN_PAYLOAD = {
    'act': 'login',
    'username': '',
    'password': ''
}
STUDENT_DATA_SEARCH_STRINGS = [
    ('NIM', 'nim'),
    ('Nama', 'name'),
    ('Fakultas', 'faculty'),
    ('Jurusan', 'major'),
    ('SKS Tempuh', 'sks'),
    ('Semester', 'semester'),
    ('IPK', 'gpa')
]
SCHEDULE_PAYLOAD = {
    'periode': '20233'
}

def login(nim, password):
    payload = LOGIN_PAYLOAD.copy()
    payload['username'] = nim
    payload['password'] = password

    session = requests.Session()
    response = session.post(GATE_URL, data=payload)
    response.raise_for_status()
    return session

def scrape_student_data(nim, password):
    try:
        session = login(nim, password)
        response = session.get(INFO_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        return {'error': str(e)}

    soup = BeautifulSoup(response.text, 'html.parser')
    results = {}

    for search_string, var_name in STUDENT_DATA_SEARCH_STRINGS:
        element = soup.find('td', string=search_string).find_next('td')
        if search_string == 'Nama':
            element = element.find_next('td')
        results[var_name] = element.text.strip().title()

    return results

def scrape_schedule(nim, password):
    try:
        session = login(nim, password)
        response = session.post(SCHEDULE_URL, data=SCHEDULE_PAYLOAD)
        response.raise_for_status()
    except requests.RequestException as e:
        return {'error': str(e)}

    soup = BeautifulSoup(response.text, 'html.parser')
    schedule_table = soup.find('table', {'class': 'table table-striped table-condensed'})
    if not schedule_table:
        return []

    rows = schedule_table.find_all('tr')[1:]  # Skip the header row
    schedule_data = []
    schedule_id = 1

    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 9:
            schedule = {
                'id': schedule_id,
                'day': cells[1].text.strip(),
                'class_start': cells[2].text.strip(),
                'class_end': cells[3].text.strip(),
                'subject_code': cells[4].text.strip(),
                'subject_name': cells[5].get_text(separator=' / ').replace(' / \n /', '').strip(), # TODO: Refactor this
                'class_number': cells[6].text.strip().split('\n')[2] if len(cells[6].text.strip().split('\n')) > 2 else '', # TODO: Refactor this
                'instructor': cells[7].text.strip(),
                'class_unit': cells[8].text.strip(),
            }
            schedule_data.append(schedule)
            schedule_id += 1

    return schedule_data