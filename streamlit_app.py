import streamlit as st

st.title("Travel Dropbox BTT")
st.write("Input your content, and watch as our bot generates your travel itinerary and provides recommendations!")
st.caption("Note only PDFs, text, and images are permitted.")

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

# add on-click open the next form

with st.form("itinerary_form"):
    st.write("Travel Itinerary")
    st.caption("Our generator compiles your content into an easy to read format. You may regenerate the itinerary as you see fit.")

    saved = st.form_submit_button("Save Itinerary")
    regenerated = st.form_submit_button("Regenerate Itinerary")
    # add buttons on same line
    # add actions for forms 

# will need to update edit vs safe versions 
with st.form("final_itinerary_form"):
    st.write("Travel Itinerary")
    st.caption("Safe travels!")

    saved = st.form_submit_button("Export PDF")
    regenerated = st.form_submit_button("Save Text")
    # add buttons on same line
    # add on-click actions for forms 
