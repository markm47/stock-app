import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')

st.title('Stock Take')

# Load the initial stock data
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

  # Add totals as strings
  df_total = pd.DataFrame([
    {'name': '', 'units': '', 'cost': '', 'total': ''},
    {'name': '', 'units': 'Total Units', 'cost': 'Total Costs', 'total': 'Total'},
    {'name': '', 'units': str(total_units), 'cost': str(total_costs), 'total': str(total_total)},
  ], index=[len(df), len(df) + 1, len(df) + 2])

  df_new = pd.concat([df, df_total], ignore_index=False)

  # Convert numeric columns to strings to handle mixed data types
  df_new[['units', 'cost', 'total']] = df_new[['units', 'cost', 'total']].astype(str)

  df_new = df_new.reset_index(drop=True)

  # Streamlit data editor that allows the user to modify the DataFrame
  edited_df = tab.data_editor(df_new, use_container_width=True, height=600, num_rows='dynamic', disabled=False, hide_index=True)

  # When the save button is pressed
  if tab.button('Save', key=i):
    # Convert numeric columns back to their original types
    edited_df[['units', 'cost', 'total']] = edited_df[['units', 'cost', 'total']].apply(pd.to_numeric, errors='coerce')

    # Remove the total rows before saving (using indices)
    edited_df = edited_df.drop([len(df), len(df) + 1, len(df) + 2])

    # Add back the 'type' column with the corresponding category value
    edited_df['type'] = categories[i]

    # Append the edited data back to the main stock DataFrame
    stock.update(edited_df)

    # Save the updated DataFrame back to the CSV file
    stock.to_csv('data/stock_clean.csv', index=False)
    st.success(f'Data for {categories[i]} saved successfully!')
