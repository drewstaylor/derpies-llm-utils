import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
)

suffix = " Your response should be silly and sassy."

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
    print(bcolors.OKCYAN + "gpt-4o-mini" + bcolors.ENDC + ":\n")

    stream = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt + suffix,
            }
        ],
        model="ft:gpt-4o-mini-2024-07-18:personal::9z5uyT9b",
        stream=True,
    )

    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")
    
    # End of content
    print("\n")

# Dynamic chat instance
async def chat():
    print(bcolors.OKCYAN + "What would you like to know?" + bcolors.ENDC + "\n" + bcolors.OKBLUE + "('x' to exit)" + bcolors.ENDC + "\n")

    prompt = input()
    if prompt != 'x':
        await ask(prompt)
        await chat()

async def main():
    await chat()

# Start program
asyncio.run(main())