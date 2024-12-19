import streamlit as st
import yfinance as yf 
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Apple Stock", page_icon="💸")

st.title('Котировки компании Apple')
st.write('### Котировки акций на момент закрытия торгов')

ticker = 'AAPL'
tickData = yf.Ticker(ticker)
tickerDf = tickData.history(period='1d', start='2000-5-31', end='2024-5-31')

st.line_chart(tickerDf.Close)
st.write('### Количество ценных бумаг, участвующих в торгах')
st.line_chart(tickerDf.Volume)
