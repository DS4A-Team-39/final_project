import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask
from flask import render_template

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from analitics import education, survival, home, protection, about, plot_model


app.layout = html.Div([
    html.Div([ 
        html.Img(src = "https://camevirtual.bucaramanga.gov.co/info/alcbucaramanga_se/media/bloque1771.png", className ="Autores__AlcaldiaImagen"),        
       html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div([                           
                html.Img(src = app.get_asset_url('home.png'), className = "Integrante__icono"),    
                dcc.Link('Home', href='/home', className= "Integrante__nombre")
                ], className="Integrante"),
            html.Div([
                html.Img(src = app.get_asset_url('crecimiento.svg'), className = "Integrante__icono"),
                dcc.Link('Development', href='/development',  className= "Integrante__nombre")
                ], className="Integrante"),
            html.Div([
                html.Img(src = app.get_asset_url('healthcare.svg'), className = "Integrante__icono"),
                dcc.Link('Protection', href='/protection',  className= "Integrante__nombre")
                ], className="Integrante"),
            html.Div([
                html.Img(src = app.get_asset_url('cama-de-hospital.svg'), className = "Integrante__icono"),
                dcc.Link('Survival', href='/survival',  className= "Integrante__nombre")
                ], className="Integrante"),
            html.Div([
                html.Img(src = app.get_asset_url('analitico.svg'), className = "Integrante__icono"),
                dcc.Link('Model', href='/models',  className= "Integrante__nombre")
                ], className="Integrante"),            
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
    if pathname == '/development':
        return education.layout
    if pathname == '/home':
        return home.layout
    if pathname == '/survival':
        return survival.layout  
    if pathname == '/models'  :
        return plot_model.layout
    if pathname == '/about'  :
        return about.layout
    if pathname == '/protection':
        return protection.layout 
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(host="0.0.0.0")