import paho.mqtt.client as mqtt_client
import random
import time

broker = 'localhost'
port = 8883
topic1 = "103994313/test"
topic2 = "public/m"
# Generate a Client ID with the publish prefix.
client_id = f'thirdthing-{random.randint(0, 1000)}'
# username = '103994313'
# password = '103994313'

# Callback when a message is received
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

    if msg.topic == topic1 and msg.payload.decode() == "messages: 5":
        try:
            client.publish(topic1, "Test successful")
        except ValueError:
            print("Invalid temperature value in message.")

def connect_mqtt() -> mqtt_client.Client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_message = on_message
    # client.username_pw_set(username, password)
    client.tls_set(
        ca_certs="fullchain.crt",
        certfile="leaf3.crt",
        keyfile="leaf3.key")
    client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.connect(broker, port)

    while True:
        choice = input("\nChoose which topic to subscribe to: [1 = test, 2 = m, 0 = finish]")
        if choice == "1":
            client.subscribe(topic1)
        elif choice == "2":
            client.subscribe(topic2)
        elif choice == "0":
            break
        else:
            print("Error: Invalid input")

    client.loop_start()

    try:
        while True:
            time.sleep(1)
            topic = input("\nEnter the topic to publish to: [1 = test, 2 = m]")
            if topic == "1":
                topic = topic1
            elif topic == "2":
                topic = topic2
            message = input("Enter the message: ")
            client.publish(topic, message)
            print(f"Published message '{message}' to topic '{topic}'")
    except KeyboardInterrupt:
        print("Exiting...")

    client.loop_stop()
    client.disconnect()

def run():
    client = connect_mqtt()
    #client.loop_start()
    client.loop_forever()

if __name__ == '__main__':
    run()