import os
import openai
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Load your API key from an environment variable or secret management service
openai.api_key = os.environ.get("OPENAI_API_KEY")


content = """\left[\begin{array}{ll}
1 & 0 \\
0 & 1
\end{array}\right] * \left[\begin{array}{ll}
2 & 0 \\
0 & 3
\end{array}\right] and explain the steps"""

message = [
    {"role": "user", "content": content}
]


chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message)

print(chat_completion["choices"][0]["message"]["content"])
