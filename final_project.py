"""
Name:       Ian Robert
CS230:      Section 5
Data:       Boston Parking Meters
URL:
Description: This program analyzes and displays notable things about the Boston Parking Meters dataset.
"""
import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt

#This block lets me set the background color of the website using html code to set RGB.
background_color = """
    <style>
    .stApp {background-color: rgb(173, 216, 230); }
    </style>
"""
st.write(background_color, unsafe_allow_html=True)

path = r"C:\Users\ianli\OneDrive - Bentley University\Desktop\Python Project Stuff\Parking_Meters.csv"

#Defining the database using the csv that was provided.
df_bosp = pd.read_csv(path)

#This block makes the sidebar.
page = st.sidebar.selectbox(
    "Go to",
    ("Home", "Extra Data") )

if page == "Home":

    #Title in html code (I wanted to edit the font)
    title_html = f"""
    <h1 style="font-family: 'Times New Roman', sans-serif;">Boston Parking Meters</h1>
    """
    st.write(title_html, unsafe_allow_html=True)

    st.write("By Ian Robert")
    st.write("Here are a few conclusions I drew from the Boston Parking Meters dataset I provided below")

    # Add a header
    st.header("Parking Meter Map")

    layer1 = pdk.Layer(
        "ScatterplotLayer",
        data=df_bosp,
        get_position=["LONGITUDE", "LATITUDE"],
         get_radius=5,
         get_fill_color=[0, 0, 230],  #blue RGB value
         pickable=True,
        auto_highlight=True
     )

    #map view
    view_state = pdk.ViewState(
        latitude=df_bosp["LATITUDE"].mean(),
        longitude=df_bosp["LONGITUDE"].mean(),
        zoom=12,
        pitch=0)

    #creation of the actual map
    map1 = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v8",
        initial_view_state=view_state,
        layers=[layer1]
    )
    # displays the map on the streamlit website
    st.pydeck_chart(map1)


    # Show the dataframe
    st.write("Dataset used for this website:", df_bosp)
    # Download button for data. I converted the dataframe into a file for the user to download.
    st.download_button(label="Download the data file here", data=df_bosp.to_csv(), file_name='Parking_Meters.csv')

    input_column = st.text_input("Enter column name")

#(1)This function makes it so that the user can enter the name of a column, and they can see all the data for that specific column.
    def column(dataframe, columnname): #dataframe is the default value, columnname is user generated, also filters data by 1 condition (user input)
        if columnname in dataframe.columns:
            values = dataframe[columnname].tolist() #.tolist() extracts the data from the selected column
            st.write(f"Values in column {columnname}")
            st.write(values)
            null_values = [value for value in values if value is None]  #list comprehension for NaN/Null values
            st.write(f"Null values in column {columnname}") #The function also shows null values in the selected column.
            st.write(null_values)
        else:
            st.write("Column not in dataframe")

    if input_column:
        column(df_bosp, input_column)

elif page == "Extra Data":
    st.header("Extra Data")

    #(2) This function makes a pie chart out of whatever column I choose in this code.
    def pie_chart(dataframe, columnname):
        if columnname in dataframe.columns:
            value_count = dataframe[columnname].value_counts()
            top_n=15
            top_values = value_count.head(top_n)
            fig, ax = plt.subplots() #I tried doing it the way its done in the video (plt.pie), but I got an error on streamlit telling me to do it with fig, ax instead.
            ax.pie(top_values, labels=top_values.index, autopct='%1.1f%%', startangle=90)
            ax.set_aspect('equal')
            ax.set_title(f"{columnname} Distribution")
            st.pyplot(fig)

    #This is the data I chose to make the pie charts out of.
    column_for_data = "VENDOR"
    column_for_data2 = "STREET"
    pie_chart(df_bosp, column_for_data)
    pie_chart(df_bosp, column_for_data2)

    #This is the code block for the bar chart.
    meter_type_counts = df_bosp["METER_TYPE"].value_counts()
    plt.figure(figsize=(8, 6))
    meter_type_counts.plot(kind="bar")
    plt.xlabel("Meter Type")
    plt.ylabel("Count")
    plt.title("Meter Type Counts")
    plt.xticks(rotation=60)
    st.pyplot(plt)

    count_multi = df_bosp["METER_TYPE"].value_counts()["MULTI-SPACE STALL"] #This line finds the amount of multi-space stalls.
    st.write(f"There are {count_multi} Multi Space Stalls.")
    count_single = df_bosp["METER_TYPE"].value_counts()["SINGLE-SPACE"] #This line finds the amount of single=space stalls.
    st.write(f"There are {count_single} Single Space Stalls.")

    st.header("Additional Data")

    #This block finds the max and the mins for the parking rate.
    max_base_rate = df_bosp["BASE_RATE"].max()
    min_base_rate = df_bosp["BASE_RATE"].min()

    st.write(f"The highest cost parking meter costs {max_base_rate} dollars an hour and the lowest cost parking meter "
        f"costs {min_base_rate} dollars per hour.")

    #This block finds and displays the amount of parking meters that cost between 0.25 and 2.
    filtered_rate = ((df_bosp['BASE_RATE'] > 0.25) & (df_bosp['BASE_RATE'] < 2.00)).sum()
    st.write(f"There are {filtered_rate} meters that cost between 0.25 and 2 dollars per hour.")

    #Pivot table for base rates by meter type.
    pivot_table = pd.pivot_table(df_bosp, values='BASE_RATE', index='METER_TYPE', aggfunc='mean')
    st.write("Average Base Rates by Meter Type:")
    st.write(pivot_table)

