#!/usr/bin/python3

import os
import sys
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
    print('Fine tuning model created successfully')


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


async def main():
    command = sys.argv[1]
    value = sys.argv[2]
    if command == "upload":
        await upload_training_data(value)
    elif command == "tune":
        await create_fine_tuning(value)
    elif command == "status":
        await fetch_fine_tuning_status(value)
    else:
        raise ValueError("Command not found " + command + ". Possible commands are: 'upload', 'tune', 'status'")

asyncio.run(main())