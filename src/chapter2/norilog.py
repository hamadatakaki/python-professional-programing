import json
from datetime import datetime

from flask import escape, redirect, render_template, request, Flask, Markup

application = Flask(__name__)

DATA_FILE = 'norilog.json'

def save_data(start, finish, memo, created_at):
    """save recorded datas.
    :param start: taking station
    :type start: str
    :param finish: getting off station
    :type finish: str
    :param memo: taking and getting off memo
    :type memo: str
    :param created_at: taking and getting off date
    :type created_at: datetime.datetime
    :return: None
    """
    
    try:
        # open database file by json module
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []

    database.insert(0, {
        "start": start,
        "finish": finish, 
        "memo": memo,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M")
    })

    json.dump(database, open(DATA_FILE, mode="w", encoding="utf-8"), indent=4, ensure_ascii=False)

def load_data():
    """get recorded datas."""
    try: 
        # open database file by json module
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []

    return database

@application.route('/')
def index():
    """top page. show pages using template."""
    
    rides = load_data()
    return render_template('index.html', rides=rides)

@application.route('/save', methods=['POST'])
def save():
    """saving data url."""
    # get posted datas and save
    start = request.form.get('start')
    finish = request.form.get('finish')
    memo = request.form.get('memo')
    create_at = datetime.now()
    save_data(start, finish, memo, create_at)

    # redirect to top page
    return redirect('/')

@application.template_filter('nl2br')
def nl2br_filter(s):
    """template filter, which replaces ¥n to br tag."""
    return escape(s).replace('\n', Markup('<br>'))


if __name__ == '__main__':
    # run application at IP address 0.0.0.0:8000
    application.run('0.0.0.0', 8000, debug=True)
