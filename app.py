# import packages
from dash import Dash, html, dcc, callback, Output, Input, clientside_callback, State, ALL, ctx, dash_table
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import plotly.graph_objs as go
import math
from datetime import datetime
from assets.styles import NAVBAR_STYLE, LAYOUT_STYLE, HEADER_TITLE_STYLE

# inital variable for neutrogena
df_neutrogena = pd.read_csv('./youtube_sentiment/youtube_comments_with_sentiment.csv')

print(df_neutrogena)

# components
navbar = dbc.Navbar(
    dbc.Container(
      children=[
        html.H4(children="Brand Sentiment Analysis", style=HEADER_TITLE_STYLE)
      ],
      fluid=True
    ),
    color="dark",
    dark=True,
    class_name="navbar",
    style=NAVBAR_STYLE
)

pie_chart_fig = px.pie(
    df_neutrogena['Sentiment'].value_counts().reset_index(), 
    values='count', 
    names='Sentiment', 
    title='Sentiment Distribution',
    color_discrete_sequence=px.colors.qualitative.Set3
)

pie_chart_container = dbc.Container(
  children=[
    pie_chart_fig
  ]
)

sentiment_plot_container = dbc.Container(
  children=[
    "sentiment line plot"
  ]
)


comments_table = dash_table.DataTable(
    id='comments-table',
    columns=[
        {'name': 'Comments', 'id': 'Comments'},
        {'name': 'Sentiment', 'id': 'Sentiment'},
        {'name': 'Sentiment Score', 'id': 'Sentiment Score'}
    ],
    page_current=0,
    page_size=10,
    page_action='custom',
    style_table={'overflowX': 'auto'},
    style_cell={
        'whiteSpace': 'normal',
        'height': 'auto',
        'textAlign': 'left',
        'paddingLeft': '10px',
        'paddingRight': '10px',
        'fontFamily': 'Arial, sans-serif',
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'  # Light grey background for odd rows (striped effect)
        }
    ],
)

news_sentiment_plot = dbc.Container(
    id='plot-container-news',
    style={'padding': '0px'},
    children=[
        html.H4(children='Sentiment Analysis Visualization'),
        dcc.Store(id='data-store-news'),
        dcc.Graph(id='pred-graph-news'),
    ])

# initialise the dash application
app = dash.Dash(
  external_stylesheets=[dbc.themes.BOOTSTRAP],
  suppress_callback_exceptions=True
)

# app layout
app.layout = dbc.Container(
  children=[
    navbar,
    pie_chart_container,
    sentiment_plot_container
  ],
  fluid=True,
  style=LAYOUT_STYLE,
)

# running the dashboard locally on http://127.0.0.1:8050/
if __name__ == '__main__':
  app.run(debug=True)