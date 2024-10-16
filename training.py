#!/usr/bin/python3

import os
import sys
import json
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
)

model = os.environ.get('OPENAI_TRAINING_MODEL')

'''
Example:
$ ./training.py moderation "data/default-08-22-2024.jsonl"

Response:
ModerationCreateResponse(id='modr-9d6a9a4050ce03fcabc5459faa9ed4ac', model='omni-moderation-latest', results=[Moderation(categories=Categories(harassment=False, harassment_threatening=False, hate=False, hate_threatening=False, self_harm=False, self_harm_instructions=False, self_harm_intent=False, sexual=False, sexual_minors=False, violence=False, violence_graphic=False, harassment/threatening=False, hate/threatening=False, illicit=False, illicit/violent=False, self-harm/intent=False, self-harm/instructions=False, self-harm=False, sexual/minors=False, violence/graphic=False), category_scores=CategoryScores(harassment=0.01970237400537813, harassment_threatening=0.0008097716541842735, hate=0.00015011822567369918, hate_threatening=6.814872211615988e-06, self_harm=0.0005011211542112085, self_harm_instructions=0.00022690684744977127, self_harm_intent=0.000249784072058715, sexual=0.3738115514626793, sexual_minors=0.001098694263059318, violence=0.0006001064513491806, violence_graphic=8.092757566536092e-06, harassment/threatening=0.0008097716541842735, hate/threatening=6.814872211615988e-06, illicit=0.0038130026525290957, illicit/violent=1.7130819343483194e-05, self-harm/intent=0.000249784072058715, self-harm/instructions=0.00022690684744977127, self-harm=0.0005011211542112085, sexual/minors=0.001098694263059318, violence/graphic=8.092757566536092e-06), flagged=False, category_applied_input_types={'harassment': ['text'], 'harassment/threatening': ['text'], 'sexual': ['text'], 'hate': ['text'], 'hate/threatening': ['text'], 'illicit': ['text'], 'illicit/violent': ['text'], 'self-harm/intent': ['text'], 'self-harm/instructions': ['text'], 'self-harm': ['text'], 'sexual/minors': ['text'], 'violence': ['text'], 'violence/graphic': ['text']})])
'''
async def check_moderation(filepath) -> None:
    print('Preparing to check moderation for file', filepath, '\n')
    inputs = []
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            jsonl = json.loads(line)
            if 'messages' in jsonl:
                for message in jsonl['messages']:
                    if 'role' in message and 'content' in message:
                        if message['role'] == 'assistant' or message['role'] == 'system':
                            parsed = {"type": "text","text": message['content']}
                            inputs.append(parsed)

    moderation = await client.moderations.create(
        model="omni-moderation-latest",
        input=inputs
    )
    print(moderation,'\n')
    print('Moderation checked successfully')


'''
Example:
$ ./training.py upload "data/default-08-22-2024.jsonl"

Response:
FileObject(id='file-nzrtkKyIv3lDfBR78bqODYKn', bytes=8303, created_at=1724346770, filename='default-08-22-2024.jsonl', object='file', purpose='fine-tune', status='processed', status_details=None)
'''
async def upload_training_data(filepath) -> None:
    print('Uploading training set at path', filepath, '\n')
    file = await client.files.create(
        file=open(filepath, "rb"),
        purpose="fine-tune"
    )
    print(file, '\n')
    print('Training set successfully uploaded')


'''
Example:
$ ./training.py tune "file-nzrtkKyIv3lDfBR78bqODYKn"

Response:
FineTuningJob(id='ftjob-uwTC0Z5FZb42OKAPheCbHF2k', created_at=1724347360, error=Error(code=None, message=None, param=None), fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(n_epochs='auto', batch_size='auto', learning_rate_multiplier='auto'), model='gpt-4o-mini-2024-07-18', object='fine_tuning.job', organization_id='org-0hI4vtfrSaFsHmuE2k55ImHb', result_files=[], seed=406982310, status='validating_files', trained_tokens=None, training_file='file-nzrtkKyIv3lDfBR78bqODYKn', validation_file=None, estimated_finish=None, integrations=[], user_provided_suffix=None)
'''
async def create_fine_tuning(file_id) -> None:
    print('Preparing to tune', file_id, '\n')
    ft = await client.fine_tuning.jobs.create(
        training_file=file_id,
        model=model
    )
    print(ft,'\n')
    print('Fine tuning job created successfully')


'''
Example:
$ ./training.py status "ftjob-uwTC0Z5FZb42OKAPheCbHF2k"

Response:
FineTuningJob(id='ftjob-uwTC0Z5FZb42OKAPheCbHF2k', created_at=1724347360, error=Error(code=None, message=None, param=None), fine_tuned_model='ft:gpt-4o-mini-2024-07-18:personal::9z5uyT9b', finished_at=1724347783, hyperparameters=Hyperparameters(n_epochs=4, batch_size=1, learning_rate_multiplier=1.8), model='gpt-4o-mini-2024-07-18', object='fine_tuning.job', organization_id='org-0hI4vtfrSaFsHmuE2k55ImHb', result_files=['file-ScJQ4jFxtamu2EJ2COAMIjtP'], seed=406982310, status='succeeded', trained_tokens=6104, training_file='file-nzrtkKyIv3lDfBR78bqODYKn', validation_file=None, estimated_finish=None, integrations=[], user_provided_suffix=None)
'''
async def fetch_fine_tuning_status(job) -> None:
    print('Checking status of job', job, '\n')
    ft = await client.fine_tuning.jobs.retrieve(job)
    print(ft, '\n')
    print('Fine tuning status checked successfully')

def help():
    print("Usage:")
    print("./training.py [command] [arg]\n")
    print("Available Commands:\n")
    print("moderation [file path]   Check if a training file doesn't violate moderation filters.")
    print("upload [file path]       Upload a training file at the specified path. Returns a file ID.")
    print("tune [file id]           Queues a training / tuning job. Returns a job ID.")
    print("status [job id]          Fetches the status of a tuning job. Returns a model ID if training completed.")
    print("help                     Print this help message")

async def main():
    if len(sys.argv) <= 1:
        return help()
    command = sys.argv[1]
    if len(sys.argv) > 2:
        value = sys.argv[2]
    if command == "moderation":
        await check_moderation(value)
    elif command == "upload":
        await upload_training_data(value)
    elif command == "tune":
        await create_fine_tuning(value)
    elif command == "status":
        await fetch_fine_tuning_status(value)
    elif command == "help":
        help()

    else:
        raise ValueError("Command not found \"" + command + "\". Possible commands are: \"upload\", \"tune\", \"status\". \"help\"")

asyncio.run(main())