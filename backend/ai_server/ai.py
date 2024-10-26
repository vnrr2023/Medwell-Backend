from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
client=Groq(api_key=os.environ['GROQ'])


def get_model_response(prompt,text):
    chat_completion=client.chat.completions.create(
        messages=[{'role':"system","content":prompt},{"role":"user","content":text}],
        model="llama3-70b-8192"
    )
    return chat_completion.choices[0].message.content
