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

from datetime import datetime, date
from app import app
from dbConnection import startConn

def display_value():

    conn = startConn()

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
    path='datasets/ComunasWGS84.geojson'
    geo_str = json.dumps(json.load(open(path, 'r'))) # map data
    nameb=json.loads(geo_str)
    scale=np.linspace(beneficiarios_icbf["prop_niños_benef_icbf"].min(),beneficiarios_icbf["prop_niños_benef_icbf"].max(),10,dtype=float).tolist()

    fig = px.choropleth_mapbox(beneficiarios_icbf, geojson=nameb,
                           featureidkey = 'properties.NOMBRE',
                           locations= "numero_comuna",
                           color='prop_niños_benef_icbf',
                           color_continuous_scale="rdylgn",
                           range_color= (0, 0.014),
                           mapbox_style="open-street-map",
                           zoom=11.5, center = {"lat": 7.122413, "lon": -73.120446},
                           opacity=0.5,
                           labels='rop_niños_benef_icbf'
                          )
    fig = fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})   
    conn.close()
    return fig
 
def map_values(row, values_dict):
        return values_dict[row]

# get relative data folder


conn = startConn()
educacion = pd.read_sql('SELECT * FROM "estadisticas_educacion"', conn)
matriculas = pd.read_sql('SELECT * FROM "matricula_educacion"', conn)
matriculas_final = pd.read_sql('SELECT * FROM "matriculas_bucaramanga"', conn)
estudiantes_2020 = pd.read_sql(
    'SELECT * FROM "estudiantes_por_barrio_2020_anonimizado"', conn)
poblacion_educacion = pd.read_sql('SELECT * FROM "poblacion"', conn)

educacion = educacion.astype('float64')
educacion = educacion[educacion['año'] >= 2018]
for column in educacion.columns:
  if column == ('año' or 'poblacion_5_16'):
    educacion[column] = educacion[column]
  else:
    educacion[column] = educacion[column]/100
educacion = educacion.drop(columns=['poblacion_5_16', 'cobertura_neta', 'cobertura_bruta', 'tamaño_promedio_de_grupo', 'sedes_conectadas_a_internet', 'desercion', 'aprobacion', 'reprobacion',
                                  'repitencia', 'tasa_matriculacion_5_16']).reset_index()
educacion = educacion.drop(columns='index')
educacion = educacion*100
educacion['año'] = educacion['año']/100


@app.callback(
    Output(component_id='bar-tasas', component_property='figure'),
    [
    Input(component_id='education-tasas-dropdown', component_property='value')
    ]
)
def plot_tasas_educativas(feature_educativa):
    fig = go.Figure(data=[
        go.Bar(name='transicion',
               x=educacion['año'], y=educacion[feature_educativa+'_transicion']),
        go.Bar(name='primaria', x=educacion['año'],
                y=educacion[feature_educativa+'_primaria']),
        go.Bar(name='secundaria',
                x=educacion['año'], y=educacion[feature_educativa+'_secundaria']),
        go.Bar(name='media', x=educacion['año'],
                y=educacion[feature_educativa+'_media'])
    ])
    # Change the bar mode
    fig =fig.update_layout(barmode='group', yaxis_title=feature_educativa+' porcentual %', title_text='Tasas de variables educativas',
                    title_x = 0.5,plot_bgcolor='azure' ,yaxis = dict(tickfont = dict(size=14)),xaxis = dict(tickfont = dict(size=14)),font=dict(size=16))
    
    return fig

matriculas_final = matriculas_final.drop(columns='index')
matriculas_final.año = matriculas_final.año.astype('int32')
matriculas_final.edad = matriculas_final.edad.astype('int32')

def matriculas_nivel_educativo(nivel,observacion):
  """This function outputs the bar graphs for each year according to the nivel_educativo and the observation that the user wants
  Arguments: 
  nivel: corresponds to one of the four educational levels: transicion,primaria,secundaria,media
  observacion: correspondons to the feature that the user wants to inspect:sector, calendario, zona, tipo_jornada,grado,edad,genero,sector_conpes"""
  matriculas_2018 = matriculas_final[(matriculas_final['nivel_educativo']==str(nivel))& (matriculas_final['año']==2018)].groupby(str(observacion)).size()
  matriculas_2019 = matriculas_final[(matriculas_final['nivel_educativo']==str(nivel))& (matriculas_final['año']==2019)].groupby(str(observacion)).size()
  matriculas_2020 = matriculas_final[(matriculas_final['nivel_educativo']==str(nivel))& (matriculas_final['año']==2020)].groupby(str(observacion)).size()
  return matriculas_2018, matriculas_2019, matriculas_2020


@app.callback(
    Output(component_id='bar-matricula', component_property='figure'),
    [
    Input(component_id='education-matricula-nivel-dropdown', component_property='value'),
    Input(component_id='education-matricula-observacion-dropdown', component_property='value'),
    Input(component_id='education-matricula-ano-dropdown', component_property='value')
    ]
)
def plot_matricula(nivel, observacion, ano):
    ano_2018=0
    ano_2019=1
    ano_2020=2
    y_2018=matriculas_nivel_educativo(nivel,observacion)[ano_2018].values
    x_2018=matriculas_nivel_educativo(nivel,observacion)[ano_2018].index
    y_2019=matriculas_nivel_educativo(nivel,observacion)[ano_2019].values
    x_2019=matriculas_nivel_educativo(nivel,observacion)[ano_2019].index
    y_2020=matriculas_nivel_educativo(nivel,observacion)[ano_2020].values
    x_2020=matriculas_nivel_educativo(nivel,observacion)[ano_2020].index
    if ano == '2018':
        fig = go.Figure(data=[
            go.Bar(name='2018', x=x_2018, y=y_2018)
        ])
        # Change the bar mode
        fig = fig.update_layout(barmode='group', plot_bgcolor='azure', title_text='Número de matriculados', yaxis_title='Frecuencia',
                            title_x = 0.5, yaxis = dict(tickfont = dict(size=14)),xaxis = dict(tickfont = dict(size=14)),font=dict(size=16))
        return fig 
    elif ano == '2019': 
        fig = go.Figure(data=[
            go.Bar(name='2019', x=x_2019, y=y_2019)
        ])
        # Change the bar mode
        fig = fig.update_layout(barmode='group', title_text='Número de matriculados', yaxis_title='Frecuencia'
                            ,title_x = 0.5 ,plot_bgcolor='azure',yaxis = dict(tickfont = dict(size=14)),xaxis=dict(tickfont = dict(size=14)), font=dict(size=16))
        return fig
    elif ano == '2020': 
        fig = go.Figure(data=[
            go.Bar(name='2020', x=x_2020, y=y_2020)
        ])
        # Change the bar mode
        fig = fig.update_layout(barmode='group', title_text='Número de matriculados', yaxis_title='Frecuencia',
                            title_x = 0.5,yaxis = dict(tickfont = dict(size=14)),xaxis=dict(tickfont = dict(size=14)),font=dict(size=16))
        return fig

list_education_features = {
    'Aprobación': 'aprobacion',
    'Cobertura bruta': 'cobertura_bruta',
    'Cobertura neta': 'cobertura_neta',
    'Desercion': 'desercion',
    'Repitencia': 'repitencia',
    'Reprobacion': 'reprobacion'
    }
observacion = {
    'Sector':'sector',
    'Calendario':'calendario',
    'Zona':'zona', 
    'Tipo_jornada':'tipo_jornada',
    'Grado':'grado','Edad':'edad',
    'Genero':'genero',
    'Sector_conpes':'sector_conpes'
    }
nivel = {
    'Transicion':'transicion',
    'Primaria':'primaria',
    'Secundaria':'secundaria',
    'Media':'media'
    }
ano = ['2018','2019','2020']

layout = html.Div([
    html.H1('Development', style={"textAlign": "center"}),

    html.Div([
        html.Div(dcc.Dropdown(
            id='education-tasas-dropdown', value='aprobacion', clearable=False,
            options=[{'label': key, 'value': value}
                for key, value in list_education_features.items()]
        ), className='six columns', style={"padding-left": "4%","padding-right": "4%"}),
    ], className='row'),
    dcc.Graph(id='bar-tasas', figure={}),

    html.Div([
    html.Div([
        html.Div(dcc.Dropdown(
            id='education-matricula-observacion-dropdown', value='edad', clearable=False,
            options=[{'label': key, 'value': value} for key, value in observacion.items()]
        ), className='three columns', style={"padding-left": "4%","padding-right": "4%"}),

        html.Div(dcc.Dropdown(
            id='education-matricula-nivel-dropdown', value='media', clearable=False,
            options=[{'label': key, 'value': value} for key, value in nivel.items()]
        ), className='three columns',style={"padding-left": "4%","padding-right": "4%"}),

        html.Div(dcc.Dropdown(
            id='education-matricula-ano-dropdown', value='2018', clearable=False,
            options=[{'label':x, 'value': x} for x in ano]
        ), className='three columns',style={"padding-left": "4%","padding-right": "4%"}),
    ], className='row'),
    dcc.Graph(id='bar-matricula', figure={}),
    ]),

    dcc.Graph(id='my-bar-prueba', figure=display_value(), className = "five columns"),

])