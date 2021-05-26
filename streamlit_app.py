import streamlit as st
from pytrends.request import TrendReq

pytrends = TrendReq()
import pandas as pd
import time
import datetime
from datetime import datetime, date, time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from parseCountries import parse
import base64
from datetime import date


def removeRestrictedCharactersAndWhiteSpaces(keywords):

    restricted_characters = ['-', ',', '\'', ')', '(', '[', ']', '{', '}', '.', '*', '?', '_', '@', '!', '$']

    preprocessed_list = []
    
    for keyword in keywords:
    
        clean_keyword = ""
        for char in keyword:
            if char not in restricted_characters:
                clean_keyword += char
        
        white_space_counter = 0
        
        for char in clean_keyword:
            if char == ' ':
                white_space_counter += 1
            else:
                break
        
        clean_keyword = clean_keyword[white_space_counter:]
        
        white_space_counter = 0
        
        for i in range(len(clean_keyword) - 1, 0, -1):
            if clean_keyword[i] == ' ':
                white_space_counter += 1
            else:
                break
        
        if white_space_counter != 0:
            clean_keyword = clean_keyword[:-white_space_counter]
        
        preprocessed_list.append(clean_keyword)
    
    return preprocessed_list
    

st.set_page_config(layout="wide")

st.title("The G-Trendalizer:snake::fire:")
st.markdown('**Your UK 5 Top & Rising Google Trends Dashboard⚡**') 

# st.markdown("## ** Paste keywords **")

linesDeduped2 = []
MAX_LINES = 5
text2 = st.markdown("Get your Top & Rising trends for 5 keywords, directly from Google Trends, no coding needed :sunglasses:.")
text3 = st.markdown("To get started: Paste 1 keyword per line, pick your country (geo) & timeframe from the drop downs & hit 'Get Trends🤘' ")
text = st.text_area("by Orit Mutznik (@oritsimu)", height=150, key=1)
#text2 = st.markdown('***Please make sure there are no extra spaces in the beginning or end of each keyword, also no apostrophes or dashes🙏**')
lines = text.split("\n")  # A list of lines
linesList = []
for x in lines:
    linesList.append(x)
linesList = list(dict.fromkeys(linesList))  # Remove dupes
linesList = list(filter(None, linesList))  # Remove empty

if len(linesList) > MAX_LINES:
    st.warning(f"⚠️ Only the first 5 keywords will be reviewed.)")
    linesList = linesList[:MAX_LINES]


country_names, country_codes = parse()
country_names, country_codes = country_names[:243], country_codes[:243]

country = st.selectbox("Your Country", country_names)
st.write(f"You selected " + country)
idx = country_names.index(country)
country_code = country_codes[idx],

selected_timeframe = ""


period_list = ["Past 12 months", "Past hour", "Past 4 hours", "Past day", "Past 7 days", "Past 30 days", "Past 90 days", "Past 5 years", "2004 - present", "Custom time range"]
tf = ["today 12-m", "now 1-H", "now 4-H", "now 1-d", "now 7-d", "today 1-m", "today 3-m", "today 5-y", "all", "custom"]
timeframe_selectbox = st.selectbox("Choose Period", period_list)

idx = period_list.index(timeframe_selectbox)

selected_timeframe = tf[idx]


todays_date = date.today()

current_year = todays_date.year

years = list(range(2005, current_year + 1))
months = list(range(1, 13))
days = list(range(1, 32))

if selected_timeframe == "custom":
    
    st.write(f"From")

    col11, col12, col13 = st.beta_columns(3)
    year_from = col11.selectbox("year", years, key="0")
    month_from = col12.selectbox("month", months, key="1")
    day_from = col13.selectbox("day", days, key="2")
    
    st.write(f"To")

    col21, col22, col23 = st.beta_columns(3)
    year_to = col21.selectbox("year", years, key="3")
    month_to = col22.selectbox("month", months, key="4")
    day_to = col23.selectbox("day", days, key="5")
    
    selected_timeframe = str(year_from) + "-" + str(month_from) + "-" + str(day_from) + " " + str(year_to) + "-" + str(month_to) + "-" + str(day_to)
        

start_execution = st.button("Get Trends! 🤘")



if start_execution:


    if len(linesList) == 0:
    
        st.warning("Please enter at least 1 keyword.")
        
    else:
    
        linesList = removeRestrictedCharactersAndWhiteSpaces(linesList)
        
        pytrends.build_payload(linesList, timeframe=selected_timeframe, geo=country_code[0])
        related_queries = pytrends.related_queries()
        
        for i in range(len(linesList)):

            st.header("GTrends data for keyword {}: {}".format(i+1, str(linesList[i])))

            c29, c30, c31 = st.beta_columns([6, 2, 6])

            with c29:

                st.subheader("Top Trends🏆")
                st.write(related_queries.get(linesList[i]).get("top"))

            with c31:

                st.subheader("Rising Trends⚡")
                st.write(related_queries.get(linesList[i]).get("rising"))

        

        st.stop()

        # suggestions = pytrends.suggestions(keyword='dresses')
        # suggestions_df = pd.DataFrame(suggestions)
        # print(suggestions_df.drop(columns= 'mid'))

