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
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Video Games|', href='/apps/vgames'),
        dcc.Link('Other Products', href='/apps/prueba'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


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
    app.run_server(host="127.0.0.1", port=8040, debug=False)