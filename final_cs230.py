"""
Name:   Nick Castaldo
CS230:  Section 6
Data:   volcanoes.csv
URL:    Link to your web application online**
Description:
This program was made to inform the general public about the volcanoes in the world. The
first and second queries were designed to retrieve information about each volcano based on their number and
their name, respectively. The third query is a section where users can guess which country they think
contains the most amount of volcanoes. Being allowed only three attempts, they must think fast. After three
guesses, a map shows up with the top five countries with the most volcanoes along with their guesses.
Another query allows people on the website to see which rock types make up most volcanoes in the world.
Finally, the most interesting query is one that allows users to see which volcano is the closest to them,
along with the eruption date of that same volcano.
"""
import streamlit as st
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import pandas as pd
from math import cos, asin, sqrt
from PIL import Image
import folium
import csv

FNAME = "volcanoes.csv"
volcanoes = []
df_volcanoes = pd.read_csv(FNAME, encoding="ISO-8859-1")
df = df_volcanoes.sort_values(by="Country") # Pandas: Sorting countries by alphabetical order
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'max_colwidth', None)

# Open the file
def openfile():
    global volcanoes
    with open(FNAME, 'r', encoding="ISO-8859-1") as csv_file:
        volcanoes = list(csv.DictReader(csv_file))
    return

    csv_file.close()

def main():
    openfile()

# Formatting the Webpage
st.set_page_config(layout="wide")
img = Image.open("volcano.png")
col2, mid, col1 = st.columns([1,1,8])
with col1:
    st.image('volcano.png', width=100)
with col2:
    st.title('**Volcanoes**')

st.caption("This is an interactive website to learn more about volcanoes. Try out the following activities below!")
st.write("")
st.write("")

# Find By Number Function
def findByNumber():
    number = [volcano["Volcano Number"] for volcano in volcanoes]
    volcanoNumber = st.selectbox("Please pick a Volcano Number:", number)
    st.write(f"The number you picked is {volcanoNumber}.")
    for volcano in volcanoes:
        if volcano["Volcano Number"] == volcanoNumber:
            for v in volcano:
                st.write(f"The {v.lower():<10} is {volcano[v]}")
    return

# Find By Name Function
def findByName():
    names = [volcano["Volcano Name"] for volcano in volcanoes]
    volcanoName = st.text_input("Enter a volcano name here: ")
    if volcanoName in names:
        for volcano in volcanoes:
            if volcano["Volcano Name"].lower() == volcanoName.lower():
                for v in volcano:
                    st.write(f"The {v.lower():<10} is {volcano[v]}")
    elif volcanoName == "":
        st.write(" ")
    else:
        st.write("Error! Please enter a different volcano name.")
    return

# Find the Country with the Most Volcanoes
def mostVolcanoes():
    countries = df['Country'].value_counts().to_dict() # Pandas: obtaining frequencies
    max_frequency = max(countries.values())

    sorted_values = sorted(countries.values(), reverse=True)
    top_five_countries = {}
    for v in sorted_values[0:5]:
        for k in countries.keys():
            if countries[k] == v:
                top_five_countries[k] = countries[k]

    countries_list = list(countries.keys())
    volcanoNamesGraph = []
    volcanoValuesGraph = []
    top_five_countries_list = list(top_five_countries.keys())
    top_five_countries_values = list(top_five_countries.values())
    for name in top_five_countries_list:
        volcanoNamesGraph.append(name)
    for value in top_five_countries_values:
        volcanoValuesGraph.append(value)
    count = 0
    valid = False

    guessCountries = st.multiselect(f"Choose the country you think has the most volcanoes (3 guesses maximum):", sorted(countries_list))
    for guess in guessCountries:
        count += 1
        if guess not in volcanoNamesGraph:
            volcanoNamesGraph.append(guess)
            volcanoValuesGraph.append(countries[guess])
    if count == 3:
        valid = True
    if len(guessCountries) <= 3:
        if volcanoNamesGraph[0] in guessCountries:
            st.write(f"You guessed it! {volcanoNamesGraph[0]} has the most amount of volcanoes with {countries[volcanoNamesGraph[0]]}.")
            valid = True
        else:
            for guess in guessCountries:
                st.write(f"__Wrong!__ {guess} has {countries[guess]} volcanoes.")
    else:
        st.write("__Error!__ Maximum number of guesses exceeded.")

    fig = plt.figure(figsize = (12, 5))
    plt.bar(volcanoNamesGraph, volcanoValuesGraph, color = "r")
    plt.xlabel("Volcano Name", fontweight = 'bold')
    plt.ylabel("Number of Volcanoes", fontweight = 'bold')
    plt.title("Number of Volcanoes for Each Country (Top 5 and Guesses)", fontweight = 'bold')

    if valid:
        st.pyplot(fig)
        st.write(f"You guessed the following:{guessCountries}")
        for guess in guessCountries:
            st.write(f"*{guess} has {countries[guess]} volcanoes.*")
        st.write(" ")
        st.write("The top five countries with the most volcanoes are:")
        volcanoCount = 0
        for volcano in top_five_countries_list:
            volcanoCount += 1
            st.write(f"*#{volcanoCount}: {volcano} with {countries[volcano]} volcanoes.*")

# Find Volcanoes by Dominant Rock Type
def rockType():
    rocks_sorted = []
    rocks_dict = df['Dominant Rock Type'].value_counts().to_dict()
    rocks = rocks_dict.keys()
    for rock in rocks_dict:
        if rock not in rocks_sorted:
            rocks_sorted.append(rock)
        if rock == "":
            rocks.remove(rock)
    rocks_sorted.sort()

    rock_input = st.selectbox("Pick the dominant rock type:", rocks_sorted)
    st.write(f'You picked "{rock_input}."')
    st.write("Here are all the volcanoes in the world that have a dominant rock type in this category:")
    rock_df = df.loc[df["Dominant Rock Type"]==rock_input, ["Volcano Number", "Volcano Name"]]
    st.write(rock_df)
    st.write("Below is a pie chart representing the top 5 most common types of dominant rock in volcanoes.")

    rockTypeCount = list(rocks_dict.keys())[0:5]
    rockTypeValues = list(rocks_dict.values())[0:5]
    fig1, ax1 = plt.subplots()
    plt.title("Top 5 most Dominant Rock Types in Volcanoes",
              fontweight='bold', pad='20')
    ax1.pie(rockTypeValues, labels=rockTypeCount, autopct='%1.1f%%',
        shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)


main()

# Haversine Formula: Calculating Distance (in km) Between Two Paris of Latitudes/Longitudes
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  #pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    d = 12742 * asin(sqrt(a)) #2*R*asin..
    return d


# Find the closest volcano to you!
def closestVolcano():
    columns_to_drop = ['Country','Primary Volcano Type','Activity Evidence','Last Known Eruption','Region','Subregion','Elevation (m)','Dominant Rock Type',
                       'Tectonic Setting','Link']
    df_volcanoes.drop(columns_to_drop, axis=1, inplace = True)
    st.write(df_volcanoes)
    latlong_dict = {}
    for volcano in volcanoes:
        latlong_dict[volcano["Volcano Number"]] = [volcano["Latitude"], volcano["Longitude"]]
    valid = False
    lat = st.number_input("Enter the latitude of where you live: ")
    long = st.number_input("Enter the longitude of where you live:")
    distance_list = []
    closestLat = 0
    closestLong = 0
    closestVolcanoNum = 0
    if lat and long:
        valid = True
    if valid:
        for num in latlong_dict:
            volLat = float(latlong_dict[num][0])
            volLong = float(latlong_dict[num][1])
            dist = distance(lat, long, volLat, volLong)
            distance_list.append(dist)
            if dist == min(distance_list):
                closestVolcanoNum = num
                closestLat = volLat
                closestLong = volLong

        for volcano in volcanoes:
            for v in volcano:
                if volcano["Volcano Number"] == closestVolcanoNum:
                    closestVolcano = volcano["Volcano Name"]
                    closestVolcanoLKE = volcano["Last Known Eruption"]


        st.write(f"You are {0.621371*min(distance_list):.2f} miles away from the nearest volcano.")
        st.write(f"The closest volcano is volcano number {closestVolcanoNum}, also known as {closestVolcano}.")
        st.write(f"It has the coordinates {closestLat}, {closestLong}.")
        st.write(f"This volcano's last eruption was {closestVolcanoLKE}")

        m = folium.Map(location=[lat,long],zoom_start=16)
        tooltip = "Your Location"
        tooltip2 = str(f"Volcano {closestVolcanoNum}")
        folium.Marker([lat, long], popup="Your Location", tooltip=tooltip).add_to(m)
        folium.Marker([closestLat,closestLong], popup=tooltip2, tooltip=tooltip2).add_to(m)
        folium.PolyLine(([lat,long], [closestLat,closestLong]), color="black", weight=2.5, opacity=1).add_to(m)
        folium_static(m)

# Setting Up Different Tabs

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
query_params = st.experimental_get_query_params()
tabs = ["Find by Number", "Find by Name", "Countries with Most Volcanoes", "Rock Types", "Closest Volcano"]
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Find by Number"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Find by Number")
    active_tab = "Find by Number"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == "Find by Number":
    findByNumber()
elif active_tab == "Find by Name":
    findByName()
elif active_tab == "Countries with Most Volcanoes":
    mostVolcanoes()
elif active_tab == "Rock Types":
    rockType()
elif active_tab == "Closest Volcano":
    closestVolcano()
else:
    st.error("Something has gone terribly wrong.")



# References:
# https://deparkes.co.uk/2016/06/03/plot-lines-in-folium/ # to plot lines with folium
# http://eyana.me/nearest-distance-python/#finale # to find Haversine (Distance) Formula
# https://discuss.streamlit.io/t/ann-streamlit-folium-a-component-for-rendering-folium-maps/4367 # to plot folium maps in streamlit
# https://github.com/streamlit/streamlit/issues/233 # to set up different tabs
# https://discuss.streamlit.io/t/image-and-text-next-to-each-other/7627/7 # to use the image


