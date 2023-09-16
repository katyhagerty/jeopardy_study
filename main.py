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

# Create API client.


def clues_remaining():
    if 'df' in st.session_state:
        if len(st.session_state.df) == 0:
            return False
    return True


@st.cache_resource(ttl=24*3600)  # , validate = clues_remaining)
def create_connection():
    # create_connection
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"])
    client = bigquery.Client(credentials=credentials)
    return client


client = create_connection()


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

    filters = ['correct = 0']

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

    query_text = f'SELECT id,category,text,target FROM `jeopardy-396902.jeopardy.clues` {filters} order by RAND() LIMIT 100'
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
    rows = st.session_state.df

    st.session_state.id = rows['id'].iloc[0]
    st.session_state.category = rows['category'].iloc[0]
    st.session_state.clue = rows['text'].iloc[0]
    st.session_state.answer = rows['target'].iloc[0]

    ind = rows.index[0]

    rows = rows.drop([ind])
    st.session_state.df = rows


def show_answer():
    if button:
        target.write(st.session_state.answer)


def record():
    data = load_data(loc)
    data.loc[int(st.session_state.id), 'correct'] = 1
    data.to_csv(loc)


if 'category' not in st.session_state:
    update()
    # pick_clue()

button = st.button('Show answer')  # , on_change= show_answer())
new_clue = st.button('New clue')  # , on_click = update())
correct = st.button('Correct')
save = st.button('Save')

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
    st.session_state.correct_answers = []

filter_cat = st.multiselect(
    'Categories', st.session_state.choices, key='filter_cat', on_change=update)
filter_round = st.multiselect(
    'Round', st.session_state.rounds, key='filter_round', on_change=update)

df = st.session_state.df
# str(len(df))
if len(df) == 0:
    'df len is 0'
    update()

if new_clue:
    # update()
    pick_clue()

if correct:
    # run_query(f'UPDATE `jeopardy-396902.jeopardy.clues` SET correct = 1 WHERE id = {st.session_state.id}')
    correct_answers = st.session_state.correct_answers
    correct_answers.append(st.session_state.id)
    st.session_state.correct_answers = correct_answers
    pick_clue()
# st.session_state


def save():
    correct = st.session_state.correct_answers
    if len(correct) > 0:
        correct_answers = reformat(str(st.session_state.correct_answers))
        query = f'UPDATE `jeopardy-396902.jeopardy.clues` SET correct = 1 WHERE id IN {correct_answers}'
        run_query(query)
        st.session_state.correct_answers = []


if save:
    save()

if button:
    target = st.write(st.session_state.answer)
else:
    target = st.empty()

header = st.header(st.session_state.category)
clue_text = st.write(st.session_state.clue)
target = st.empty()

remaining_clues = st.session_state.df
st.write(str(len(remaining_clues)))
if len(remaining_clues) == 0:
    save()
    'Saving clues before updating'
    update()

# if correct:
    # run_query(f'UPDATE `jeopardy-396902.jeopardy.clues` SET correct = 1 WHERE id = {st.session_state.id}')

# if len(st.session_state.correct_answers) > 0:
#     correct_answers = reformat(str(st.session_state.correct_answers))
#     run_query(f'UPDATE `jeopardy-396902.jeopardy.clues` SET correct = 1 WHERE id IN {correct_answers}')
#     time.sleep(300)
# st.session_state
