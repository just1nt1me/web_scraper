import streamlit as st
from oakhouse import Oakhouse
#from email_vacancies import send_emails
import email_config

st.markdown('''
            ## Welcome to this Oakhouse availabity warning!
            ''')

user_input = st.text_input('Input the desired oakhouse to scrape from:')
if user_input:
    oakhouse = Oakhouse()
    oakhouse.get_soups(user_input)
    oakhouse.get_vacancies()
    out = oakhouse.get_output()
    st.write(out)
