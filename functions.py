import os
import subprocess


def axel_request(message, end=" the end"):
    if(message == "subscribe"):
        return "Axel has been subscribed to the newsletter" + end
    else:
        return "I do not understand that message"

def run_on_terminal(command):
    try:
        # Run the command and capture both stdout and stderr
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Return stdout if the command was successful
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Return stderr if the command failed
        return f"Error in executing command: {e.stderr}"
    except Exception as e:
        return f"Unexpected error: {e}"

def get_user_feedback(question):
    """Simulate getting feedback from the user."""
    # In a real application, this would involve a more complex dialogue system
    response = input(question)
    return response


def get_file_content(filepath):
    """Get the code from a file as string."""
    try:
        with open(filepath, 'r') as file:
            # Read the entire content of the file into a string
            file_content = file.read()

        # Now, 'file_content' contains the whole content of 'file.py' as a string
        # You can use 'file_content' as needed in your program
        return(file_content)

    except Exception as e:
        return (f"Error in retrieving code: {e}")

def add_node(path, name, is_dir):
            node = {"name": name, "full_root_path": os.path.join(path, name)}
            if is_dir:
                node["children"] = []
            return node

def get_directory_tree():
    directory = os.getcwd()
    root_node = add_node(directory, os.path.basename(directory), True)
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
            dir_node = add_node(root, dir_name, True)
            current_node["children"].append(dir_node)

        # Add files as children
        for file_name in files:
            file_node = add_node(root, file_name, False)
            current_node["children"].append(file_node)

    return str(root_node)

def get_personal_information_about_user(user_name):
    if(user_name == "Axel" or user_name == "axel"):
        name = "Axel Fridman"
        age = "22"
        job = "Software Engineer"
    elif(user_name == "Juan" or user_name == "juan"):
        name = "Juan W."
        age = "27"
        job = "AI Engineer"
    elif(user_name == "chechu" or user_name == "cecilia"):
        name = "Cecilia B."
        age = "24"
        job = "Data Scientist"
    else:
        return "I do not have information about that user"
    return str({"name": name, "age": age, "job": job})
