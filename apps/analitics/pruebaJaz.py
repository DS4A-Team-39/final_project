import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash
import pandas as pd
import numpy as np
import pathlib
import operator
import pandas as pd 
import numpy as np 
import re
import plotly.graph_objects as go
import plotly.express as px
import operator
import json

from app import app
from dbConnection import startConn

# get relative data folder


sales_list= ['f', 'M']

layout = html.Div([
    html.H1('Prueba Mapa', style={"textAlign": "center"}),

    html.Div([
        html.Div(dcc.Dropdown(
            id='grupos-dropdown-jaz', value='Strategy', clearable=False,
            options=[{'label': x, 'value': x} for x in sorted(sales_list)]
        ), className='six columns'),

        
    ], className='row'),

    dcc.Graph(id='my-bar-prueba-jaz', figure={}),

    
    # html.Iframe(id='map', src='/apps/graficos/mapaPrueba.html', width ='100%', height='600'),

])


@app.callback(
    Output(component_id='my-bar-prueba-jaz', component_property='figure'),
    [
    Input(component_id='grupos-dropdown-jaz', component_property='value')
    ]
)
def display_value(grupo_chosen):

    conn = startConn()
    salud = pd.read_sql('SELECT * FROM salud_bucaramanga', conn)
    poblacion=pd.read_sql('SELECT * FROM poblacion', conn)
    salud['curso_de_vida']=salud['curso_de_vida'].astype('str')
    salud['nombre_comuna']=salud['nombre_comuna'].astype('str')
    salud['barrio']=salud['barrio'].astype('str')
    poblacion['id']=poblacion['id'].astype('int')
    poblacion['primera_infancia_2021']=poblacion['primera_infancia_2021'].astype('int')
    poblacion['infancia_2021']=poblacion['infancia_2021'].astype('int')
    poblacion['adolencencia_2021']=poblacion['adolencencia_2021'].astype('int')
    poblacion['comuna']=poblacion['comuna'].astype('str')
    salud['nombre_comuna']=salud['nombre_comuna'].replace('nan', np.NaN)
    salud['barrio']=salud['barrio'].replace('nan', np.NaN)
    
    dictomu= {'ciudadela':'La Ciudadela',
          'provenza': 'Provenza',
          'cabecera del llano':'Cabecera del llano',
          'centro':'Centro',   
          'garcia rovira':'García Rovira',
          'la concordia': 'La Concordia',
          'lagos del cacique' :'Lagos del Cacique',
          'morrorico':'Morrorico',
          'mutis' : 'Mutis',
          'nororiental' : 'Nororiental',
          'norte' :'Norte',
          'occidental' :  'Occidental',
          'oriental'  :'Oriental',
          'pedregosa'  : 'La Pedregosa',
          'san francisco' :  'San Francisco',
          'sur'  : 'Sur',
          'suroccidente' :  'Sur Occidente'
    }

    dictoid= {'La Ciudadela':7,
            'Provenza': 10,
            'Cabecera del llano':12,
            'Centro': 15,   
            'García Rovira':5,
            'La Concordia': 6,
            'Lagos del Cacique': 16,
            'Morrorico':14,
            'Mutis': 17,
            'Nororiental': 2,
            'Norte': 1,
            'Occidental': 4,
            'Oriental':13,
            'La Pedregosa': 9,
            'San Francisco':3,
            'Sur': 11,
            'Sur Occidente': 8
    }

    salud["nombre_comuna"]=salud["nombre_comuna"].str.strip()
    salud=salud.replace({"nombre_comuna": dictomu})
    salud['nombre_comuna']=salud['nombre_comuna'].fillna(salud['barrio'])

    dictbar={
        'el uvo':'Provenza',
        'asent. la ladrillera':'Sur',
        'patio bonito':'Norte',
        'la calera':'Norte',
        'invasion nuevo horizonte':'Nororiental',
        'km 3 via giron':'Occidental'
    }

    salud=salud.replace({"nombre_comuna": dictbar})

    salud['comuna_id']=salud["nombre_comuna"]


    salud=salud.replace({"comuna_id": dictoid})
    salud_com=salud.groupby(['nombre_comuna','comuna_id','curso_de_vida'])['eps'].agg('count').reset_index()
    salud_com=salud_com[salud_com['comuna_id'].isin(range(0,18))]


    pob=pd.melt(poblacion, id_vars=['id'], value_vars=['primera_infancia_2021',	'infancia_2021',	'adolencencia_2021'], ignore_index=False)

    values_dict = {'primera_infancia_2021': 'primera infancia', 'infancia_2021': 'infancia', 'adolencencia_2021': 'adolescencia'}

    pob['curso_de_vida'] = pob['variable'].apply(map_values, args = (values_dict,))

    pob['index'] = pob['id'].astype('str')+" "+pob['curso_de_vida'].astype('str')
    salud_com['index'] = salud_com['comuna_id'].astype('str')+" "+salud_com['curso_de_vida'].astype('str')
    cober2=salud_com.merge(pob, how='outer', on='index')
    cober2['tasa']=cober2['eps']/cober2['value']
    cober2['id']=cober2['id'].astype('int')
    
    
    path='apps/datasets/ComunasWGS84.geojson'
    geo_str = json.dumps(json.load(open(path, 'r'))) # map data
    nameb=json.loads(geo_str)
    scale=np.linspace(cober2['tasa'].min(),cober2['tasa'].max(),10,dtype=float).tolist()

    fig = px.choropleth_mapbox(cober2[cober2['curso_de_vida_x']=='primera infancia'], geojson=nameb,
                           featureidkey = 'properties.NOMBRE',
                           locations= "comuna_id",
                           color='tasa',
                           color_continuous_scale="viridis",
                           range_color= (cober2['tasa'].min(), cober2['tasa'].max()),
                           mapbox_style="open-street-map",
                           zoom=11.5, center = {"lat": 7.122413, "lon": -73.120446},
                           opacity=0.7,
                           labels='tasa'
                          )
    fig = fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def map_values(row, values_dict):
        return values_dict[row]