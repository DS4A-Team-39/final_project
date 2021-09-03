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

group_age={'Primera Infancia': 'primera infancia',
                'Infancia': 'infancia',
                'Adolescencia': 'adolescencia'
                }

year={'Año 2020': 2020,
        'Año 2019':2019}

layout = html.Div([
    html.H1('Prueba Mapa Aurelio', style={"textAlign": "center"}),

    
    
    dcc.Graph(id='bar-map-survival-one', figure=graph_one(), className = "five columns"),

    dcc.Graph(id='bar-map-survival-two', figure=graph_two(), className = "five columns"),

    html.Div([
        html.Div(dcc.Dropdown(
            id='grupos-dropdown-jaz', value='primera infancia', clearable=False,
            options=[{'label': key, 'value': value}
                for key, value in group_age.items()]
        ), className='five columns'),
        html.Div(dcc.Dropdown(
            id='grupos-dropdown-jaz2', value=2019, clearable=False,
            options=[{'label': key, 'value': value}
                for key, value in year.items()]
        ), className='five columns'),
    ], className='row'),
    dcc.Graph(id='my-bar-prueba-jaz', figure={}, className = "five columns"),

    dcc.Graph(id='my-bar-prueba-jaz2', figure={}, className = "five columns"),

])



@app.callback(
    Output(component_id='my-bar-prueba-jaz', component_property='figure'),
    [
    Input(component_id='grupos-dropdown-jaz', component_property='value')
    ]
)
def display_value_salud(grupo_chosen):

    conn = startConn()

    salud = pd.read_sql('SELECT * FROM salud_bucaramanga', conn)
    poblacion=pd.read_sql('SELECT * FROM poblacion', conn)
    salud=salud[salud['curso_de_vida']!='jovenes']
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

    def map_values(row, values_dict):
        return values_dict[row]

    values_dict = {'primera_infancia_2021': 'primera infancia', 'infancia_2021': 'infancia', 'adolencencia_2021': 'adolescencia'}

    pob['curso_de_vida'] = pob['variable'].apply(map_values, args = (values_dict,))

    pob['index'] = pob['id'].astype('str')+" "+pob['curso_de_vida'].astype('str')
    salud_com['index'] = salud_com['comuna_id'].astype('str')+" "+salud_com['curso_de_vida'].astype('str')
    cober2=salud_com.merge(pob, how='outer', on='index')
    cober2['Tasa verificada de cobertura en salud']=cober2['eps']/cober2['value']
    cober2['id']=cober2['id'].astype('int')
    cober2['Tasa verificada de cobertura en salud normalizada']=(cober2['Tasa verificada de cobertura en salud']-cober2['Tasa verificada de cobertura en salud'].min())/(cober2['Tasa verificada de cobertura en salud'].max()-cober2['Tasa verificada de cobertura en salud'].min())
    
    path='datasets/ComunasWGS84.geojson'
    geo_str = json.dumps(json.load(open(path, 'r'))) # map data
    nameb=json.loads(geo_str)
    scale=np.linspace(cober2['Tasa verificada de cobertura en salud'].min(),cober2['Tasa verificada de cobertura en salud'].max(),10,dtype=float).tolist()
    fig = px.choropleth_mapbox(cober2[cober2['curso_de_vida_x']==grupo_chosen], geojson=nameb,
                           featureidkey = 'properties.NOMBRE',
                           locations= "comuna_id",
                           color='Tasa verificada de cobertura en salud',
                           color_continuous_scale="RdYlGn",
                           range_color= (cober2['Tasa verificada de cobertura en salud'].min(), cober2['Tasa verificada de cobertura en salud'].max()),
                           mapbox_style="open-street-map",
                           zoom=11.5, center = {"lat": 7.122413, "lon": -73.120446},
                           opacity=0.7,
                           labels='Tasa verificada de cobertura en salud'
                          )
    fig = fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig 

def map_values(row, values_dict):
        return values_dict[row]



@app.callback(
    Output(component_id='my-bar-prueba-jaz2', component_property='figure'),
    [
    Input(component_id='grupos-dropdown-jaz2', component_property='value')
    ]
)
def display_value_malnutrition(year_chosen):

    conn = startConn()

    malnutrition= pd.read_sql('SELECT * FROM desnutricion',conn)## conection to desnutricion table to malnutrition DataFrame for filter the data
    poblacion=pd.read_sql('SELECT * FROM poblacion', conn)## conection to poblacion table to pobla

    malnutrition['nombre_comuna']=malnutrition['nombre_comuna'].replace('nan', np.NaN) # To assing NaN values to 'nan' text strig for select with NaN. 
    malnutrition['id_comuna']=malnutrition['id_comuna'].replace('nan', np.NaN) 
    malnutrition=malnutrition[malnutrition['id_comuna'].notnull()]
    malnutrition['año']=malnutrition['año'].astype('int')# Change data  type for operations 
    malnutrition['nombre_comuna']=malnutrition['nombre_comuna'].astype('str')# Change data  type for operations 
    malnutrition['id_comuna']=malnutrition['id_comuna'].astype('int') # Change data  type for operations 
    malnutrition['curso_de_vida']=malnutrition['curso_de_vida'].astype('str')# Change data  type for operations  
    poblacion['id']=poblacion['id'].astype('int')# Change data  type for operations 
    poblacion['primera_infancia_2021']=poblacion['primera_infancia_2021'].astype('int')# Change data  type for operations 
    poblacion['infancia_2021']=poblacion['infancia_2021'].astype('int')# Change data  type for operations 
    poblacion['adolencencia_2021']=poblacion['adolencencia_2021'].astype('int')# Change data  type for operations 
    poblacion['comuna']=poblacion['comuna'].astype('str')# Change data  type for operations  

    
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
    malnutrition["nombre_comuna"]=malnutrition["nombre_comuna"].str.strip()
    malnutrition=malnutrition.replace({"nombre_comuna": dictomu})
    malnutrition['comuna_id']=malnutrition["nombre_comuna"] # duplicate column nombre_comuna
    malnutrition=malnutrition.replace({"comuna_id": dictoid}) # replace comuna_id or key in dictoid dict
    malnutrition_set=malnutrition.groupby(['año','nombre_comuna','comuna_id'])['edema'].agg(['count']).reset_index() # count to children in each commune
    malnutrition_set=malnutrition_set[malnutrition_set['comuna_id'].isin(range(0,18))] # filter comune for eliminate data from 'corregimientos'
    malnutrition_set=malnutrition_set.rename(columns={"count":"casos"}) # remane columns to be friendly dataset


    pob=poblacion[['comuna','id','primera_infancia_2021']]# filter data, drop innecesaries columns
    pob=pob.rename(columns={"id": "comuna_id"}) # remane columns for key 
    pob['primera_infancia_2020']=(pob['primera_infancia_2021']//1.13).astype('int') # calculte the poblation integer with 1.13 rate (DANE)
    pob['primera_infancia_2019']=(pob['primera_infancia_2020']//1.13).astype('int') # calculte the poblation integer with 1.13 rate (DANE)


    pob1=pd.melt(pob, id_vars=['comuna_id'], value_vars=['primera_infancia_2021',	'primera_infancia_2020',	'primera_infancia_2019'], ignore_index=False)
    #reverse the pivot table for age group in the poblacion table
    pob1['año']=pob1['variable'].str.rsplit("_", n=1, expand=True)[1] #select to year the poblation data
    pob1['index'] = pob1['comuna_id'].astype('str')+" "+pob1['año'].astype('str') # concatenate the text for join datafrme for two columns, age group and comune_id
    malnutrition_set['index']=malnutrition_set['comuna_id'].astype('str')+" "+malnutrition_set['año'].astype('str') # concatenate the text for join dataframe for two columns, year and comune_id
    pob1['año']=pob1['año'].astype('int') # change the data type, for plot in map, the year is a input to select.
    cober2=malnutrition_set.merge(pob1[pob1['año']<2021], how='outer', on='index')  # join teh data set with index string key.
    # cober2['tasa']=cober2['casos']/cober2['primera_infancia_2021']*100
    cober2=cober2.drop(columns=['año_x','comuna_id_x','index']) # remove repeat columns.
    cober2=cober2.rename(columns={'value':'poblacion','comuna_id_y':'comuna_id','año_y':'año'}) # rename the columns because cober2 is a dataframe the output.
    cober2['casos']=cober2['casos'].fillna(0) # fill NaN bacause the 0 is NAN in this case, this to be part the analysis.
    cober2.iloc[28:]['nombre_comuna']=['La Ciudadela','Cabecera del llano','Centro','Lagos del Cacique','La Pedregosa','Centro'] # Add the commune name information.
    cober2['Casos de desnutricion reportados']=cober2['casos']/cober2['poblacion']*100 # calculate the rate 
    cober2['Casos de desnutricion reportados normalizado']=(cober2['Casos de desnutricion reportados'].max()-cober2['Casos de desnutricion reportados'])/(cober2['Casos de desnutricion reportados'].max()-cober2['Casos de desnutricion reportados'].min())
    
    path='datasets/ComunasWGS84.geojson'
    geo_str = json.dumps(json.load(open(path, 'r'))) # map data
    nameb=json.loads(geo_str)
    scale=np.linspace(cober2['Casos de desnutricion reportados'].min(),cober2['Casos de desnutricion reportados'].max(),10,dtype=float).tolist()

    fig = px.choropleth_mapbox(cober2[cober2['año']==year_chosen], geojson=nameb,
                           featureidkey = 'properties.NOMBRE', # key the geo data
                           locations= "comuna_id", # key the dataframe with geodata.
                           color='Casos de desnutricion reportados',# columns to plot value
                           color_continuous_scale="RdYlGn_r", # select colors to map
                           range_color= (cober2['Casos de desnutricion reportados'].min(), cober2['Casos de desnutricion reportados'].max()), # scale
                           mapbox_style="open-street-map", # backgoung
                           zoom=11.5, center = {"lat": 7.122413, "lon": -73.120446}, # center of the map
                           opacity=0.7, 
                           labels='Casos de desnutrición por cada 100 niños de 0 a 2 años' # add values to map
                          )
    fig = fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
 
def map_values(row, values_dict):
        return values_dict[row]