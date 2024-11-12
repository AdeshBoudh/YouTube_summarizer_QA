import os
from dotenv import load_dotenv
load_dotenv()

google_api = os.environ['google_api']

if not  google_api:
    raise ValueError("Google API key not found. Please set 'google_api' in the .env file.")


import google.generativeai as genai

genai.configure(api_key=google_api)
model = genai.GenerativeModel("gemini-1.5-flash")

import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

# List of supported languages with their ISO codes
supported_languages = {
    "English": "en",
    "Japanese": "ja",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-Hans",
    "Chinese (Traditional)": "zh-Hant",
    "Korean": "ko",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Dutch": "nl",
    "Arabic": "ar",
    "Hindi": "hi",
    "Swedish": "sv",
    "Norwegian": "no",
    "Danish": "da",
    "Finnish": "fi",
    "Greek": "el",
    "Polish": "pl",
}

# Regular expression pattern to extract the video ID
def extract_video_id(url):
    pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|embed/|v/|.+/|)([\w-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Function to fetch and translate transcript
def fetch_and_translate_transcript(video_id):
    transcript_paragraph = ""

    try:
        # Get available transcripts (manual and auto-generated)
        transcript_info = YouTubeTranscriptApi.list_transcripts(video_id)

        # Check if an English transcript is available
        for transcript in transcript_info:
            language_code = transcript.language_code

            if language_code == "en":
                # Directly fetch the English transcript if available
                entries = transcript.fetch()
                transcript_paragraph += " ".join([entry['text'] for entry in entries])
                break  # Stop after fetching the English transcript

            elif language_code in supported_languages.values():
                # Translate the transcript to English if it's in a supported language
                translated_transcript = transcript.translate('en').fetch()
                transcript_paragraph += " ".join([entry['text'] for entry in translated_transcript])
                break  # Stop after fetching the translated transcript

    except TranscriptsDisabled:
        print("Transcripts are disabled for this video.")
    except Exception as e:
        print("An error occurred:", e)

    return transcript_paragraph


"""
# YouTube URL
url = "https://youtu.be/qV3yjIyj7Dc?si=fT2pWkNSecaoZwmL"


# Extract video ID from URL
video_id = extract_video_id(url)

# Fetch and print the transcript paragraph
if video_id:
    transcript_paragraph = fetch_and_translate_transcript(video_id)
    # print(transcript_paragraph)
else:
    print("Invalid YouTube URL.")
"""


def summarize_text(transcript_paragraph):
    response = model.generate_content([f"The text is transcript of a YouTube Video. Summarize the following text in detail: {transcript_paragraph}. Present them in points if possible."])
    return response.text

"""
summary = summarize_text(transcript_paragraph)
print(summary)
"""

def generate_faq(transcript_paragraph):

    response = model.generate_content([f"""
    The following text is a transcript of a YouTube Video: {transcript_paragraph}

    Generate 10 frequently asked questions (FAQs) related to these topics.
    Finally, extract information from the transcript that can be used to answer each FAQ.

    Please ensure that the generated FAQs and answers do not infringe on any copyrights.
    If you encounter any potentially copyrighted material, please skip it and focus on other parts of the transcript.
    """])
    return response.text

"""
faq = generate_faq(transcript_paragraph)
print(faq)

question = input("Enter your question: ")
"""

def question_text(transcript_paragraph, question):
    response = model.generate_content([f"Please answer the following question based on the provided text: {transcript_paragraph}. Question: {question}"])
    response_text = response.text
    cleaned_text = response_text.replace('\n', '')
    return cleaned_text


"""
answer = question_text(transcript_paragraph, question)
answer
"""

def initialize_chatbot_context(transcript_paragraph):
    """
    Initializes the chatbot context with the given transcript paragraph.
    Returns a list to store conversation history.
    """
    # Starting context message for the chatbot, summarizing the source of the information
    conversation_history = [
        f"This is a QA chatbot. The information source is a transcript of a YouTube video. "
        f"Feel free to ask questions based on this content:\n\n{transcript_paragraph}\n"
    ]
    return conversation_history

def qa_chatbot(conversation_history, user_question):
    """
    Chatbot function that takes conversation history and user question as input.
    Generates a response based on the context and returns the updated history.
    """
    # Add the user's question to the conversation history
    conversation_history.append(f"User: {user_question}")

    # Prepare the prompt to send to the model
    prompt = "\n".join(conversation_history) + "\nBot:"

    # Generate the response
    response = model.generate_content([prompt])
    bot_answer = response.text.strip()  # Get the bot's answer and strip any leading/trailing whitespace

    # Add the bot's answer to the conversation history
    conversation_history.append(f"Bot: {bot_answer}")

    return bot_answer, conversation_history