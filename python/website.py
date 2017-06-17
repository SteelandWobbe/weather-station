import flask as f
import DbClass
from passlib.hash import pbkdf2_sha512
import random
import string
# import simplejson               needs to be installed for decimal support to json; does not need to be imported


app = f.Flask(__name__)
db = DbClass.DbClass()


def verify_password(password, hashed_password):
    return pbkdf2_sha512.verify(password, hashed_password)


def add_user_db(username, password):
    try:
        db.add_user(username,
                    pbkdf2_sha512.using(salt_size=64, rounds=100000).hash(password))
        return True
    except:
        return False


def get_passwordhash_db(useraname):
    try:
        return db.get_password_user(useraname)
    except:
        return None


def read_data_db(datetime_start, datetime_stop, type):
    data = db.read_measurement(datetime_start, datetime_stop, type)[0]
    values = []
    for a in data:
        values.append(a[0])
    return values


@app.route('/')
def home():
    if 'username' in f.session:
        temp = db.get_last_measurement(1)[0][0]
        hum = db.get_last_measurement(2)[0][0]
        light = db.get_last_measurement(4)[0][0]
        return f.render_template('home.html',
                                 temp=temp,
                                 hum=hum,
                                 light=light)
    return f.redirect(f.url_for('login'))


@app.route('/data', methods=['GET', 'POST'])
def data():
    if 'username' in f.session:
        if f.request.method == 'POST':
            start_date = f.request.form.get('datetime_start')
            end_date = f.request.form.get('datetime_stop')
            f.session['graph_data'] = []

            if f.request.form.get('temperature') is not None:
                f.session['graph_data'].append([read_data_db(start_date, end_date, 1), "Temperatuur"])

            if f.request.form.get('humidity') is not None:
                f.session['graph_data'].append([read_data_db(start_date, end_date, 2), "Vochtigheid"])

            if f.request.form.get('light') is not None:
                f.session['graph_data'].append([read_data_db(start_date, end_date, 4), "Lichtsterkte"])

            f.session['graph_labels'] = db.get_measurement_dates(start_date, end_date)
            return f.render_template('data.html',
                                     data=f.session['graph_data'],
                                     labels=f.session['graph_labels'])
        return f.render_template('data.html', data=f.session['graph_data'], labels=f.session['graph_labels'])
    return f.redirect(f.url_for('login'))


@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    if 'username' in f.session:
        if f.request.method == 'POST':
            f.session['forecast_location'] = f.request.form.get('location')
            return f.render_template('forecast.html', location=f.session['forecast_location'])
        return f.render_template('forecast.html', location=f.session['forecast_location'])
    return f.redirect(f.url_for('login'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' in f.session:
        if f.request.method == 'POST':
            password_old = f.request.form.get('password_old')
            new_password1 = f.request.form.get('password_new1')
            new_password2 = f.request.form.get('password_new2')
            if new_password1 == new_password2:
                if verify_password(password=password_old,
                                   hashed_password=db.get_password_user(f.session['username'])):
                    db.update_password_user(f.session['username'], pbkdf2_sha512.hash(new_password1))
                    return f.render_template('settings.html')
            return f.render_template('settings.html')
        return f.render_template('settings.html')
    return f.redirect(f.url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if f.request.method == 'POST':
        username = f.request.form.get('username')
        password_db = get_passwordhash_db(username)
        if password_db is not None:
            if verify_password(password=f.request.form.get('password'),
                               hashed_password=password_db):
                f.session['username'] = username
                f.session['graph_data'] = []
                f.session['graph_labels'] = []
                f.session['forecast_location'] = ''
                return f.redirect(f.url_for('home'))
        return f.render_template('login.html', failed=True)
    return f.render_template('login.html')


@app.route('/logout')
def logout():
    if 'username' in f.session:
        f.session.pop('username', None)
        return f.redirect(f.url_for('login'))
    return f.redirect(f.url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if f.request.method == 'POST':
        password1 = f.request.form.get('password1')
        if password1 == f.request.form.get('password2'):
            if add_user_db(username=f.request.form.get('username'),
                           password=password1
                           ):
                return f.redirect(f.url_for('login'))
        return f.render_template('register.html', failed=True)
    return f.render_template('register.html')




app.secret_key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(128))
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=80)
