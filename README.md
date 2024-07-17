# Brand Sentiment Analysis Dashboard

## Overview
This project is a dashboard for analyzing the sentiment of comments of Brand from YouTube and Reddit. It visualizes the data using various charts and tables to provide insights into customer sentiment.

## Features
1. Sentiment distribution donut charts.
2. Weekly sentiment bar chart.
3. Word clouds for positive, neutral, and negative sentiments.
4. Top keywords for each sentiment.
5. Data table displaying comments with sentiment scores.

## Prerequisites
To run this application, you'll need to have Python 3 installed along with the following Python packages:

- dash
- dash-bootstrap-components
- plotly
- pandas
- scikit-learn
- wordcloud

## Installation

Before running the code, ensure you have the required packages installed. You can install them using `pip`:

```sh
pip install dash dash-bootstrap-components plotly pandas scikit-learn wordcloud
```

## Running the Dashboard

To start the application, run the following command:

```sh
python app.py
```

This will launch the dashboard locally at http://127.0.0.1:8050/ and open it in your default web browser.