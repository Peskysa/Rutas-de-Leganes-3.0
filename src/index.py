#-------------------------------------------------------------------------------#
#--------------------------CALCULA RUTA ENTRE PUNTOS ---------------------------#
#-------------------------------------------------------------------------------#


import os  
import pandas as pd
from todas_clases.clase1_direcciones import Direcciones_coordenadas_API_Google
from todas_clases.clase2_mapas import Mapa
from flask import Flask, render_template, request
import googlemaps
from datetime import datetime, timedelta 
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans 

#os.chdir("C:\\GITHUB\\apli_web\\src") # ejecutar en carpeta completa
os.getcwd()

clave_google = 'API' 

origin = "Av. de Fuenlabrada, 2, 28912 Leganés, Madrid"   
destination = "Av. de Fuenlabrada, 2, 28912 Leganés, Madrid"
# para rutas en leganes poner el centro de leganes
center = "Poligono 5 de Rustica, 95, 28918 Leganés, Madrid"
nº_camiones = 8
que_datos = 70


if que_datos == 25:
    # lee datos
    datos_excel = pd.read_excel('src\static\dire_25.xlsx') 
elif que_datos == 70:  
    datos_excel = pd.read_excel('src\static\dire_70.xlsx') 

# saca coordenadas
coordenadas = Direcciones_coordenadas_API_Google(datos_excel,clave_google)   
resultado_apy = coordenadas.coordenadas_API_Google() 
# crea mapa interactivo
columnas = ['lat', 'lon'] # definimos los nombres de las columnas
df1 = pd.DataFrame(resultado_apy, columns=columnas, index=None)
crea_html = Mapa(df1)
crea_html.mapa_con_puntos()

df_segundo = pd.DataFrame(resultado_apy)
columnas2 = ['Latitud', 'Longitud'] # definimos los nombres de las columnas
df2 = pd.DataFrame(resultado_apy, columns=columnas2, index=None)
# escribir el DataFrame en excel
excel = pd.ExcelWriter('src\static\elquesea.xlsx')
df2.to_excel(excel)
# guardar el excel
excel.save()
# leer el generado
df = pd.read_excel('src\static\elquesea.xlsx') 
#································································
df.plot.scatter(x='Longitud',  y='Latitud', c='DarkGreen')

plt.grid("--")
plt.title("Todos los puntos")
#plt.show()
plt.savefig('src\static\grafico.png')
#......................................................................
# Normalizamos los datos
min_max_scaler = MinMaxScaler() 
df = min_max_scaler.fit_transform(df)
df = pd.DataFrame(df) # Convertimos a Dataframe
#print(df.head())
# Aplicamos k-means a nuestro dataset
km = KMeans(n_clusters=nº_camiones, init='random', 
            max_iter=200, random_state=0)
y_km = km.fit_predict(df)
# Gráfico con los puntos y su cluster y los centroides
plt.figure(figsize=(9,9))
plt.scatter(df[y_km == 0][0], df[y_km == 0][1], 
            s=50, c='green', marker='o', 
            edgecolor='black', label='cluster 1')
plt.scatter(df[y_km == 1][0], df[y_km == 1][1],  
            s=50, c='orange', marker='s', 
            edgecolor='black', label='cluster 2')
plt.scatter(df[y_km == 2][0], df[y_km == 2][1], 
            s=50, c='lightblue', marker='v', 
            edgecolor='black', label='cluster 3')
plt.scatter(df[y_km == 3][0], df[y_km == 3][1], 
            s=50, c='purple', marker='d', 
            edgecolor='black', label='cluster 4')
plt.scatter(df[y_km == 4][0], df[y_km == 4][1], 
            s=50, c='blue', marker='o', 
            edgecolor='black', label='cluster 5')
plt.scatter(df[y_km == 5][0], df[y_km == 5][1], 
            s=50, c='pink', marker='s', 
            edgecolor='black', label='cluster 6')
plt.scatter(df[y_km == 6][0], df[y_km == 6][1], 
            s=50, c='yellow', marker='v', 
            edgecolor='black', label='cluster 7')
plt.scatter(df[y_km == 7][0], df[y_km == 7][1], 
            s=50, c='black', marker='d', 
            edgecolor='black', label='cluster 8')
"""plt.scatter(km.cluster_centers_[:, 0], 
            km.cluster_centers_[:, 1], s=400, 
            marker='*', c='red', 
            edgecolor='black', label='centroides')"""
plt.legend(loc="best")
plt.grid("--")
plt.title("Los puntos separados por rutas")
plt.savefig('src\static\cluster.png')

#  los datos normalizados a lista de coordenadas
if nº_camiones == 1:
    primer_cluster = df[y_km == 0]
    primer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(primer_cluster)
elif nº_camiones == 2:
    primer_cluster = df[y_km == 0]
    primer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(primer_cluster)
    segundo_cluster = df[y_km == 1]
    segundo_cluster_lista_coordenadas = min_max_scaler.inverse_transform(segundo_cluster)
elif nº_camiones == 3:
    primer_cluster = df[y_km == 0]
    primer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(primer_cluster)
    segundo_cluster = df[y_km == 1]
    segundo_cluster_lista_coordenadas = min_max_scaler.inverse_transform(segundo_cluster)
    tercer_cluster = df[y_km == 2]
    tercer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(tercer_cluster)
elif nº_camiones == 4:
    primer_cluster = df[y_km == 0]
    primer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(primer_cluster)
    segundo_cluster = df[y_km == 1]
    segundo_cluster_lista_coordenadas = min_max_scaler.inverse_transform(segundo_cluster)
    tercer_cluster = df[y_km == 2]
    tercer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(tercer_cluster)
    cuarto_cluster = df[y_km == 3]
    cuarto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(cuarto_cluster)
elif nº_camiones == 5:
    primer_cluster = df[y_km == 0]
    primer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(primer_cluster)
    segundo_cluster = df[y_km == 1]
    segundo_cluster_lista_coordenadas = min_max_scaler.inverse_transform(segundo_cluster)
    tercer_cluster = df[y_km == 2]
    tercer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(tercer_cluster)
    cuarto_cluster = df[y_km == 3]
    cuarto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(cuarto_cluster)
    quinto_cluster = df[y_km == 4]
    quinto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(quinto_cluster)
elif nº_camiones == 6:
    primer_cluster = df[y_km == 0]
    primer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(primer_cluster)
    segundo_cluster = df[y_km == 1]
    segundo_cluster_lista_coordenadas = min_max_scaler.inverse_transform(segundo_cluster)
    tercer_cluster = df[y_km == 2]
    tercer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(tercer_cluster)
    cuarto_cluster = df[y_km == 3]
    cuarto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(cuarto_cluster)
    quinto_cluster = df[y_km == 4]
    quinto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(quinto_cluster)
    sexto_cluster = df[y_km == 5]
    sexto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(sexto_cluster)
elif nº_camiones == 7:
    primer_cluster = df[y_km == 0]
    primer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(primer_cluster)
    segundo_cluster = df[y_km == 1]
    segundo_cluster_lista_coordenadas = min_max_scaler.inverse_transform(segundo_cluster)
    tercer_cluster = df[y_km == 2]
    tercer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(tercer_cluster)
    cuarto_cluster = df[y_km == 3]
    cuarto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(cuarto_cluster)
    quinto_cluster = df[y_km == 4]
    quinto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(quinto_cluster)
    sexto_cluster = df[y_km == 5]
    sexto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(sexto_cluster)
    septimo_cluster = df[y_km == 6]
    septimo_cluster_lista_coordenadas = min_max_scaler.inverse_transform(septimo_cluster)
elif nº_camiones == 8:
    primer_cluster = df[y_km == 0]
    primer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(primer_cluster)
    segundo_cluster = df[y_km == 1]
    segundo_cluster_lista_coordenadas = min_max_scaler.inverse_transform(segundo_cluster)
    tercer_cluster = df[y_km == 2]
    tercer_cluster_lista_coordenadas = min_max_scaler.inverse_transform(tercer_cluster)
    cuarto_cluster = df[y_km == 3]
    cuarto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(cuarto_cluster)
    quinto_cluster = df[y_km == 4]
    quinto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(quinto_cluster)
    sexto_cluster = df[y_km == 5]
    sexto_cluster_lista_coordenadas = min_max_scaler.inverse_transform(sexto_cluster)
    septimo_cluster = df[y_km == 6]
    septimo_cluster_lista_coordenadas = min_max_scaler.inverse_transform(septimo_cluster)
    octavo_cluster = df[y_km == 7]
    octavo_cluster_lista_coordenadas = min_max_scaler.inverse_transform(octavo_cluster)


def imprime_r(cluster,lista):
        gmaps = googlemaps.Client(key=clave_google)
        for i in cluster:
            i.pop(0)    
        pp=[]
        for i in cluster:
            for j in i:
                pp.append(str(j))
        hhh=[]
        par=0
        impar=1
        contador =(len(pp))
        contador = int(contador/2)
        for i in range(contador):
            hhh.append(pp[par]+","+pp[impar])  
            par = par+2
            impar = impar+2
        lista_coordenadas= []
        lista_tiempo = []
        lista_distancia = []
        for i in hhh:
            geocode_result = gmaps.geocode(i)
            lista_coordenadas.append(geocode_result[0]["formatted_address"]) 
            
        results = gmaps.directions(
                                origin = "Av. de Fuenlabrada, 2, 28912 Leganés, Madrid",    
                                destination = "Av. de Fuenlabrada, 2, 28912 Leganés, Madrid",              
                                                                                    
                                waypoints = lista_coordenadas,
                                optimize_waypoints = True,
                                departure_time=datetime.now() + timedelta(hours=1))
        ruta_total_str=[]           
        for i, leg in enumerate(results[0]["legs"]):
                            lista_tiempo.append(leg["duration"]["text"]) 
                            lista_distancia.append(leg["distance"]["text"])                  
                            ruta_total_str.append(
                            "Parada: {0} || {1} ==> {2} || Distancia: {3} || Tiempo: {4}".format(                
                                str(i),leg["start_address"],leg["end_address"],leg["distance"]["text"],leg["duration"]["text"]))
        #l_ruta_total.clear()
        for i in ruta_total_str:
            lista.append(i)            
            #print(i)
        return [lista_tiempo,lista_distancia]

wp = datos_excel["direcciones"].tolist()

def pinta_mapa(wp):
        wpy=[]
        for i in wp:
            wpy.append(i[1:3])    
        gmaps = googlemaps.Client(key=clave_google)

        results = gmaps.directions(
                                origin = origin,
                                destination = destination,                                     
                                waypoints = wpy,
                                optimize_waypoints = True,
                                departure_time=datetime.now() + timedelta(hours=1))
        marker_points = []
        waypoints = []
        for leg in  results[0]["legs"]:
                        leg_start_loc = leg["start_location"]
                        marker_points.append(f'{leg_start_loc["lat"]},{leg_start_loc["lng"]}')
                        for step in leg["steps"]:
                                end_loc = step["end_location"]
                                waypoints.append(f'{end_loc["lat"]},{end_loc["lng"]}')
        last_stop =   results[0]["legs"][-1]["end_location"]
        marker_points.append(f'{last_stop["lat"]},{last_stop["lng"]}')                        
        markers = [ "color:red|size:mid|label:" + chr(65+i) + "|" 
                                + r for i, r in enumerate(marker_points)]
        result_map = gmaps.static_map(
                                center = center,
                                scale=2, 
                                zoom=14,
                                size=[640, 640], 
                                format="jpg", 
                                maptype="roadmap",
                                markers=markers,
                                path="color:0xFF0000|weight:2|" + "|".join(waypoints))   
        return result_map                         

def saca_jpj():
    if nº_camiones == 1:
        with open('src\static\primeraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(primer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
    elif nº_camiones == 2:
        with open('src\static\primeraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(primer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\segundaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(segundo_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
    elif nº_camiones == 3:
        with open('src\static\primeraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(primer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\segundaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(segundo_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\\terceraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(tercer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
    elif nº_camiones == 4:
        with open('src\static\primeraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(primer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\segundaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(segundo_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\\terceraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(tercer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\cuartaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(cuarto_cluster_lista_coordenadas.tolist()):
                img.write(chunk)         
    elif nº_camiones == 5:
        with open('src\static\primeraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(primer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\segundaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(segundo_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\\terceraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(tercer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\cuartaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(cuarto_cluster_lista_coordenadas.tolist()):
                img.write(chunk) 
        with open('src\static\quintaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(quinto_cluster_lista_coordenadas.tolist()):
                img.write(chunk)  
    elif nº_camiones == 6:
        with open('src\static\primeraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(primer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\segundaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(segundo_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\\terceraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(tercer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\cuartaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(cuarto_cluster_lista_coordenadas.tolist()):
                img.write(chunk) 
        with open('src\static\quintaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(quinto_cluster_lista_coordenadas.tolist()):
                img.write(chunk)         
        with open('src\static\sextaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(sexto_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
    elif nº_camiones == 7:
        with open('src\static\primeraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(primer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\segundaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(segundo_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\\terceraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(tercer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\cuartaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(cuarto_cluster_lista_coordenadas.tolist()):
                img.write(chunk) 
        with open('src\static\quintaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(quinto_cluster_lista_coordenadas.tolist()):
                img.write(chunk)         
        with open('src\static\sextaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(sexto_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\septimaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(septimo_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
    elif nº_camiones == 8:
        with open('src\static\primeraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(primer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\segundaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(segundo_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\\terceraruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(tercer_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\cuartaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(cuarto_cluster_lista_coordenadas.tolist()):
                img.write(chunk) 
        with open('src\static\quintaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(quinto_cluster_lista_coordenadas.tolist()):
                img.write(chunk)         
        with open('src\static\sextaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(sexto_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\septimaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(septimo_cluster_lista_coordenadas.tolist()):
                img.write(chunk)
        with open('src\static\octabaruta.jpg', 'wb') as img:
            for chunk in pinta_mapa(octavo_cluster_lista_coordenadas.tolist()):
                img.write(chunk)

saca_jpj() 

def suma_tiempo(cluster):
    suma_t = [] 
    for i in cluster[0]:
        suma_t.append(int(i[0]))  
    suma_tiempos = 0
    for i in suma_t:
        suma_tiempos  += i
    return suma_tiempos 

def suma_distancia(cluster):
    suma_d = [] 
    for i in cluster[1]:
        suma_d.append(float(i[0:3]))  
    suma_distancias = 0
    for i in suma_d:
        suma_distancias  += i
    return suma_distancias 

if nº_camiones == 1:
    l_ruta_total1=[]
    uno = imprime_r(primer_cluster_lista_coordenadas.tolist(),l_ruta_total1)
    
elif nº_camiones == 2:
    l_ruta_total1=[]
    uno = imprime_r(primer_cluster_lista_coordenadas.tolist(),l_ruta_total1)
   
    l_ruta_total2=[]
    dos = imprime_r(segundo_cluster_lista_coordenadas.tolist(),l_ruta_total2)
 
elif nº_camiones == 3:
    l_ruta_total1=[]
    uno = imprime_r(primer_cluster_lista_coordenadas.tolist(),l_ruta_total1)
   
    l_ruta_total2=[]
    dos = imprime_r(segundo_cluster_lista_coordenadas.tolist(),l_ruta_total2)
  
    l_ruta_total3=[]
    tres = imprime_r(tercer_cluster_lista_coordenadas.tolist(),l_ruta_total3)
  
elif nº_camiones == 4:
    l_ruta_total1=[]
    uno = imprime_r(primer_cluster_lista_coordenadas.tolist(),l_ruta_total1)
  
    l_ruta_total2=[]
    dos = imprime_r(segundo_cluster_lista_coordenadas.tolist(),l_ruta_total2)
    
    l_ruta_total3=[]
    tres = imprime_r(tercer_cluster_lista_coordenadas.tolist(),l_ruta_total3)
   
    l_ruta_total4=[]
    cuatro = imprime_r(cuarto_cluster_lista_coordenadas.tolist(),l_ruta_total4)
 
elif nº_camiones == 5:
    l_ruta_total1=[]
    uno = imprime_r(primer_cluster_lista_coordenadas.tolist(),l_ruta_total1)
   
    l_ruta_total2=[]
    dos = imprime_r(segundo_cluster_lista_coordenadas.tolist(),l_ruta_total2)
  
    l_ruta_total3=[]
    tres = imprime_r(tercer_cluster_lista_coordenadas.tolist(),l_ruta_total3)
  
    l_ruta_total4=[]
    cuatro = imprime_r(cuarto_cluster_lista_coordenadas.tolist(),l_ruta_total4)
  
    l_ruta_total5=[]
    cinco = imprime_r(quinto_cluster_lista_coordenadas.tolist(),l_ruta_total5)
    
elif nº_camiones == 6:
    l_ruta_total1=[]
    uno = imprime_r(primer_cluster_lista_coordenadas.tolist(),l_ruta_total1)

    l_ruta_total2=[]
    dos = imprime_r(segundo_cluster_lista_coordenadas.tolist(),l_ruta_total2)
 
    l_ruta_total3=[]
    tres = imprime_r(tercer_cluster_lista_coordenadas.tolist(),l_ruta_total3)
   
    l_ruta_total4=[]
    cuatro = imprime_r(cuarto_cluster_lista_coordenadas.tolist(),l_ruta_total4)

    l_ruta_total5=[]
    cinco = imprime_r(quinto_cluster_lista_coordenadas.tolist(),l_ruta_total5)
  
    l_ruta_total6=[]
    seis = imprime_r(sexto_cluster_lista_coordenadas.tolist(),l_ruta_total6)
  
elif nº_camiones == 7:
    l_ruta_total1=[]
    uno = imprime_r(primer_cluster_lista_coordenadas.tolist(),l_ruta_total1)
  
    l_ruta_total2=[]
    dos = imprime_r(segundo_cluster_lista_coordenadas.tolist(),l_ruta_total2)
  
    l_ruta_total3=[]
    tres = imprime_r(tercer_cluster_lista_coordenadas.tolist(),l_ruta_total3)
 
    l_ruta_total4=[]
    cuatro = imprime_r(cuarto_cluster_lista_coordenadas.tolist(),l_ruta_total4)
    
    l_ruta_total5=[]
    cinco = imprime_r(quinto_cluster_lista_coordenadas.tolist(),l_ruta_total5)
   
    l_ruta_total6=[]
    seis = imprime_r(sexto_cluster_lista_coordenadas.tolist(),l_ruta_total6)
    
    l_ruta_total7=[]
    siete = imprime_r(septimo_cluster_lista_coordenadas.tolist(),l_ruta_total7)
   
elif nº_camiones == 8:
    l_ruta_total1=[]
    uno = imprime_r(primer_cluster_lista_coordenadas.tolist(),l_ruta_total1)
  
    l_ruta_total2=[]
    dos = imprime_r(segundo_cluster_lista_coordenadas.tolist(),l_ruta_total2)

    l_ruta_total3=[]
    tres = imprime_r(tercer_cluster_lista_coordenadas.tolist(),l_ruta_total3)
   
    l_ruta_total4=[]
    cuatro = imprime_r(cuarto_cluster_lista_coordenadas.tolist(),l_ruta_total4)
   
    l_ruta_total5=[]
    cinco = imprime_r(quinto_cluster_lista_coordenadas.tolist(),l_ruta_total5)
  
    l_ruta_total6=[]
    seis = imprime_r(sexto_cluster_lista_coordenadas.tolist(),l_ruta_total6)
  
    l_ruta_total7=[]
    siete = imprime_r(septimo_cluster_lista_coordenadas.tolist(),l_ruta_total7)
    
    l_ruta_total8=[]
    ocho = imprime_r(octavo_cluster_lista_coordenadas.tolist(),l_ruta_total8)
   


#######################################################################
app = Flask(__name__)

@app.route ("/")
def home():           
    return render_template('hom.html')   

@app.route ("/post", methods=['POST'])
def post():  
    nº_camiones = int(request.form['camiones']) 
    quedatos = int(request.form['quedatos'])           
    return render_template('home.html',
     loquequieras = f'Ruta optima para {quedatos} puntos de reparto con {nº_camiones} camiones')      


@app.route ("/uno")
def uno_():           
    return render_template('home1.html', 
    dis = round(suma_distancia(uno),2) ,
    tie = suma_tiempo(uno),
    rut = l_ruta_total1)

@app.route ("/dos")
def dos_():           
    return render_template('home2.html', 
    dis = round(suma_distancia(dos),2) ,
    tie = suma_tiempo(dos),
    rut = l_ruta_total2)   

@app.route ("/tres")
def tres_():           
    return render_template('home3.html', 
    dis = round(suma_distancia(tres),2) ,
    tie = suma_tiempo(tres),
    rut = l_ruta_total3)    
             
@app.route ("/cuatro")
def cuatro_():           
    return render_template('home4.html', 
    dis = round(suma_distancia(cuatro),2) ,
    tie = suma_tiempo(cuatro),
    rut = l_ruta_total4)

@app.route ("/cinco")
def cinco_():           
    return render_template('home5.html', 
    dis = round(suma_distancia(cinco),2) ,
    tie = suma_tiempo(cinco),
    rut = l_ruta_total5)

@app.route ("/seis")
def seis_():           
    return render_template('home6.html', 
    dis = round(suma_distancia(seis),2) ,
    tie = suma_tiempo(seis),
    rut = l_ruta_total6)   

@app.route ("/siete")
def siete_():           
    return render_template('home7.html', 
    dis = round(suma_distancia(siete),2) ,
    tie = suma_tiempo(siete),
    rut = l_ruta_total7)    
             
@app.route ("/ocho")
def ocho_():           
    return render_template('home8.html', 
    dis = round(suma_distancia(ocho),2) ,
    tie = suma_tiempo(ocho),
    rut = l_ruta_total8)    

@app.route ("/mapa")
def mapa_():           
    return render_template('Mapa.html')  





# lo ejecutamos diciendo que se mantenga activado siempre
if __name__ == '__main__':
    app.run(debug=True)



