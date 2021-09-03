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



conn = startConn()

conflicto = pd.read_sql('SELECT * FROM "victimas_de_conflicto_armado"',conn);
poblacion = pd.read_sql('SELECT * FROM "poblacion"',conn);

fuerza_de_trabajo = pd.read_sql('SELECT * FROM "eh_fuerza_de_trabajo_buc"',conn);
trabajadores = pd.read_sql('SELECT * FROM "eh_ocupados_buc"',conn);
personas= pd.read_sql('SELECT * FROM "eh_personas_buc"',conn);

#We change the type of data per column that we will need 
poblacion.primera_infancia_2021 = poblacion.primera_infancia_2021.astype('float64')
poblacion.infancia_2021 = poblacion.infancia_2021.astype('float64')
poblacion.adolencencia_2021 = poblacion.adolencencia_2021.astype('float64')

#We change the types of data we will use 
poblacion["primera_infancia_2020"] = poblacion["primera_infancia_2021"]/1.13
poblacion["primera_infancia_2019"] = poblacion["primera_infancia_2020"]/1.13
poblacion["primera_infancia_2018"] = poblacion["primera_infancia_2019"]/1.13

poblacion["infancia_2020"] = poblacion["infancia_2021"]/1.13
poblacion["infancia_2019"] = poblacion["infancia_2020"]/1.13
poblacion["infancia_2018"] = poblacion["infancia_2019"]/1.13

poblacion["adolencencia_2020"] = poblacion["adolencencia_2021"]/1.13
poblacion["adolencencia_2019"] = poblacion["adolencencia_2020"]/1.13
poblacion["adolencencia_2018"] = poblacion["adolencencia_2019"]/1.13

pob2018_primera_inf = poblacion["primera_infancia_2018"].sum()
pob2019_primera_inf = poblacion["primera_infancia_2019"].sum()
pob2020_primera_inf = poblacion["primera_infancia_2020"].sum()
pob2021_primera_inf = poblacion["primera_infancia_2021"].sum()

pob2018_inf = poblacion["infancia_2018"].sum()
pob2019_inf = poblacion["infancia_2019"].sum()
pob2020_inf = poblacion["infancia_2020"].sum()
pob2021_inf = poblacion["infancia_2021"].sum()

pob2018_adol = poblacion["adolencencia_2018"].sum()
pob2019_adol = poblacion["adolencencia_2019"].sum()
pob2020_adol = poblacion["adolencencia_2020"].sum()
pob2021_adol = poblacion["adolencencia_2021"].sum()

#we focus on the age groups concerned with our analysis. 
niños_conflicto=conflicto[(conflicto['ciclo_vital']=='entre 0 y 5') | (conflicto['ciclo_vital']=='entre 6 y 11') | (conflicto['ciclo_vital']=='entre 12 y 17')]
#we focus on the stipulated years 
niños_conflicto=niños_conflicto[(niños_conflicto['vigencia']=='2018') |(niños_conflicto['vigencia']=='2019') | (niños_conflicto['vigencia']=='2020')|(niños_conflicto['vigencia']=='2021')]

niños_conflicto['ciclo_vital']= niños_conflicto['ciclo_vital'].replace(['entre 0 y 5','entre 6 y 11','entre 12 y 17'],['primera infancia','infancia','adolecencia'])
niños_conflicto_tasas= niños_conflicto.groupby(['ciclo_vital', 'vigencia'])['hecho'].count().to_frame()
niños_conflicto_tasas.hecho=niños_conflicto_tasas.hecho.astype('float64')
pob_total=[ pob2018_adol, 
  pob2019_adol, 
  pob2020_adol, 
  pob2021_adol,
  pob2018_inf,
  pob2019_inf, 
  pob2020_inf, 
  pob2021_inf,
  pob2018_primera_inf, 
  pob2019_primera_inf, 
  pob2020_primera_inf, 
  pob2021_primera_inf
]

niños_conflicto_tasas['hecho']=niños_conflicto_tasas['hecho']/pob_total
# indexes are restarted
niños_conflicto_tasas=niños_conflicto_tasas.reset_index()

niños_conflicto_tasas = niños_conflicto_tasas.rename(columns={'ciclo_vital':'grupo etareo',
                                   'vigencia':'año',
                                   'hecho':'tasa'});

#We change the type of data per column that we will need 

personas.p6040 = personas.p6040.astype('int64')
personas.p6030s3 = personas.p6030s3.astype('float64')
personas.code = personas.code.astype('int64')
personas.año = personas.año.astype('int64')

#The important codes are identified in the dataframe, the code p6040 is the age, the code p6030s3 is the year of birth and the p6020 as the sex. 
personas = personas.rename(columns={'p6040':'edad',
                                   'p6030s3':'año_de_nacimiento',
                                   'p6020':'sexo'})

#Now we relate the working condition of the people by making a relationship with the workers dataframe. 
trabajadores.code = trabajadores.code.astype('int64')
personas["Ocupados"] = personas.code.isin(trabajadores["code"])+0
#With the intention of making the analysis easier, it was determined to separate them by age group so that a new column would be formed. For this, a new dataframe called childhood will be created with only boys under 18 years of age. 
infancia=personas[personas['edad'] < 18]

#Age groups are created 
infancia["grupo_etario"]=None

infancia.loc[infancia.edad<=5 ,'grupo_etario']='Primera Infancia'

infancia.loc[(infancia.edad>5) & (infancia.edad<=11),'grupo_etario']='Infancia'

infancia.loc[(infancia.edad>11) & (infancia.edad<18),'grupo_etario']='Adolecencia'
niños_trabajando= infancia.groupby('grupo_etario')['Ocupados'].count().to_frame()

niños_trabajando['2018']=None
niños_trabajando['2019']=None
niños_trabajando['2020']=None
niños_trabajando['2021']=None
#rates are calculated 
tasa_adolecente_2018=infancia[(infancia['grupo_etario']=='Adolecencia') & (infancia['Ocupados']==1) & (infancia['año']==2018)]['code'].count()/(infancia[(infancia['grupo_etario']=='Adolecencia')  & (infancia['año']==2018)]['code'].count())
tasa_adolecente_2019=infancia[(infancia['grupo_etario']=='Adolecencia') & (infancia['Ocupados']==1) & (infancia['año']==2019)]['code'].count()/(infancia[(infancia['grupo_etario']=='Adolecencia')  & (infancia['año']==2019)]['code'].count())
tasa_adolecente_2020=infancia[(infancia['grupo_etario']=='Adolecencia') & (infancia['Ocupados']==1) & (infancia['año']==2020)]['code'].count()/(infancia[(infancia['grupo_etario']=='Adolecencia')  & (infancia['año']==2020)]['code'].count())
tasa_adolecente_2021=infancia[(infancia['grupo_etario']=='Adolecencia') & (infancia['Ocupados']==1) & (infancia['año']==2021)]['code'].count()/(infancia[(infancia['grupo_etario']=='Adolecencia')  & (infancia['año']==2021)]['code'].count())

tasa_infancia_2018=infancia[(infancia['grupo_etario']=='Infancia') & (infancia['Ocupados']==1) & (infancia['año']==2018)]['code'].count()/(infancia[(infancia['grupo_etario']=='Infancia') & (infancia['año']==2018)]['code'].count())
tasa_infancia_2019=infancia[(infancia['grupo_etario']=='Infancia') & (infancia['Ocupados']==1) & (infancia['año']==2019)]['code'].count()/(infancia[(infancia['grupo_etario']=='Infancia') & (infancia['año']==2019)]['code'].count())
tasa_infancia_2020=infancia[(infancia['grupo_etario']=='Infancia') & (infancia['Ocupados']==1) & (infancia['año']==2020)]['code'].count()/(infancia[(infancia['grupo_etario']=='Infancia') & (infancia['año']==2020)]['code'].count())
tasa_infancia_2021=infancia[(infancia['grupo_etario']=='Infancia') & (infancia['Ocupados']==1) & (infancia['año']==2021)]['code'].count()/(infancia[(infancia['grupo_etario']=='Infancia') & (infancia['año']==2021)]['code'].count())


tasa_primera_infancia_2018=infancia[(infancia['grupo_etario']=='Primera Infancia') & (infancia['Ocupados']==1) & (infancia['año']==2018)]['code'].count()/(infancia[(infancia['grupo_etario']=='Primera Infancia') & (infancia['año']==2018)]['code'].count())
tasa_primera_infancia_2019=infancia[(infancia['grupo_etario']=='Primera Infancia') & (infancia['Ocupados']==1) & (infancia['año']==2019)]['code'].count()/(infancia[(infancia['grupo_etario']=='Primera Infancia') & (infancia['año']==2019)]['code'].count())
tasa_primera_infancia_2020=infancia[(infancia['grupo_etario']=='Primera Infancia') & (infancia['Ocupados']==1) & (infancia['año']==2020)]['code'].count()/(infancia[(infancia['grupo_etario']=='Primera Infancia') & (infancia['año']==2020)]['code'].count())
tasa_primera_infancia_2021=infancia[(infancia['grupo_etario']=='Primera Infancia') & (infancia['Ocupados']==1) & (infancia['año']==2021)]['code'].count()/(infancia[(infancia['grupo_etario']=='Primera Infancia') & (infancia['año']==2021)]['code'].count())

# We organize the rates calculated in the form of the table cut in armed conflict 
tasas_2018=[tasa_adolecente_2018,tasa_infancia_2018,tasa_primera_infancia_2018]
tasas_2019=[tasa_adolecente_2019,tasa_infancia_2019,tasa_primera_infancia_2019]
tasas_2020=[tasa_adolecente_2020,tasa_infancia_2020,tasa_primera_infancia_2020]
tasas_2021=[tasa_adolecente_2021,tasa_infancia_2021,tasa_primera_infancia_2021]

niños_trabajando['2018']=tasas_2018
niños_trabajando['2019']=tasas_2019
niños_trabajando['2020']=tasas_2020
niños_trabajando['2021']=tasas_2021

# a list with the rates is created 
niños_trabajando_tasa=niños_conflicto_tasas.copy()

tasa_trabajo=[0.061327,
           0.072573,
           0.044466,
           0.053592,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0]

# is placed in the same format given above 
niños_trabajando_tasa['tasa']=tasa_trabajo

def graph_one():
    #Rate of child victims of the armed conflict 
    fig = px.line(niños_conflicto_tasas, x="año", y="tasa", color='grupo etareo')
    fig = fig.update_layout(
        title='Tasa de menores victimas de conflicto armado',
        plot_bgcolor="white",
    )
    return fig

def graph_two():
    #Child labor rate 
    fig = px.line(niños_trabajando_tasa, x="año", y="tasa", color='grupo etareo')
    fig =fig.update_layout(
        title='Tasa de trabajo infantil',
        plot_bgcolor="white",
    )
    return fig


sales_list= ['f', 'M']

layout = html.Div([
    html.H1('Prueba Mapa Aurelio', style={"textAlign": "center"}),

    
    
    dcc.Graph(id='bar-map-survival-one', figure=graph_one(), className = "five columns"),

    dcc.Graph(id='bar-map-survival-two', figure=graph_two(), className = "five columns"),
])

