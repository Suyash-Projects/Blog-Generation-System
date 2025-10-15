import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
print(f"Testing API Key: {api_key[:20]}..." if api_key else "No API key!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    default_headers={
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Blog Generation System"
    }
)

try:
    response = client.chat.completions.create(
        model="meta-llama/llama-3.2-3b-instruct:free",
        messages=[{"role": "user", "content": "Say hello"}],
        temperature=0.7
    )
    print("✅ API Key is VALID!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ API Key is INVALID: {e}")
    print("\nThe key is either:")
    print("1. Expired")
    print("2. Invalid")
    print("3. Account deleted")
    print("\nGet a new key from: https://openrouter.ai/keys")