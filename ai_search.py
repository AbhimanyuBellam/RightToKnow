import google.generativeai as genai

gemini_api_key = ""
genai.configure(api_key=gemini_api_key)

class Gemini():
  def __init__(self, create_new_chat=True) -> None:
    self.model = genai.GenerativeModel('gemini-pro')
    self.gemini_chat = self.model.start_chat()
  
  def ask_gemini(self, conversation):
    response = self.gemini_chat.send_message(conversation)
    text = response.text

    

    to_extracat_from = ["**Answer:**", "proof.", "Assistant**", "Assistant:**"]
    for to_extract in to_extracat_from:
      if to_extract in text:
        index = text.rfind(to_extract)
        output = text[index+len(to_extract):]

        output = output.replace("*", "")

        return output
        
    text = text.replace("*", "")
    return text
  


# #For formatting
# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# gemini_api_key = "AIzaSyDKNjuXDUZNM0gnxcVKUl9Rne9fkKPM0Bo"
# genai.configure(api_key=gemini_api_key)
# # print(gemini_api_key) 

# query = "Rules for driving in North Carolina"

# model = genai.GenerativeModel('gemini-pro')

# gemini_chat = model.start_chat()

# # Identify who is the speaker of that sentence based on the text. 

# conversation = f"""
# The following is a conversation between a police officer and a driver. After which, there is a question, please answer that.

# Good evening, sir. I’m Officer Johnson. Do you know why I pulled you over? Uh, no, officer. Was I speeding? Yes, you were. You were going 
# 20 miles over the speed limit. 
# That’s quite reckless, don’t you think? Get out of the car. I'm going to search your car. And don't record me! 


# Is there any law that protects me? Be specific about the details of the laws, put them in bullet points, 
# and limit it to 500 words and point us to the government document section that works as a proof. 

# """

# response1 = gemini_chat.send_message(conversation)
# print(response1.text)

# response2 = gemini_chat.send_message("what is my name?")
# print(response2.text)