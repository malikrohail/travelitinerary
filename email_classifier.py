import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai  
import time

load_dotenv()

# Get the API key
API_KEY = os.getenv('GENAI_API_KEY')  

# Configure the  AI model
genai.configure(api_key=API_KEY)  
model = genai.GenerativeModel("gemini-1.5-flash")  

# Load datasets
df_booking = pd.read_csv('/Users/test/Downloads/dropbox/travel-itinerary/data/booking.csv', header=None)
df_non_booking = pd.read_csv('/Users/test/Downloads/dropbox/travel-itinerary/data/nonbooking.csv', header=None)
#print(df_booking.shape)
#print(df_non_booking.shape)

# Print the first few rows and columns
#print("Booking Data Sample:")
#print(df_booking.head())

#print("\nNon-Booking Data Sample:")
#print(df_non_booking.head())

# Function to load and save emails without classification
def load_and_save_emails():
    # Load the booking dataset
    df_booking = pd.read_csv('/Users/test/Downloads/dropbox/travel-itinerary/data/booking.csv', header=None)
    # Load the non-booking dataset
    df_non_booking = pd.read_csv('/Users/test/Downloads/dropbox/travel-itinerary/data/nonbooking.csv', header=None)

    # Initialize a list to hold email content with their type labels
    categorized_emails = []

    # Capture booking emails
    for index, row in df_booking.iterrows():
        for email in row.dropna().astype(str):  # Iterate over each email in the row
            categorized_emails.append({'Email_Content': email, 'Email_Type': 1})  # 1 for booking

    # Capture non-booking emails
    for index, row in df_non_booking.iterrows():
        for email in row.dropna().astype(str):  # Iterate over each email in the row
            categorized_emails.append({'Email_Content': email, 'Email_Type': 0})  # 0 for non-booking

    # Create a DataFrame for output
    output_df = pd.DataFrame(categorized_emails)  # Create DataFrame with email content and type labels

    # Print the total number of categorized email contents before saving
    #print(f"Total number of email contents before saving: {len(output_df)}")  # Print the count of email contents

    # Save the results to a new CSV file
    output_csv_path = '/Users/test/Downloads/dropbox/travel-itinerary/data/categorized_emails.csv'
    output_df.to_csv(output_csv_path, index=False)  # Save with appropriate headers

    # Print the total number of email contents saved
    #print(f"Total number of email contents saved to CSV: {len(output_df)}")  # Print the count of email contents saved
   # #print(f"Results saved to {output_csv_path}")

def classify_emails():
    # Load the emails from the previously saved categorized CSV file
    df = pd.read_csv('/Users/test/Downloads/dropbox/travel-itinerary/data/categorized_emails.csv')
    
    # Ensure that each email is treated individually
    emails = df['Email_Content'].tolist()

    predictions = []
    
    # only 5 emails 
    for email in emails[5:10]:  
        prompt = (
            f"You are an email classification assistant. Please classify the following email:\n\n"
            f"Email Content: {email}\n\n"
            f"Classify this email as 0 for non-booking and 1 for booking. "
            f"Provide only the number (0 or 1) as your response."
        ) 
        
        try:
            response = model.generate_content(prompt)  # Generate content using the model
            predicted_label = response.candidates[0].content.parts[0].text.strip()  # Extract the predicted label
            
            # Ensure the response is strictly binary
            if predicted_label not in ['0', '1']:
                print(f"Unexpected response for email: {email}. Response: {predicted_label}")
                predictions.append(None)  # Append None if the response is not binary
            else:
                predictions.append(predicted_label)  # Append the predicted label to the list
            
        
        except Exception as e:
            print(f"An error occurred while processing email: {email}. Error: {e}")
            predictions.append(None)  # Append None if there's an error

    # Create a new DataFrame for the predictions
    predictions_df = pd.DataFrame({'Email_Content': emails[5:10], 'Predicted_Label': predictions})  # Create DataFrame with email content and predictions
    # Map binary values to labels
    predictions_df['Predicted_Label'] = predictions_df['Predicted_Label'].map({'0': 'non-booking', '1': 'booking'})
    # Save the results to a new CSV file
    output_csv_path = '/Users/test/Downloads/dropbox/travel-itinerary/data/classified_emails_with_labels.csv'
    predictions_df.to_csv(output_csv_path, index=False) 
    print(f"Results saved to {output_csv_path}")

# Main execution
if __name__ == "__main__":
    load_and_save_emails()  # Load and save emails without classification
    classify_emails()  # Classify emails using gemini