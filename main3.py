import yfinance as yf
import streamlit as st
import pandas as pd

# Streamlit application
def main():
    st.title('Financial Statement Viewer')

    # User input for the ticker symbol
    tickerSymbol = st.text_input('Enter the Stock Ticker Symbol (e.g., RELIANCE.NS)', 'RELIANCE.NS')

    if tickerSymbol:
        # Get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)

        # Get financial statements
        balance_sheet = tickerData.balance_sheet
        income_statement = tickerData.financials
        cash_flow = tickerData.cashflow

        # Display and allow download of the data in pandas DataFrame format
        display_and_download_data("Balance Sheet", balance_sheet)
        display_and_download_data("Income Statement", income_statement)
        display_and_download_data("Cash Flow Statement", cash_flow)

def display_and_download_data(title, data):
    st.write(title)
    st.dataframe(data)
    csv = convert_df_to_csv(data)
    st.download_button(label=f"Download {title} as CSV",data=csv,file_name=f"{title.lower().replace(' ', '_')}.csv",mime='text/csv')

def convert_df_to_csv(data):
    return data.to_csv().encode('utf-8')

if __name__ == "__main__":
    main()
