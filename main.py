import streamlit as st
import speech_recognition as sr
import pyaudio

language_codes = {
    'English (US)': 'en-US',
    'English (UK)': 'en-GB',
    'Spanish (Spain)': 'es-ES',
    'Spanish (Mexico)': 'es-MX',
    'French (France)': 'fr-FR',
    'German (Germany)': 'de-DE',
    'Italian (Italy)': 'it-IT',
    'Portuguese (Brazil)': 'pt-BR',
    'Chinese (Simplified, China)': 'zh-CN',
    'Chinese (Traditional, Taiwan)': 'zh-TW',
    'Japanese (Japan)': 'ja-JP',
    'Korean (South Korea)': 'ko-KR',
    'Russian (Russia)': 'ru-RU',
    'Dutch (Netherlands)': 'nl-NL',
    'Swedish (Sweden)': 'sv-SE',
    'Turkish (Turkey)': 'tr-TR',
    'Arabic (Saudi Arabia)': 'ar-SA',
    'Hindi (India)': 'hi-IN',
    'Bengali (Bangladesh)': 'bn-BD',
    'Thai (Thailand)': 'th-TH'
}


def transcribe_speech(api, language=None, ibm_username=None, ibm_password=None, wit_key=None):
    # Initialize recognizer class
    r = sr.Recognizer()
    # Reading Microphone as source
    with sr.Microphone() as source:
        st.info("Speak now...")
        # listen for speech and store in audio_text variable
        audio_text = r.listen(source)
        st.info("Transcribing...")

        try:
            if api == 'google':
                text = r.recognize_google(audio_text, language=language)
            elif api == 'ibm':
                text = r.recognize_ibm(audio_text, language=language, username=ibm_username, password=ibm_password)
            elif api == 'wit':
                text = r.recognize_wit(audio_text, key=wit_key)
            elif api == 'OpenAI Whisper (English only)':
                text = r.recognize_whisper(audio_text)
            return text
        except ValueError as e:
            return f"Sorry, I did not get that. : {e}"


def main():
    st.title("Speech Recognition App")
    st.write("Click on the microphone to start speaking:")
    available_languages = list(language_codes.keys())

    api = st.selectbox(label='Choose an API', options=['OpenAI Whisper (English only)', 'google', 'ibm', 'wit'],
                       help='In process')
    language = 'English (US)'
    ibm_username = None
    ibm_password = None
    wit_key = None

    if api != 'OpenAI Whisper (English only)':
        language = st.selectbox(label='Choose a language',
                                options=available_languages,
                                help='In process')

    if api == 'ibm' or api == 'wit':
        if api == 'ibm':
            ibm_username = st.text_input(label='Enter your IBM username:')
            ibm_password = st.text_input(label='Enter your IBM password:', type='password')
        elif api == 'wit':
            wit_key = st.text_input(label='Enter your WIT key:', type='password')


    # add a button to trigger speech recognition
    if st.button("Start Recording"):
        st.write("Language selected: ", language_codes[language], " \nAPI selected :", api)
        text = transcribe_speech(api=api, language=language_codes[language], ibm_username=ibm_username, ibm_password=ibm_password, wit_key=wit_key)
        st.write("Transcription: ", text)
        st.download_button(label='Download the transcribed text as a text file', data= text, file_name='output.txt')


if __name__ == "__main__":
    main()
