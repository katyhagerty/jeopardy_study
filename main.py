#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 21:37:39 2023

@author: katyhagerty
"""

import streamlit as st
import pandas as pd

from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.


# @st.cache_resource(ttl = 24*3600)
def create_connection():
    # create_connection
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"])
    client = bigquery.Client(credentials=credentials)
    return client


client = create_connection()

def run_query(query):
    # st.write(query)
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

# Reform list to syntax for query
def reformat(text):
    text = text.replace('[','(')
    text = text.replace(']',')')
    return text

def update():
    filters = []
    
    if 'filter_cat' in st.session_state and len(st.session_state.filter_cat) > 0:
        cats = reformat(str(st.session_state.filter_cat))
        # st.write(f'input parameter {cats}')
        filters.append(f'WHERE category IN {cats}')
        
    if 'filter_round' in st.session_state and len(st.session_state.filter_round) > 0:
        rounds = reformat(str(st.session_state.filter_round))
        filters.append(f'WHERE _round IN {rounds}')
        
    filters = ' AND '.join(filters)
    
    query_text = f'SELECT * FROM `jeopardy-396902.jeopardy.clues` {filters} order by RAND() LIMIT 1'
    rows = run_query(query_text)
    
    st.session_state.category = rows[0]['category']
    st.session_state.clue = rows[0]['text']
    st.session_state.answer = rows[0]['target']

def record():
    data = load_data(loc)
    data.loc[int(st.session_state.id), 'correct'] = 1
    data.to_csv(loc)


if 'category' not in st.session_state:
    update()

st.checkbox(
    label="Save",
    key="switch_1",
    # label_after="Saving session",
)

button = st.button('Show answer')  # , on_click= show_answer())
new_clue = st.button('New clue')  # , on_click = update())

if 'choices' or 'rounds' not in st.session_state:
    options = pd.DataFrame(run_query('SELECT category, COUNT(category) AS count FROM `jeopardy-396902.jeopardy.clues`  group by category HAVING count > 100'))
    options.sort_values(by = 'category', inplace = True)
    st.session_state['choices'] = list(options.category)
    rounds = pd.DataFrame(run_query('SELECT DISTINCT round_ FROM `jeopardy-396902.jeopardy.clues`'))
    st.session_state['rounds'] = list(rounds.round_)

filter_cat = st.multiselect('Categories', st.session_state.choices, key='filter_cat')
filter_round = st.multiselect('Round', st.session_state.rounds, key='filter_round')

if new_clue:
    update()

header = st.header(st.session_state.category)
clue_text = st.write(st.session_state.clue)


if button:
    target = st.write(st.session_state.answer)
else:
    target = st.empty()


# st.session_state
