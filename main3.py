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

        # Display the data in pandas DataFrame format
        st.write("Balance Sheet:")
        st.dataframe(balance_sheet)

        st.write("\nIncome Statement:")
        st.dataframe(income_statement)

        st.write("\nCash Flow Statement:")
        st.dataframe(cash_flow)

if __name__ == "__main__":
    main()

