import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from analitics import vgames, prueba


app.layout = html.Div([
    html.Div([ 
        html.Img(src = "https://camevirtual.bucaramanga.gov.co/info/alcbucaramanga_se/media/bloque1771.png", className ="Autores__AlcaldiaImagen"),        
       html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div([                           
                html.Img(src = app.get_asset_url('home.png'), className = "Integrante__icono"),    
                dcc.Link('Home', href='/', className= "Integrante__nombre")
                ], className="Integrante"),
            html.Div([dcc.Link('Pruebas mapas', href='/apps/prueba', className= "Integrante__nombre")], className="Integrante"),
            html.Div([dcc.Link('Pruebas', href='/apps/vgames',  className= "Integrante__nombre")], className="Integrante"),
            html.Div([dcc.Link('About us', href='/apps/vgames',  className= "Integrante__nombre")], className="Integrante"),
            
            
            ], className="Autores__integrante"),
        ], className="Autores"),
    html.Div([
        html.H1("Observatorio Digital Municipal de bucaramanga", className="Titulo"),
        html.Div([
            html.Div(className="Dashboard__Mapa", id='page-content', children=[]),
            # html.Div([], className="Dashboard__Datos"),
        ], className="Dashboard"),
    ], className="Observatorio"),
     
], className= 'Main') 



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/vgames':
        return vgames.layout
    if pathname == '/apps/prueba':
        return prueba.layout    
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(host="127.0.0.1", port=8040, debug=True)