import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from analitics import vgames, prueba, pruebaJaz, education, survival


app.layout = html.Div([
    html.Div([ 
        html.Img(src = "https://camevirtual.bucaramanga.gov.co/info/alcbucaramanga_se/media/bloque1771.png", className ="Autores__AlcaldiaImagen"),        
       html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div([                           
                html.Img(src = app.get_asset_url('home.png'), className = "Integrante__icono"),    
                dcc.Link('Home', href='/', className= "Integrante__nombre")
                ], className="Integrante"),
            html.Div([dcc.Link('Care', href='/care',  className= "Integrante__nombre")], className="Integrante"),
            html.Div([dcc.Link('Development', href='/development',  className= "Integrante__nombre")], className="Integrante"),
            html.Div([dcc.Link('Survival', href='/survival',  className= "Integrante__nombre")], className="Integrante"),
            html.Div([dcc.Link('Model and tools', href='/models',  className= "Integrante__nombre")], className="Integrante"),
            
            html.Div([
                html.Img(src = app.get_asset_url('team.svg'), className = "Integrante__icono"),  
                dcc.Link('About us', href='/about',  className= "Integrante__nombre")
                ], className="Integrante"),

            html.Div([dcc.Link('Prueba', href='/prueba',  className= "Integrante__nombre")], className="Integrante"),
            
            
            ], className="Autores__integrante"),
        ], className="Autores"),
    html.Div([
        html.H1("Observatorio Digital Municipal de Bucaramanga", className="Titulo"),
        html.Div([
            html.Div(className="Dashboard__Mapa", id='page-content', children=[]),
            # html.Div([], className="Dashboard__Datos"),
        ], className="Dashboard"),
    ], className="Observatorio"),
], className= 'Main') 



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/care':
        return "En Proceso"
    if pathname == '/development':
        return education.layout
    if pathname == '/survival':
        return survival.layout  
    if pathname == '/models'  :
        return "En proceso"
    if pathname == '/about'  :
        return "En proceso"
    if pathname == '/prueba'  :
        return pruebaJaz.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)