# Derpies Training and Model Testing

This repo contains code for training and testing custom Derpies OpenAI language models (LLMs)

1. [chat.py](./chat.py) - Test an LLM
2. [training.py](./training.py) - Train and tune an LLM

## Setup and Installation

Install dependencies
```bash
pip install -r requirements.txt
```

Create environment file
```bash
cp env.example .env
```

Configure environment file
```
# Example `.env` file settings:

# 1. API key for accessing OpenAI API
OPENAI_API_KEY="secret"

# 2. Model for LLM testing (chat.py)
OPENAI_MODEL="ft:gpt-4o-mini-2024-07-18:personal::9z5uyT9b" 

# 3. Model for LLM training (training.py)
OPENAI_TRAINING_MODEL="gpt-4o-mini-2024-07-18"
```

## Training an LLM

1. Create an input training file (for file format and training prompt examples see the [data](./data/) folder)
2. Upload your training file to OpenAI. If your file has formatting mistakes, it will be rejected.
3. Queue a training job (returns a job id)
4. Fetch the status of a job id (returns a custom model if job is completed)

#### Running the `help` Command

Command example
```bash
./training.py help
```

Response example
```bash
Usage:
./training.py [command] [arg]

Available Commands:

moderation [file path]  Check if a training file doesn't violate moderation filters.
upload [file path]      Upload a training file at the specified path. Returns a file ID.
tune [file id]          Queues a job for training / tuning. Returns a job ID.
status [job id]         Fetches the status of a tuning job. Returns a model ID if training completed.
help                    Print this help message
```

#### Checking Training Does Not Violate Moderation Filters
Request example
```bash
./training.py moderation "data/default-08-22-2024.jsonl"
```

Response example
```bash
ModerationCreateResponse(id='modr-9d6a9a4050ce03fcabc5459faa9ed4ac', model='omni-moderation-latest', results=[Moderation(categories=Categories(harassment=False, harassment_threatening=False, hate=False, hate_threatening=False, self_harm=False, self_harm_instructions=False, self_harm_intent=False, sexual=False, sexual_minors=False, violence=False, violence_graphic=False, harassment/threatening=False, hate/threatening=False, illicit=False, illicit/violent=False, self-harm/intent=False, self-harm/instructions=False, self-harm=False, sexual/minors=False, violence/graphic=False), category_scores=CategoryScores(harassment=0.01970237400537813, harassment_threatening=0.0008097716541842735, hate=0.00015011822567369918, hate_threatening=6.814872211615988e-06, self_harm=0.0005011211542112085, self_harm_instructions=0.00022690684744977127, self_harm_intent=0.000249784072058715, sexual=0.3738115514626793, sexual_minors=0.001098694263059318, violence=0.0006001064513491806, violence_graphic=8.092757566536092e-06, harassment/threatening=0.0008097716541842735, hate/threatening=6.814872211615988e-06, illicit=0.0038130026525290957, illicit/violent=1.7130819343483194e-05, self-harm/intent=0.000249784072058715, self-harm/instructions=0.00022690684744977127, self-harm=0.0005011211542112085, sexual/minors=0.001098694263059318, violence/graphic=8.092757566536092e-06), flagged=False, category_applied_input_types={'harassment': ['text'], 'harassment/threatening': ['text'], 'sexual': ['text'], 'hate': ['text'], 'hate/threatening': ['text'], 'illicit': ['text'], 'illicit/violent': ['text'], 'self-harm/intent': ['text'], 'self-harm/instructions': ['text'], 'self-harm': ['text'], 'sexual/minors': ['text'], 'violence': ['text'], 'violence/graphic': ['text']})])
```

#### Uploading Training Data

Request example
```bash
./training.py upload "data/default-08-22-2024.jsonl"
```

Response example
```bash
FileObject(
    id='file-nzrtkKyIv3lDfBR78bqODYKn', # Upload ID
    bytes=8303, 
    created_at=1724346770, 
    filename='default-08-22-2024.jsonl', 
    object='file', 
    purpose='fine-tune', 
    status='processed', 
    status_details=None
)
```

#### Creating Training Jobs

Request example
```bash
./training.py tune "file-nzrtkKyIv3lDfBR78bqODYKn"
```

Response example
```bash
FineTuningJob(
    id='ftjob-uwTC0Z5FZb42OKAPheCbHF2k', # Job ID
    created_at=1724347360, 
    error=Error(code=None, message=None, param=None), 
    fine_tuned_model=None, 
    finished_at=None, 
    hyperparameters=Hyperparameters(
        n_epochs='auto', 
        batch_size='auto', 
        learning_rate_multiplier='auto'
    ), 
    model='gpt-4o-mini-2024-07-18', 
    object='fine_tuning.job', 
    organization_id='org-0hI4vtfrSaFsHmuE2k55ImHb', 
    result_files=[], 
    seed=406982310, 
    status='validating_files', 
    trained_tokens=None, 
    training_file='file-nzrtkKyIv3lDfBR78bqODYKn', 
    validation_file=None, 
    estimated_finish=None, 
    integrations=[], 
    user_provided_suffix=None
)
```

#### Fetching Results of Training Jobs

Request example
```bash
./training.py status "ftjob-uwTC0Z5FZb42OKAPheCbHF2k"
```

Response example
```bash
FineTuningJob(
    id='ftjob-uwTC0Z5FZb42OKAPheCbHF2k',
    created_at=1724347360, 
    error=Error(code=None, message=None, param=None),
    fine_tuned_model='ft:gpt-4o-mini-2024-07-18:personal::9z5uyT9b', # Output model ID (training result)
    finished_at=1724347783, 
    hyperparameters=Hyperparameters(
        n_epochs=4, 
        batch_size=1, 
        learning_rate_multiplier=1.8
    ), 
    model='gpt-4o-mini-2024-07-18', # Input model ID (untrained model)
    object='fine_tuning.job', 
    organization_id='org-0hI4vtfrSaFsHmuE2k55ImHb', 
    result_files=['file-ScJQ4jFxtamu2EJ2COAMIjtP'], 
    seed=406982310, 
    status='succeeded', # If not 'succeeded' model can't be used
    trained_tokens=6104, # Cost for training the model
    training_file='file-nzrtkKyIv3lDfBR78bqODYKn', 
    validation_file=None, 
    estimated_finish=None, 
    integrations=[], 
    user_provided_suffix=None
)
```

## Testing an LLM You've Trained

1. Update the value of `OPENAI_MODEL` in `.env` with the model ID fetched from `./training.py status [job id]` after your custom tuning job has completed
2. Execute `chat.py` to initiate a test conversation with your custom tuned LLM

#### Start a Test Conversation

```
./chat.py
# Or use `python chat.py`
```
