import streamlit as st
import pandas as pd

st.title('FP Dashboard')

st.info('MR Pack and Family planning dashboard')

df = pd.read_csv("https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv")
 
