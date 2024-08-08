from pyshelle import ShelleClient
import re
import webbrowser
import streamlit as st

# Get input file from user
st.set_page_config(page_title="LFI Audit Assist", page_icon="🧊", layout="wide")
st.header(":blue[LFI Audit Assist]")

uploaded_file = st.file_uploader(
    label="Upload a csv file and get the insights", type=["csv"]
)

# Initializing Credentials
CLIENT_ID = ""
CLIENT_PASS = ""
CLIENT_SECRET = ""
SUBSCRIPTION_KEY = ""
ENDPOINT = ""

dict = {}
p = []
extracted_text = ""
url = ""
pattern = r"\(/TempImageProxy/[^)]+\)"


# Function to load file and take in prompts to answer
def file_prompt(prompt, file):
    APPLICATION_ID = 4  # Csv_Agent
    client = ShelleClient(
        APPLICATION_ID,
        CLIENT_ID,
        CLIENT_PASS,
        CLIENT_SECRET,
        subscription_key=SUBSCRIPTION_KEY,
        endpoint=ENDPOINT,
        proxies={
            #
            #
        },
    )
    file.seek(0)
    response = client.upload_file(buffer=file)
    response = client.get_response(prompt)
    if not response.error:
        trimmed_message = response.message
        trimmed_message = trimmed_message.split("Invoking")[-1].split("\n\n")[1:]
        output_final = "Your question : " + prompt + "\n\n"
        for i in trimmed_message:
            output_final = output_final + i + "\n"
        output_final = output_final.replace("\n\n", "\n").strip()
        return output_final


# Function to get the response and call azure assistant to build the plot
def file_prompt_2(prompt, file):
    APPLICATION_ID = 4  # Csv_Agent
    client = ShelleClient(
        APPLICATION_ID,
        CLIENT_ID,
        CLIENT_PASS,
        CLIENT_SECRET,
        subscription_key=SUBSCRIPTION_KEY,
        endpoint=ENDPOINT,
        proxies={
            #
            #
        },
    )
    file.seek(0)
    response = client.upload_file(buffer=file)
    response = client.get_response(prompt)
    if not response.error:
        dict[prompt] = response.message
        azure_assist(dict[prompt])


# Function for azure assitant call
def azure_assist(a):
    APPLICATION_ID = 47  # Azure_Assistant_Agent
    client = ShelleClient(
        APPLICATION_ID,
        CLIENT_ID,
        CLIENT_PASS,
        CLIENT_SECRET,
        subscription_key=SUBSCRIPTION_KEY,
        endpoint=ENDPOINT,
        proxies={
            #
            #
        },
    )
    response = client.get_response(
        "Give me the plot instead of python code for bar chart on your analysis on"
        + " "
        + a
    )
    if not response.error:
        match = re.search(pattern, response.message)
        if match:
            extracted_text = match.group(0)[1:-1]  # Remove the parentheses
            url = "https://uat-shell-e-chat.shell.com/api" + extracted_text
            st.write(url)
            webbrowser.open_new_tab(url)
            return


# Suggetions once file uploaded
output = ""
if uploaded_file is not None:
    if st.button("Click here to visualize events vs most occurrences"):
        file_prompt_2(
            "Show me the result of events which are repeated and their count of occurence",
            uploaded_file,
        )
    st.write(
        ":green[Get detailed insights about the data by clicking below suggestions or type in your own question in the input box:]"
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Show me event  ID with RAM Potential 4A,B,C,D"):
            output = file_prompt(
                "Show me event  ID with RAM Potential 4A,B,C,D", uploaded_file
            )

    with col2:
        if st.button("Show me events repeated Most no of times"):
            output = file_prompt(
                "Show me events repeated Most no of times", uploaded_file
            )

    with col3:
        if st.button("Show me the Trends of 2024 Events"):
            output = file_prompt("Show me the Trends of 2024 Events ", uploaded_file)

    x = st.text_input(
        "Enter your question", placeholder="Eg: Get all the events from 2023"
    )
    if x != "":
        output = file_prompt(x, uploaded_file)
    if output != "":
        with st.container(border=True):
            st.write(output)
