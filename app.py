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
from assets.styles import NAVBAR_STYLE, LAYOUT_STYLE, HEADER_TITLE_STYLE, PLOT_CONTAINER_STYLE

# inital variable for neutrogena
df_neutrogena = pd.read_csv('./youtube_sentiment/youtube_comments_with_sentiment.csv')
sentiment_counts = df_neutrogena['Sentiment'].value_counts()
labels_with_counts = [f'{label} ' for label, count in zip(sentiment_counts.index, sentiment_counts.values)]

# print(df_neutrogena)

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

# donut chart for sentiment count
donut_chart = go.Figure(data=[go.Pie(
    labels=labels_with_counts,
    values=sentiment_counts.values,
    hole=.3,
    textinfo='label+percent', 
    hoverinfo='label+value+percent',
)])

donut_chart.update_layout(
    title_text='Sentiment Distribution',
    annotations=[dict(text='Sentiment', x=0.5, y=0.5, font_size=12, showarrow=False)],
    legend=dict(
            x=0.5,
            y=-0.2,
            xanchor='center',
            yanchor='top',
            orientation='h'
        )
)

pie_chart_container = dbc.Container(
  children=[
    dcc.Graph(figure=donut_chart)
  ],
  style=PLOT_CONTAINER_STYLE
)

# bar chart for weekly sentiment
weekly_sentiment = df_neutrogena.groupby(['Week', 'Sentiment']).size().unstack(fill_value=0)

print(weekly_sentiment)
bar_chart = go.Figure()

# Add positive sentiments
if 'positive' in weekly_sentiment:
  bar_chart.add_trace(go.Bar(
        x=weekly_sentiment.index,
        y=weekly_sentiment['positive'],
        name='Positive',
        # marker_color='green'
    ))

# Add neutral sentiments
if 'neutral' in weekly_sentiment:
  bar_chart.add_trace(go.Bar(
        x=weekly_sentiment.index,
        y=weekly_sentiment['neutral'],
        name='Neutral',
        # marker_color='orange'
    ))

# Add negative sentiments (inverted to point downwards)
if 'negative' in weekly_sentiment:
  bar_chart.add_trace(go.Bar(
        x=weekly_sentiment.index,
        y=-weekly_sentiment['negative'],
        name='Negative',
        # marker_color='red'
    ))

# Update layout
bar_chart.update_layout(
    title='Weekly Sentiment',
    xaxis_title='Time',
    yaxis_title='Count',
    barmode='group',
    bargap=0.2,
    bargroupgap=0.1,
    legend_title_text='Sentiment',
    legend=dict(
            x=0.5,
            y=-0.2,
            xanchor='center',
            yanchor='top',
            orientation='h'
        )
)

sentiment_plot_container = dbc.Container(
  children=[
    dcc.Graph(figure=bar_chart)
  ],
  style=PLOT_CONTAINER_STYLE
)


comments_table = dash_table.DataTable(
    id='comments-table',
    columns=[
        {'name': 'Comments', 'id': 'Comment'},
        {'name': 'Source', 'id' : 'Source'},
        {'name': 'Sentiment', 'id': 'Sentiment'},
        {'name': 'Sentiment Score', 'id': 'Sentiment_Score'}
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

comments_table_container = dbc.Container(
  children=[
    html.H4(children="Comments Overview"),
    dcc.Store(id='data-store-comments'),
    comments_table
  ],
  style=PLOT_CONTAINER_STYLE
)

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
    sentiment_plot_container,
    comments_table_container
  ],
  fluid=True,
  style=LAYOUT_STYLE,
)

# callbacks
@app.callback(
    Output('comments-table', 'data'),
    [Input('comments-table', 'page_current'),
     Input('comments-table', 'page_size')]
)
def update_comments_table(page_current, page_size):
    start = page_current * page_size
    end = start + page_size

    comments_df = df_neutrogena

    # Modify headlines to include anchor tags
    paginated_df = comments_df[['Comment', 'Source', 'Sentiment', 'Sentiment_Score']].iloc[start:end].copy()
    # paginated_df['Headline'] = paginated_df.apply(lambda row: f"[{row['Headline']}]({row['URL']})", axis=1)

    return paginated_df.to_dict('records')

# running the dashboard locally on http://127.0.0.1:8050/
if __name__ == '__main__':
  app.run(debug=True)