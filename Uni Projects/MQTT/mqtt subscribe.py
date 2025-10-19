import random
from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 8883
topic1 = "103994313/#"
topic2 = "public/#"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = '103994313'
# password = '103994313'
ca_cert = "/home/spark/Uni/TNE30024/MQTT/mosquitto/ca_certificates/ca.crt"

def connect_mqtt() -> mqtt_client.Client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    # client.username_pw_set(username, password)
    client.tls_set(
        ca_certs="/home/spark/Uni/TNE30024/MQTT/fullchain.crt",
        certfile="/home/spark/Uni/TNE30024/MQTT/leaf1.crt",
        keyfile="/home/spark/Uni/TNE30024/MQTT/leaf1.key")
    client.tls_insecure_set(True)
    client.on_connect = on_connect

    try:
        client.connect(broker, port)
    except Exception as e:
        print(f"Connection failed: {e}")
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    
    client.subscribe(topic1)
    client.subscribe(topic2)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()