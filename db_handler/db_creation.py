from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://amanitarar:lFomSlznEeQ3kkRQ@amanita.onbcb.mongodb.net/?retryWrites=true&w=majority&appName=Amanita"
# Create a new client and connect to the server
client = MongoClient(uri,tls=True, tlsAllowInvalidCertificates=True, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
db = client["amanitauserdb"]  # Создание или подключение к базе данных
collection = db["Users"]  # Создание или подключение к коллекции

