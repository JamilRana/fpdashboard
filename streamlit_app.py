import streamlit as st
import pandas as pd

st.title('FP Dashboard')

st.info('MR Pack and Family planning dashboard')

with st.expender('Data'):
 st.write('**Raw Data**')
 df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')
 df 

st.write('**X**')
x = df.drop('species', axis =1)
x


 
