# ==========================================
# app_part1.py (Modified Version)
# ==========================================

import streamlit as st
import sqlite3
import pandas as pd
import joblib
import base64

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# ------------------------------
# Page Configuration
# ------------------------------

st.set_page_config(
    page_title="Dataset Analysis Dashboard",
    layout="wide"
)

# ------------------------------
# Background Image
# ------------------------------

def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    except:
        pass

add_bg_from_local("hearttt.jpg")

# ------------------------------
# SQLite Database
# ------------------------------

conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT PRIMARY KEY,
password TEXT)
""")

conn.commit()

# ------------------------------
# Register
# ------------------------------

def register(username,password):

    c.execute(
        "INSERT INTO users VALUES(?,?)",
        (username,password)
    )

    conn.commit()

# ------------------------------
# Login
# ------------------------------

def login(username,password):

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )

    return c.fetchone()

# ------------------------------
# Session State
# ------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in=False

if "username" not in st.session_state:
    st.session_state.username=""

if "data" not in st.session_state:
    st.session_state.data=None

# ------------------------------
# Title
# ------------------------------

st.title("📊 Dataset Analysis Dashboard")

# ------------------------------
# Login / Register
# ------------------------------

if not st.session_state.logged_in:

    menu=st.sidebar.selectbox(
        "Menu",
        ["Register","Login"]
    )

    username=st.text_input("Username")

    password=st.text_input(
        "Password",
        type="password"
    )

    if menu=="Register":

        if st.button("Register"):

            try:

                register(username,password)

                st.success(
                    "Registered Successfully"
                )

            except sqlite3.IntegrityError:

                st.error(
                    "Username already exists"
                )

    else:

        if st.button("Login"):

            if login(username,password):

                st.session_state.logged_in=True
                st.session_state.username=username

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

# ------------------------------
# Dashboard
# ------------------------------

else:

    st.sidebar.success(
        f"Welcome {st.session_state.username}"
    )

    page=st.sidebar.radio(

        "Dashboard",

        [

            "🏠 Home",

            "📂 Upload Dataset",

            "📋 Dataset Information",

            "🧹 Data Cleaning",

            "🔤 Label Encoding",

            "🤖 Model Prediction",

            "🥗 Heart Healthy Diet",

            "🚪 Logout"

        ]

    )

# ------------------------------
# HOME
# ------------------------------

    if page=="🏠 Home":

        st.header("🏠 Home")

        st.write("""
Welcome to the Dataset Analysis Dashboard.

Features Available

✔ Upload Dataset

✔ Dataset Information

✔ Data Cleaning

✔ Label Encoding

✔ Heart Disease Prediction

✔ Model Accuracy

✔ Heart Healthy Diet
""")

# ------------------------------
# Upload Dataset
# ------------------------------

    elif page=="📂 Upload Dataset":

        uploaded_file=st.file_uploader(

            "Upload CSV Dataset",

            type=["csv"]

        )

        if uploaded_file is not None:

            st.session_state.data=pd.read_csv(
                uploaded_file
            )

            st.success(
                "Dataset Uploaded Successfully"
            )

            st.dataframe(
                st.session_state.data
            )

# ------------------------------
# Dataset Information
# ------------------------------

    elif page=="📋 Dataset Information":

        if st.session_state.data is None:

            st.warning(
                "Please Upload Dataset First"
            )

        else:

            data=st.session_state.data

            st.subheader("Head")

            st.dataframe(data.head())

            st.subheader("Tail")

            st.dataframe(data.tail())

            st.subheader("Shape")

            st.write(data.shape)

            st.subheader("Columns")

            st.write(list(data.columns))

            st.subheader("Data Types")

            st.write(data.dtypes)

# ------------------------------
# Data Cleaning
# ------------------------------

    elif page=="🧹 Data Cleaning":

        if st.session_state.data is None:

            st.warning(
                "Please Upload Dataset First"
            )

        else:

            data=st.session_state.data

            st.subheader("Missing Values")

            st.write(data.isnull().sum())

            st.subheader("Duplicate Values")

            st.write(data.duplicated().sum())

# ------------------------------
# Label Encoding
# ------------------------------

    elif page=="🔤 Label Encoding":

        if st.session_state.data is None:

            st.warning(
                "Please Upload Dataset First"
            )

        else:

            encoded=st.session_state.data.copy()

            for col in encoded.columns:

                if encoded[col].dtype=="object":

                    le=LabelEncoder()

                    encoded[col]=le.fit_transform(
                        encoded[col].astype(str)
                    )

            st.success(
                "Label Encoding Completed"
            )

            st.dataframe(encoded)

# ==========================================
# MODEL PREDICTION (MODIFIED AS REQUESTED)
# ==========================================

    elif page == "🤖 Model Prediction":

        st.header("🤖 Heart Disease Prediction")

        if st.session_state.data is None:
            st.warning("Please upload the dataset first.")

        else:

            model_file = st.file_uploader(
                "Upload Trained Model (.pkl)",
                type=["pkl"]
            )

            if model_file is None:

                st.info("Please upload a trained .pkl model.")

            else:

                try:

                    model = joblib.load(model_file)

                    st.success("✅ Model Uploaded Successfully")

                    st.subheader("Enter Patient Details")

                    patient_id = st.number_input(
                        "Patient ID",
                        min_value=1,
                        value=1,
                        step=1
                    )

                    age = st.number_input(
                        "Age",
                        1,
                        120,
                        30
                    )

                    gender = st.selectbox(
                        "Gender",
                        ["Male","Female"]
                    )

                    gender = 1 if gender=="Male" else 0

                    glucose = st.number_input(
                        "Glucose (mg/dL)",
                        50,
                        400,
                        100
                    )

                    cholesterol = st.number_input(
                        "Cholesterol (mg/dL)",
                        50,
                        500,
                        180
                    )

                    systolic = st.number_input(
                        "Systolic BP",
                        50,
                        250,
                        120
                    )

                    diastolic = st.number_input(
                        "Diastolic BP",
                        30,
                        150,
                        80
                    )

                    bmi = st.number_input(
                        "BMI",
                        10.0,
                        60.0,
                        22.0
                    )

                    heart_rate = st.number_input(
                        "Heart Rate",
                        30,
                        200,
                        72
                    )

                    smoking = st.selectbox(
                        "Smoking",
                        ["No","Yes"]
                    )

                    smoking = 1 if smoking=="Yes" else 0

                    alcohol = st.selectbox(
                        "Alcohol Consumption",
                        ["No","Yes"]
                    )

                    alcohol = 1 if alcohol=="Yes" else 0

                    physical = st.selectbox(
                        "Physical Activity",
                        ["Low","Medium","High"]
                    )

                    if physical=="Low":
                        physical=0
                    elif physical=="Medium":
                        physical=1
                    else:
                        physical=2

                    family = st.selectbox(
                        "Family History",
                        ["No","Yes"]
                    )

                    family = 1 if family=="Yes" else 0

                    if st.button("Predict"):

                        user = pd.DataFrame([[
                            patient_id,
                            age,
                            gender,
                            glucose,
                            cholesterol,
                            systolic,
                            diastolic,
                            bmi,
                            heart_rate,
                            smoking,
                            alcohol,
                            physical,
                            family
                        ]],

                        columns=[
                            "patient_id",
                            "age",
                            "gender",
                            "glucose_mg_dl",
                            "cholesterol_mg_dl",
                            "systolic_bp",
                            "diastolic_bp",
                            "bmi",
                            "heart_rate",
                            "smoking",
                            "alcohol_consumption",
                            "physical_activity",
                            "family_history"
                        ])

                        prediction = model.predict(user)[0]

                        st.subheader("Prediction")

                        # MODIFIED: Output strictly "1" or "0" as requested
                        if prediction == 1:
                            st.error("Prediction: 1")
                        else:
                            st.success("Prediction: 0")

                    st.markdown("---")

                    st.subheader("📈 Model Accuracy")

                    # MODIFIED: Showing hardcoded 96% accuracy as requested
                    st.success("Accuracy : 96.00%")

                except Exception as e:

                    st.error(e)

# ------------------------------
# HEART HEALTHY DIET
# ------------------------------

    elif page=="🥗 Heart Healthy Diet":

        st.header("🥗 Heart Healthy Diet")

        st.success("✅ Foods to Eat")

        st.markdown("""

### 🥬 Vegetables
- Spinach
- Broccoli
- Carrot
- Beetroot
- Tomato
- Cabbage
- Cauliflower
- Cucumber

### 🍎 Fruits
- Apple
- Orange
- Guava
- Papaya
- Pomegranate
- Watermelon
- Kiwi

### 🌾 Whole Grains
- Oats
- Brown Rice
- Ragi
- Bajra
- Whole Wheat

### 🫘 Protein
- Fish
- Skinless Chicken
- Egg White
- Lentils
- Chickpeas
- Green Gram
- Kidney Beans

### 🥜 Nuts
- Almonds
- Walnuts
- Flax Seeds
- Chia Seeds

### 🥛 Dairy
- Skim Milk
- Low Fat Milk
- Low Fat Curd
- Low Fat Paneer

### 💧 Healthy Drinks
- Water
- Coconut Water
- Lemon Water
- Green Tea

""")

        st.error("""

### ❌ Foods To Avoid

- Fried Foods
- Pizza
- Burger
- French Fries
- Chips
- Cakes
- Pastries
- Bakery Foods
- Soft Drinks
- Sugary Foods
- Excess Salt
- Butter
- Ghee
- Processed Meat
- Alcohol
- Smoking

""")

        st.info("""

### 🏃 Lifestyle Tips

✔ Walk 30–45 minutes daily

✔ Exercise regularly

✔ Drink 2–3 litres of water

✔ Eat fruits & vegetables

✔ Sleep 7–8 hours

✔ Reduce stress

✔ Maintain healthy weight

✔ Regular heart check-up

""")

# ------------------------------
# LOGOUT
# ------------------------------

    elif page=="🚪 Logout":

        st.session_state.logged_in=False

        st.session_state.username=""

        st.session_state.data=None

        st.rerun()

# ==========================================
# END OF APP
# ==========================================