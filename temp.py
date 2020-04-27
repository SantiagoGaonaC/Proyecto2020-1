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
    print("Cantidad de cuentas usuario: ",total_login)
    collection = bd_data_copia()
    total_collection = collection.count_documents({})
    print("Cantidad de datos bd_copia: ",total_collection)

    
def chat_admin(): ####################### C H A T ###################################
    
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
    disparate=Statement('Mala Respuesta')#convertimos una frase en un tipo statement
    entradaDelUsuario="" #variable que contendrá lo que haya escrito el usuario
    entradaDelUsuarioAnterior=""
    print("***Recuerda: para corregir una PQRS escribe >>> Mala Respuesta <<< y >>> adios <<< para salir.")
    while entradaDelUsuario!="adios":
        entradaDelUsuario = input(">>> ")
        if entradaDelUsuario == '':
            print('Digiste un algo')
        else:
            respuesta = chatbot.get_response(Statement(entradaDelUsuario))
            print('Bot:'+str(respuesta))
        if levenshtein_distance.compare(Statement(entradaDelUsuario),Statement(disparate))>0.51:
            print('¿Qué debería haber dicho?')
            entradaDelUsuarioCorrecta = input(">>> ")
            treiner2.train([entradaDelUsuarioAnterior,entradaDelUsuarioCorrecta])
            print("He aprendiendo que cuando digas: {}. Debo responder: {}".format(entradaDelUsuarioAnterior,entradaDelUsuarioCorrecta))
        entradaDelUsuarioAnterior=entradaDelUsuario
        #print("\n%s\n\n" % respuesta) # IMPRESIÓN
        
def chat_users():
    bd_data_copia()
    stats = bd_data_copia()
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
    
    #disparate=Statement('Mal')#convertimos una frase en un tipo statement
    
    entradaDelUsuario="" #variable que contendrá lo que haya escrito el usuario
    entradaDelUsuarioAnterior=""
    print("***Recuerda, escribe >>> adios <<< para salir del ChatBot***")
    while entradaDelUsuario!="adios":
        entradaDelUsuario = input(">>> ")
        if entradaDelUsuario == '':
            print('Digite su PQRS!')
        else:
            respuesta = chatbot.get_response(Statement(entradaDelUsuario))
            print('ChatBotUPB:'+str(respuesta))
            stats.insert_one({"pqrs_usuario": entradaDelUsuario, "respuesta_pqrs": str(respuesta)})
                      
        # if levenshtein_distance.compare(Statement(entradaDelUsuario),Statement(disparate))>0.51:
        #     print('¿Qué debería haber dicho?')
        #     entradaDelUsuarioCorrecta = input(">>>")
        #     treiner2.train([entradaDelUsuarioAnterior,entradaDelUsuarioCorrecta])
        #     print("He aprendiendo que cuando digas {} debo responder {}".format(entradaDelUsuarioAnterior,entradaDelUsuarioCorrecta))
        # entradaDelUsuarioAnterior=entradaDelUsuario
        # #print("\n%s\n\n" % respuesta) # IMPRESIÓN
    
def registro_users():
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
    
def registro_admin():
    bd_connection()
    login = bd_connection()
    print("\nIngrese usuario y contraseña para el registro: ")
    user = input("Ingrese su nombre y apellido: ")
    password = input("Ingrese contraseña: ")
    password = password.encode() 
    contra = bcrypt.gensalt() #SEMILLA
    pass_hash = bcrypt.hashpw(password, contra)
    login.insert_one({"user_admin": user, "pass_admin": pass_hash})
    print("Admin registrado correctamente")
        
def ingreso_users():
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
                
                chat_users()
                
            else:
                print("INCORRECTOOOO")
                break
            
def ingreso_admin():
    bd_connection()
    login = bd_connection()
    usuario = input("Ingrese el nombre de usuario del admin: ")
    resultado = login.find({"user_admin": usuario})
    if len(list(resultado)) == 0: #################
        print("Administrador no encontrado...")
    else:
        print("Existe el usuario " + usuario + ", Por favor, ingrese la contraseña Admin: ")
        pass_user = input("\n>>> ")                
        semillaa = pass_user.encode()
        resultado = login.find({"user_admin": usuario})
        for i in resultado:
            if i["user_admin"] == usuario and bcrypt.checkpw(semillaa,i["pass_admin"]):
                print("Existe el administrador\n Ahora contiene permisos de Administrador...")
                
                chat_admin() ########## A D M I N #############################
                
            else:
                print("Admin Incorrecto...")
                break

    
def menu():
    while True:
        print("\n1) Ingresar Usuarios")
        print("2) Registro Usuarios")
        print("3) Ingreso Admin")
        print("4) Salir")
        #print("5) Register Admin") # BORRRAAAARRRR
        opcion_menu = input("Inserta una opción: ")
        if opcion_menu == "1":
            ingreso_users()
            break
        elif opcion_menu == "2":
            registro_users()
        elif opcion_menu == "3":
            ingreso_admin()
            break
        elif opcion_menu == "4":
            print("Saliendo...")
            break
        #elif opcion_menu == "5":
            #registro_admin()
        else:
            print("")
            input("No has pulsado ninguna opción correcta...\nPulsa una tecla para continuar")
            
menu()
cantidad_bd()