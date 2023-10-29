import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go


START = "2011-01-01"
TODAY = date.today().strftime("2023-10-29")

st.title("Stock Predictor")

stocks  = ('^NYFANG', 'RELIANCE.NS', 'TATAMOTORS.NS', 'KPITTECH.NS', 'TATAPOWER.NS','TITAN.NS','BTC-USD')
selected_stock = st.selectbox('Select Stock: ', stocks)

n_years = st.slider("Years of prediction:", 1,5)

period = n_years * 365


def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace = True)
    return data

data_load_state = st.text("Loading data...")
data  = load_data(selected_stock)
data_load_state.text("Data Loaded!....")

st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = data['Date'], y = data['Open'], name = 'stock_open', line=dict(color='red')))
    fig.add_trace(go.Scatter(x = data['Date'], y = data['Close'], name = 'stock_close', line=dict(color='green')))
    fig.layout.update(title_text = "Time Series Data", xaxis_rangeslider_visible = True)
    st.plotly_chart(fig)

plot_raw_data()

# Forecasting
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns = {"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=int(period))

forecast = m.predict(future)
st.subheader('Forecast data')
st.write(forecast.tail())

st.write('Forecast Data')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1,line=dict())

st.write("Forecast Components")
fig2 = m.plot_components(forecast)
st.write(fig2)