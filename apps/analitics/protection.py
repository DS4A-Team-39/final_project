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

niños_conflicto['ciclo_vital']= niños_conflicto['ciclo_vital'].replace(['entre 0 y 5','entre 6 y 11','entre 12 y 17'],['Early Childhood','Childhood','Adolescence'])
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

niños_conflicto_tasas = niños_conflicto_tasas.rename(columns={'ciclo_vital':'Age group',
                                   'vigencia':'year',
                                   'hecho':'rate'})

#We change the type of data per column that we will need 

personas.p6040 = personas.p6040.astype('int64')
personas.p6030s3 = personas.p6030s3.astype('float64')
personas.code = personas.code.astype('int64')
personas.año = personas.año.astype('int64')

#The important codes are identified in the dataframe, the code p6040 is the age, the code p6030s3 is the year of birth and the p6020 as the sex. 
personas = personas.rename(columns={'p6040':'edad',
                                   'p6030s3':'año_de_nacimiento',
                                   'año':'year',
                                   'p6020':'sexo'})

#Now we relate the working condition of the people by making a relationship with the workers dataframe. 
trabajadores.code = trabajadores.code.astype('int64')
personas["Ocupados"] = personas.code.isin(trabajadores["code"])+0
#With the intention of making the analysis easier, it was determined to separate them by age group so that a new column would be formed. For this, a new dataframe called childhood will be created with only boys under 18 years of age. 
infancia=personas[personas['edad'] < 18]

#Age groups are created 
infancia["grupo_etario"]=None

infancia.loc[infancia.edad<=5 ,'grupo_etario']='Early Childhood'

infancia.loc[(infancia.edad>5) & (infancia.edad<=11),'grupo_etario']='Childhood'

infancia.loc[(infancia.edad>11) & (infancia.edad<18),'grupo_etario']='Adolescence'
niños_trabajando= infancia.groupby('grupo_etario')['Ocupados'].count().to_frame()

niños_trabajando['2018']=None
niños_trabajando['2019']=None
niños_trabajando['2020']=None
niños_trabajando['2021']=None
#rates are calculated 
tasa_adolecente_2018=infancia[(infancia['grupo_etario']=='Adolescence') & (infancia['Ocupados']==1) & (infancia['year']==2018)]['code'].count()/(infancia[(infancia['grupo_etario']=='Adolescence')  & (infancia['year']==2018)]['code'].count())
tasa_adolecente_2019=infancia[(infancia['grupo_etario']=='Adolescence') & (infancia['Ocupados']==1) & (infancia['year']==2019)]['code'].count()/(infancia[(infancia['grupo_etario']=='Adolescence')  & (infancia['year']==2019)]['code'].count())
tasa_adolecente_2020=infancia[(infancia['grupo_etario']=='Adolescence') & (infancia['Ocupados']==1) & (infancia['year']==2020)]['code'].count()/(infancia[(infancia['grupo_etario']=='Adolescence')  & (infancia['year']==2020)]['code'].count())
tasa_adolecente_2021=infancia[(infancia['grupo_etario']=='Adolescence') & (infancia['Ocupados']==1) & (infancia['year']==2021)]['code'].count()/(infancia[(infancia['grupo_etario']=='Adolescence')  & (infancia['year']==2021)]['code'].count())

tasa_infancia_2018=infancia[(infancia['grupo_etario']=='Childhood') & (infancia['Ocupados']==1) & (infancia['year']==2018)]['code'].count()/(infancia[(infancia['grupo_etario']=='Childhood') & (infancia['year']==2018)]['code'].count())
tasa_infancia_2019=infancia[(infancia['grupo_etario']=='Childhood') & (infancia['Ocupados']==1) & (infancia['year']==2019)]['code'].count()/(infancia[(infancia['grupo_etario']=='Childhood') & (infancia['year']==2019)]['code'].count())
tasa_infancia_2020=infancia[(infancia['grupo_etario']=='Childhood') & (infancia['Ocupados']==1) & (infancia['year']==2020)]['code'].count()/(infancia[(infancia['grupo_etario']=='Childhood') & (infancia['year']==2020)]['code'].count())
tasa_infancia_2021=infancia[(infancia['grupo_etario']=='Childhood') & (infancia['Ocupados']==1) & (infancia['year']==2021)]['code'].count()/(infancia[(infancia['grupo_etario']=='Childhood') & (infancia['year']==2021)]['code'].count())


tasa_primera_infancia_2018=infancia[(infancia['grupo_etario']=='Early Childhood') & (infancia['Ocupados']==1) & (infancia['year']==2018)]['code'].count()/(infancia[(infancia['grupo_etario']=='Early Childhood') & (infancia['year']==2018)]['code'].count())
tasa_primera_infancia_2019=infancia[(infancia['grupo_etario']=='Early Childhood') & (infancia['Ocupados']==1) & (infancia['year']==2019)]['code'].count()/(infancia[(infancia['grupo_etario']=='Early Childhood') & (infancia['year']==2019)]['code'].count())
tasa_primera_infancia_2020=infancia[(infancia['grupo_etario']=='Early Childhood') & (infancia['Ocupados']==1) & (infancia['year']==2020)]['code'].count()/(infancia[(infancia['grupo_etario']=='Early Childhood') & (infancia['year']==2020)]['code'].count())
tasa_primera_infancia_2021=infancia[(infancia['grupo_etario']=='Early Childhood') & (infancia['Ocupados']==1) & (infancia['year']==2021)]['code'].count()/(infancia[(infancia['grupo_etario']=='Early Childhood') & (infancia['year']==2021)]['code'].count())

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
niños_trabajando_tasa['rate']=tasa_trabajo

def graph_one():
    #Rate of child victims of the armed conflict 
    fig = px.line(niños_conflicto_tasas, x="year", y="rate", color='Age group')
    fig = fig.update_layout(
        title='Minor victims of armed conflict rate',
        plot_bgcolor="#F2F9F0",
    )
    return fig

def graph_two():
    #Child labor rate 
    fig = px.line(niños_trabajando_tasa, x="year", y="rate", color='Age group')
    fig =fig.update_layout(
        title='Child labor rate',
        plot_bgcolor="#F2F9F0",
    )
    return fig

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

crimes = pd.read_sql('select * from tmp_ind_crimen',conn)
crimes=crimes.rename(columns={'tasa':'rate'})
crimes['rate']=crimes['rate'].astype('float')
crimes['num']=crimes['num'].astype('int')
crimes['den']=crimes['den'].astype('int')
crimes['periodo']=crimes['periodo'].astype('int')


list_features = {
'Sexual crimes':'DELITOS_SEXUALES',
'Murder':'HOMICIDIOS',
'Mortality':'MORTALIDAD',
'Death in traffic accidents':'MORTALIDAD_ACC_TRANSITO',
'Violence':'VIOLENCIA',
'Domestic Violence' :'VIOLENCIA_INTRAFAMILIAR'
}

trans_ind={'DELITOS_SEXUALES':'Sexual crimes','HOMICIDIOS':'Murder','MORTALIDAD':'Mortality','MORTALIDAD_ACC_TRANSITO':'Death in traffic accidents','VIOLENCIA':'Violence','VIOLENCIA_INTRAFAMILIAR' : 'Domestic Violence'}
trans_age_group={'PRIMERA_INFANCIA':'early childhood','ADOLESCENCIA':'Adolescence','INFANCIA':'childhood','MENORES':'Minors'}

layout = html.Div([
    html.H1('Protection', style={"textAlign": "center","color":"#004883"}),
    html.H2('Armed conflict, child labour, crimes and violence', style={"textAlign": "center"}),
    html.Div(dcc.Dropdown(
            id='features-dropdown', value='DELITOS_SEXUALES', clearable=False,
            options=[{'label': key, 'value': value}
                for key, value in list_features.items()]
        ),style={"padding-left": "4%","padding-right": "4%"}),
    dcc.Graph(id='bar-tasas-crimes', figure={}, style={"padding-left": "4%","padding-right": "4%"}),
    dcc.Graph(id='bar-map-survival-one', figure=graph_one(), className = "five columns"),
    dcc.Graph(id='bar-map-survival-two', figure=graph_two(), className = "five columns"),
    dcc.Graph(id='my-bar-prueba', figure=display_value(), className = "five columns"),


], style={"backgroundColor": "white","height":"100%"})


@app.callback(
    Output(component_id='bar-tasas-crimes', component_property='figure'),
    [
    Input(component_id='features-dropdown', component_property='value')
    ]
)

def plot_tasas_crimes(feature):
     tmp=crimes[crimes['ind']==feature]
     data_array=[]
     for j,grupo_edad in enumerate(tmp['grupo_edad'].unique()):
          data_array.append(go.Bar(name=trans_age_group[grupo_edad], x=tmp[tmp['grupo_edad']==grupo_edad]['periodo'], y=tmp[tmp['grupo_edad']==grupo_edad]['rate']))
     fig = go.Figure(data=data_array)
     fig.update_layout(barmode='group', yaxis_title=trans_ind[feature], title_text='Crimes and violence rates',
                    title_x = 0.5 ,yaxis = dict(tickfont = dict(size=14)),xaxis = dict(tickfont = dict(size=14)),font=dict(size=16),plot_bgcolor="#F2F9F0")
     return fig


