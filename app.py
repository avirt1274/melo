# asyncio.set_event_loop_policy(io.WindowsSelectorEventLoopPolicy())

import flask, logging
from databaser import Databaser

app = flask.Flask(__name__)
db = Databaser(db_name='database.db')

ip = '0.0.0.0'
port = '5555'
# 19132
# 95.31.8.49

@app.route('/')
def root():
    return flask.render_template('login.html')

@app.route('/policy_terms')
def policy_terms():
    return flask.render_template('policy_terms.html')

@app.route('/main/<phone>')
def main(phone):
    if db.get_user(phone):
        return flask.render_template('main.html', name = db.get_user_name(phone), level = db.get_user_level(phone), phone_number = phone, language = db.get_user_language(phone))
    else:
        return flask.redirect('/')
    
# LESSONS
@app.route('/lesson/<phone>', methods=['GET'])
def lesson(phone):
    if db.get_user(phone):
        lesson_to_ref = db.get_user_language(phone) + '_' + str(db.get_user_level(phone)) + '.html'

        return flask.render_template(lesson_to_ref, name = db.get_user_name(phone), phone_number = phone)
    else:
        return flask.redirect('/')
    
@app.route('/lesson/<phone>/<points>/end', methods=['POST'])
def lesson_end(phone, points):
    if db.get_user(phone):
        if int(points) >= 7:
            return lesson_success(phone)
        else:
            return lesson_failed(phone)
    else:
        return flask.redirect('/')

def lesson_success(phone):
    if db.get_user(phone):
        db.set_user_level(str(int(db.get_user_level(phone)) + 1), phone)
        return 'success'
    else:
        return '404'

def lesson_failed(phone):
    if db.get_user(phone):
        return 'failed'
    else:
        return '404'
# LESSONS

@app.route('/db/user_create/<username>/<language>/<phone>', methods=['POST'])
def create_user(username, language, phone):
    if db.get_user(phone):
        return '404'
    else:
        db.add_user(username, language, phone)
        return '200'
    
@app.route('/db/user_remove/<phone>', methods=['POST'])
def remove_user(phone):
    if db.get_user(phone):
        db.remove_user(phone)
        return 'removed'
    else:
        return 'not found'

@app.route('/db/is_user_exists/<phone>', methods=['POST'])
def is_user_exists(phone):
    if db.get_user(phone):
        return 'exists'
    else:
        return 'no'
    
@app.route('/level/get_level/<phone>', methods=['POST'])
def get_level(phone):
    if db.get_user(phone):
        return db.get_user_level(phone)
    else:
        return '404'

@app.route('/level/set_level/<level_id>/<phone>', methods=['POST'])
def set_level(level_id, phone):
    try:
        db.set_user_level(level_id, phone)
    except Exception as e:
        logging.error(f"Error: {e}")
        return '500'
    
@app.route('/language/set_language/<language>/<phone>', methods=['POST'])
def get_language(language, phone):
    try:
        db.set_user_language(language, phone)
    except Exception as e:
        logging.error(f"Error: {e}")
        return '500'
    
@app.route('/language/get_language/<phone>', methods=['POST'])
def set_language(phone):
    try:
        db.get_user_language(phone)
    except Exception as e:
        logging.error(f"Error: {e}")
        return '500'

if __name__ == '__main__':
    app.run(host=ip, port=int(port))