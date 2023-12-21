# Abimereki Muzaale

import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the model and beta coefficients
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)
    
with open('betas.pkl', 'rb') as file:
    betas = pickle.load(file)

# Define a function to calculate the risk of mortality
def calculate_risk(demographic, history, exam, labs):
    # Combine all input features into a single array
    features = np.concatenate([demographic, history, exam, labs])
    
    # Calculate the log hazard ratio using the beta coefficients
    log_hr = np.sum(features * betas)
    
    # Calculate the absolute risk using the Cox proportional hazards formula
    risk = np.exp(log_hr) * baseline_risk
    
    return risk

# Define the baseline risk for a healthy individual
baseline_risk = 0.0028 #from literature & base-case survival

# Define the input fields for the calculator
age = st.slider('Age', 18, 100, 5)
female = st.selectbox('Sex', ['Male', 'Female'])
racecat = st.selectbox('Race', ['Hispanic', 'Other', 'White'])
dm = st.checkbox('Diabetes')
htn = st.checkbox('Hypertension')
acr = st.slider('ACR', 0.0, 100.0, 0.0)
hba1c = st.slider('HbA1c', 0.0, 20.0, 5.0)
egfr = st.slider('eGFR', 0, 200, 100)
sbp = st.slider('SBP', 50, 250, 120)

# Convert categorical variables to one-hot encoding
if female == 'Male':
    sex_male = 1
else:
    sex_male = 0
    
if racecat == 'Hispanic':
    race_hispanic = 1
    race_other = 0
    race_white = 0
elif racecat == 'Other':
    race_hispanic = 0
    race_other = 1
    race_white = 0
else:
    race_hispanic = 0
    race_other = 0
    race_white = 1

# Combine all input features into a single array
demographic = np.array([age, sex_male, race_hispanic, race_other, race_white])
history = np.array([int(dm), int(htn)])
exam = np.array([sbp])
labs = np.array([acr,hba1c, egfr])  # Add any additional lab features here if needed

# Calculate the risk of mortality using the input features
risk = calculate_risk(demographic, history, exam, labs)

# Display the calculated risk
st.write('30-Year Risk of Mortality:', risk)
