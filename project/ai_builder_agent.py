import json
from backend.llm_api import initialize_client, get_ai_response

class AIBuilderAgent:
    def __init__(self):
        self.client = initialize_client()
        self.build_agent_history = []

    def start_requirement_gathering(self):
        # Initial prompt to start the requirement gathering conversation
        initial_prompt = (
            "You are an assistant that helps users build custom AI agents. "
            "Please ask the user about the steps and functionalities they want their custom agent to have."
        )
        self.build_agent_history.append({"role": "system", "content": initial_prompt})
    
    def add_user_message(self, message):
        # Adds user's message to the conversation history
        self.build_agent_history.append({"role": "user", "content": message})

    def add_ai_response(self, message):
        # Adds AI's response to the conversation history
        self.build_agent_history.append({"role": "assistant", "content": message})

    def generate_agent_definition(self):
        # Prompt to generate strict JSON definition of the agent
        strict_json_prompt = (
            "Now that you've gathered all the requirements, please generate a JSON definition of the agent "
            "with the following structure:\n\n"
            "```json\n"
            "{\n"
            '  "initial_node": "node_name",\n'
            '  "nodes": {\n'
            '    "node_name": {\n'
            '      "type": "node_type",\n'
            '      "next_node": "next_node_name",\n'
            '      "button_text": "Button Text",\n'
            '      "prompt": "Prompt text for the node (if applicable)"\n'
            '    },\n'
            '    // ... other nodes\n'
            '  }\n'
            "}\n"
            "```\n\n"
            "Ensure that the JSON only contains the necessary fields and strictly follows the above structure. "
            "Do not include any additional explanations or text outside the JSON code block."
        )
        self.build_agent_history.append({"role": "system", "content": strict_json_prompt})
        
        # Get AI response containing the JSON definition
        ai_response = get_ai_response(self.client, "mistral-large-latest", self.build_agent_history)
        
        # Parse JSON from AI response
        try:
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

    def get_build_agent_history(self):
        return self.build_agent_history
