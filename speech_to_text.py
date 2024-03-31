import speech_recognition as sr


class SpeechToText():
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
    
    def convert_speech_to_text(self,audio_file_path):
        with sr.AudioFile(audio_file_path) as source:
            # Listen for the data (load audio to memory)
            audio_data = self.recognizer.record(source)
            text = ""
            # Recognize (convert from speech to text)
            try:
                text = self.recognizer.recognize_google(audio_data)
                print(text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
        

            return text

# # Initialize recognizer class (for recognizing the speech)
# recognizer = sr.Recognizer()

# # Load your audio file
# audio_file_path = 'test_audios/Recording.wav'

# # Use the audio file as the audio source
# with sr.AudioFile(audio_file_path) as source:
#     # Listen for the data (load audio to memory)
#     audio_data = recognizer.record(source)
#     # Recognize (convert from speech to text)
#     try:
#         text = recognizer.recognize_google(audio_data)
#         print(text)
#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#     except sr.RequestError as e:
#         print(f"Could not request results from Google Speech Recognition service; {e}")


