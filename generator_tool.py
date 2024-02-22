import os
from openai import OpenAI
import json
import example.functions
import example.functions2

import example.functions_utils
import example.functions2_utils


from dotenv import load_dotenv

load_dotenv()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

def generate_tools_json_from_functions(filepath="functions.py"):

    with open("example/functions.py", 'r') as file:
        # Read the entire content of the file into a string
        functions_content_example1 = file.read()

    with open("example/functions2.py", 'r') as file:
        # Read the entire content of the file into a string
        functions_content_example2 = file.read()

    functions_util_tool_json1 = json.dumps(example.functions_utils.tools, indent=4)
    functions_util_tool_json2 = json.dumps(example.functions2_utils.tools, indent=4)


    with open("functions.py", 'r') as file:
        functions_real = file.read()

    messages = [{"role": "system", "content":
                    "You are a helpful assistant whose job is to generate a JSON called tools that lists all the functions present in a file and describes them to be consumed by openAi api"},#, the JSON generated should follow this schema: " + schema},
                {"role": "user", "content": functions_content_example1},
                {"role": "assistant", "content": functions_util_tool_json1},
                {"role": "user", "content": "Great, now that you get how it works lets try with a new different file that is independant from the last example"},
                {"role": "user", "content": functions_content_example2},
                {"role": "assistant", "content": functions_util_tool_json2},
                {"role": "user", "content": "Great, now that you get how it works lets try with a new different file that is independant from the last example"},
                {"role": "user", "content": functions_real}]

    endFunc =   {
                    "type": "function",
                    "function": {
                        "name": "end_conversation",
                        "description": "Ends the conversation. Run only when the conversation is finished and the user is satisfied with the result",
                            "parameters": {
                            "type": "object",
                            "properties": {
                            },
                            "required": []
                        }
                    }
                }


    response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                response_format={ "type": "json_object" },
                messages=messages)


    tools = (response.choices[0].message.content)
    tools = json.loads(tools)
    tools["functions"].append(endFunc)
    with open("tools.json", 'w') as file:
        file.write(json.dumps(tools, indent=4))
