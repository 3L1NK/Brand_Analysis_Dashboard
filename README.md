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
To run this application, you will need to have Python 3 installed along with the following Python packages:

- dash
- dash-bootstrap-components
- plotly
- pandas
- scikit-learn
- wordcloud

Here is the `requirements.txt` file for the specified Python libraries:

```
dash==2.9.3
dash-bootstrap-components==1.4.1
plotly==5.15.0
pandas==2.0.3
scikit-learn==1.3.0
wordcloud==1.9.2
```

## Installation and Setup

To run this application you will need to have Python 3 installed on your machine. Follow the steps below to set up your environment and run the application:

1. **Clone the repository**:
   ```sh
   git clone https://github.com/3L1NK/Brand_sentiment_analysis.git
   cd https://github.com/3L1NK/Brand_sentiment_analysis.git
   ```

2. **Create a virtual environment** (optional but recommended):
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```sh
   python app.py
   ```

## Running the Dashboard

To start the application, run the following command:

```sh
python app.py
```

This will launch the dashboard locally at http://127.0.0.1:8050/ and open it in your default web browser.
