#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 21:37:39 2023

@author: katyhagerty
"""

import streamlit as st
import pandas as pd
# from streamlit_toggle import st_toggle_switch

# loc = 'all_data_v2.csv'

# import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows


# st.cache_data()
# def load_data(loc):
#     data = pd.read_csv(loc)
    
#     if 'filter_cat' in st.session_state:
#         if len(st.session_state.filter_cat) > 0:
#             data = data[data.category.isin(st.session_state.filter_cat)]
    
#     return data

# data = load_data(loc)

def display_clue(df):
    category = df.category.iloc[0].upper()
    clue = df.text.iloc[0]
    return category,clue
    
# def display_answer(df):
#     return df.target.iloc[0]
    
def pick_clue(data):
    return data.sample(1)

def show_answer():
    # answer = df.target.iloc[0]
    # st.session_state.answer = answer
    # target.write(st.session_state.answer)
    'show_answer'
    st.session_state.answer
    # function displays answer but nothing ever removes it afterwards
    
def update():
    # data = load_data(loc)
    # df = pick_clue(data)
    # category, clue = display_clue(df)
    if 'filter_cat' in st.session_state:
        if len(st.session_state.filter_cat) >0:
            cats = tuple(st.session_state.filter_cat)
            rows = run_query(f'SELECT * FROM `jeopardy-396902.jeopardy.clues` WHERE category IN {cats} order by RAND() LIMIT 1')
    else:
        rows = run_query('SELECT * FROM `jeopardy-396902.jeopardy.clues` order by RAND() LIMIT 1')
    
    # st.session_state.id = 
    st.session_state.category = rows[0]['category']
    st.session_state.clue = rows[0]['text']
    st.session_state.answer = rows[0]['target']
    
    # return df
    
# def find_choices():
#     all_data = pd.read_csv('clues.csv')
#     cats = all_data.groupby(by = 'category').count().reset_index()
#     options = set(cats[cats['round_'] >= 100].category)
#     st.session_state.choices = options
    
#     return st.session_state.choices

def record():
    data = load_data(loc)
    data.loc[int(st.session_state.id), 'correct'] = 1
    data.to_csv(loc)
    
if 'category' not in st.session_state:
    # 'category not in session state'
    # data = load_data(loc)
    update()
    # clue = run_query('SELECT * FROM `jeopardy-396902.jeopardy.clues` LIMIT 1')
    # st.session_state.id = df.index[0]
    # st.session_state.category = category
    # st.session_state.clue = clue
    # st.session_state.answer = df.target.iloc[0]

st.checkbox(
    label="Save",
    key="switch_1",
    # label_after="Saving session",
)

# on_click called with every update even if button was not clicked prior
button = st.button('Show answer') #, on_click= show_answer())
new_clue = st.button('New clue') #, on_click = update())
# correct = st.button('Correct', on_click = record)

if 'choices' or 'rounds' not in st.session_state:
    # all_data = pd.read_csv(loc)
    # cats = all_data.groupby(by = 'category').count().reset_index()
    options = pd.DataFrame(run_query('SELECT category, COUNT(category) AS count FROM `jeopardy-396902.jeopardy.clues`  group by category HAVING count > 100'))
    st.session_state['choices'] = list(options.category)
    rounds = pd.DataFrame(run_query('SELECT DISTINCT round_ FROM `jeopardy-396902.jeopardy.clues`'))
    st.session_state['rounds'] = list(rounds.round_)
# print(st.session_state)

filter_cat = st.multiselect('Categories', st.session_state.choices, key = 'filter_cat')
filter_round = st.multiselect('Round', st.session_state.rounds, key = 'filter_round')

if new_clue:
    update()

header = st.header(st.session_state.category)
clue_text = st.write(st.session_state.clue)
# target = st.empty()
    

if button:
    target = st.write(st.session_state.answer)
else:
    target = st.empty()

    
st.session_state
