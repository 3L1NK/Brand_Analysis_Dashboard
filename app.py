#!/usr/bin/python3 
# -- coding: utf-8 --
"""
Created on Wed July 17 17:06:37 2024

@author: Eric Korin Syahreza
"""

'''
you need to install the following packages:
#!pip install dash dash-bootstrap-components plotly pandas scikit-learn wordcloud
'''

# import packages
from dash import Dash, html, dcc, callback, Output, Input, clientside_callback, ALL, ctx, dash_table
from assets.styles import NAVBAR_STYLE, LAYOUT_STYLE, HEADER_TITLE_STYLE, PLOT_CONTAINER_STYLE
from dash_bootstrap_components._components.Container import Container
from sklearn.feature_extraction.text import CountVectorizer
import dash_bootstrap_components as dbc
from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objs as go
import pandas as pd
import webbrowser
import base64
import dash
import io
import re


# Importing Sentiment Data
df1 = pd.read_csv('./youtube_sentiment/youtube_comments_with_sentiment.csv')
df2 = pd.read_csv('./reddit_sentiment/neutrogena_reddit.csv')
df1['Source'] = 'YouTube'
df2['Source'] = 'Reddit'
df = pd.concat([df1, df2], ignore_index=True)



# Define a function to clean the comments
def clean_comment(comment):
    # Remove URLs
    comment = re.sub(r'http\S+', '', comment)
    # Remove non-alphabetic characters and convert to lowercase
    comment = re.sub(r'[^A-Za-z\s]', '', comment).lower()
    return comment

df['Cleaned_Comment'] = df['Comment'].apply(clean_comment)

# Define additional stop words
additional_stopwords = {"skin", "product", "https", "use", "one", "would", "get", "neutrogena", "im"}

# Filter out neutral sentiments for net sentiment calculation
def filter_df_by_source(df, source):
    if source:
        return df[df['Source'] == source]
    return df

def green_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(120, 100%, {}%)".format(random_state.randint(30, 70))  # Green color with lightness between 30% and 70%

# Generating Wordcloud
def generate_wordclouds(df):
    positive_comments = " ".join(comment for comment in df[df.Sentiment == 'positive'].Cleaned_Comment)
    neutral_comments = " ".join(comment for comment in df[df.Sentiment == 'neutral'].Cleaned_Comment)
    negative_comments = " ".join(comment for comment in df[df.Sentiment == 'negative'].Cleaned_Comment)
    
    positive_wordcloud = WordCloud(width=400, height=200, background_color='white', color_func=green_color_func, stopwords=STOPWORDS).generate(positive_comments)
    neutral_wordcloud = WordCloud(width=400, height=200, background_color='white', colormap='gist_gray', stopwords=STOPWORDS).generate(neutral_comments)
    negative_wordcloud = WordCloud(width=400, height=200, background_color='white', colormap='Reds', stopwords=STOPWORDS).generate(negative_comments)

    return positive_wordcloud, neutral_wordcloud, negative_wordcloud

def wordcloud_to_image(wordcloud):
    buf = io.BytesIO()
    wordcloud.to_image().save(buf, format='PNG')
    buf.seek(0)
    return buf

def extract_keywords(df, sentiment, n=10):
    # Define unwanted keywords inside the function
    unwanted_keywords = ['neutrogena', 'im', 'just', 'like']
    
    comments = df[df['Sentiment'] == sentiment]['Cleaned_Comment']
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(comments)
    word_counts = X.sum(axis=0).A1
    keywords = [(word, word_counts[idx]) for word, idx in vectorizer.vocabulary_.items()]
    
    # Filter out unwanted keywords
    filtered_keywords = [kw for kw in keywords if kw[0] not in unwanted_keywords]
    
    sorted_keywords = sorted(filtered_keywords, key=lambda x: x[1], reverse=True)[:n]
    return sorted_keywords


# Components
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

# Colors for sentiments
sentiment_colors = {
    'positive': 'green',
    'neutral': 'grey',
    'negative': 'red'
}
comments_table = dash_table.DataTable(
    id='comments-table',
    columns=[
        {'name': 'Comments', 'id': 'Comment'},
        {'name': 'Source', 'id': 'Source'},
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
# Dropdown to select source
source_dropdown = dcc.Dropdown(
    id='source-dropdown',
    options=[
        {'label': 'All', 'value': ''},
        {'label': 'YouTube', 'value': 'YouTube'},
        {'label': 'Reddit', 'value': 'Reddit'}
    ],
    value='',
    clearable=False,
    style={'margin-bottom': '20px'}
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
        source_dropdown,
        dbc.Container(id='charts-container'),
        comments_table_container
    ],
    fluid=True,
    style=LAYOUT_STYLE,
)

@app.callback(
    Output('charts-container', 'children'),
    Input('source-dropdown', 'value')
)
def update_charts(source):
    filtered_df = filter_df_by_source(df, source)
    
    sentiment_counts = filtered_df['Sentiment'].value_counts()
    labels_with_counts = [f'{label} ' for label, count in zip(sentiment_counts.index, sentiment_counts.values)]
    
    net_sentiment_counts = filtered_df[filtered_df['Sentiment'] != 'neutral']['Sentiment'].value_counts()
    net_labels_with_counts = [f'{label} ' for label, count in zip(net_sentiment_counts.index, net_sentiment_counts.values)]

    # Donut chart for sentiment count
    donut_chart = go.Figure(data=[go.Pie(
        labels=labels_with_counts,
        values=sentiment_counts.values,
        hole=.3,
        textinfo='label+percent', 
        hoverinfo='label+value+percent',
        marker=dict(colors=[sentiment_colors[label.strip()] for label in sentiment_counts.index])
    )])

    donut_chart.update_layout(
        title_text='Sentiment Distribution',
        annotations=[dict(text='Sentiment', x=0.5, y=0.5, font_size=12, showarrow=False)],
        showlegend=False
    )

    # Net sentiment donut chart
    net_donut_chart = go.Figure(data=[go.Pie(
        labels=net_labels_with_counts,
        values=net_sentiment_counts.values,
        hole=.3,
        textinfo='label+percent', 
        hoverinfo='label+value+percent',
        marker=dict(colors=[sentiment_colors[label.strip()] for label in net_sentiment_counts.index])
    )])

    net_donut_chart.update_layout(
        title_text='Net Sentiment Distribution (Positive vs Negative)',
        annotations=[dict(text='Net Sentiment', x=0.5, y=0.5, font_size=12, showarrow=False)],
        showlegend=False
    )

    # Custom legend
    custom_legend = html.Div(
        [
            html.Span("Sentiment: ", style={'font-weight': 'bold'}),
            html.Span("Positive", style={'color': sentiment_colors['positive'], 'margin-right': '10px'}),
            html.Span("Neutral", style={'color': sentiment_colors['neutral'], 'margin-right': '10px'}),
            html.Span("Negative", style={'color': sentiment_colors['negative']})
        ],
        style={'text-align': 'center', 'margin-top': '10px'}
    )

    # Donut charts container
    donut_charts_container = dbc.Container(
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=donut_chart), width=6),
                dbc.Col(dcc.Graph(figure=net_donut_chart), width=6)
            ]
        ),
        style=PLOT_CONTAINER_STYLE
    )

    # Weekly sentiment bar chart
    weekly_sentiment = filtered_df.groupby(['Week', 'Sentiment']).size().unstack(fill_value=0)

    bar_chart = go.Figure()

    # Add positive sentiments
    if 'positive' in weekly_sentiment:
        bar_chart.add_trace(go.Bar(
            x=weekly_sentiment.index,
            y=weekly_sentiment['positive'],
            name='Positive',
            marker_color=sentiment_colors['positive']
        ))

    # Add neutral sentiments
    if 'neutral' in weekly_sentiment:
        bar_chart.add_trace(go.Bar(
            x=weekly_sentiment.index,
            y=weekly_sentiment['neutral'],
            name='Neutral',
            marker_color=sentiment_colors['neutral']
        ))

    # Add negative sentiments (inverted to point downwards)
    if 'negative' in weekly_sentiment:
        bar_chart.add_trace(go.Bar(
            x=weekly_sentiment.index,
            y=-weekly_sentiment['negative'],
            name='Negative',
            marker_color=sentiment_colors['negative']
        ))

    bar_chart.update_layout(
        title='Weekly Sentiment',
        xaxis_title='Time',
        yaxis_title='Count',
        barmode='group',
        bargap=0.2,
        bargroupgap=0.1,
        showlegend=False
    )

    bar_chart_custom_legend = html.Div(
        [
            html.Span("Sentiment: ", style={'font-weight': 'bold'}),
            html.Span("Positive", style={'color': sentiment_colors['positive'], 'margin-right': '10px'}),
            html.Span("Neutral", style={'color': sentiment_colors['neutral'], 'margin-right': '10px'}),
            html.Span("Negative", style={'color': sentiment_colors['negative']})
        ],
        style={'text-align': 'center', 'margin-top': '10px'}
    )

    sentiment_plot_container = dbc.Container(
        children=[
            dcc.Graph(figure=bar_chart),
            bar_chart_custom_legend
        ],
        style=PLOT_CONTAINER_STYLE
    )

    positive_wordcloud, neutral_wordcloud, negative_wordcloud = generate_wordclouds(filtered_df)
    positive_image = wordcloud_to_image(positive_wordcloud)
    neutral_image = wordcloud_to_image(neutral_wordcloud)
    negative_image = wordcloud_to_image(negative_wordcloud)

    wordcloud_container = dbc.Container(
        children=[
            html.H4("Word Cloud Sentiment", style={'text-align': 'center'}),
            dbc.Row(
                [
                    dbc.Col(html.Img(src="data:image/png;base64,{}".format(base64.b64encode(positive_image.read()).decode())), width=4),
                    dbc.Col(html.Img(src="data:image/png;base64,{}".format(base64.b64encode(neutral_image.read()).decode())), width=4),
                    dbc.Col(html.Img(src="data:image/png;base64,{}".format(base64.b64encode(negative_image.read()).decode())), width=4),
                ],
            ),
            html.Div(
                [
                    html.Span("Word Cloud Sentiment: ", style={'font-weight': 'bold'}),
                    html.Span("Positive", style={'color': sentiment_colors['positive'], 'margin-right': '10px'}),
                    html.Span("Neutral", style={'color': sentiment_colors['neutral'], 'margin-right': '10px'}),
                    html.Span("Negative", style={'color': sentiment_colors['negative']})
                ],
                style={'text-align': 'center', 'margin-top': '10px'}
            )
        ],
        style=PLOT_CONTAINER_STYLE
    )
    # Extract top keywords for each sentiment
    positive_keywords = extract_keywords(filtered_df, 'positive')
    neutral_keywords = extract_keywords(filtered_df, 'neutral')
    negative_keywords = extract_keywords(filtered_df, 'negative')

    # Keywords container
    keywords_container = dbc.Container(
        children=[
            html.H4("Top Keywords", style={'text-align': 'center'}),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H5("Positive"),
                                dash_table.DataTable(
                                    columns=[{"name": "Keyword", "id": "Keyword"}, {"name": "Count", "id": "Count"}],
                                    data=[{"Keyword": keyword, "Count": count} for keyword, count in positive_keywords],
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
                            ]
                        ),
                        width=4
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H5("Neutral"),
                                dash_table.DataTable(
                                    columns=[{"name": "Keyword", "id": "Keyword"}, {"name": "Count", "id": "Count"}],
                                    data=[{"Keyword": keyword, "Count": count} for keyword, count in neutral_keywords],
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
                            ]
                        ),
                        width=4
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H5("Negative"),
                                dash_table.DataTable(
                                    columns=[{"name": "Keyword", "id": "Keyword"}, {"name": "Count", "id": "Count"}],
                                    data=[{"Keyword": keyword, "Count": count} for keyword, count in negative_keywords],
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
                            ]
                        ),
                        width=4
                    ),
                ]
            )
        ],
        style=PLOT_CONTAINER_STYLE
    )

    return [donut_charts_container, custom_legend, sentiment_plot_container, wordcloud_container, keywords_container]


@app.callback(
    Output('comments-table', 'data'),
    [Input('comments-table', 'page_current'),
     Input('comments-table', 'page_size'),
     Input('source-dropdown', 'value')]
)
def update_comments_table(page_current, page_size, source):
    filtered_df = filter_df_by_source(df, source)
    start = page_current * page_size
    end = start + page_size
    paginated_df = filtered_df[['Comment', 'Source', 'Sentiment', 'Sentiment_Score']].iloc[start:end].copy()
    return paginated_df.to_dict('records')

# running the dashboard locally on http://127.0.0.1:8050/
if __name__ == '__main__':
    port = 8050
    webbrowser.open(f'http://127.0.0.1:{port}')
    app.run(debug=False, port=port)
    print("running the dashboard locally on http://127.0.0.1:8050/")
