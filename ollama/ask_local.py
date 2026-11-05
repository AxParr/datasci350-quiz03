from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="granite4:350m",
    messages=[{"role": "user", "content": "What does git commit do?"}],
    temperature=0,
)

print(response.choices[0].message.content)
print(response.usage)
