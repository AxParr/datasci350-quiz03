import json

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="commentator",
    messages=[{"role": "user", "content": 'Reply in JSON with the keys "answer" and "confidence". What does git commit do?'}],
    temperature=0,
    max_tokens=300,
    response_format={"type": "json_object"},
)

reply = response.choices[0].message.content
print(reply)
print(response.choices[0].finish_reason)
print(json.loads(reply)["answer"])
