import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
)

async def upload_training_data() -> None:
    file = await client.files.create(
        file=open("data/default-08-22-2024.jsonl", "rb"),
        purpose="fine-tune"
    )

    print(file)
    print('\n')
    print('Training set successfully uploaded')

async def create_fine_tuning() -> None:
    ft = await client.fine_tuning.jobs.create(
        training_file="file-nzrtkKyIv3lDfBR78bqODYKn",
        model="gpt-4o-mini-2024-07-18"
    )

    print(ft)
    print('\n')
    print('Fine tuned model created successfully')

async def fetch_fine_tuning_status() -> None:
    ft = await client.fine_tuning.jobs.retrieve("ftjob-uwTC0Z5FZb42OKAPheCbHF2k")

    print(ft)
    print('\n')
    print('Fine tuning status checked successfully')

async def main():
    # await upload_training_data()
    # await create_fine_tuning()
    await fetch_fine_tuning_status()

asyncio.run(main())

# UPLOAD OUTPUT:
# FileObject(id='file-nzrtkKyIv3lDfBR78bqODYKn', bytes=8303, created_at=1724346770, filename='default-08-22-2024.jsonl', object='file', purpose='fine-tune', status='processed', status_details=None)

# CREATE TUNING OUTPUT:
# FineTuningJob(id='ftjob-uwTC0Z5FZb42OKAPheCbHF2k', created_at=1724347360, error=Error(code=None, message=None, param=None), fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(n_epochs='auto', batch_size='auto', learning_rate_multiplier='auto'), model='gpt-4o-mini-2024-07-18', object='fine_tuning.job', organization_id='org-0hI4vtfrSaFsHmuE2k55ImHb', result_files=[], seed=406982310, status='validating_files', trained_tokens=None, training_file='file-nzrtkKyIv3lDfBR78bqODYKn', validation_file=None, estimated_finish=None, integrations=[], user_provided_suffix=None)

# TUNING STATUS OUTPUT:
'''
FineTuningJob(
  id='ftjob-uwTC0Z5FZb42OKAPheCbHF2k', 
  created_at=1724347360, 
  error=Error(code=None, message=None, param=None),
  fine_tuned_model='ft:gpt-4o-mini-2024-07-18:personal::9z5uyT9b', 
  finished_at=1724347783, 
  hyperparameters=Hyperparameters(n_epochs=4, batch_size=1, learning_rate_multiplier=1.8), 
  model='gpt-4o-mini-2024-07-18', 
  object='fine_tuning.job', 
  organization_id='org-0hI4vtfrSaFsHmuE2k55ImHb', 
  result_files=['file-ScJQ4jFxtamu2EJ2COAMIjtP'], 
  seed=406982310, 
  status='succeeded', 
  trained_tokens=6104, 
  training_file='file-nzrtkKyIv3lDfBR78bqODYKn', 
  validation_file=None, 
  estimated_finish=None, 
  integrations=[], 
  user_provided_suffix=None
)
'''