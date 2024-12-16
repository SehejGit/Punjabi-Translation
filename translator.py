import streamlit as st
from googletrans import Translator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import pandas as pd
import random

# Initialize the translator
translator = Translator()

# Load the Punjabi words data
@st.cache_data
def load_swear_words(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        st.error(f"Error loading funny words data: {e}")
        return pd.DataFrame(columns=["Word", "Meaning"])

swear_words_df = load_swear_words("swear_words.csv")

# Function to transliterate Punjabi text into Latin script
def transliterate_punjabi(text):
    return transliterate(text, sanscript.GURMUKHI, sanscript.ITRANS)

# Function to randomly generate a sentence using funny words
def generate_random_sentence():
    # Define sentence templates
    templates = [
        "The [adjective] [noun] is [verb]",
        "I saw the [adjective] [noun] near the [noun]",
        "He likes to [verb] with the [adjective] [noun]",
        "What a [adjective] [noun]!",
        "They [verb] the [noun] every day.",
        "[noun] , that is unbelievable!"
    ]
    
    # Split the funny words into categories
    nouns = swear_words_df[swear_words_df['Category'] == 'noun']['Word'].tolist()
    verbs = swear_words_df[swear_words_df['Category'] == 'verb']['Word'].tolist()
    adjectives = swear_words_df[swear_words_df['Category'] == 'adjective']['Word'].tolist()
    
    # Select a random template
    template = random.choice(templates)
    
    # Replace placeholders with random words from the appropriate categories
    if '[noun]' in template:
        template = template.replace("[noun]", random.choice(nouns), 1)
    if '[verb]' in template:
        template = template.replace("[verb]", random.choice(verbs), 1)
    if '[adjective]' in template:
        template = template.replace("[adjective]", random.choice(adjectives), 1)
    
    return template
    
# Inject custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: white; /* Set background to white */
        color: #87CEEB; /* Sky blue font color */
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #87CEEB; /* Sky blue for all headers */
    }

    .stButton>button {
        background-color: #87CEEB; /* Sky blue button background */
        color: white; /* White text for buttons */
    }

    .stTextInput>div>div>input {
        color: #87CEEB; /* Sky blue text inside input boxes */
    }

    .stMarkdown p {
        color: #87CEEB; /* Sky blue for all markdown text */
    }
    
    .st-expander-header {
        color: #87CEEB; /* Sky blue for expander headers */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set up the Streamlit app
st.title("English to Punjabi Learning Guide")

# Create tabs for Translator and Funny Words
tabs = st.tabs(["Translator", "Slang Punjabi Words and Phrases", "Generate Random Sentence"])

with tabs[0]:
    st.header("Translator")
    # Input from the user
    input_text = st.text_area("Enter text in English:")

    # When the user presses the "Translate" button
    if st.button("Translate"):
        if input_text:
            try:
                # Translate the text to Punjabi (Gurmukhi script)
                translation = translator.translate(input_text, src='en', dest='pa')
                punjabi_text = translation.text
                
                # Transliterate the Punjabi (Gurmukhi) script into Latin script
                transliterated_text = transliterate_punjabi(punjabi_text).lower()
                
                # Optional: Highlight swear words in the transliterated text
                for index, row in swear_words_df.iterrows():
                    punjabi_word = row['Word']
                    meaning = row['Meaning']
                    if punjabi_word in transliterated_text:
                        # Highlight the swear word
                        transliterated_text = transliterated_text.replace(
                            punjabi_word, f"**{punjabi_word}** (_{meaning}_)"
                        )

                st.subheader("Translation in Punjabi (Transliterated):")
                st.write(transliterated_text)
            except Exception as e:
                st.error(f"Translation failed: {e}")
        else:
            st.warning("Please enter some text to translate.")

with tabs[1]:
    st.header("Search Slang Punjabi Words by Meaning")
    
    # Input field for searching by meaning
    search_meaning = st.text_input("Enter the meaning to search for a Punjabi word:")
    
    if search_meaning:
        # Find matching words based on the meaning
        matched_words = swear_words_df[swear_words_df['Meaning'].str.contains(search_meaning, case=False, na=False)]
        
        if not matched_words.empty:
            st.write("Matching Punjabi Words:")
            
            # Loop through each word and show only the word initially
            for index, row in matched_words.iterrows():
                word = row['Word']
                meaning = row['Meaning']
                
                # Create an expander that reveals the meaning when clicked
                with st.expander(word):
                    st.write(f"Meaning: {meaning}")
        else:
            st.write("No matching words found for the given meaning.")


with tabs[2]:
    st.header("Generate Random Sentence Using Funny Punjabi Words")
    
    if not swear_words_df.empty:
        # Display a button to generate a random sentence
        if st.button("Generate Sentence"):
            random_sentence = generate_random_sentence()
            st.write(random_sentence)
    else:
        st.write("No funny words data available.")

# Notes to fix - fix funny to slang and get one good sentence structure 
