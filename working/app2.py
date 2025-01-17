import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import pygwalker as pyg

def app2():


    df = pd.read_csv("wrestling_fake_data_Sheet1.csv")
    pyg_html = pyg.walk(df, return_html=True)

    components.html(pyg_html, height=1000, scrolling=True)
                    

    # #load local data file
    # @st.cache
    # def load_data():
    #   df = pd.read_csv("wrestling_fake_data_Sheet1.csv")
    #   return df
    
    # #set up Pygwalker
    # def load_config(file_path):
    #   with open(file_path, 'r') as config_file:
    #     config_str = config_file.read()
    #   return config_str
    # config = load_config('config.json')
    # pyg.walk(df, env='streamlit', dark='dark', spec=config)