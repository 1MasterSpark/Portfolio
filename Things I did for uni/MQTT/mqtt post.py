import paho.mqtt.client as mqtt_client
import random
import time

broker = 'rule28.i4t.swin.edu.au'
port = 1883
topic1 = "103994313/test"
topic2 = "public/#"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
username = '103994313'
password = '103994313'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

    # Subscribe to the public topic
    client.subscribe("public/#")

    return client

def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic1, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Sent `{msg}` to topic1 `{topic1}`")
        else:
            print(f"Failed to send message to topic1 {topic1}")
        if status == 0:
            print(f"Sent `{msg}` to topic2 `{topic2}`")
        else:
            print(f"Failed to send message to topic1 {topic2}")
        msg_count += 1
        if msg_count > 5:
            break
        
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    client.subscribe(topic1)
    client.subscribe(topic2)
    publish(client)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    #client.loop_start()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()