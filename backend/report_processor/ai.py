from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
client=Groq(api_key=os.environ["GROQ_KEY"])


def get_model_response(prompt,text):
    chat_completion=client.chat.completions.create(
        messages=[{'role':"system","content":prompt},{"role":"user","content":text}],
        model="llama-3.3-70b-versatile"
    )
    return chat_completion.choices[0].message.content

