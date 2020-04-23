# -*- coding: utf-8 -*-
from pymongo import MongoClient
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

database ='mongodb://localhost:27017/PrototipoDB'

client = MongoClient(database)

db = client['PrototipoDB']
collection = db['data_copia']

total = collection.count_documents({})
print(total)

train = []
resultados = collection.find()
for r in resultados:
    train.append(r['Preguntas'])
    train.append(r['Respuestas'])

chatbot = ChatBot('RobotUPB')

trainer = ListTrainer(chatbot)
trainer.train(train[:1024 * 8])

while True:
    Pregunta = input('You: ')
    respuesta = chatbot.get_response(Pregunta)
    print('RobotUPB: ', respuesta)