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
df_modelo1 = pd.read_sql('SELECT * FROM df_modelo')

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


def cluster(n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    Z = kmeans.predict(X)
    return kmeans, Z


# n_clusters = max_clusters would be trivial clustering.
max_clusters = len(df)

n_clusters = 3  # Number of clusters
model, Z = cluster(n_clusters)

# Plot
fig = px.scatter(components, x=0, y=1, color=Z.astype("str"), labels={'0': 'PC 1', '1': 'PC 2'}, size=df['poblacion_2020'], opacity=0.6,
                 text=df["comuna"])
fig.update_layout(
    title='Clusters de comunas por sus dos primeras componentes principales',
    plot_bgcolor="white",
    showlegend=False
)
fig.update_traces(textposition='top right')
fig.show()
