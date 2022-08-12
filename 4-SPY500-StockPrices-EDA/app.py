import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests as re
import yfinance as yf
import streamlit as st
import base64

st.set_page_config(page_title= "SP500 EDA" , layout="wide" )

def load_data():
    response = re.get(url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",headers=0)
    df = pd.read_html(response.text)
    data = df[0]
    return data

sp_data = load_data()

sectors = sp_data.groupby("GICS Sector")
unique_sectors = list(sp_data["GICS Sector"].unique())
unique_sectors.sort()
selected_sectors = st.sidebar.multiselect("Sector" , unique_sectors)

selected_sector_data = sp_data[sp_data["GICS Sector"].isin(selected_sectors)]

st.write("""
# SP500 DATA
#### COMPANIES IN SELECTED SECTORS
""")
st.dataframe(selected_sector_data)

def file_download(data):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = "<a href = 'data:file/csv;base64,{0}' download='SP500.csv'>Download CSV file</a>".format(b64)
    return href

st.markdown(file_download(selected_sector_data),unsafe_allow_html=True)

def organize_data():
    df = pd.read_excel("stocks.xlsx" , header=[0,1])
    prices = df.drop("Unnamed: 0_level_0" , axis=1 , level=0)
    prices = prices.drop(0)
    dates = df["Unnamed: 0_level_0"][1:]
    dates.columns = ["Date"]
    stocks =  pd.concat([dates,prices] ,axis=1 )
    stocks = stocks.round(3)
    # stocks = stocks.drop(0)
    return stocks

# stocks = organize_data()
stocks = yf.download(tickers=list(selected_sector_data[:10].Symbol) , group_by="ticker" , period="ytd" , interval="1d")

num_companies = st.sidebar.slider("Number of Companies" , 1,10)

def price_plot(sym):
    df = pd.DataFrame(stocks[sym].Close)
    df["Date"] = df.index
    fig = plt.figure(figsize=(12,6))
    plt.title(sym)
    plt.fill_between(df.Date , df.Close , alpha=0.3)
    plt.plot(df.Date,df.Close,alpha=0.8)
    plt.xlabel("Date")
    plt.ylabel("Closing price")
    return st.pyplot(fig)

if st.button("Show Plots"):
    st.header("Stock Closing Prices")
    for i in list(selected_sector_data.Symbol)[:num_companies]:
        price_plot(i)

