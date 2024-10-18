import streamlit as st
import random
import time

st.title("Travel Dropbox BTT")
st.write("Input your content, and watch as our bot generates your travel itinerary and provides recommendations!")
st.caption("Note only PDFs, text, and images are permitted.")

# need to fix color
st.markdown("""
<style>
button {
    background-color: #456990;
    color: #D8E1EB;
}
</style>"""
, unsafe_allow_html=True)

with st.form("my_form"):
    st.write("Select one of the two modes of submitting.")
    
    # add dropdown menu so both don't show up at once 
    text_val = st.text_area("Copy and paste your email(s).",value="", placeholder="Emails", label_visibility="visible")
    
    uploaded_files = st.file_uploader(
    "Choose a file(s).", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("text", text_val, "image",uploaded_file )
st.text(" ")
# add on-click open the next form
# need to update button spacing
with st.form("itinerary_form"):
    st.write("Travel Itinerary")
    st.caption("Our generator compiles your content into an easy to read format. You may regenerate the itinerary as you see fit.")
    passengers = st.text_area("Passengers",value="", placeholder="Original response", label_visibility="visible")
    flights = st.text_area("Flight Information",value="", placeholder="Original response", label_visibility="visible")
    st.warning('Flight has already happened.', icon="⚠️")
    hotel = st.text_area("Hotel Information",value="", placeholder="Original response", label_visibility="visible")
    activities = st.text_area("Activities",value="", placeholder="Original response", label_visibility="visible")
    
    col1, col2 = st.columns(2)
    with col1:
        saved = st.form_submit_button("Save Itinerary")
    with col2:
        regenerated = st.form_submit_button("Regenerate Itinerary")
    # add actions for forms 

# will need to update edit vs safe versions 
with st.form("final_itinerary_form"):
    st.write("Travel Itinerary")
    with st.expander("Passengers"):
        st.write("1. Name: ")
    with st.expander("Flight Information"):
        st.write("Departure: ")
        st.write("Arrival: ")
        st.write("Booking Reference: ")
        st.write("Flight Code: ")
    with st.expander("Hotel Information"):
        st.write("Check-In: ")
        st.write("Check-Out: ")
        st.write("Address: ")
    with st.expander("Activities"):
        st.write("Title: ")
        st.write("Date: ")
        st.write("Reference: ")
    st.caption("Safe travels!")
    col1, col2 = st.columns(2)
    with col1:
        saved = st.form_submit_button("Export PDF")
    with col2:
        regenerated = st.form_submit_button("Save Text")
    # add on-click actions for forms 

# as something nice to have for project, can add these features at end once everything else is finalized 
st.text(" ")
st.subheader("Next Steps")

# space for a restaurant API, could be automatically called 

# placeholder code
def response_generator():
    yield "Placeholder, would be the list of recommendations"
        
# one option 
st.write("Restaurant Option 1")
with st.chat_message("assistant"):
    st.write("Would you now like restaurant recommendations?")

    prompt = st.chat_input("Say something")
    if prompt == "Yes":
        st.write(f"User wants restaurant recommendations based on itinerary information.") # existing location
        response = st.write_stream(response_generator())
    if prompt == "No":
        st.write("Have a good day!")
    #st.session_state.messages.append({"role": "assistant", "content": response})
       # end 
# other option, automatically done 
    # need to add call to API 
st.write("Restaurant Option 2")
with st.chat_message("assistant"):
    st.write("Based on your itinerary, we recommend these restaurants:")
    response = st.write_stream(response_generator())

# space for uber API
st.write("Uber")
with st.form("uber_call"):
    st.write("Space for Uber API")
    submitted = st.form_submit_button("Book Transportation")

# add back to top button
