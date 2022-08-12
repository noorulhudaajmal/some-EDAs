from app import  load_data
import yfinance as yf

sp_data = load_data()
stocks = yf.download(tickers=list(sp_data.Symbol) , group_by="ticker" , period="ytd" , interval="1d")

stocks.to_excel("stocks.xlsx")
