import streamlit as st
import csv
import re
import requests
from io import StringIO
from fuzzywuzzy import fuzz

# Read the CSV file and create a dictionary of keywords and paragraphs
def read_csv_file(file_url):
    response = requests.get(file_url)
    response.raise_for_status()

    data = {}

    csvfile = StringIO(response.text)
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row

    for row in reader:
        keyword = row[0].lower()  # Convert keyword to lowercase for case-insensitive search
        paragraph = row[1]
        data[keyword] = paragraph

    return data

# Search for keywords in the user question and return corresponding paragraphs
def search_keywords(user_question, data):
    user_question = user_question.lower()  # Convert user question to lowercase for case-insensitive search
    found_paragraphs = []

    for keyword, paragraph in data.items():
        if keyword in user_question:
            found_paragraphs.append(paragraph)
        elif fuzz.partial_token_set_ratio(user_question, keyword) >= 80:
            found_paragraphs.append(paragraph)

    return found_paragraphs

def main():
    st.title("If-Else Bot")

    # Git repository CSV file URL
    csv_file_url = "https://github.com/Huzaifa-ali/Scraping/blob/main/mechanical_flow_measurement_devices.csv"

    data = read_csv_file(csv_file_url)

    # User input for the question
    user_question = st.text_input("Ask me a question")

    if user_question:
        found_paragraphs = search_keywords(user_question, data)

        if found_paragraphs:
            st.subheader("Found paragraphs:")
            for paragraph in found_paragraphs:
                st.write(paragraph)
        else:
            st.write("No matching paragraphs found.")

if __name__ == "__main__":
    main()