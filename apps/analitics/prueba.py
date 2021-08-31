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
conn = startConn()
dfv = pd.read_sql('SELECT * FROM aseguramiento_edad', conn)
salud = pd.read_sql('SELECT * FROM salud_bucaramanga', conn)
poblacion = pd.read_sql('SELECT * FROM poblacion', conn)
sisben = pd.read_sql('SELECT * FROM sisben', conn)
sales_list= ['f', 'M']

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("./graficos").resolve()
DATA_PATH = DATA_PATH.joinpath("mapaPrueba.html")

layout = html.Div([
    html.H1('Prueba Mapa', style={"textAlign": "center"}),

    html.Div([
        html.Div(dcc.Dropdown(
            id='grupos-dropdown', value='Strategy', clearable=False,
            options=[{'label': x, 'value': x} for x in sorted(salud.curso_de_vida.unique())]
        ), className='six columns'),

        
    ], className='row'),

    dcc.Graph(id='my-bar-prueba', figure={}),

    
    # html.Iframe(id='map', src='/apps/graficos/mapaPrueba.html', width ='100%', height='600'),

])


@app.callback(
    Output(component_id='my-bar-prueba', component_property='figure'),
    [
    Input(component_id='grupos-dropdown', component_property='value')
    ]
)
def display_value(grupo_chosen):

    salud = pd.read_sql('SELECT * FROM salud_bucaramanga', conn)
    poblacion = pd.read_sql('SELECT * FROM poblacion', conn)
    df_sisben = pd.read_sql('SELECT * FROM sisben', conn)
    poblacion["primera_infancia_2020"] = poblacion["primera_infancia_2021"].astype(int)/1.13
    poblacion["primera_infancia_2019"] = poblacion["primera_infancia_2020"].astype(int)/1.13
    poblacion["primera_infancia_2018"] = poblacion["primera_infancia_2019"].astype(int)/1.13

    poblacion["infancia_2020"] = poblacion["infancia_2021"].astype(int)/1.13
    poblacion["infancia_2019"] = poblacion["infancia_2020"].astype(int)/1.13
    poblacion["infancia_2018"] = poblacion["infancia_2019"].astype(int)/1.13

    poblacion["adolencencia_2020"] = poblacion["adolencencia_2021"].astype(int)/1.13
    poblacion["adolencencia_2019"] = poblacion["adolencencia_2020"].astype(int)/1.13
    poblacion["adolencencia_2018"] = poblacion["adolencencia_2019"].astype(int)/1.13

    pob2018_primera_inf = poblacion["primera_infancia_2018"].astype(int).sum()
    pob2019_primera_inf = poblacion["primera_infancia_2019"].astype(int).sum()
    pob2020_primera_inf = poblacion["primera_infancia_2020"].astype(int).sum()
    pob2021_primera_inf = poblacion["primera_infancia_2021"].astype(int).sum()

    pob2018_inf = poblacion["infancia_2018"].astype(int).sum()
    pob2019_inf = poblacion["infancia_2019"].astype(int).sum()
    pob2020_inf = poblacion["infancia_2020"].astype(int).sum()
    pob2021_inf = poblacion["infancia_2021"].astype(int).sum()

    pob2018_adol = poblacion["adolencencia_2018"].astype(int).sum()
    pob2019_adol = poblacion["adolencencia_2019"].astype(int).sum()
    pob2020_adol = poblacion["adolencencia_2020"].astype(int).sum()
    pob2021_adol = poblacion["adolencencia_2021"].astype(int).sum()

    df_icbf_pard = pd.read_sql('SELECT * FROM pard_icbf', conn)
    df_icbf_pard1 = df_icbf_pard[df_icbf_pard["rango_edad"] == "de 0 a 5 años"]
    df_icbf_pard2 = df_icbf_pard[df_icbf_pard["rango_edad"] == "de 6 a 11 años"]
    df_icbf_pard3 = df_icbf_pard[df_icbf_pard["rango_edad"] == "de 12 a 17 años"]
    lista_tasa_restablecimiento_derechos = list(map(operator.truediv, df_icbf_pard1[["año", "mes"]].groupby(["año"]).count()["mes"].tolist(),
                                                [pob2018_primera_inf, pob2019_primera_inf, pob2020_primera_inf, pob2021_primera_inf])) + list(map(operator.truediv,
                                                                                                                                                  df_icbf_pard2[["año", "mes"]].groupby(["año"]).count()["mes"].tolist(),
                                                                                                                                                  [pob2018_inf, pob2019_inf, pob2020_inf, pob2021_inf])) + list(map(operator.truediv,
                                                                                                                                                                                                                    df_icbf_pard3[["año", "mes"]].groupby(["año"]).count()["mes"].tolist(),
                                                                                                                                                                                                                    [pob2018_adol, pob2019_adol, pob2020_adol, pob2021_adol]))

    lista_ano_restablecimiento_derechos =  df_icbf_pard1[["año", "mes"]].groupby(["año"]).count().index.tolist()*3
    lista_edad_restablecimiento_derechos = np.array(["primera infancia", "infancia", "adolescencia"])
    lista_edad_restablecimiento_derechos = np.repeat(lista_edad_restablecimiento_derechos, 4, axis=0)

    tasa_restablecimiento_derechos_por_ano = pd.DataFrame({"grupo etareo": lista_edad_restablecimiento_derechos, "año": lista_ano_restablecimiento_derechos,
                                                        "tasa": [round(num,5) for num in lista_tasa_restablecimiento_derechos]})

    df_sisben["icbf_ninos_beneficiarios"] = df_sisben["icbf_ninos_beneficiarios"].astype("int")
    beneficiarios_icbf = df_sisben.groupby(["num_comuna", "nom_comuna"])[["icbf_ninos_beneficiarios"]].sum()
    beneficiarios_icbf = beneficiarios_icbf.reset_index()
    beneficiarios_icbf["numero_comuna"] = beneficiarios_icbf["num_comuna"].astype("int")
    beneficiarios_icbf["prop_niños_benef_icbf"] = beneficiarios_icbf["icbf_ninos_beneficiarios"].astype("int") / pob2018_primera_inf
    path='apps/datasets/ComunasWGS84.geojson'
    geo_str = json.dumps(json.load(open(path, 'r'))) # map data
    nameb=json.loads(geo_str)
    scale=np.linspace(beneficiarios_icbf["prop_niños_benef_icbf"].min(),beneficiarios_icbf["prop_niños_benef_icbf"].max(),10,dtype=float).tolist()

    fig = px.choropleth_mapbox(beneficiarios_icbf, geojson=nameb,
                           featureidkey = 'properties.NOMBRE',
                           locations= "numero_comuna",
                           color='prop_niños_benef_icbf',
                           color_continuous_scale="viridis",
                           range_color= (0, 0.014),
                           mapbox_style="open-street-map",
                           zoom=11.5, center = {"lat": 7.122413, "lon": -73.120446},
                           opacity=0.5,
                           labels='rop_niños_benef_icbf'
                          )
    fig = fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})   
    
    return fig
 
def map_values(row, values_dict):
        return values_dict[row]