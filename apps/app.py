import dash
# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
# import dash_html_components as html
# import flask
# import pandas as pd
# from dbConnection import startConn


# server = flask.Flask(__name__)
# app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.config.suppress_callback_exceptions = True

# app.layout = html.Div(
#     children=[
#         html.H1(children="Coronamos"),
#         html.Div(children="""Dash: A web application framework for Python."""),
#         dcc.Graph(
#             id="example-graph",
#             figure={
#                 "data": [
#                     {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
#                     {
#                         "x": [1, 2, 3],
#                         "y": [2, 4, 5],
#                         "type": "bar",
#                         "name": u"Montréal",
#                     },
#                 ],
#                 "layout": {"title": "Dash Data Visualization"},
#             },
#         ),
#     ]
# )


# if __name__ == "__main__":
#     import os


#     conn = startConn()
#     SQL_Query = pd.read_sql('SELECT * FROM aseguramiento_edad', conn)
#     print(SQL_Query.columns)
    
#     app.run_server(host="0.0.0.0", port=8050, debug=True)

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server