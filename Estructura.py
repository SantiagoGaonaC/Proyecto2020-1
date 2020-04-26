from pymongo import MongoClient
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import bcrypt


def bd_connection(): #registros
    database ='mongodb://localhost:27017/PrototipoDB'
    client = MongoClient(database)
    db = client['PrototipoDB']
    login = db['login']   
    return login

def bd_data_copia(): #preguntas respuestas
    database ='mongodb://localhost:27017/PrototipoDB'
    client = MongoClient(database)
    db = client['PrototipoDB']
    collection = db['data_copia']
    return collection
    
def cantidad_bd(): #VER CIFRAS
    
    bd_connection()
    login = bd_connection()
    total_login = login.count_documents({})  
    print("Cantidad de datos: ",total_login)
    collection = bd_data_copia()
    total_collection = collection.count_documents({})
    print("Cantidad de datos: ",total_collection) 
    
    
    
def chat(): ####################### C H A T ###################################
    

    collection = bd_data_copia()
    chatbot = ChatBot('RobotUPB') #Asignación nombre Robot
    train = []
    resultados = collection.find()
    for r in resultados:
        train.append(r['Preguntas'])
        train.append(r['Respuestas'])
    # chatbot = ChatBot('RobotUPB')
    trainer = ListTrainer(chatbot)
    trainer.train(train[:1024])
    
    
    
    
    while True:
        Pregunta = input('Tu: ')
        respuesta = chatbot.get_response(Pregunta)
        print('RobotUPB: ', respuesta)
        #break
        
        
def registro():
    bd_connection()
    login = bd_connection()
    print("\nIngrese usuario y contraseña para el registro: ")
    user = input("Ingrese su nombre y apellido: ")
    password = input("Ingrese contraseña: ")
    password = password.encode() 
    contra = bcrypt.gensalt() #SEMILLA
    pass_hash = bcrypt.hashpw(password, contra)
    login.insert_one({"usuario": user, "contraseña": pass_hash})
    print("Usuario registrado correctamente")
    # info = login.find()
    # for r in info:
    #     print(r)
        
def ingreso():
    bd_connection()
    login = bd_connection()
    usuario = input("Ingrese su usuario: ")
    resultado = login.find({"usuario": usuario})
    if len(list(resultado)) == 0: #################
        print("Usuario no encontrado...")
    else:
        print("EXISTE EL USUARIO")
        pass_user = input("\nIngrese su contraseña: ")                
        semillaa = pass_user.encode()
        resultado = login.find({"usuario": usuario})
        for i in resultado:
            if i["usuario"] == usuario and bcrypt.checkpw(semillaa,i["contraseña"]):
                print("CORRECTOOOO")
                
                chat()
                
            else:
                print("INCORRECTOOOO")
                break
            
def menu():
    while True:
        print("\n1) Ingresar")
        print("2) Registrarse")
        print("3) Salir")
        opcion_menu = input("Inserta una opción: ")
        if opcion_menu == "1":
            ingreso()
            break
        elif opcion_menu == "2":
            registro()
            break
        elif opcion_menu == "3":
            print("Saliendo...")
            break
        else:
            print("")
            input("No has pulsado ninguna opción correcta...\nPulsa una tecla para continuar")
            
menu()
cantidad_bd()