
class Mapa:
    """Devuelve un html (mapa de Madrid con los puntos de un DataFame
    representados) despues lo visualiza en un navegador.
     
    Es necesario como parametro un DataFame."""
    def __init__(self,df):
        self.df =df
            
    def mapa_con_puntos(self):
        """Devuelve un html con un mapa de Madrid con los puntos de un DataFame representados
        en un circulo azul."""              
        import folium       
        #Creamos el mapa de madrid 
        madrid_coordinates = (40.336616, -3.759923)
        m2 = folium.Map(location=madrid_coordinates, 
                    zoom_start=14, 
                    tiles="OpenStreetMap")
        #marcamos centros de logistica 
        for index, row in self.df.iterrows():
            folium.CircleMarker([row[0], row[1]],radius=10,
                                popup=row[1],fill_color="blue",).add_to(m2)          
        return m2.save("src\\templates\Mapa.html")

    def visualiza_mapa(self,ruta_desde_C):
        """Visualiza el mapa en un navegador.
        
        Hay que poner en "aplicaciones predeterminadas por tipo de archivo" de Windows,
        un navegador en el tipo de archivo HTML         
        
        Necesita como parametro la ruta desde C: donde se encueste este programa.
        
        ej: "Users\Jose\Documents" """

        import webbrowser        
        url = 'file:///C:\{}\\apli_web\src\\templates\Mapa.html'.format(ruta_desde_C)

        # antes hay que poner en aplicaciones predeterminadas por tipo de archivo 
        # HTML con un navegador
        webbrowser.open(url, new=1, autoraise=True)
       







  
