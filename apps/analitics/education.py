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

# get relative data folder
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
        ), className='six columns'),
    ], className='row'),
    dcc.Graph(id='bar-tasas', figure={}),

    html.Div([
    html.Div([
        html.Div(dcc.Dropdown(
            id='education-matricula-observacion-dropdown', value='edad', clearable=False,
            options=[{'label': key, 'value': value} for key, value in observacion.items()]
        ), className='three columns'),

        html.Div(dcc.Dropdown(
            id='education-matricula-nivel-dropdown', value='media', clearable=False,
            options=[{'label': key, 'value': value} for key, value in nivel.items()]
        ), className='three columns'),

        html.Div(dcc.Dropdown(
            id='education-matricula-ano-dropdown', value='2018', clearable=False,
            options=[{'label':x, 'value': x} for x in ano]
        ), className='three columns'),
    ], className='row'),
    dcc.Graph(id='bar-matricula', figure={}),
    ])
])

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