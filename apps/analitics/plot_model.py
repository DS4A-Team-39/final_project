import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import pathlib
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# dataset

from app import app
from dbConnection import startConn

layout = html.Div([
    html.H1('Prueba Mapa', style={"textAlign": "center"}),

    html.Div([
        html.Div(dcc.Slider(
        id='my-slider',
        min=1,
        max=7,
        step=1,
        value=3,
        marks = {
            1:'1 clusters',
            3:'3 clusters',
            5:'5 clusters',
            7:'7 clusters',
        }
         ), className='six columns'),

        
    ], className='row'),

    dcc.Graph(id='my-bar-modelo', figure={}),
])


def cluster(n_clusters, X):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    Z = kmeans.predict(X)
    return kmeans, Z

@app.callback(
    Output(component_id='my-bar-modelo', component_property='figure'),
    [
    Input(component_id='my-slider', component_property='value')
    ]
)
def graph_clusters(n_clusters):     
    # dataset
    conn = startConn()
    df_modelo1 = pd.read_sql('SELECT * FROM df_modelo',conn)

    df_modelo1[["tp15_1_ocu", "tp19_ee_1", "tp19_acu_1", "tp19_alc_1", "tp19_gas_1", "tp19_recb1", "tp19_inte1", "tp51superi",
                "tp51postgr", "tp51_13_ed", "tp15_2_ocu", "tp19_ee_2", "tp19_acu_2", "tp19_alc_2", "tp19_gas_2", "tp19_recb2",
                "tp19_inte2", "tp51primar", "tp51secund", "icbf_ben", "salud_pi", "salud_i", "salud_a", "malnutricion_2020",
                "matricula_com_pi", "matricula_com_i", "matricula_com_a"]] = df_modelo1[["tp15_1_ocu", "tp19_ee_1", "tp19_acu_1", "tp19_alc_1", "tp19_gas_1", "tp19_recb1", "tp19_inte1", "tp51superi",
                                                                                        "tp51postgr", "tp51_13_ed", "tp15_2_ocu", "tp19_ee_2", "tp19_acu_2", "tp19_alc_2", "tp19_gas_2", "tp19_recb2",
                                                                                        "tp19_inte2", "tp51primar", "tp51secund", "icbf_ben", "salud_pi", "salud_i", "salud_a", "malnutricion_2020",
                                                                                        "matricula_com_pi", "matricula_com_i", "matricula_com_a"]].astype("float64")


    df_modelo1[["poblacion_2020"]] = df_modelo1[["poblacion_2020"]].astype("int")

    # PCA
    df = df_modelo1
    X = df_modelo1.drop(
        columns=["cd_lc_cm", "nmb_lc_cm_x", "comuna", "poblacion_2020"])
    features = X.columns.to_list()

    pca = PCA(n_components=2)  # Number of components
    components = pca.fit_transform(X)  # Coef components

    # K-means
    # Let the number of clusters be a parameter, so we can get a feel for an appropriate
    # value thereof.
    # Number of clusters
    # n_clusters = max_clusters would be trivial clustering.
    max_clusters = len(df)
    model, Z = cluster(n_clusters, X)

    # Plot
    fig = px.scatter(components, x=0, y=1, color=Z.astype("str"), labels={'0': 'PC 1', '1': 'PC 2'}, size=df['poblacion_2020'], opacity=0.6,
                    text=df["comuna"])
    fig = fig.update_layout(
        title='Clusters de comunas por sus dos primeras componentes principales',
        plot_bgcolor="white",
        showlegend=False
    )
    fig = fig.update_traces(textposition='top right')

    conn.close()
    return fig
