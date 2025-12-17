import os
import openai
from dotenv import load_dotenv

# Load environment variables once
load_dotenv()

# Set API key from env
openai.api_key = os.getenv("OPENAI_API_KEY")

def llm_complete(prompt: str, temperature: float = 0.2, max_tokens: int = 800, model: str = "gpt-4o-mini", json_mode: bool = False) -> str:
    """
    Generate a completion from the LLM.
    
    Args:
        prompt: The user prompt.
        temperature: Creativity parameter (0.0 to 1.0).
        max_tokens: Maximum tokens to generate.
        model: Model identifier.
        
    Returns:
        The generated text content.
    """
    if not openai.api_key:
        print("WARNING: OPENAI_API_KEY is not set.")
        return "[MOCK] LLM Response (No API Key)"

    client = openai.OpenAI(api_key=openai.api_key)

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert writer." + (" You output JSON." if json_mode else "")},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"} if json_mode else None
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"LLM Error: {e}")
        return f"[ERROR] Could not generate text: {e}"
