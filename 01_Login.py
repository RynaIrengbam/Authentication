import pandas as pd
import streamlit as st 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go
import hashlib
import sqlite3 
from sklearn.datasets import load_iris
from sklearn import datasets


def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def main():
    st.subheader("Login Section")

    username = st.text_input("Username")
    password = st.text_input("Password",type = 'password')
    if st.button("Login"):
        create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(username,check_hashes(password,hashed_pswd))
        if result:
            st.success("Logged in as {}".format(username))
            st.header("Iris Dataset")
            st.write("The following is the iris dataset")

            iris = datasets.load_iris()
            X = pd.DataFrame(iris.data)
            Y = pd.Series(iris.target, name = 'class')
            df = pd.concat([X,Y], axis = 1)
            st.write(df)
            
        else:
            st.warning("Incorrect username/password")

if __name__ == '__main__':
    main()