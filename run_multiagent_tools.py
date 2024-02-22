import os
from openai import OpenAI
import json
import conversation_visualizer
import inspect
from dotenv import load_dotenv
import generator_tool
import functions

load_dotenv()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

def get_tools(path="tools.json"):
    with open(path, 'r') as file:
        # Read the entire content of the file into a string
        tools = json.load(file)
    return tools


def run_conversation(initialPrompt, maxCicles = 20, generateTools = True):
    # Step 1: send the conversation and available functions to the model
    messages = [{"role": "system", "content":
                 "You are a helpful assistant with the ability to orchestrate many functions to solve problems. Only one function at a time, after you get the response you can run a new function or the same, but only after. When unsure you ask the user feedback, when finished and you think you have responded succesfully you run end_conversation function."},
                 {"role": "user", "content": initialPrompt}]
    messagesMine =  messages.copy()
    if(generateTools):
        generator_tool.generate_tools_json_from_functions()
    tools = get_tools()["functions"]

    available_functions = {name: obj for name, obj in inspect.getmembers(functions, inspect.isfunction)}
    ciclo = 1
    while True:
        print("cicle "+str(ciclo))
        ciclo = ciclo + 1
        if(ciclo > maxCicles):
            print("maxCicles reached")
            return messages
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        messages.append(response_message)  # extend conversation with assistant's reply
        messagesMine.append(response_message)
        messagesMine.append({"role": "assistant", "content": response_message.content})
        conversation_visualizer.generate_visualization(messages=messagesMine)

        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors

            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                if(function_name == "end_conversation"):
                    messagesMine.append( {
                        "role": "tool_end_conversation",
                        "content": "end_conversation was called, the conversation is over.",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                    })
                    conversation_visualizer.generate_visualization(messages=messagesMine)
                    return messages
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                function_response = function_to_call(**function_args)


                data =   {
                        "role": "tool",
                        "content": function_response,

                        "tool_call_id": tool_call.id,
                        "name": function_name,
                    }
                messages.append(data)  # extend conversation with function response
                data2 = data.copy()
                data2["args"] = tool_call.function.arguments
                messagesMine.append(data2)
            conversation_visualizer.generate_visualization(messages=messagesMine)

run_conversation(
                initialPrompt="say Hi and then end the conversation ",
                #initialPrompt="chat with me like a robot, in order for me to talk ask for my feedback, never end this conversation until i say so",
                 maxCicles = 20,
                 generateTools = True)
