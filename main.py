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
    
# def display_answer(df):
#     return df.target.iloc[0]
    
def pick_clue(data):
    return data.sample(1)

def show_answer():
    # answer = df.target.iloc[0]
    # st.session_state.answer = answer
    target.write(st.session_state.answer)
    
def update():
    df = pick_clue(data)
    category, clue = display_clue(df)
    
    
    # st.session_state.answer_button = False
    st.session_state.category = category
    st.session_state.clue = clue
    st.session_state.answer = df.target.iloc[0]
    
    return df
    
if 'category' not in st.session_state:
    update()

header = st.header(st.session_state.category)
clue_text = st.write(st.session_state.clue)

button = st.button('Show answer')#, on_click= show_answer())
new_clue = st.button('New clue', on_click = update())

if button:
    target = st.write(st.session_state.answer)
else:
    target = st.empty()
    
