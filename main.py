#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 21:37:39 2023

@author: katyhagerty
"""

import streamlit as st
import pandas as pd

loc = 'clues.csv'

st.cache()
def load_data(loc):
    return pd.read_csv(loc)

data = load_data(loc)

def display_clue(df):
    category = df.category.iloc[0].upper()
    clue = df.text.iloc[0]
    return category,clue
    
def display_answer(df):
    return df.target.iloc[0]
    
def pick_clue(data):
    return data.sample(1)



st.session_state

if 'category' not in st.session_state:
    df = pick_clue(data)
    category, clue = display_clue(df)
    answer = display_answer(df)    
    
    st.session_state.category = category
    st.session_state.clue = clue
    st.session_state.answer = answer
    
# if clue not in st.session_state:
#     st.session_state.clue = clue
    
# if answer not in st.session_state:
#     st.session_state.answer = answer

def show_answer():
    target.write(st.session_state.answer)
    
def update():
    df = pick_clue(data)
    category, clue = display_clue(df)
    answer = display_answer(df)
    
    st.session_state.answer_button = False
    st.session_state.category = category
    st.session_state.clue = clue
    st.session_state.answer = answer

# st.header(category)
# st.write(clue)
header = st.header(st.session_state.category)
clue_text = st.write(st.session_state.clue)
target = st.empty()

button = st.button('Show answer')
new_clue = st.button('New clue', on_click = update())

if button:
    target.write(st.session_state.answer)
    
# if new_clue:
#     df = pick_clue(data)
#     category, clue = display_clue(df)
#     answer = display_answer(df)
#     st.session_state.category = category
#     st.session_state.clue = clue
#     st.session_state.answer = answer
    
