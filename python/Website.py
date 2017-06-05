import flask as f
import DbClass

app = f.Flask(__name__)

db = DbClass.DbClass()


def read_data_db(datetime_start, datetime_stop, type):
    data = db.read_measurement(datetime_start, datetime_stop, type)[0]
    values = []
    for a in data:
        values.append(a[0])
    return values


# asd = (db.get_measurement_dates('2017-1-1', '2018-1-1'))
# print(asd)

@app.route('/')
def home():
    return f.render_template('home.html')


@app.route('/data')
def data():
    return f.render_template('data.html', data='')


@app.route('/data_graph', methods=['POST'])
def data_graph():
    start_date = f.request.form['datetime_start']
    end_date = f.request.form['datetime_stop']
    data = []

    temp = f.request.form.get('temperature') is not None
    if temp:
        data.append([read_data_db(start_date, end_date, 1), "Temperatuur"])

    humidity = f.request.form.get('humidity') is not None
    if humidity:
        data.append([read_data_db(start_date, end_date, 2), "Vochtigheid"])

    light = f.request.form.get('light') is not None
    if light:
        data.append([read_data_db(start_date, end_date, 4), "Lichtsterkte"])
    labels = db.get_measurement_dates(start_date, end_date)

    print(data)
    return f.render_template('data.html', data=data, labels=labels)


@app.route('/forecast')
def forecast():
    return f.render_template('forecast.html')


@app.route('/settings')
def settings():
    return f.render_template('settings.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )
