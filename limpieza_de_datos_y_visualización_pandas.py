# -*- coding: utf-8 -*-
"""Limpieza_de_datos_y_visualización_pandas.ipynb

# - Autor: 
### Borja Delgado González
# - Objetivo: 
### Limpieza y visualización de los datos recogidos en un archivo .csv a partir del código del repositorio "Webscraping_de_videojuegos"
---

1. Importamos las librerías a usar en este proyecto
"""

#Librerías

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""2. Cargamos el archivo .csv en forma de DataFrame y echamos un vistazo previo."""

df = pd.read_csv('ventas_vj_completo.csv')
df.head()

"""3. Eliminamos las dos primeras columnas y luego obtenemos la información del DataFrame para ver a qué nos enfrentamos."""

df = df.drop(columns=df.columns[0:2], axis=1)

df.head()

df.info()

"""Podemos ver que hay muchos "NA" en las columnas de ventas, fruto de que en la fuente no se disponía de los datos. Si eliminamos los "NA" de ventas o los sustituimos por 0, el análisis estadístico sería poco representativo al perder casi 55000 filas de datos, o sesgado al haber demasiados valores como 0.
Por ello, nos centraremos en las variables "fecha_salida" y "genero" para realizar algunas visualizaciones.

---

4. Creamos algunas variables que necesitaremos para la limpieza y visualizaciones posteriores.
"""

#Variables

generos = {'Action' : 'Acción',
        'Action-Adventure' : 'Acción-Aventura',
        'Adventure' : 'Aventura',
        'Board Game' : 'Juego de mesa',
        'Education' : 'Educación',
        'Fighting' : 'Lucha',
        'Music' : 'Música',
        'Party' : 'Fiesta',
        'Platform' : 'Plataformas',
        'Racing' : 'Carreras',
        'Role-Playing' : 'RPG',
        'Sandbox' : 'Mundo abierto',
        'Simulation' : 'Simulación',
        'Sports' : 'Deportes',
        'Strategy' : 'Estrategia',
        'Visual Novel' : 'Novela Visual'}

ventas = ['ventas_na','ventas_eu','ventas_jp', 'ventas_otras', 'ventas_tot']

etiquetas = ['Acción', 'Acción-Aventura', 'Aventura', 'Carreras', 'Deportes', 'Educación', 'Estrategia', 'Fiesta', 'Juego de mesa',
            'Lucha', 'MMO', 'Misc', 'Mundo abierto', 'Música', 'Novela Visual', 'Plataformas', 'Puzzle', 'RPG', 'Shooter', 'Simulación']

"""5. Comenzamos la limpieza del dataset.

Eliminamos las filas que tengan "Series" y "All" como plataforma porque agrupan varios juegos. También nos deshacemos de las filas sin fecha de salida.
Traducimos los géneros al español.
"""

df = df.loc[df['plataforma'] != 'Series']
df = df.loc[df['plataforma'] != 'All']

df.dropna(subset = ['fecha_salida'], axis = 0, inplace=True)

df[ventas] = df[ventas].replace(np.nan,0)
df['genero'] = df['genero'].replace(generos)

suma_ventas = df['ventas_na'] + df['ventas_eu'] + df['ventas_jp'] + df['ventas_otras']
df['ventas_suma'] = suma_ventas

df.info()

"""Comprobamos que el rango de fechas sea correcto..."""

print(df['fecha_salida'].min(), '-', df['fecha_salida'].max())

"""Parece que el rango no es correcto. Comprobamos cuáles son los valores que son erróneos y por lo tanto, debemos cambiar."""

df['fecha_salida'].value_counts()

fechas = {2070 : 1970,
        2073 : 1973,
        2075 : 1975,
        2077 : 1977,
        2078 : 1978,
        2079 : 1979}

df['fecha_salida'] = df['fecha_salida'].replace(fechas).astype(int)

print(df['fecha_salida'].min(), '-', df['fecha_salida'].max())

"""6. Algunas visualizaciones de datos"""

fig = plt.figure(figsize=(10,7))
sns.countplot(x='fecha_salida',data = df, color = 'gold')
plt.xticks(rotation = 55, fontsize = 7)
plt.title('Número de videojuegos publicados por año')
plt.xlabel('Año')
plt.ylabel('Número de videojuegos publicados');

"""El DataFrame generado a continuación muestra qué tipo de juego fue el más publicado por año. Vemos que han prevalecido los videojuegos de acción, aunque en los últimos años el tipo más publicado es el RPG."""

moda_genero = pd.DataFrame(df.groupby(['fecha_salida'])['genero'].agg(pd.Series.mode))

moda_genero

suma_genero = pd.DataFrame(df.groupby(['genero'])['genero'].agg(pd.Series.count))
suma_genero = suma_genero.rename(columns = {'genero':'conteo'})
suma_genero['genero'] = etiquetas
suma_genero['porcentaje'] = (suma_genero['conteo']/suma_genero['conteo'].sum())*100

suma_genero

umbral = 1
resto_generos = suma_genero.loc[suma_genero['porcentaje'] < umbral].sum(axis=0)
resto_generos.loc['genero'] = 'resto de generos'
suma_genero = suma_genero[suma_genero['porcentaje'] >= umbral]

fig2 = plt.figure(figsize=(10,7))
colores = sns.color_palette('Set2')
plt.pie(suma_genero['conteo'], labels=suma_genero['genero'], colors = colores, autopct='%0.1f%%', pctdistance=0.8)
plt.title('Juegos publicados por género (%)');

"""El género "Misc" agrupa muchos juegos que pueden pertenecer a varios géneros, por lo que vamos a eliminarlo de la visualización para ver cómo se reparten el resto de géneros."""

umbral = 1
suma_genero = suma_genero.drop('Misc')
resto_generos = suma_genero.loc[suma_genero['porcentaje'] < umbral].sum(axis=0)
resto_generos.loc['genero'] = 'resto de generos'
suma_genero = suma_genero[suma_genero['porcentaje'] >= umbral]

fig2 = plt.figure(figsize=(10,7))
colores = sns.color_palette('Set2')
plt.pie(suma_genero['conteo'], labels=suma_genero['genero'], colors = colores, autopct='%0.1f%%', pctdistance=0.8)
plt.title('Juegos publicados por género (%)');
