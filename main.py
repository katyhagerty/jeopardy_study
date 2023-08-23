#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 21:37:39 2023

@author: katyhagerty
"""

import streamlit as st
import pandas as pd
# from streamlit_toggle import st_toggle_switch

loc = 'all_data_v2.csv'


st.cache_data()
def load_data(loc):
    data = pd.read_csv(loc)
    
    if 'filter_cat' in st.session_state:
        if len(st.session_state.filter_cat) > 0:
            data = data[data.category.isin(st.session_state.filter_cat)]
    
    return data

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
    data = load_data(loc)
    df = pick_clue(data)
    category, clue = display_clue(df)
    
    st.session_state.id = df.index[0]
    st.session_state.category = category
    st.session_state.clue = clue
    st.session_state.answer = df.target.iloc[0]
    
    # return df
    
# def find_choices():
#     all_data = pd.read_csv('clues.csv')
#     cats = all_data.groupby(by = 'category').count().reset_index()
#     options = set(cats[cats['round_'] >= 100].category)
#     st.session_state.choices = options
    
#     return st.session_state.choices

def record():
    data = load_data(loc)
    data.iloc[st.session_state.id, 'correct'] = 1
    data.to_csv(loc)
    
if 'category' not in st.session_state:
    # 'category not in session state'
    data = load_data(loc)
    update()

st.checkbox(
    label="Save",
    key="switch_1",
    # label_after="Saving session",
)

# on_click called with every update even if button was not clicked prior
button = st.button('Show answer') #, on_click= show_answer())
new_clue = st.button('New clue') #, on_click = update())
correct = st.button('Correct', on_click = record)

if 'choices' not in st.session_state:
    all_data = pd.read_csv('all_clues.csv')
    cats = all_data.groupby(by = 'category').count().reset_index()
    options = list(set(cats[cats['round_'] >= 100].category))
    st.session_state['choices'] = options
    st.session_state['rounds'] = list(set(all_data.round_))
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

    
# st.session_state
