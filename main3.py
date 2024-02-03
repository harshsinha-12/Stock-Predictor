import yfinance as yf
import streamlit as st
import pandas as pd

# Function to convert DataFrame values to crores
def convert_to_crores(df):
    return df.apply(lambda x: x / 10000000)

# Streamlit application
def main():
    st.title('Financial Statement Viewer')

    # User input for the ticker symbol
    tickerSymbol = st.text_input('Enter the Stock Ticker Symbol (e.g., RELIANCE.NS)', 'RELIANCE.NS')
    st.text('Note: For Indian stocks, use the ".NS" extension. For US stocks, use the stock symbol only.')
    st.text('For example, for Reliance Industries, use "RELIANCE.NS" and for Apple Inc., use "AAPL"')
    st.text('For a list of stock symbols, visit https://in.finance.yahoo.com/ or https://finance.yahoo.com/')
    st.text("All data is in Crores of Indian Rupees (INR) or US Dollars (USD) as applicable.")
    st.write('You entered:', tickerSymbol)
    # Radio button for selecting annual or quarterly data
    data_frequency = st.radio("Select Data Frequency", ('Annual', 'Quarterly'))

    if tickerSymbol:
        # Get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)

        # Get financial statements based on the selected frequency
        if data_frequency == 'Annual':
            balance_sheet = convert_to_crores(tickerData.balance_sheet)
            income_statement = convert_to_crores(tickerData.financials)
            cash_flow = convert_to_crores(tickerData.cashflow)
        else:  # Quarterly data
            balance_sheet = convert_to_crores(tickerData.quarterly_balance_sheet.iloc[:, :5])
            income_statement = convert_to_crores(tickerData.quarterly_financials.iloc[:, :5])
            cash_flow = convert_to_crores(tickerData.quarterly_cashflow.iloc[:, :5])

        # Display and allow download of the data in pandas DataFrame format
        display_and_download_data("Balance Sheet", balance_sheet)
        display_and_download_data("Income Statement", income_statement)
        display_and_download_data("Cash Flow Statement", cash_flow)

def display_and_download_data(title, data):
    st.write(title)
    st.dataframe(data)
    csv = convert_df_to_csv(data)
    st.download_button(label=f"Download {title} as CSV",data=csv,file_name=f"{title.lower().replace(' ', '_')}_last_5_quarters_crores.csv",mime='text/csv')

def convert_df_to_csv(data):
    return data.to_csv().encode('utf-8')

if __name__ == "__main__":
    main()
