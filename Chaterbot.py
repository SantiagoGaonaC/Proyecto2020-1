from pymongo import MongoClient
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.conversation import Statement
from chatterbot.comparisons import JaccardSimilarity
import bcrypt
import os


def borrarPantalla():
    #Definimos la función estableciendo el nombre que queramos
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

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
    
    chatbot = ChatBot(
    'RobotUPB',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    #database_uri='mongodb://localhost:27017/PrototipoDB',
    #database='./database.sqlite', #./database.sqlite5 fichero de la base de datos (si no existe se creará automáticamente)

    input_adapter='chatterbot.input.TerminalAdapter', #indica que la pregunta se toma del terminal
    output_adapter='chatterbot.output.TerminalAdapter', #indeica que la respuesta se saca por el terminal
    output_format="text",
    trainer='chatterbot.trainers.ListTrainer',
    
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        'chatterbot.logic.MathematicalEvaluation',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Lo siento pero no entiendo..',
            'maximum_similarity_threshold': 1
        },
    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
)
    treiner = ChatterBotCorpusTrainer(chatbot)
    treiner2 = ListTrainer(chatbot)
    treiner.train("./PreguntasYRespuestas.yml")
    #treiner.train("chatterbot.corpus.spanish")
    levenshtein_distance = LevenshteinDistance()
    disparate=Statement('Mal')#convertimos una frase en un tipo statement
    entradaDelUsuario="" #variable que contendrá lo que haya escrito el usuario
    entradaDelUsuarioAnterior=""
    while entradaDelUsuario!="adios":
        borrarPantalla()
        entradaDelUsuario = input(">>>")
        if entradaDelUsuario == '':
            print('escribe algo por favor!')
        else:
            respuesta = chatbot.get_response(Statement(entradaDelUsuario))
            print('Bot:'+str(respuesta))
        if levenshtein_distance.compare(Statement(entradaDelUsuario),Statement(disparate))>0.51:
            print('¿Qué debería haber dicho?')
            entradaDelUsuarioCorrecta = input(">>>")
            treiner2.train([entradaDelUsuarioAnterior,entradaDelUsuarioCorrecta])
            print("He aprendiendo que cuando digas {} debo responder {}".format(entradaDelUsuarioAnterior,entradaDelUsuarioCorrecta))
        entradaDelUsuarioAnterior=entradaDelUsuario
        #print("\n%s\n\n" % respuesta) # IMPRESIÓN

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
            
            break
        elif opcion_menu == "4":
            print("Saliendo...")
            break
        else:
            print("")
            input("No has pulsado ninguna opción correcta...\nPulsa una tecla para continuar")
            
menu()
cantidad_bd()