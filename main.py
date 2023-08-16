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

df = pick_clue(data)
category, clue = display_clue(df)
answer = display_answer(df)

st.header(category)
st.write(clue)
target = st.empty()
button = st.button('Show answer')
new_clue = st.button('New clue')

if button:
    target.write(answer)
    
if new_clue:
    df = pick_clue(data)
    category, clue = display_clue(df)
    answer = display_answer(df)
