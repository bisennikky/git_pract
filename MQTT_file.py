import random
from datetime import datetime
from paho.mqtt import client as mqtt_client
import mysql.connector

broker = "107.180.94.60"
port = 18889

topic = "EVZ_DPTH_02/status"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

# configure the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="status_control"
)
cursor = mydb.cursor()

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    value = str(message.payload.decode("utf-8"))
    topic = message.topic
    
    # Define the expected topic for strict matching
    expected_topic = "EVZ_DPTH_02/status"

    # Check if the received topic strictly matches the expected topic
    if topic == expected_topic:
        print('topic matched')
        
        # Define the required fields
        required_fields = ['dp', 't', 'h']

        # Check if all required fields are present in the topic and message
        if all(field in value and field in value for field in required_fields):
            print("All required fields are present.")

            # Split the string into individual fields
            fields = value.split(',')

            # Initialize variables with default values
            dp_value = None
            t_value = None
            h_value = None

            # Iterate through the fields to find the values
            for field in fields:
                if 'dp' in field:
                    dp_parts = field.split(':')
                    if len(dp_parts) >= 2:
                        dp_value = dp_parts[1]  # Extract value after colon
                elif 't' in field:
                    t_parts = field.split(':')
                    if len(t_parts) >= 2:
                        t_value = t_parts[1]  # Extract value after colon
                elif 'h' in field:
                    h_parts = field.split(':')
                    if len(h_parts) >= 2:
                        h_value = h_parts[1]  # Extract value after colon

            # Validate data values before inserting
            if dp_value is not None and t_value is not None and h_value is not None:
                time = datetime.now()

                print('val',dp_value,t_value,h_value)
                query = "INSERT INTO dp_tm_hm (serial_no, dp_value, tm_value, hm_value, timestamp) VALUES (%s, %s, %s, %s, %s)"
                val = (topic, dp_value, t_value, h_value, time)
                
                # Execute the SQL query and commit the transaction
                cursor.execute(query, val)
                mydb.commit()
                
                print("Value inserted into the database.")
            else:
                print("Missing or invalid data values. Data not inserted.")

        else:
            print("Required fields are missing in the topic or message.")

    else:
        print('Topic does not match the expected topic for insertion.')


def subscribe(client):
    client.on_message = on_message 
    print("inside subscribe") 
    # client.subscribe("EVZ_DPTH_02/status")
    client.subscribe("#")
    
   
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()