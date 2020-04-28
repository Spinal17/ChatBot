#Codigo Extraido de pagina de youtube
#Nombre del Canal: Cursos y asesorías de programación
#Nombre del deuño del canal: Miguel Islas Hernández
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow
import json
import getpass
import random
import pickle
from pymongo import MongoClient
import plotly
import bcrypt
import sys
from sklearn.model_selection import GridSearchCV
	 
def bot(NombreCom, idUsu):
	MongoURL = 'mongodb://localhost'
	client = MongoClient(MongoURL)
	db = client['base']	
	colletion = db['Informacion']

	datos = colletion.find_one()
	# with open("prueba.json") as archivo:
	# 	datos = json.load(archivo)
	try:
		with open("variables.pickle","rb") as archivoPickle:
			palabras, tags, entrenamiento, salida = pickle.load(archivoPickle)
	except:		
		palabras = []
		tags=[]
		auxX=[]
		auxY=[]

		for contenido in datos["contenido"]:
			for patrones in contenido["patrones"]:
				auxPalabra = nltk.word_tokenize(patrones)
				palabras.extend(auxPalabra)
				auxX.append(auxPalabra)
				auxY.append(contenido["tag"])	

				if contenido["tag"] not in tags:
					tags.append(contenido["tag"])

		#ALGORITMO DE LA CUBETA

		palabras = [stemmer.stem(w.lower()) for w in palabras if w !="?"]
		palabras= sorted(list(set(palabras)))
		tags = sorted(tags)

		entrenamiento = []
		salida = []
		salidaVacia = [ 0 for _ in range(len(tags))]

		for x, documento in enumerate(auxX):
			cubeta = []
			auxPalabra = [stemmer.stem(w.lower()) for w in documento]
			for w in palabras:
				if w in auxPalabra:
					cubeta.append(1)
				else:
					cubeta.append(0)
			filaSalida = salidaVacia[:]
			filaSalida[tags.index(auxY[x])]	= 1
			entrenamiento.append(cubeta)
			salida.append(filaSalida)
		# print(entrenamiento)
		# print(salida)
		#RED NEURNAL
		entrenamiento = numpy.array(entrenamiento)
		salida = numpy.array(salida)
		with open("variables.pickle", "wb") as archivoPickle:
			pickle.dump((palabras, tags, entrenamiento,salida), archivoPickle)

	tensorflow.reset_default_graph()
	red = tflearn.input_data(shape=[None,len(entrenamiento[0])])
	#columnas de neuronas 
	red = tflearn.fully_connected(red,10)
	red = tflearn.fully_connected(red,10)
	red = tflearn.fully_connected(red,len(salida[0]),activation = "softmax")
	red = tflearn.regression(red)
	modelo = tflearn.DNN(red)
	# param={"kernel":"linear",
	# "c":[30,80,100,120],
	# "degree":[3,8,10,20],
	# "coef0":[0.001,10,0.5],
	# "gamma":("auto","scale")
	# }
	# grids = GridSearchCV(modelo,param,cv=5)
	# grids.fit(entrenamiento,salida)
	# grids.best_params_
	try:
		modelo.load("modelo.tflearn")
	except:
		modelo.fit(entrenamiento,salida,n_epoch=1000,batch_size=10,show_metric=True)
		modelo.save("modelo.tflearn")

	def mainBot():
		print("===============================================================================")
		Entrada = "g"
		print("Si deseas salir ingresa 0")
		while Entrada != "0":
			Entrada = input(NombreCom + ": ")
			print()
			if Entrada != "0":
				cubeta = [0 for _ in range(len(palabras))]
				entradaProcesada = nltk.word_tokenize(Entrada)
				entradaProcesada = [stemmer.stem(palabra.lower()) for palabra in entradaProcesada]
				for palabraindi in entradaProcesada:
					for i,palabra in enumerate(palabras):
						if palabra == palabraindi:
							cubeta[i] = 1
				resultados = modelo.predict([numpy.array(cubeta)])			
				resultadosIndices = numpy.argmax(resultados)
				tag = tags[resultadosIndices]
				
				for tagAux in datos["contenido"]:
					if tagAux["tag"] == tag:
						respuesta = tagAux["respuestas"]
				print("Bot: ", random.choice(respuesta))
				print()
			else:
				print("Bot: Adios")
				print("===============================================================================")
				ComentariosUsu = input("Porfavor ingresa un comentario de tu experiencia con el bot \n (ingresa NA si no quieres colocar comentario): ")			
				d = False
				while d != True:
					Estrellas = input("ingresa de 1-5 (1 es la peor y 5 es excelente): ")
					if Estrellas != "1" and Estrellas != "2" and Estrellas != "3" and Estrellas != "4" and Estrellas != "5":
						print("Dato incorrecto, nuelve a intentar")
						d= False
					else:
						d = True
						colletion2 = db['Comentarios']
						colletion2.insert_one({
								"_id" : idUsu,
								"Nombre": NombreCom,
								"Comentario": ComentariosUsu,
								"Estrellas": Estrellas
							})
						print("===============================================================================")
						print("Graicas por utilizar el chat")
						print("===============================================================================")

		Menu()	
	mainBot()
def registro():
	cc = True
	MongoURL = 'mongodb://localhost'
	client = MongoClient(MongoURL)
	db = client['base']	
	colletion = db['Login']
	print("===============================================================================")
	print("Bienvenido al registo")
	print("===============================================================================")
	while cc:
		results = colletion.find()
		verificar = 0
		Nombre = input("Ingresa tu nombre: ")
		for r in results:
			if r["Nombre"] == Nombre:
				verificar = verificar + 2
		if verificar > 0:
			print("Ya exsiste este Usuario")
			cc = True
		else:
			cc = False 	
	Apellido = input("Ingresa tu apellido: ")
	Email = input("Ingresa tu Email: ")
	Password = getpass.getpass("Ingresa tu contraseña: ")
	PassCrypt = Password.encode()
	semilla = bcrypt.gensalt()
	textoFinal = bcrypt.hashpw(PassCrypt,semilla)

	colletion.insert_one({
		"Nombre" : Nombre,
		 "Apellido" : Apellido,
		 "Email" : Email,
		 "Password" : textoFinal
		 })
	print("===============================================================================")
	print("Usuario ya creado")
	print("===============================================================================")
	Menu()
def login():
	MongoURL = 'mongodb://localhost'
	client = MongoClient(MongoURL)
	db = client['base']	
	colletion = db['Login']
	print("===============================================================================")
	print("Bienvenido al login")
	print("===============================================================================")
	x = True
	while x:
		try:
			Nombre = input("Ingresa tu nombre: ")
			Password = getpass.getpass("Ingresa tu contraseña: ")
			x = False
		except Exception as e:
			print("Error en los datos intenta otra vez")
			print()
			salidae = input("Si queires salir ingresa 0: ")
			if salidae == "0":
				Menu()
			x = True
		
	PassCrypt = Password.encode()
	results = colletion.find({"Nombre": Nombre})
	contador = 1
	for r in results:
		if r["Nombre"] == Nombre and bcrypt.checkpw(PassCrypt,r["Password"]):
			NombreCompleto = Nombre +" " +  r["Apellido"]
			print("===============================================================================")
			print("Bienvenido " + NombreCompleto)
			print("===============================================================================")
			bot(NombreCompleto, r["_id"])
		else:
			contador = contador + 1

	if contador > 0:
		print("===============================================================================")
		print("Error, vuelva a intertarlo")
		print("===============================================================================")
		login()	
def cerrar():
    print("===============================================================================")
    print()
    print("Gracias por utilizar el programa")
    print()
    print("===============================================================================")
    sys.exit()
def Menu():
    print("===============================================================================")
    print("Ingresa 1 para entrar al login")
    print("Ingresa 2 para registarte")
    print("Ingresa 3 para salir")
    print("===============================================================================")

    f = True
    while f:
        uno = input('--->')
        if uno == "1":
            login()
            f = False
        elif uno == "2":
            registro()
            f = False
        elif uno == "3":
            cerrar()
            f = False
        else:
            print('dato no valido')
            f = True

Menu()
