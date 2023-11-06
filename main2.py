
import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

st.title("Stock Predictor by Harsh")

# Custom "today" date input
custom_today = st.date_input("Select a custom 'today' date:", date.today())

# Custom stock names input
custom_stocks = st.text_input("Enter custom stock name (in format of Yahoo Finance like RELIANCE.NS or select from below select box):")

stocks = custom_stocks.split(',') if custom_stocks else ('^NYFANG', 'RELIANCE.NS', 'TATAMOTORS.NS', 'KPITTECH.NS', 'TATAPOWER.NS', 'TITAN.NS', 'BTC-USD')

selected_stock = st.selectbox('Select Stock:', stocks)

n_years = st.slider("Years of prediction:", 1, 5)

period = n_years * 365
START = "2011-01-01"
def load_data(ticker, custom_today):
    data = yf.download(ticker, START, custom_today.strftime("%Y-%m-%d"))
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Loading data...")
data = load_data(selected_stock, custom_today)
data_load_state.text("Data Loaded!....")

from tickertape import *

stock_exchanges = {
    "NSE": {
        "display": "NSE (🇮🇳)",
        "data": "data/NSE.json",
        "information_display": [
            tickertape_company_profile,
            tickertape_technical_analysis,
            tickertape_fundamental_data,
        ],
    }



def tickertape_company_profile(st, components, exchange, symbol):
    st.write("### Company Profile")
    components.html(
        """
            <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget"></div>
                <div class="tradingview-widget-copyright">
                    <a href="https://in.tradingview.com/symbols/$$exchange$$-$$symbol$$/" rel="noopener" target="_blank">
                    <!-- <span class="blue-text">$$symbol$$ Profile</span></a> Powered by TradingView -->
                </div>
                <script type="text/javascript" 
                src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-profile.js" async>
                    {
                    "symbol": "$$exchange$$:$$symbol$$",
                    "width": "100%",
                    "height": 300,
                    "colorTheme": "dark",
                    "isTransparent": false,
                    "locale": "in"
                    }
                </script>
            </div>
        """.replace(
            "$$symbol$$", symbol
        ).replace(
            "$$exchange$$", exchange
        ),
        height=300,
        scrolling=True,
    )


def tickertape_technical_analysis(st, components, exchange, symbol):
    st.write("### Technical Analysis")
    components.html(
        """
            <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget"></div>
                <div class="tradingview-widget-copyright">
                    <a href="https://in.tradingview.com/symbols/$$exchange$$-$$symbol$$/technicals/" 
                        rel="noopener" target="_blank">
                </div>
                <script type="text/javascript" 
                    src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {
                    "interval": "1m",
                    "width": "100%",
                    "isTransparent": false,
                    "height": 500,
                    "symbol": "$$exchange$$:$$symbol$$",
                    "showIntervalTabs": true,
                    "locale": "in",
                    "colorTheme": "dark"
                    }
                </script>
            </div>
        """.replace(
            "$$symbol$$", symbol
        ).replace(
            "$$exchange$$", exchange
        ),
        height=450,
        scrolling=True,
    )


def tickertape_fundamental_data(st, components, exchange, symbol):

    st.write("### Fundamental Data")
    components.html(
        """
            <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget"></div>
                <div class="tradingview-widget-copyright">
                    <a href="https://in.tradingview.com/symbols/$$exchange$$-$$symbol$$/financials-overview/" rel="noopener" target="_blank">
                </div>
                <script type="text/javascript" 
                src="https://s3.tradingview.com/external-embedding/embed-widget-financials.js" async>
                    {
                    "symbol": "$$exchange$$:$$symbol$$",
                    "colorTheme": "dark",
                    "isTransparent": false,
                    "largeChartUrl": "",
                    "displayMode": "regular",
                    "width": "100%",
                    "height": 450,
                    "locale": "in"
                    }
                </script>
            </div>
        """.replace(
            "$$symbol$$", symbol
        ).replace(
            "$$exchange$$", exchange
        ),
        height=450,
        scrolling=True,
    )

st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close', line=dict(color='green')))
    fig.update_layout(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Forecasting
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=int(period))

forecast = m.predict(future)
st.subheader('Forecast data')
st.write(forecast.tail())

st.write('Forecast Data')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast Components")
fig2 = m.plot_components(forecast)
st.write(fig2)
