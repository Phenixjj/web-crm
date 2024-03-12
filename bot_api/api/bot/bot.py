import json
import subprocess


# Function to pull a model from a specified API
def pull_model(model_name):
    """
    This function sends a request to an API to pull a model.

    Args:
        model_name (str): The name of the model to be pulled.

    Returns:
        None
    """
    # Define the command to pull the model
    pull_command = (
        f"""curl -s http://ollama:11434/api/pull -d '{{"name": "{model_name}"}}'"""
    )

    # Execute the command
    process = subprocess.Popen(
        pull_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    process.communicate()


# Function to generate a response from a specified API
def generate_response(prompt):
    """
    This function sends a request to an API to generate a response.

    Args:
        prompt (str): The prompt to be sent to the API.

    Returns:
        str: The response from the API.
    """
    # Define the command to generate the response
    curl_command = f"""curl -s http://ollama:11434/api/generate -d '{{"model": "mistral", "prompt":"{prompt}"}}'"""

    # Execute the command
    process = subprocess.Popen(
        curl_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Initialize the full response
    full_response = ""

    # Loop to read the output line by line
    while True:
        output_line = process.stdout.readline()
        if not output_line and process.poll() is not None:
            break
        if output_line:
            try:
                # Try to parse the output line as JSON
                response_data = json.loads(output_line.strip())
                # Append the response to the full response
                full_response += response_data.get("response", "")
            except json.JSONDecodeError:
                # If the output line is not valid JSON, return an error
                return "Invalid response format", 500
    return full_response


# Function to get user input and generate a response
def get_user_input_and_generate():
    """
    This function gets a prompt from the user and generates a response.

    Returns:
        None
    """
    # Get the prompt from the user
    prompt = input("Enter a prompt: ")
    # Generate the response
    response = generate_response(prompt)
    # Print the response
    print("Response:", response)


# Main function
if __name__ == "__main__":
    # Call the function to get user input and generate a response
    get_user_input_and_generate()
