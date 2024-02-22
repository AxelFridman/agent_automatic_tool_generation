import os
import json

def generate_visualization(messages):
    # create or modify messages.txt

    with open("messages.txt", "w") as file:
        file.write("")

    # each message has its own line being appended
    for mes in messages:
        if(type(mes)!=dict):
            continue
        with open("messages.txt", "a") as file:
            if(mes["content"]==None):
                mes["content"] = ""
            if(mes["role"] == "tool"):
                mes["role"] = "tool_"+mes["name"]
                mes["content"] = "After running with arguments \n     "+ mes["args"] +"\n      it returned: \n      "+ mes["content"]

            else:
                file.write(mes["role"] + ": " + mes["content"] + "\n")
            file.write("\n")

messages = [
        {"role": "system", "content": "You are a helpful assistant with the ability to orchestrate many functions to solve problems. When unsure you ask the user feedback, when finished and you think you have responded succesfully you run end_conversation function."},
        {"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}
    ]
#generate_visualization(messages=messages)
