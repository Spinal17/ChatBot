import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
from collections import Counter
from wordcloud import WordCloud
import nltk # importar el toolkit de NLP
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('stopwords')
import string
from nltk.stem import PorterStemmer 

data = pd.read_csv('C:/Users/Acer/Desktop/OneDrive_2_9-3-2020/yelp_data122.csv',)
data_copia = data.copy()
x = [f.split(" + -") for f in data_copia['DatosAdquiridos']]
lista2 = data_copia['Preguntas'] = [x[c][0] for c in range(len(x))]
lista3 = data_copia['Respuesta'] = [x[c][1] for c in range(len(x))]
data_copia = data_copia.drop(columns=['DatosAdquiridos']).copy()
lista2 = [x for x in data_copia['Preguntas']]
lista3 = [x for x in data_copia['Respuesta']]
with open("prueba.json") as archivo:
	datos = json.load(archivo)
contador = 0
for d in range(len(x)):
	contador = contador + 1
	datos['contenido'].append({
    'tag': "conador" + str(contador),
    'patrones': [x[d][0]],
    'respuestas': [x[d][1]]
    })
with open("prueba.json", 'w') as file:
	json.dump(datos,file)   

word_cloud_text = ''.join(data_copia['Preguntas'])
tokenized_words = nltk.word_tokenize(word_cloud_text)
palabrasL = []

for j in tokenized_words:
    palabrasL.append(j.lower().lstrip("¿"))
    
palabrasL.remove(",")
palabrasL.remove("?")

ord_cloud_text = ' '.join(palabrasL)
tokenized_words = nltk.word_tokenize(ord_cloud_text)

# Definiendo las stop words
stopwords = stopwords.words('spanish')

# Removiendo las stop words
word_tokens_clean = [word for word in tokenized_words if word.lower() not in stopwords and len(word.lower()) > 2]
Spera = nltk.word_tokenize(wor)
word_freq = Counter(Spera)
word_freq.most_common()