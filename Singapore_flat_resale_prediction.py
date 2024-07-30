import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
st.set_page_config(page_title='SINGAPORE FLAT RESALE PREDICTION',layout="wide")
url="https://raw.githubusercontent.com/RajiVenkat89/SingaporeFlatResalePrediction/main/Model/Regression_model.pkl"
st.markdown(f'<h1 style= "text-align:center;size:24px;color:blue;">SINGAPORE FLAT RESALE PREDICTION</h1>',unsafe_allow_html=True)
st.header(":blue[**Welcome!!!**]")
town_df=pd.read_csv("https://raw.githubusercontent.com/RajiVenkat89/SingaporeFlatResalePrediction/main/Data/town_list.csv")
town_df=town_df.sort_values(by='town')
flat_type_df=pd.read_csv("https://raw.githubusercontent.com/RajiVenkat89/SingaporeFlatResalePrediction/main/Data/flat_type_list.csv")
flat_type_df=flat_type_df.sort_values(by='flat_type_int')
flat_model_df=pd.read_csv("https://raw.githubusercontent.com/RajiVenkat89/SingaporeFlatResalePrediction/main/Data/flat_model_list.csv")
flat_model_df=flat_model_df.sort_values(by='flat_model')
street_name_df=pd.read_csv("https://raw.githubusercontent.com/RajiVenkat89/SingaporeFlatResalePrediction/main/Data/street_list.csv")
street_name_df=street_name_df.sort_values(by='street_name')
storey_range_df=pd.read_csv("https://raw.githubusercontent.com/RajiVenkat89/SingaporeFlatResalePrediction/main/Data/storey_range_list.csv")
storey_range_df=storey_range_df.sort_values(by='storey_lower')
block_df=pd.read_csv("https://raw.githubusercontent.com/RajiVenkat89/SingaporeFlatResalePrediction/main/Data/block_list.csv")
block_df=block_df.sort_values(by='block_Integer')
years=list(range(1990,2025))
months=list(range(1,13))
col1,col2=st.columns(2)
with col1:
    year=st.selectbox("Registration Year",years)
    lease_commence_date=st.selectbox("Lease Year",years)
    street_name=st.selectbox("StreetName",street_name_df["street_name"])
    storey_range =st.selectbox("Storey Range",storey_range_df["storey_range"])
    flat_model=st.selectbox("Flat Model",flat_model_df["flat_model"])
with col2:    
    month_only=	st.selectbox("Registration Month",months)
    town=st.selectbox("Town",town_df["town"])
    block=st.selectbox("Block",block_df["block"])
    flat_type = st.selectbox("Flat Type",flat_type_df["flat_type"])
    floor_area_sqm=st.text_input("Floor Area(in Sqm)",value="")

town_int=town_df.loc[town_df['town'] == town, 'town_int'].iloc[0]
remaining_lease=99-(year-lease_commence_date)
storey_lower=storey_range_df.loc[storey_range_df['storey_range'] == storey_range, 'storey_lower'].iloc[0]
storey_upper=storey_range_df.loc[storey_range_df['storey_range'] == storey_range, 'storey_upper'].iloc[0]
block_Int = block_df.loc[block_df['block'] == block, 'block_Integer'].iloc[0]
block_alpint = block_df.loc[block_df['block'] == block, 'block_alp_int'].iloc[0]
flat_type_int=flat_type_df.loc[flat_type_df['flat_type'] == flat_type, 'flat_type_int'].iloc[0]
street_name_int=street_name_df.loc[street_name_df['street_name'] == street_name, 'street_name_int'].iloc[0]
flat_model_int=flat_model_df.loc[flat_model_df['flat_model'] == flat_model, 'flat_model_int'].iloc[0]
user_input=np.array([[floor_area_sqm,lease_commence_date,remaining_lease,year,month_only,storey_lower,storey_upper,block_Int,town_int,flat_type_int,block_alpint,street_name_int,flat_model_int]])

if(year>=lease_commence_date):
    col3,col4,col5=st.columns(3)
    with col4:
        select=st.button(":blue[**PREDICT RESALE PRICE**]")
        try:
                    if select:
                        #Loading the already available pickled Regression Model for Prediction
                        response = requests.get(url)
                        sp_model = pickle.loads(response.content)
                        Resale_price=sp_model.predict(user_input)
                        st.write(f":green[SELLING PRICE: {round(Resale_price[0],2)}]")
        except Exception as e:
                    st.write(e)    
                    st.write(":red[INVALID INPUT]")
else:
      st.write(":red[**Registration year should be greater than the lease year**]")                    