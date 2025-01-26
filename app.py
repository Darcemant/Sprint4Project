import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


st.header('Market of Vehicles in the US')
st.write('Filter the data below to see')

df = pd.read_csv("vehicles_us.csv")
df['price'] = df['price'].astype('float')
df['model_year'] = df['model_year'].fillna(df['model_year'].mean()).astype('int')
df['cylinders'] = df['cylinders'].fillna('Na').astype('str')
df['odometer'] = df['odometer'].fillna(df['odometer'].mean()).astype('int')
df['paint_color'] = df['paint_color'].fillna('Na')
df['date_posted'] = pd.to_datetime(df['date_posted'], format='%Y-%m-%d')

df['is_4wd'] = df['is_4wd'].fillna(0)
df['is_4wd'] = df['is_4wd'].astype('int')

make_choice = df['model'].unique()

selected_menu = st.selectbox('Select the Make', make_choice)

min_year, max_year = df['model_year'].min(), df['model_year'].max()

year_range = st.slider('Choose years', value=(min_year, max_year), min_value=min_year, max_value=max_year)

actual_range = list(range(year_range[0], year_range[1]+1))


df_filtered = df[ (df.model == selected_menu) & (df.model_year.isin(list(actual_range)) )]

df_filtered

st.header('Price Analysis')
st.write("""
         Let's look and see what influences the price the most. Let's check what influences the price based on...
         """)
list_for_hist = ['condition', 'type', 'paint_color', 'fuel']

selected_type = st.selectbox('Split for price distribution', list_for_hist)

fig1 = px.histogram(df, x="price", color=selected_type)
fig1.update_layout(title= "<b> Split of price by {}</b>".format(selected_type))

st.plotly_chart(fig1)

df['car_age'] = 2025 - df['model_year']

def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'

df['age_category'] = df['car_age'].apply(age_category)


list_for_scatter = ['odometer', 'cylinders', 'days_listed']

choice_for_scatter = st.selectbox('Price dependency on', list_for_scatter)

fig2 = px.scatter(df, x="price", y=choice_for_scatter, color='age_category', hover_data=['model_year'])
fig2.update_layout(title="<b> Price vs {}</b>".format(choice_for_scatter))
st.plotly_chart(fig2)
