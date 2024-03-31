from ai_search import Gemini
from speech_to_text import SpeechToText


audio_file_path = "test_audios/Recording.wav"

speech_to_text_engine = SpeechToText()
text_from_speech = speech_to_text_engine.convert_speech_to_speech(audio_file_path)

gemini_bot = Gemini()

first_prompt_flag = True

if first_prompt_flag:
    first_prompt_text = "The following is a conversation between a police officer and a driver. "
    first_prompt_flag = False
prompt = f"""
        
        Split up the 
        After which, there is a question, please answer that.
        
        {text_from_speech}

        Is there any law that protects me? Be specific about the details of the laws, put them in bullet points, 
        and limit it to 500 words and point us to the government documents on the web that work as a proof. 
        """

gemini_response = gemini_bot.ask_gemini(prompt)

print(gemini_response)
