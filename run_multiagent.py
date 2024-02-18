import os
from openai import OpenAI
import json

OPENAI_API_KEY='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'
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

# Set your OpenAI API key here
class Agent:
    def __init__(self, nameId, descriptionForOthers=""):
        self.nameId = nameId
        self.callSign = "@calling:"+nameId+"@"
        self.descriptionForOthers = descriptionForOthers

    def __str__(self):
        return self.nameId

    def get_callsign(self):
        return self.callSign

    def get_description(self):
        return self.descriptionForOthers

    def is_generative(self):
        return False

class ExecutionAgent(Agent):
    def main(self, command):
        self.execute_command(command)

    def execute_command(self, command):
        """Execute a shell command and return the output."""
        result = os.popen(command).read()
        #print(f"Executing command: {command}\nResult: {result}")
        return result

class FeedbackAgent(Agent):
    def main(self, prompt):
        return self.get_feedback(prompt)
    def get_feedback(self, prompt):
        """Simulate getting feedback from the user."""
        # In a real application, this would involve a more complex dialogue system
        response = input(prompt)
        return response

class CodeGenerationAgent(Agent):
    def main(self, prompt):
        self.generate_code(prompt)


    def is_generative(self):
        return True

    def generate_code(self, prompt):
        """Generate code based on a prompt using OpenAI's Codex."""
        try:
            #prompt = f'System: you are {self.get_description()}\and the conversation so far is: {prompt}'
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",  # Use an appropriate engine for code generation
                prompt=prompt,
                temperature=0.5,
                max_tokens=150,
                stop=None
            )
            generated_code = response.choices[0].text.strip()
            print(f"Generated code: {generated_code}")
            return generated_code
        except Exception as e:
            print(f"Error in generating code: {e}")
            return None

class FileInformationAgent(Agent):
    def main(self, file_name):
        return self.retrieve_code_in_file(file_name)

    def retrieve_code_in_file(self, file_name):
        """Get the code from a file as string."""
        try:
            with open(file_name, 'r') as file:
                # Read the entire content of the file into a string
                file_content = file.read()

            # Now, 'file_content' contains the whole content of 'file.py' as a string
            # You can use 'file_content' as needed in your program
            return(file_content)

        except Exception as e:
            print(f"Error in retrieving code: {e}")
            return None

class DirectoryInformationAgent(Agent):
    def main(self, directory):
        return self.build_tree(directory)

    def add_node(self, path, name, is_dir):
            node = {"name": name, "full_root_path": os.path.join(path, name)}
            if is_dir:
                node["children"] = []
            return node
    def build_tree(self, directory):
        root_node = self.add_node(directory, os.path.basename(directory), True)
        for root, dirs, files in os.walk(directory):
            # Find the parent node in the tree for the current path
            parts = root.split(os.sep)
            current_node = root_node
            for part in parts[1:]:
                for child in current_node.get("children", []):
                    if child["name"] == part:
                        current_node = child
                        break

            # Add directories as children
            for dir_name in dirs:
                dir_node = self.add_node(root, dir_name, True)
                current_node["children"].append(dir_node)

            # Add files as children
            for file_name in files:
                file_node = self.add_node(root, file_name, False)
                current_node["children"].append(file_node)

        return str(root_node)
# Example usage

class Agent_system():
    def __init__(self, agents, human_prompt="make a conversation with me as a friendly dog, i want to chat with you."):
        self.agents = agents
        self.verify_unique_agents()
        self.messages = []
        self.logs = []
        self.human_prompt = human_prompt
        self.orchestrator_give_next()

    def orchestrator_give_next(self):
        print("messages:" + str(self.messages))
        print("logs:" + str(self.logs))
        desc = self.agents_description()
        try:
            prompt = f'System: you are an orchestrator that should call the next agent and decide what input give to it. IMPORTANT: You must only call one agent at most. The human prompt that you should satisfy is: {self.human_prompt}. The agent description is: {self.agents_description()} and the conversation so far is: {str(self.messages)} if you wish to call no one call @calling:exit@. First call the agent (or exit) and then write the prompt'
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",  # Use an appropriate engine for code generation
                prompt=prompt,
                temperature=0.5,
                max_tokens=150,
                stop=None
            )
            generated_response = response.choices[0].text.strip()
            self.logs.append(str("Orchestrator: ") + generated_response)
            if("@calling:exit@" in generated_response):
                return None
            else:
                agent = generated_response.split("@calling:")[1].split("@")[0]
                prompt = generated_response.split("@calling:")[1].split("@")[1]
                self.call_agent(agent, prompt)

        except Exception as e:
            print(f"Error in generating orchestrator: {e}")
            return None

    def call_agent(self, agent, prompt):
        agent = self.agent_map[agent]
        res = agent.main(prompt)
        self.messages.append(res)
        self.logs.append(str(agent.nameId)+": " + res)

        self.orchestrator_give_next()

    def verify_unique_agents(self):
        agent_map = {}
        agent_description = {}
        for agent in self.agents:
            if agent.nameId in agent_map.keys():
                # Raise an exception if an agent with the same name already exists
                raise ValueError(f"Agent with name {agent.nameId} already exists")
            agent_map[agent.nameId] = agent
            agent_description[agent.nameId]  = agent.get_description() + " to call this agent use the following call sign: " + agent.get_callsign()

        self.agent_map = agent_map
        self.agent_description = agent_description

    def agents_description(self):
        return str(self.agent_description)








execution_agent = ExecutionAgent("execution_agent", "An Agent that has the ability to execute shell commands, and provide feedback of its response to other agents. Input to this agent must be terminal executable with no other addittion or comment")
feedback_agent = FeedbackAgent("feedback_agent", "An Agent that has the ability to provide feedback to other agents from the user, use when unsure on how to continue or when a decision is needed. Input to this agent must be a question or a prompt for the user to answer.")
code_generation_agent = CodeGenerationAgent("codegen1_agent", "An Agent that has the ability to generate code based on a prompt using OpenAI's Codex. Input to this agent must be a prompt for the code generation.")
file_data_agent = FileInformationAgent("data_agent", "An Agent that has the ability to retrieve code from a file and provide it to other agents. Input to this agent must be a file name and it will return as string all the content of the file.")
directory_data_agent = DirectoryInformationAgent("directory_agent", "An Agent that has the ability to retrieve all the information of the directory and return it as a tree dictionary.")

agents = [execution_agent, feedback_agent, code_generation_agent, file_data_agent, directory_data_agent]
agent_system = Agent_system(agents, "Help the user make the terminal commands he needs. Ask about what he needs first")
#agent_system.send_message("Hello, world!")

"""
print(agent_system.agents_description())

print(1/0)
print(input("Enter any key to continue..."))

data_file = file_data_agent.retrieve_code_in_file("test_file.py")
print(data_file)

tree = file_data_agent.build_tree('.')
print(tree)
# Execution Agent example
execution_agent.execute_command("echo Hello, world!")

# Feedback Agent example
feedback = feedback_agent.get_feedback("Do you want to add more features? (yes/no): ")
feedback_agent.provide_feedback_to_generation_agent(feedback)

# Code Generation Agent example
#prompt = "Write a Python function to add two numbers"
#code_generation_agent.generate_code(prompt)
"""
