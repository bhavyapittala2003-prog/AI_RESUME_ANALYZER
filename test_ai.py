from ollama import chat

response = chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain Python in one simple sentence."
        }
    ]
)

print(response.message.content)