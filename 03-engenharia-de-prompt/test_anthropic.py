from dotenv import load_dotenv
import os
import traceback

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("ERROR: ANTHROPIC_API_KEY not set")
    raise SystemExit(1)

from anthropic import Anthropic

client = Anthropic(api_key=api_key)
model = "claude-3-5-sonnet-20241022"

try:
    response = client.messages.create(
        model=model,
        max_tokens=100,
        messages=[{"role": "user", "content": "What is the capital of Brazil?"}],
    )
    # Print a short confirmation and the model text output
    try:
        print("SUCCESS")
        print(response.content[0].text)
    except Exception:
        print("SUCCESS but couldn't parse response object")
        print(response)
except Exception:
    print("REQUEST FAILED")
    traceback.print_exc()
