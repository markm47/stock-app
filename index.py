import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')

st.title('Stock Take')

stock = pd.read_csv('data/stock_clean.csv', index_col=None)

categories = stock['type'].unique().tolist()

tab_labels = [cat.capitalize() for cat in categories]

tabs = st.tabs(tabs=tab_labels)

for i, tab in enumerate(tabs):

  df = stock[stock['type'] == categories[i]]
  df = df.drop(['type'], axis=1)

  total_units = df['units'].sum()
  total_costs = df['cost'].sum()
  total_total = df['total'].sum()

  df_total = pd.DataFrame([
    {  'name': '', 'units': '', 'cost': '', 'total': '' },
    {  'name': '', 'units': 'Total Units', 'cost': 'Total Costs', 'total': 'Total' },
    {  'name': '', 'units': total_units, 'cost': total_costs, 'total': total_total },
  ], index=None)
  
  df = pd.concat([df, df_total], ignore_index=True)

  if tab.button('Print', key=i):
    # df.to_excel('data/test.xlsx')
    os.startfile('test.xlsx', 'print')

  tab.data_editor(df, use_container_width=True, height=600, num_rows='dynamic')
