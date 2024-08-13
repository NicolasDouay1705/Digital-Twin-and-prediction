import paho.mqtt.client as mqtt
import json
import threading
import pandas as pd

# import paho.mqtt.client as mqtt
# import json
# import threading
# import os
# import shutil
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset, Dataset
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.feature_selection import SelectFromModel
# from sklearn.preprocessing import MinMaxScaler, StandardScaler
# from sklearn.feature_selection import SelectFromModel
# from sklearn.ensemble import RandomForestClassifier
# from tensorflow import keras
# from tensorflow.keras import layers
# from tensorflow.keras.layers import Dense, LSTM, BatchNormalization, Dropout
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error

class DigitalTwin:
    def __init__(self, broker_address, port, thing_id):
        self.broker_address = broker_address
        self.port = port
        self.thing_id = thing_id
        self.base_topic = f"devices/{thing_id}"
        self.command_topic = self.base_topic  
        self.response_topic = self.base_topic
        
        self.voltage = None
        self.current = None
        self.capacity = None
        self.stock_value = pd.DataFrame(columns=["Voltage", "Current", "Capacity"])

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.prediction_model = None

        self.connected_event = threading.Event()

    def connect(self):
        try:
            self.client.connect(self.broker_address, self.port)
            self.client.loop_start()
        except Exception as e:
            print(f"Erreur lors de la connexion au broker : {e}")

    def disconnect(self):
        try:
            self.client.unsubscribe(self.response_topic)
            self.client.loop_stop()
            self.client.disconnect()
            print("Déconnexion réussie")
        except Exception as e:
            print(f"Erreur lors de la déconnexion du broker : {e}")

    def publish_message(self, message):
        try:
            message["header"] = {"reply-to": self.response_topic}
            json_message = json.dumps(message)
            print("Message à envoyer : " + json_message)
            self.client.publish(self.command_topic, json_message, qos=1)
            print("Message publié")
        except Exception as e:
            print(f"Erreur lors de l'envoi du message : {e}")

    def on_connect(self, client, userdata, flags, rc):
        try:
            print("Connexion au broker MQTT établie avec le code : " + str(rc))
            print(f"S'abonner au topic de réponse : {self.response_topic}")
            self.client.subscribe(self.response_topic)
            self.connected_event.set()
            self.get_features()
        except Exception as e:
            print(f"Erreur lors de la connexion : {e}")

    def on_message(self, client, userdata, msg):
        try:
            print("Message reçu sur le topic " + msg.topic + " : " + str(msg.payload.decode()))
            if msg.topic == self.response_topic:
                self.handle_response(msg.payload.decode())
        except Exception as e:
            print(f"Erreur lors de la réception du message : {e}")

    def handle_response(self, payload):
        try:
            response = json.loads(payload)

            print("Réponse JSON :", response)

            if response.get("topic") == "battery.prediction/hivelab/things/twin/commands/retrieve":
                
                self.voltage = response.get("voltage", None)
                self.current = response.get("current", None)
                self.capacity = response.get("capacity", None)

                self.voltage = response.get('value', {}).get('Voltage', {}).get('properties', {}).get('value', None)
                self.current = response.get('value', {}).get('Current', {}).get('properties', {}).get('value', None)
                self.capacity = response.get('value', {}).get('Capacity', {}).get('properties', {}).get('value', None)

                
                if self.voltage is not None:
                    print(f"Valeur de la tension : {self.voltage}")
                else:
                    print("tension non trouvée dans la réponse.")

                if self.current is not None:
                    print(f"Valeur du courant : {self.current}")
                else:
                    print("courant non trouvé dans la réponse.")

                if self.capacity is not None:
                    print(f"Valeur de la capacité : {self.capacity}")
                else:
                    print("capacité non trouvée dans la réponse.")
            
            else:
                print("Mauvaise Réponse")

        except Exception as e:
            print(f"Erreur lors du traitement de la réponse : {e}")

    def on_publish(self, client, userdata, mid):
        print("Message publié avec succès avec l'ID : " + str(mid))

    def update_features(self, voltage=None, current=None, capacity=None):
        try:
            # Mettre à jour les attributs locaux
            if voltage is not None:
                self.voltage = voltage
            if current is not None:
                self.current = current
            if capacity is not None:
                self.capacity = capacity
            
            # Créer le message de mise à jour des features
            message = {
                "thingId": self.thing_id,
                "command": "modify",
                "voltage": self.voltage,
                "current": self.current,
                "capacity": self.capacity,
            }
            
            # Publier le message de mise à jour
            self.publish_message(message)
        except Exception as e:
            print(f"Erreur lors de la mise à jour des features : {e}")
    
    def get_features(self):
        try:
            message = {
                "thingId": self.thing_id,
                "command": "retrieve"
            }
            self.publish_message(message)
            new_row = pd.DataFrame([{
                "Voltage": self.voltage,
                "Current": self.current,
                "Capacity": self.capacity
            }])
            self.stock_value = pd.concat([self.stock_value, new_row], ignore_index= True)
        except Exception as e:
            print(f"Erreur lors de la demande des features : {e}")