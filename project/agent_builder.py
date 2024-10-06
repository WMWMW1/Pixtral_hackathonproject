import json
from backend.llm_api import initialize_client, get_ai_response

def build_ai_agent(build_agent_history):
    # Initialize Mistral client
    client = initialize_client()

    # Get AI response with the strict JSON prompt already included in the chat history
    ai_response = get_ai_response(client, "mistral-large-latest", build_agent_history)
    
    # Parse JSON from AI response
    try:
        # Extract JSON block from response
        start = ai_response.find("```json")
        end = ai_response.find("```", start + 7)
        if start != -1 and end != -1:
            json_str = ai_response[start + 7:end].strip()
            agent_json = json.loads(json_str)
            return agent_json
        else:
            print("AI response does not contain a JSON block.")
            return None
    except json.JSONDecodeError:
        print("Unable to parse AI response as JSON.")
        return None
