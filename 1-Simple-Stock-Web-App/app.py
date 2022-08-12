import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title= "Stocks Tracker" , layout="wide" )

st.write("""
# STOCK PRICE APP
## tracking stocks from yahoo-finance
""")

opt1 , opt2 ,opt3 = st.columns((1,1,1))
with opt1:
    symbol = st.text_input("Enter the ticker symbol","APL")
with opt2:
    startDate = st.date_input("Starting date", datetime.date(2005, 1, 1))
with opt3:
    endDate = st.date_input("End date",datetime.datetime.now())

chart1 , chart2 = st.columns((1,1.5))

data =  yf.Ticker(symbol)
df = data.history(period = "1d", start = startDate , end = endDate)
stock = df[["Open" ,"High" , "Low" , "Close" , "Volume"]]
stock = pd.DataFrame.round(stock,2)

if stock.empty:
    st.write("NO record against this symbol found!")
else:
    with chart1:
        st.write("### HISTORICAL DATA")
        fig = go.Figure(
            data = [go.Table (columnorder = [0,1,2,3,4,5], columnwidth = [10,10,10,10,10,10],
                              header = dict(
                                  values = list(stock.columns),
                                  font=dict(size=12, color = 'white'),
                                  fill_color = '#264653',
                                  line_color = 'rgba(255,255,255,0.2)',
                                  align = ['left','center'],
                                  height=40
                              )
                              , cells = dict(
                    values = [stock[K].tolist() for K in stock.columns],
                    font=dict(size=12 , color = "black"),
                    align = ['left','center'],
                    line_color = 'rgba(255,255,255,0.2)',
                    height=50))])
        fig.update_layout(title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)
        st.plotly_chart(fig, use_container_width=True)

    with chart2:
        st.write("### QUICK SUMMARY")
        var = st.selectbox('Choose Variable :', stock.columns)

        fig = px.line(stock, x=df.index, y=var)

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title=var,
            width = 750,
            height = 500
        )

        st.plotly_chart(fig)