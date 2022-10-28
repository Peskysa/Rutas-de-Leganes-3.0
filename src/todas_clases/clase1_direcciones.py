
class Direcciones_coordenadas_API_Google:
        """"Devuelve una lista de las coordenadas que coinciden con las 
        direcciones sacadas de un excel.
        
        Es necesario como primer parametro un excel leido con Pandas               
        y como segundo paramero una APY KEY de Google Maps"""
        def __init__(self,excel,apikey):
               self.excel = excel
               self.apikey = apikey
        def coordenadas_API_Google(self):
            """"Devuelve una lista de las coordenadas que coinciden con las 
            direcciones sacadas de un excel."""               
            lista_json_coordenadas = []
            import googlemaps
            gmaps = googlemaps.Client(key=self.apikey) # en un str
            lista_json_coordenadas = []
            for i in self.excel["direcciones"]:
                lista_json_coordenadas.append(gmaps.geocode(i))
            lista_coordedas =[]
            for i in lista_json_coordenadas:                                
                c= i[0]
                d= c["geometry"]
                e= d['location']
                f= e['lat']
                j= e['lng']
                lista_coordedas.append([f,j])                    
            return lista_coordedas    





