"""
CMD Command written and executed by AI.
Latest update: 01.12.2023
A console-based program that executes commands in CMD based on human language input.
If something didn't work, try adjusting the variable context.
"""

# Import necessary modules
import subprocess
import ctypes
import sys
import importlib
import time

# Install necessary modules
required_modules = ['openai']

missing_modules = []

for module in required_modules:
    try:
        importlib.import_module(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    for module in missing_modules:
        try:
            subprocess.check_call([f"pip install {module}"])
        except subprocess.CalledProcessError as e:
            print(f'Start failed. Program will break in 5s')
            time.sleep(5)
            sys.exit()

# Import necessary modul
import openai

# Set OpenAI API key
openai.api_key = ''

# Initial context providing instructions to the AI
context = "From now on, you are an AI that only provides ready-made commands to be executed in Windows CMD as requested. If a command requires a username, replace it with %USERNAME%. Strive to execute commands as precisely as possible. Do not add anything else to your responses. Execute all commands whenever possible in a single line."

# Generate AI response using OpenAI's GPT-3.5-turbo model.
def ai(prompt):
    global context
    messages = [{"role": "system", "content": context}, {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    # Check if the script is run with administrator privileges
    if ctypes.windll.shell32.IsUserAnAdmin():
        
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "bye", "exit"]:
                break

            # Generate AI response
            response = ai(user_input)
            print(response)

            # Prompt user to execute the generated command
            ask = input("Continue y/n: ")
            if ask.lower() == "y":
                # Execute the command in CMD
                process = subprocess.Popen(response, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()
                if process.returncode == 0:
                    print("Done")
                else:
                    print("Something went wrong")
            else:
                pass

    else:
        # If not run as admin, attempt to run the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)