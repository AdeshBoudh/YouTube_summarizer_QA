import streamlit as st
from yt_summarizer_and_QA.src.yt_summarizer_qa import *

st.set_page_config(layout="wide")

def main():
    st.title("YouTube Summarizer and Question Answering")

    # Input for YouTube URL
    youtube_url = st.text_input("Enter a YouTube URL", value=st.session_state.get('youtube_url', ''))

    # Submit button for URL submission
    if st.button("Submit"):
        if youtube_url:
            st.session_state['youtube_url'] = youtube_url  # Save the URL in session state
            video_id = extract_video_id(youtube_url)
            transcript_paragraph = fetch_and_translate_transcript(video_id)

            # Generate and store summary and FAQ in session_state
            st.session_state['summary'] = summarize_text(transcript_paragraph)
            st.session_state['faq'] = generate_faq(transcript_paragraph)
            st.session_state['transcript_paragraph'] = transcript_paragraph  # Store for answering questions

    # Check if summary and FAQ are available in session state to display them
    if 'summary' in st.session_state and 'faq' in st.session_state:
        col1, col2 = st.columns(2)

        with col1:
            # Display Summary if available
            st.header("Video Summary")
            st.markdown(st.session_state['summary'])

        with col2:
            # Display FAQs if available
            st.header("Frequently Asked Questions (FAQs)")
            st.markdown(st.session_state['faq'])

        # Show QA session only after summary and FAQ have been generated
        st.subheader("Ask a Question")
        question = st.text_input("Enter your question")

        if st.button("Get Answer"):
            if question:
                answer = question_text(st.session_state['transcript_paragraph'], question)
                st.session_state['answer'] = answer

        # Display Answer if available
        if 'answer' in st.session_state:
            st.subheader("Answer")
            st.markdown(st.session_state['answer'])

if __name__ == "__main__":
    main()
