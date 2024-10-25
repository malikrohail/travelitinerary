import streamlit as st
import google.generativeai as genai


# back-end functions


def extract_passengers(response):
   sections = response.split("Passengers:")
   passengers = sections[1].split("Flight Information:")[0]
   return passengers


def extract_flights(response):
   sections = response.split("Flight Information:")
   flights = sections[1].split("Travel Information:")[0]
   return flights


def extract_hotel(response):
   sections = response.split("Travel Information:")
   hotel = sections[1].split("Activities:")[0]
   return hotel


def extract_activities(response):
   sections = response.split("Activities:")
   return sections[1]


st.markdown('# Travel Itinerary Generator')
st.write("Input your content, and watch as our bot generates your travel itinerary and provides recommendations!")
st.caption("Note only PDFs, text, and images are permitted.")
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown("""
   <style>
   button:first-child {
       background-color: #456990;
       color: #D8E1EB;
       border-radius:10px 10px 10px 10px;
       height: 2.5em;
       width: 7em;
   }
   </style>
   """, unsafe_allow_html=True)


if 'current_form' not in st.session_state:
   st.session_state.current_form = 'initial'  # Track which form to show
show_next_steps = False


if st.session_state.current_form == 'initial':
   with st.form("initial_form"):
       st.write("Select one of the two modes of submitting.")
      
       # add dropdown menu so both don't show up at once


       # text
       text_val = st.text_area("Copy and paste your email(s).",value="", placeholder="Emails", label_visibility="visible")
       st.session_state.travel_info = text_val


       # files
       uploaded_files = st.file_uploader(
       "Choose a file(s).", accept_multiple_files=True)
       for uploaded_file in uploaded_files:
           bytes_data = uploaded_file.read()
           st.write("File:", uploaded_file.name)
           st.write(bytes_data)


       submitted = st.form_submit_button("Submit")
       if submitted:
           generated_itinerary = model.generate_content("Generate a travel itineray based on these emails, organize response by 4 category titles, passengers, flight information, travel information, and activities if applicable: " + text_val)
           st.session_state.generated_itinerary = generated_itinerary
           formatted_response = generated_itinerary.candidates[0].content.parts[0].text
           st.session_state.formatted_response = formatted_response
           #st.write(formatted_response)
           #st.write("image",uploaded_file )
           #show_itinerary_form = True # will allow next form to show up now
           #show_final_itinerary_form = False
           #show_initial_form = False
           st.session_state.current_form = 'itinerary'


st.text(" ")


if st.session_state.current_form == 'itinerary':
   with st.form("itinerary_form"):
       st.write("Travel Itinerary")
       st.caption("Our generator compiles your content into an easy to read format. You may regenerate the itinerary as you see fit.")
       passengers_info = extract_passengers(st.session_state.formatted_response)
       flights_info = extract_flights(st.session_state.formatted_response)
       hotel_info = extract_hotel(st.session_state.formatted_response)
       activities_info = extract_activities(st.session_state.formatted_response)


       passengers = st.text_area("Passengers",value=passengers_info, placeholder=passengers_info, label_visibility="visible")
       flights = st.text_area("Flight Information",value=flights_info, placeholder=flights_info, label_visibility="visible")
       st.warning('Flight has already happened.', icon="⚠️")
       hotel = st.text_area("Hotel Information",value=hotel_info, placeholder=hotel_info, label_visibility="visible")
       activities = st.text_area("Activities",value=activities_info, placeholder=activities_info, label_visibility="visible")


       saved = st.form_submit_button("Save")
       if saved:
           st.session_state.current_form = 'final'


if st.session_state.current_form == 'final':
   with st.form("final_itinerary_form"):
       st.write("Travel Itinerary")
       st.caption("Safe travels!")


       with st.expander("Passengers"):
           #st.write("1. Name: ")
           st.write(passengers)


       with st.expander("Flight Information"):
           #st.write("Departure: ")
           #st.write("Arrival: ")
           #st.write("Booking Reference: ")
           #st.write("Flight Code: ")
           st.write(flights)


       with st.expander("Hotel Information"):
           #st.write("Check-In: ")
           #st.write("Check-Out: ")
           #st.write("Address: ")
           st.write(hotel)


       with st.expander("Activities"):
           #st.write("Title: ")
           #st.write("Date: ")
           #st.write("Reference: ")
           st.write(activities)


       col1, col2 = st.columns(2)
       with col1:
           saved = st.form_submit_button("Export PDF")
           show_next_steps = True
       with col2:
           regenerated = st.form_submit_button("Save Text")
           show_next_steps = True




if st.session_state.current_form != 'initial':
   if st.button("Start Over"):
       st.session_state.current_form = 'initial'



#def export_itinerary(p, f, h, a):
   # return f"Passengers:\n{p}\n\nFlight Information:\n{f}\n\Travel Information:\n{h}\n\nActivities:\n{a}"
#saved_text = st.download_button("Save Text", itinerary_text, file_name="itinerary.txt")
#itinerary_text = export_itinerary(passengers, flights, hotel, activities)

















# as something nice to have for project, can add these features at end once everything else is finalized 
st.text(" ")

if show_next_steps: 
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
        submitted = st.form_submit_button("Book")

st.markdown('[Back to Top](#travel-itinerary-generator)')

