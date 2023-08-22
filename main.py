#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 21:37:39 2023

@author: katyhagerty
"""

import streamlit as st
import pandas as pd
# from streamlit_toggle import st_toggle_switch

loc = 'clues.csv'

st.cache_data()
def load_data(loc):
    data = pd.read_csv(loc)
    
    if 'filter_cat' in st.session_state:
        if st.session_state.filter_cat != '':
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
    
    cats = data.groupby(by = 'category').count()
    options = set(cats[cats['round_'] >= 100].category)
    st.session_state.choices = options
    # st.session_state.answer_button = False
    st.session_state.category = category
    st.session_state.clue = clue
    st.session_state.answer = df.target.iloc[0]
    
    # return df
    
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
filter_cat = st.multiselect('Categories', st.session_state.choices, key = 'filter_cat')

if new_clue:
    update()

header = st.header(st.session_state.category)
clue_text = st.write(st.session_state.clue)
# target = st.empty()
    

if button:
    target = st.write(st.session_state.answer)
else:
    target = st.empty()

    
