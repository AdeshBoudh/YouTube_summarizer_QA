import streamlit as st
from yt_summarizer_and_QA.src.yt_summarizer_qa import *

def main():
    st.title("YouTube Summarizer and Question Answering")

    # Input for YouTube URL
    youtube_url = st.text_input("Enter a YouTube URL")
    
    # Submit button for URL submission
    if st.button("Submit"):
        if youtube_url:
            video_id = extract_video_id(youtube_url)
            transcript_paragraph = fetch_and_translate_transcript(video_id)
            
            # Generate and store summary and FAQ in session_state
            st.session_state['summary'] = summarize_text(transcript_paragraph)
            st.session_state['faq'] = generate_faq(transcript_paragraph)
            st.session_state['transcript_paragraph'] = transcript_paragraph  # Store for answering questions

    # Display Summary if available
    if 'summary' in st.session_state:
        st.subheader("Summary")
        st.markdown(st.session_state['summary'])

    # Display FAQs if available
    if 'faq' in st.session_state:
        st.subheader("FAQs")
        st.markdown(st.session_state['faq'])

        # Input for question and display answer
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