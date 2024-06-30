# import packages
from dash import Dash, html, dcc, callback, Output, Input, clientside_callback, State, ALL, ctx, dash_table
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import plotly.io as pio
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import plotly.graph_objs as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import math
from PIL import Image
import io
import re
from datetime import datetime
from assets.styles import NAVBAR_STYLE, LAYOUT_STYLE, HEADER_TITLE_STYLE, PLOT_CONTAINER_STYLE

# initial variable for neutrogena
df1 = pd.read_csv('./youtube_sentiment/youtube_comments_with_sentiment.csv')
df2 = pd.read_csv('./reddit_sentiment/neutrogena_reddit.csv')
df = pd.concat([df1, df2], ignore_index=True)

sentiment_counts = df['Sentiment'].value_counts()
labels_with_counts = [f'{label} ' for label, count in zip(sentiment_counts.index, sentiment_counts.values)]

# Filter out neutral sentiments for net sentiment calculation
net_sentiment_counts = df[df['Sentiment'] != 'neutral']['Sentiment'].value_counts()
net_labels_with_counts = [f'{label} ' for label, count in zip(net_sentiment_counts.index, net_sentiment_counts.values)]

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

# Filter comments based on sentiment
positive_comments = " ".join(comment for comment in df[df.Sentiment == 'positive'].Cleaned_Comment)
neutral_comments = " ".join(comment for comment in df[df.Sentiment == 'neutral'].Cleaned_Comment)
negative_comments = " ".join(comment for comment in df[df.Sentiment == 'negative'].Cleaned_Comment)

# Generate the word clouds
positive_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Blues', stopwords=STOPWORDS.union(additional_stopwords)).generate(positive_comments)
neutral_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='gist_gray', stopwords=STOPWORDS.union(additional_stopwords)).generate(neutral_comments)
negative_wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Reds', stopwords=STOPWORDS.union(additional_stopwords)).generate(negative_comments)

fig, ax = plt.subplots(1, 3, figsize=(20, 10))

# Positive words cloud
ax[0].imshow(positive_wordcloud, interpolation='bilinear')
ax[0].set_title('Positive Sentiment', fontsize=20)
ax[0].axis('off')

# Neutral words cloud
ax[1].imshow(neutral_wordcloud, interpolation='bilinear')
ax[1].set_title('Neutral Sentiment', fontsize=20)
ax[1].axis('off')

# Negative words cloud
ax[2].imshow(negative_wordcloud, interpolation='bilinear')
ax[2].set_title('Negative Sentiment', fontsize=20)
ax[2].axis('off')

# Convert Matplotlib figure to PNG image
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
img = Image.open(buf) 

# Convert the image to a Plotly figure
wordcloud_fig = go.Figure()

# Add layout image to the Plotly figure
wordcloud_fig.add_layout_image(
    dict(
        source=img,
        x=0,
        y=1,
        sizex=1,
        sizey=1,
        xref="paper",
        yref="paper",
        opacity=1,
        layer="below"
    )
)

wordcloud_fig.update_layout(
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    margin=dict(l=0, r=0, t=0, b=0)
)


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

# Colors for sentiments
sentiment_colors = {
    'positive': 'blue',
    'neutral': 'grey',
    'negative': 'red'
}

# donut chart for sentiment count
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

# Create the net sentiment donut chart
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

# Container for both donut charts side by side
donut_charts_container = dbc.Container(
    dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=donut_chart), width=6),
            dbc.Col(dcc.Graph(figure=net_donut_chart), width=6)
        ]
    ),
    style=PLOT_CONTAINER_STYLE
)

# bar chart for weekly sentiment
weekly_sentiment = df.groupby(['Week', 'Sentiment']).size().unstack(fill_value=0)

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

# Update layout
bar_chart.update_layout(
    title='Weekly Sentiment',
    xaxis_title='Time',
    yaxis_title='Count',
    barmode='group',
    bargap=0.2,
    bargroupgap=0.1,
    showlegend=False
)

# Custom legend for bar chart
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

wordcloud_container = dbc.Container(
    dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=wordcloud_fig)),
       ], 
    ),
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
        donut_charts_container,
        custom_legend,
        sentiment_plot_container,
        wordcloud_container,
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

    comments_df = df

    # Modify headlines to include anchor tags
    paginated_df = comments_df[['Comment', 'Source', 'Sentiment', 'Sentiment_Score']].iloc[start:end].copy()
    # paginated_df['Headline'] = paginated_df.apply(lambda row: f"[{row['Headline']}]({row['URL']})", axis=1)

    return paginated_df.to_dict('records')

# running the dashboard locally on http://127.0.0.1:8050/
if __name__ == '__main__':
    app.run(debug=True)
