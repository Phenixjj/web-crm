import subprocess
import json


def pull_model(model_name):
    pull_command = f"""curl -s http://ollama:11434/api/pull -d '{{"name": "{model_name}"}}'"""
    try:
        process = subprocess.Popen(pull_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process.communicate()
        return {"Response": f"Model {model_name} pulled successfully"}
    except Exception as e:
        return {"Response": f"Failed to pull model: {str(e)}"}


def generate_response(prompt):
    curl_command = f"""curl -s http://ollama:11434/api/generate -d '{{"model": "mistral", "prompt":"{prompt}"}}'"""

    process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    full_response = ""

    while True:
        output_line = process.stdout.readline()
        if not output_line and process.poll() is not None:
            break
        if output_line:
            try:
                response_data = json.loads(output_line.strip())
                full_response += response_data.get("response", "")
            except json.JSONDecodeError:
                return "Invalid response format", 500
    return full_response


def get_user_input_and_generate():
    prompt = input("Enter a prompt: ")
    response = generate_response(prompt)
    print("Response:", response)


if __name__ == '__main__':
    get_user_input_and_generate()
