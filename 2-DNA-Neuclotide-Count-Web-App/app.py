import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title= "DNA App" , layout="wide" )

st.write(""" # DNA Nucleotide Count """)

sample_sequence = """GCCTCCAGAGTCAAATCCCGTGATAGAAATATCGAACGCTACTGTGATAAAATACGTGGT
GACGAACCCATATCGCGGTAGCAGTCATTACGGATGGCACCGATTCCTGGGGAGAGAAAT
CCGGCCTAGGTCTAGCGTCGATAGCCATCGCGCCGATGGGCATAACTCTTCTGATATTGA
AGGTGGACACCATACTCGTCTGCAAGAGGACCAGAACCCGATATATTCTCACACTTAGTC
CATATAGTGACCAAAACCTATTGCCCGTGCAGACAACGTGGCTAAAACGTGGTGGGTTTG
TGGACTTAGTAGGTCTATTTGCGATGACGGGGCCAGGCTCTCCTGCGACGCACCGAACGT
TTTTCGATCTGCCTTCGAAGTTTAACCCCACTTGTATGTCGGTATCCCGCCCTCAGTAAA
CGGCTAGGGCCCAGTGTCCTGGACTTCCCGCAGTAAGTTCTCAGTCATGTACCGTACACG
GTTGATAGTCTACAAGCTTCCCTGCGGCCGTGAGCTCATATAGAGCTGTAAGGTCACTTG
GTCGTATGTCCCATTGGGCGGTCCATTATGGACAAAGCGGTATCGTTTGGGCTGCCACCT
AAAGATTGCGTCGTAAGTACTTAAACCAGACAAAAACATTGTGAACGCTTCAGAAAGAAA
TAACACGTTCACACACGGCGCTTTCGACTGTCGCAATCCGGGTAACGAGCGAGTTAACTC
AACCGTGCCAGACGCCTCAGTTGAGAAGACTGCAAACAGCTCGGCCCGAGAACAATGTCG
ATGTCAAATGAAACCATGGTGTCAGTACGATAGTCATGGACTAGTAGTCAGGTGAGAAGC
TACGCCAATTATGTTCCAGGTCATTGTTAAAGGGTCTGATGGGAGCAGAGGCCGAGTTGA
TTATGTTGGCAGCTTTTAGCGCGGCATGCCAGACATAGATCCGGGATTCGACGTCAAAGT
GTAGTGGCGGTGGGTGACCTGGCATCCGTATAACACCGAT"""

st.write("#### Enter the DNA pattern/sequence:")
sequence = st.text_area("",sample_sequence , height = 250)
sequence = sequence.splitlines()
sequence = "".join(sequence)

st.write(""" ### DNA Sequence Insights """)

dna_summary = {"Nucleotide" : ["A","C","G","T"],
               "Counts" : [sequence.count("A"),sequence.count("C"),sequence.count("G"),sequence.count("T")]}

data = pd.DataFrame.from_dict(dna_summary)
col1 , col2 = st.columns((1,2))
with col1:
    fig = go.Figure(
        data = [go.Table (columnorder = [0,1,2], columnwidth = [10,10,10],
                          header = dict(
                              values = list(data.columns),
                              font=dict(size=28, color = 'white'),
                              fill_color = '#264653',
                              line_color = 'rgba(255,255,255,0.2)',
                              align = ['left','center'],
                              height=60
                          )
                          , cells = dict(
                values = [data[K].tolist() for K in data.columns],
                font=dict(size=12 , color = "black"),
                align = ['left','center'],
                line_color = 'rgba(255,255,255,0.2)',
                height=50))])
    fig.update_layout(title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.bar(data,x="Nucleotide",y="Counts")
    st.plotly_chart(fig)