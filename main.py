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

import time
from st_login_form import login_form


# Create API client.
@st.cache_resource(ttl=24*3600)  # , validate = clues_remaining)
def create_connection():
    # create_connection
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"])
    client = bigquery.Client(credentials=credentials)
    return client

def run_query(query):
    # st.write(query)
    st.cache_data.clear()
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

# Reform list to syntax for query


def reformat(text):
    text = text.replace('[', '(')
    text = text.replace(']', ')')
    return text


def update():

    filters = []

    if 'filter_cat' in st.session_state and len(st.session_state.filter_cat) > 0:
        cats = reformat(str(st.session_state.filter_cat))
        # st.write(f'input parameter {cats}')
        filters.append(f'category IN {cats}')

    if 'filter_round' in st.session_state and len(st.session_state.filter_round) > 0:
        rounds = reformat(str(st.session_state.filter_round))
        filters.append(f'round_ IN {rounds}')

    if len(filters) > 1:
        filters = 'WHERE ' + ' AND '.join(filters)
    else:
        filters = f'WHERE {filters[0]}'

    query_text = f'SELECT id,category,text,target,date,value,daily_double FROM `jeopardy-396902.jeopardy.clues` {filters} order by RAND() LIMIT 100'
    # query_text
    rows = run_query(query_text)

    if len(rows) == 0:
        st.balloons()
        st.info(
            'You already no all the clues that match these filters. Please change filter options')
    else:
        st.session_state.df = pd.DataFrame(rows)
        pick_clue()


def pick_clue():
    if len(st.session_state.df) == 0:
        update()
    else:
        
        rows = st.session_state.df
    
        st.session_state.id = rows['id'].iloc[0]
        st.session_state.category = rows['category'].iloc[0]
        st.session_state.clue = rows['text'].iloc[0]
        st.session_state.answer = rows['target'].iloc[0]
        st.session_state.display_answer = ''
        st.session_state.date = rows['date'].iloc[0]
        st.session_state.value = rows['value'].iloc[0]
        st.session_state.daily_double = rows['daily_double'].iloc[0]
    
        ind = rows.index[0]
    
        rows = rows.drop([ind])
        st.session_state.df = rows

client = create_connection()

if 'category' not in st.session_state:
    update()
    # pick_clue()

if 'choices' not in st.session_state:
    options = pd.DataFrame(run_query(
        'SELECT category, COUNT(category) AS count FROM `jeopardy-396902.jeopardy.clues` group by category HAVING count > 100'))
    options.sort_values(by='category', inplace=True)
    st.session_state['choices'] = list(options.category)

if 'rounds' not in st.session_state:
    rounds = pd.DataFrame(
        run_query('SELECT DISTINCT round_ FROM `jeopardy-396902.jeopardy.clues`'))
    st.session_state['rounds'] = list(rounds.round_)

if 'correct_answers' not in st.session_state:
    st.session_state['correct_answers'] = list()
   
df = st.session_state.df
# st.write(str(len(df)))
if len(df) == 0:
    save()
    update()

# Frontend

answer_button = st.button('Show answer')  # , on_change= show_answer())
new_clue = st.button('New clue')  # , on_click = update())
correct = st.button('Correct')

if new_clue:
    # update()
    pick_clue()

if correct:
    st.session_state['correct_answers'].append(st.session_state.id)
    pick_clue()


if answer_button:
    st.session_state.display_answer = st.session_state.answer
else:
    target = st.empty()

filter_cat = st.multiselect(
    'Categories', st.session_state.choices, key='filter_cat', on_change=update)
filter_round = st.multiselect(
    'Round', st.session_state.rounds, key='filter_round', on_change=update)

header = st.header(st.session_state.category)
clue_text = st.write(st.session_state.clue)
target = st.write(st.session_state.display_answer)

with st.expander("Clue info:", expanded=False):
    st.write(f"Date:          {st.session_state.date}")
    st.write(f"Value:         {st.session_state.value}")
    st.write(f"Daily Double:  {st.session_state.daily_double}")

    
