# Manual · Rutas de Leganés 3

1. Pega o importa un CSV UTF-8 con columnas nombre,lat,lon (nombre es opcional). Se acepta coma o punto y coma como separador; si usas coma decimal, utiliza punto y coma entre campos.
2. Elige entre 1 y 8 rutas, sin superar el número de paradas.
3. Pulsa Calcular reparto.
4. Revisa el esquema y el orden de paradas; exporta CSV.

Máximo 500 paradas y 2 MB. Se reparte por turnos entre rutas, eligiendo para cada una la siguiente parada más cercana. Es una heurística determinista, sin depósito ni retorno al origen. **No garantiza la ruta óptima y no calcula distancias por carretera ni tiempos de conducción.** No convierte direcciones a coordenadas. No llama a Google Maps ni a otros servicios.

La API Python local añade importación XLSX: `POST /api/plan`, multipart con file y routes. No guarda los archivos. Usa las mismas columnas. El navegador y los paquetes gráficos procesan CSV, no XLSX. El material histórico de src/ se conserva con GPL-2.0 y se ha retirado su entrada para impedir llamadas externas accidentales.
