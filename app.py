import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Smart Health Predictor", layout="wide")

# Custom CSS for UI improvements
st.markdown(
    """
    <style>
        /* Title Text */
        .title-blue {
            color: blue !important;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
        }

        /* Change label text color */
        div[data-testid="stFormLabel"], label {
            color: black !important;
            font-weight: bold;
        }

        /* Background color */
        .stApp {
            background-color: #f5f7fa;
        }

        /* Success Message */
        .stSuccess {
            color: green !important;
            font-weight: bold;
            font-size: 20px;
            text-align: center;
        }

        /* Warning Message */
        .stWarning {
            color: red !important;
            font-weight: bold;
            font-size: 20px;
            text-align: center;
        }

        /* Menu Bar Styling */
        .menu-bar {
            display: flex;
            justify-content: center;
            background-color: #0066cc;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .menu-item {
            color: white;
            font-size: 18px;
            font-weight: bold;
            margin: 0 20px;
            cursor: pointer;
        }

        /* Button Styling */
        .predict-btn {
            background-color: #0066cc;
            color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-size: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Get working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load saved models
diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))

# Custom Navigation Menu at Top
selected = st.selectbox("Choose Prediction Type", ["Diabetes Prediction", "Heart Disease Prediction"])

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.markdown('<p class="title-blue">🩺 Diabetes Prediction using ML</p>', unsafe_allow_html=True)

    # Input fields
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')
    with col2:
        Glucose = st.text_input('Glucose Level')
    with col3:
        BloodPressure = st.text_input('Blood Pressure value')
    with col1:
        SkinThickness = st.text_input('Skin Thickness value')
    with col2:
        Insulin = st.text_input('Insulin Level')
    with col3:
        BMI = st.text_input('BMI value')
    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
    with col2:
        Age = st.text_input('Age of the Person')

    # Prediction logic
    diab_diagnosis = ''
    
    if st.button('🔍 Get Diabetes Test Result', help="Click to predict diabetes"):
        try:
            user_input = [float(Pregnancies), float(Glucose), float(BloodPressure), float(SkinThickness), 
                          float(Insulin), float(BMI), float(DiabetesPedigreeFunction), float(Age)]
            
            diab_prediction = diabetes_model.predict([user_input])

            if diab_prediction[0] == 1:
                diab_diagnosis = '<p class="stWarning">🚨 The person is diabetic!</p>'
            else:
                diab_diagnosis = '<p class="stSuccess">✅ The person is not diabetic!</p>'
        except:
            diab_diagnosis = '<p class="stWarning">⚠ Please enter valid numeric values!</p>'

    st.markdown(diab_diagnosis, unsafe_allow_html=True)

    # Downloadable report
    if diab_diagnosis:
        st.download_button(label="📥 Download Report", data=diab_diagnosis, file_name="diabetes_report.txt")

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.markdown('<p class="title-blue">❤️ Heart Disease Prediction using ML</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')
    with col2:
        sex = st.text_input('Sex (1 = Male, 0 = Female)')
    with col3:
        cp = st.text_input('Chest Pain Type (0-3)')
    with col1:
        trestbps = st.text_input('Resting Blood Pressure')
    with col2:
        chol = st.text_input('Serum Cholesterol in mg/dl')
    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl (1 = True, 0 = False)')
    with col1:
        restecg = st.text_input('Resting ECG Results (0-2)')
    with col2:
        thalach = st.text_input('Maximum Heart Rate Achieved')
    with col3:
        exang = st.text_input('Exercise-Induced Angina (1 = Yes, 0 = No)')
    with col1:
        oldpeak = st.text_input('ST Depression Induced by Exercise')
    with col2:
        slope = st.text_input('Slope of Peak Exercise ST Segment (0-2)')
    with col3:
        ca = st.text_input('Major Vessels Colored by Fluoroscopy (0-4)')
    with col1:
        thal = st.text_input('Thalassemia (0 = Normal, 1 = Fixed Defect, 2 = Reversible Defect)')

    # Prediction logic
    heart_diagnosis = ''

    if st.button('🔍 Get Heart Disease Test Result', help="Click to predict heart disease"):
        try:
            user_input = [float(age), float(sex), float(cp), float(trestbps), float(chol),
                          float(fbs), float(restecg), float(thalach), float(exang),
                          float(oldpeak), float(slope), float(ca), float(thal)]

            heart_prediction = heart_disease_model.predict([user_input])

            if heart_prediction[0] == 1:
                heart_diagnosis = '<p class="stWarning">🚨 The person has heart disease!</p>'
            else:
                heart_diagnosis = '<p class="stSuccess">✅ The person does not have heart disease!</p>'
        except:
            heart_diagnosis = '<p class="stWarning">⚠ Please enter valid numeric values!</p>'

    st.markdown(heart_diagnosis, unsafe_allow_html=True)

    # Downloadable report
    if heart_diagnosis:
        st.download_button(label="📥 Download Report", data=heart_diagnosis, file_name="heart_disease_report.txt")
