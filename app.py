import streamlit as st
import pandas as pd
import joblib
import base64
from pathlib import Path

# BMW Background Image
bg_path = Path("BMW.jpg")

if bg_path.exists():
    with open(bg_path, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(
                rgba(10, 15, 25, 0.65),
                rgba(10, 15, 25, 0.65)
            ),
            url("data:image/png;base64,{encoded_image}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.warning("BMW background image not found!")

# Load trained model and columns
model = joblib.load("car_price_model.pkl")
model_columns = joblib.load("model_columns.pkl")

st.set_page_config(page_title="Car Price Prediction", page_icon="🏎️")
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #1e293b);
}

.stApp h1 {
    color: #38bdf8 !important;
    text-align: center;
    font-size: 42px;
}

p {
    color: #e2e8f0;
}

.stButton > button {
    background-color: #0284c7;
    color: white;
    border-radius: 10px;
    width: 100%;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #0369a1;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# BMW Background Image
bg_path = Path("bmw_background.png")

if bg_path.exists():
    with open(bg_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(10,15,25,0.65), rgba(10,15,25,0.65)),
        url("data:image/png;base64,{encoded_image}") !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.warning("BMW background image not found!")

st.title("🏎️ Car Price Prediction")
st.write("Enter your car details to predict its price.")

with st.form("car_form"):

    make = st.selectbox("Car Company", [
        "alfa-romero", "audi", "bmw", "chevrolet", "dodge",
        "honda", "isuzu", "jaguar", "mazda", "mercedes-benz",
        "mercury", "mitsubishi", "nissan", "peugot", "plymouth",
        "porsche", "renault", "saab", "subaru", "toyota",
        "volkswagen", "volvo"
    ])

    fuel_type = st.selectbox("Fuel Type", ["gas", "diesel"])
    aspiration = st.selectbox("Aspiration", ["std", "turbo"])
    doors = st.selectbox("Number of Doors", ["four", "two"])
    body_style = st.selectbox("Body Style", [
        "hardtop", "wagon", "sedan", "hatchback", "convertible"
    ])
    drive_wheels = st.selectbox("Drive Wheels", ["4wd", "fwd", "rwd"])
    engine_location = st.selectbox("Engine Location", ["front", "rear"])

    symboling = st.number_input("Symboling", -3, 3, 0)
    normalized_losses = st.number_input("Normalized Losses", 65, 256, 150)
    wheel_base = st.number_input("Wheel Base", 86.6, 120.9, 100.0)
    length = st.number_input("Length", 141.1, 208.1, 170.0)
    width = st.number_input("Width", 60.3, 72.3, 65.0)
    height = st.number_input("Height", 47.8, 59.8, 54.0)
    curb_weight = st.number_input("Curb Weight", 1488, 4066, 2500)

    engine_type = st.selectbox("Engine Type", [
        "dohc", "dohcv", "l", "ohc", "ohcf", "ohcv", "rotor"
    ])
    cylinders = st.selectbox("Number of Cylinders", [
        "eight", "five", "four", "six", "three", "twelve", "two"
    ])

    engine_size = st.number_input("Engine Size", 61, 326, 150)
    fuel_system = st.selectbox("Fuel System", [
        "1bbl", "2bbl", "4bbl", "idi", "mfi", "mpfi", "spdi", "spfi"
    ])

    bore = st.number_input("Bore", 2.54, 3.94, 3.0)
    stroke = st.number_input("Stroke", 2.07, 4.17, 3.0)
    compression_ratio = st.number_input("Compression Ratio", 7.0, 23.0, 9.0)
    horsepower = st.number_input("Horsepower", 48, 288, 100)
    peak_rpm = st.number_input("Peak RPM", 4150, 6600, 5000)
    city_mpg = st.number_input("City MPG", 13, 49, 25)
    highway_mpg = st.number_input("Highway MPG", 16, 54, 30)

    predict = st.form_submit_button("Predict Car Price")

if predict:

    input_data = {
        "symboling": symboling,
        "normalized-losses": normalized_losses,
        "fuel-type": fuel_type,
        "aspiration": aspiration,
        "num-of-doors": doors,
        "body-style": body_style,
        "drive-wheels": drive_wheels,
        "engine-location": engine_location,
        "wheel-base": wheel_base,
        "length": length,
        "width": width,
        "height": height,
        "curb-weight": curb_weight,
        "engine-type": engine_type,
        "num-of-cylinders": cylinders,
        "engine-size": engine_size,
        "fuel-system": fuel_system,
        "bore": bore,
        "stroke": stroke,
        "compression-ratio": compression_ratio,
        "horsepower": horsepower,
        "peak-rpm": peak_rpm,
        "city-mpg": city_mpg,
        "highway-mpg": highway_mpg
    }

    input_df = pd.DataFrame([input_data])
    input_df = pd.get_dummies(input_df)

    input_df = input_df.reindex(columns=model_columns, fill_value=0)

    prediction = model.predict(input_df)[0]

    st.success(f"Estimated Car Price: {prediction:,.2f}")
