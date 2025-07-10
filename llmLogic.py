import getpass
import json
import re
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder



# Load credentials and check for API key



def format_hotspot(hotspot: dict) -> str:
    return "\n".join(f"{k}: {v}" for k, v in hotspot.items())

def analyze_hotspot(hotspot):

    model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "I will provide you with an object which has 'Vulnerability Name', 'File', 'Line', and 'Code Snippet'. "
                "Based on this information, reply with a **JSON object** of the format "
                "{{'Vulnerability Name': 'A short proper vulnerability name', 'Detailed Observation': 'A 1-2 line description of the vulnerability', "
                "'Impact': 'A 1-2 line impact of the vulnerability', 'Recommendation': 'A 1-2 line recommendation of the vulnearbility', "
                "'False Positive': 'Yes, Maybe or No'}}. Respond with JSON only."
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    formatted = format_hotspot(hotspot)
    prompt = prompt_template.format_prompt(messages=[HumanMessage(content=formatted)])
    # input_message = [HumanMessage(hotspot)]
    response = model.invoke(prompt)
    # return response.content
    
    try:
        cleaned = re.sub(r"^```(?:json)?\n|```$", "", response.content.strip(), flags=re.IGNORECASE | re.MULTILINE)
        result = json.loads(cleaned)
        return result
    except json.JSONDecodeError:
        # Optional: fallback or error handling
        print("Failed to parse JSON. Raw response:", response.content)
        return {
                "Vulnerability Name": hotspot["Vulnerability Name"],
                "Detailed Observation": "-",
                "Impact": "-",
                "Recommendation": "-",
                "False Positive": "maybe",
                }  # or None / raise an exception