import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objs as go
from datetime import date


st.title("Future Price Predictor")

# Input selection
custom_today = st.date_input("Select a custom 'today' date:", date.today())
custom_stocks = st.text_input("Enter custom stock name (in format of Yahoo Finance like RELIANCE.NS or select from below select box):")
stocks = custom_stocks.split(',') if custom_stocks else ['^NYFANG', 'RELIANCE.NS', 'TATAMOTORS.NS', 'KPITTECH.NS', 'TATAPOWER.NS', 'TITAN.NS', 'BTC-USD']
selected_stock = st.selectbox('Select Stock:', stocks)
n_years = st.slider("Years of prediction:", 1, 5)
period = n_years * 365
START = "2011-01-01"

@st.cache_data
def load_data(ticker, custom_today):
    data = yf.download(ticker, START, custom_today.strftime("%Y-%m-%d"))
    data.reset_index(inplace=True)
    return data

# Load data
data_load_state = st.text("Loading data...")
data = load_data(selected_stock, custom_today)
data_load_state.text("Data Loaded!")

df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=int(period))
forecast = m.predict(future)

# Calculate and display prediction limits
last_date = forecast['ds'].iloc[-1]
last_yhat_lower = forecast['yhat_lower'].iloc[-1]
last_yhat_upper = forecast['yhat_upper'].iloc[-1]
col3, col4, col5 = st.columns(3)
col3.markdown(f"Predicted Price Range for {last_date.date()}:")
col4.metric("Lower Estimate:", f"{last_yhat_lower:.2f}")
col5.metric(" Upper Estimate:", f"{last_yhat_upper:.2f}")

# st.markdown(f"### Predicted Price Range for {last_date.date()}:")
# st.markdown(f"#### Lower Estimate: ${last_yhat_lower:.2f}")
# st.markdown(f"#### Upper Estimate: ${last_yhat_upper:.2f}")

# Plotting raw data
st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close', line=dict(color='green')))
    fig.update_layout(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
plot_raw_data(data)

# Display forecast
st.subheader('Forecast data')
st.write(forecast.tail())
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)
