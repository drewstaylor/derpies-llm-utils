#!/usr/bin/python3

import os
import time
import json
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
)

model = os.environ.get('OPENAI_MODEL')

data_dir = './log/'
log_suffix = '.json'
chat_history = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Chat worker
async def ask(prompt) -> None:
    print("\n")
    print(bcolors.OKCYAN + model + " says:" + bcolors.ENDC + "\n")

    user_message = {
        "role": "user",
        "content": prompt,
    }

    stream = await client.chat.completions.create(
        messages=[user_message],
        model=model,
        stream=True,
    )

    chunks = []
    async for chunk in stream:
        chunks.append(chunk.choices[0].delta.content or "")
        print(chunk.choices[0].delta.content or "", end="")
    
    assembled_chunks = "".join(chunks)
    assistant_message = {
        "role": "assistant",
        "content": assembled_chunks,
    }

    chat_history.append(user_message)
    chat_history.append(assistant_message)

    # End of content
    print("\n")

# Export log
def export():
    timestamp = int(time.time())
    file = data_dir + str(timestamp) + log_suffix
    
    with open(file, 'w') as f:
        json.dump(chat_history, f)
        print(bcolors.OKGREEN + "Chat history exported to " + file)

# Dynamic chat instance
async def chat():
    print(bcolors.OKCYAN + "What would you like to know?" + bcolors.ENDC + "\n" + bcolors.OKBLUE + "('x' to exit, 'log' to export a chat log)" + bcolors.ENDC + "\n")

    prompt = input()

    if prompt == 'log':
        export()
    elif prompt != 'x':
        await ask(prompt)
        await chat()

async def main():
    await chat()

# Start program
asyncio.run(main())