import openai
import os

# Set API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(prompt_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

prompt = "Explain what is a large language model in three simple sentences."
response_text = ask_gpt(prompt)

print("---My Prompt---")
print(prompt)
print("\n---GPT's RESPONSE---")
print(response_text)
