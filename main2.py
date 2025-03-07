import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objs as go
from datetime import date

st.title("Stock Price Predictor")

# Input selection
custom_today = st.date_input("Select a custom 'today' date:", date.today())
custom_stocks = st.text_input("Enter custom stock symbols (comma-separated, e.g., RELIANCE.NS, TCS.NS) or select from the list below:")
stocks = custom_stocks.split(',') if custom_stocks else ['RELIANCE.NS', 'TATAMOTORS.NS', 'KPITTECH.NS', 'TATAPOWER.NS', 'TITAN.NS', 'BTC-USD']
selected_stock = st.selectbox('Select Stock:', stocks)
n_years = st.slider("Years of prediction:", 1, 5)
period = n_years * 365
START = "2011-01-01"

@st.cache_data
def load_data(ticker, custom_today):
    try:
        data = yf.download(ticker, START, custom_today.strftime("%Y-%m-%d"))
        if data.empty:
            st.error(f"Failed to fetch data for {ticker}. The ticker might be incorrect or delisted.")
            return None
        data.reset_index(inplace=True)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

# Load data
data_load_state = st.text("Loading data...")
data = load_data(selected_stock, custom_today)
data_load_state.text("Data Loaded!" if data is not None else "Data Loading Failed!")

if data is not None and len(data) > 2:
    df_train = data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})
    
    try:
        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=int(period))
        forecast = m.predict(future)

        # Display Prediction
        last_date = forecast['ds'].iloc[-1]
        last_yhat_lower = forecast['yhat_lower'].iloc[-1]
        last_yhat_upper = forecast['yhat_upper'].iloc[-1]

        col1, col2, col3 = st.columns(3)
        col1.metric("Prediction Date", last_date.date())
        col2.metric("Lower Estimate", f"{last_yhat_lower:.2f}")
        col3.metric("Upper Estimate", f"{last_yhat_upper:.2f}")

        # Raw Data
        st.subheader('Raw data')
        st.write(data.tail())

        def plot_raw_data(data):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Open', line=dict(color='red')))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close', line=dict(color='green')))
            fig.update_layout(title="Stock Price Over Time", xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)

        plot_raw_data(data)

        # Forecast Plot
        st.subheader('Forecast Data')
        st.write(forecast.tail())
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)
    
    except Exception as e:
        st.error(f"Error in prediction: {e}")

else:
    st.warning("Not enough data to perform predictions. Please select a valid stock symbol.")
