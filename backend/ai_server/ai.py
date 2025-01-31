from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
client=Groq(api_key=os.environ['GROQ'])


def get_model_response(prompt,text):
    chat_completion=client.chat.completions.create(
        messages=[{'role':"system","content":prompt},{"role":"user","content":text}],
        model="llama-3.3-70b-versatile"
    )
    return chat_completion.choices[0].message.content
