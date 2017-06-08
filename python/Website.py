import flask as f
import DbClass

# import sensor



app = f.Flask(__name__)
# app.debug = True
# app.config['DEBUG'] = True
db = DbClass.DbClass()


# sen = sensor.Sensor()


def read_data_db(datetime_start, datetime_stop, type):
    data = db.read_measurement(datetime_start, datetime_stop, type)[0]
    values = []
    for a in data:
        values.append(a[0])
    return values


# def add_data_db():
#     data = sen.get_data_arduino()
#     db.add_measurement(data[0], 1)
#     db.add_measurement(data[1], 2)
#     db.add_measurement(data[2], 4)


@app.route('/')
def home():
    temp = db.get_last_measurement(1)[0][0]
    hum = db.get_last_measurement(2)[0][0]
    light = db.get_last_measurement(4)[0][0]
    return f.render_template('home.html', temp=temp, hum=hum, light=light)


@app.route('/data')
def data():
    return f.render_template('data.html', data='')


@app.route('/data', methods=['POST'])
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

    # print(data)
    return f.render_template('data.html', data=data, labels=labels)


@app.route('/forecast')
def forecast():
    return f.render_template('forecast.html')


@app.route('/forecast', methods=['POST'])
def forecast_w_data():
    location = f.request.form.get('location')
    return f.render_template('forecast.html', location=location)


@app.route('/settings')
def settings():
    return f.render_template('settings.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )
