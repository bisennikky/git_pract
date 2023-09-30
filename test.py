from flask import Flask, render_template, jsonify
from flask_cors import CORS
from paho.mqtt import client as mqtt_client
import mysql.connector
from MQTT_file import mydb,cursor

app = Flask(__name__) 
CORS(app)

data = None
latest_data = None


@app.route('/test', methods = ["POST"])
def test():
    global data,latest_data
    cursor.execute("SELECT * FROM dp_tm_hm")
    data = cursor.fetchall()

    for row in data:
        latest_data = row
    print("Data.....", latest_data)
    mydb.commit()
    return jsonify({'dp':latest_data[2], 'temp':latest_data[3], 'hum':latest_data[4] })


@app.route('/')
def api():
    global latest_data
    return render_template('temp_hum_dp.html', rows = latest_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug = True)
