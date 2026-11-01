"""Planificador local independiente del código GPL histórico.
SPDX-License-Identifier: AGPL-3.0-only
"""
import csv
import io
import math
import zipfile

def parse_rows(rows):
    rows=iter(rows)
    try: head=[str(v or '').strip().lower() for v in next(rows)]
    except StopIteration: raise ValueError('El archivo está vacío.') from None
    if 'lat' not in head or 'lon' not in head:
        raise ValueError('Se requieren columnas lat y lon; nombre es opcional.')
    points=[]
    li,oi=head.index('lat'),head.index('lon')
    ni=head.index('nombre') if 'nombre' in head else None
    for row in rows:
        if not any(v is not None and str(v).strip() for v in row):continue
        if len(points)>=500:raise ValueError('Máximo 500 paradas.')
        try:
            if type(row[li]) is bool or type(row[oi]) is bool:raise ValueError()
            lat=float(str(row[li]).replace(',','.'));lon=float(str(row[oi]).replace(',','.'))
            if not math.isfinite(lat) or not math.isfinite(lon) or abs(lat)>90 or abs(lon)>180:raise ValueError()
        except (ValueError,TypeError,IndexError):raise ValueError('Coordenada no válida en fila '+str(len(points)+2)) from None
        name=str(row[ni] or '') if ni is not None and ni<len(row) else ''
        points.append(dict(id=len(points),name=(name or 'Parada '+str(len(points)+1))[:120],lat=lat,lon=lon))
    if not points:raise ValueError('No hay paradas.')
    return points

def parse_file(data,name):
    if len(data)>2_000_000:raise ValueError('Límite: 2 MB.')
    if name.lower().endswith('.csv'):
        try:text=data.decode('utf-8-sig')
        except UnicodeDecodeError:raise ValueError('Usa CSV con codificación UTF-8.') from None
        if not text.strip():raise ValueError('El archivo está vacío.')
        delimiter=';' if ';' in text.splitlines()[0] else ','
        try:return parse_rows(csv.reader(io.StringIO(text),delimiter=delimiter,strict=True))
        except csv.Error:raise ValueError('CSV con comillas o filas no válidas.') from None
    if name.lower().endswith('.xlsx'):
        from openpyxl import load_workbook
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                if sum(p.file_size for p in archive.infolist())>20_000_000 or len(archive.infolist())>1000:
                    raise ValueError('XLSX expandido demasiado grande.')
            book=load_workbook(io.BytesIO(data),read_only=True,data_only=True,keep_links=False)
            try:
                sheet=book.active
                if sheet.max_row>501 or sheet.max_column>20:raise ValueError('Máximo 500 paradas y 20 columnas.')
                return parse_rows(sheet.iter_rows(values_only=True))
            finally:book.close()
        except ValueError:raise
        except Exception:raise ValueError('El archivo no es un XLSX válido.') from None
    raise ValueError('Usa un archivo CSV o XLSX.')

def distance(a,b):
    lat1,lat2=math.radians(a['lat']),math.radians(b['lat'])
    dlat=lat2-lat1;dlon=math.radians(b['lon']-a['lon'])
    h=math.sin(dlat/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 6371*2*math.atan2(math.sqrt(min(1,h)),math.sqrt(max(0,1-h)))

def plan(points,count):
    if type(count) is not int or not 1<=count<=min(8,len(points)):raise ValueError('Entre 1 y 8 rutas, sin superar las paradas.')
    remaining=list(points);routes=[[] for _ in range(count)]
    while remaining:
        for route in routes:
            if not remaining:break
            index=min(range(len(remaining)),key=lambda i:distance(route[-1],remaining[i])) if route else 0
            route.append(remaining.pop(index))
    return [dict(stops=r,km=sum(distance(a,b) for a,b in zip(r,r[1:]))) for r in routes]
