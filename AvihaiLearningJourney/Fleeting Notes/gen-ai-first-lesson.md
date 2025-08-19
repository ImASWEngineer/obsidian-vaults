[[DB+Liron Ratzabi+generative-ai-course]]
## open source models vs offline models
private information on prem - vs public open model

## public open models
- using public rest api
- having models which have ongoing updates

## on prem models
- for private close data flow

## LLM developer
- just using public open model and create product on top of it
- SLM - small language model for low effort functions

# LLM flavors
- predicting next word - language models
- instruction tuned - getting tasks or instructions and perform them
- Dialog Tuned - have context with instructions

# Hugging face
- open source community for having open source llms which can be used offline
- get the image to text best llm for the task and use it offline with docker
- (Gemma SLM)
- LM Studio for holding the language models and talk with them
- use VsCode extension to talk with the SLMs
- LM Studio > playground - talk and test the models which were downloads
- LM Studio > Local server - create endpoint locally for interfacing with the SLM

# GPT4all
- create models and develop for on prem usage
- looks like hugging face with additional specific SLM

# meta llama - llama.com
- best on prems models - like hugging face

# ollama
- ollama.com
- tool for developers to talk with models via CLI
- ollama - download installer to the computer and run "ollama pull [model]" (e.g. "ollama pull gemma3")
- ollama run gemma3
- "ollama list" - models which are downloaded

# genai limitations
- not real time model with the latest information from the world
- frauds
- very biased toward specific opinion

# transformers arch
- encoder decoder arch
- each word and according to weights statistically find the next word
- encoder - get input - set insights (math weight)
- all above insights goes to decoders
	- methematically find for each word the reevant word  - 
	- starts building reponse
	- gets for each word the previous information with the decoders last output
	- recieves the repsonse
- last arch are decoders only (with huge amount of weights)

# open ai
- gpt models
	- 4.1 latest gpt model
- oX models
	- reasoning models
	- smaller tasks with reasoning and context
- embedding modesl
- multi modal models

## openai playground
platform.openai.com
### LLM parameters
- text format [text, ]
- temperature - 0 (deterministic) -> 2 (creative) - suggestion until 1 
	- how much the model is consistent and deterministic vs creative 
- max tokens 
	- how much request and response i should waste to single prompt
		- !!!we shuold try and use some system which compress the token usage of the request!!!!
		- we should summarize the history for the code session before we ask new prompt when we have irrelevant context in the chat history
		- there are cached tokens (not all models) which takes repeated context and not reprice it in its tokens 
- top p
	- 
- store logs [ ]
### Context engineering for pre-prompt
- system message context
	- give cached context to the llm which describe the general enviornment he should consider in your prompts
- user , session context
	- to create a history of a previous session which the llm should conside in his context to be used when asking new prompts
	- user - prompt from user
	- assisten - response from LLM

# prompt engineering 
## Patterns
- flip pattern - how to talk with the llm in order to recieve some specific prompt
- writing prompt with causing the llm to think more
## prompt strategies
### shot learning
- zero shot - use only the llm knowledge
- one shot - give single example then prompt
- few shot - give few examples with more context and the whys!!! and then prompt
### principles
- delimiters between data and the instructions
- tell which format the result should be (json with specific structure)
- check whether conditions and assumptions are satisfied
- 
## Description
- one shot to recieve information from the question
- compressing the prompts in order to have less tokens price
- multi model prompting for comparing answer+model
- prompt injections - injecting code to extract answers which are not returned
	- SECURITY-BEST-PRACTICES!!!!
	- LM Security
		- e.g. add permissions for the model requests repsones per user role
- public Knowledge base which i cannot extract all data from outside
- Azure are the only cloud which hosts the open ai models and ecosystem (comitment to azure)
### using the platform.openai.com vs azure
- domain and api key vs using the azure security and cloud services
- not application ecosystem vs full integrated ecosystem for system arch
	- not scalable vs scalable
	- not secured vs secured
	- billing criteria
	- rest api with public key vs full secured ecosystem
	- cost management (many different costs vs azure single cost and discount for other services)
## Azure ai foundery
- secured cloud
- many models to use via azure services
- Deployment type
	- use cases configuration for different types of deploymnets
- create new instance for model and its different deployment configurations
	- create endpoint for the specific instance
- creates a full python program which includes the full instance config to be used in a local host to communicate with the azure services and use inside local agent

## prompting functionality
- more info less illusions more information bigger results
- add reference to the source information which the llm should back his information on hes reply

# python code
## google colab
### jupiter notebook

- prompt playground openai API librearies
- pip install openai
- 1-guidelines.ipynb
- we can ask prompts which returns information inside ``` in json format and then we can parse info into our runtime
- check assumption - > like asking to create multi steps and then check that the result can not be splitted the tell me i cannot split this
- guided task to give the llm in order to guide the llm to our final solution
	- decompose the request to steps
	- prompting is less then different steps in single prompt (cost and performance wise)
- use the following fomat to the results (headert to each output in the results)
- to check result
- make the llm to solve the probelm on its own
	- compare the result to the prompt result
# writing iterative prompt
- iteratively improve the prompt according to the results which the llm returns
- like 
	- getting chair fact sheet chair to html
		- 1st - full information *too long*
		- 2nd - not informative *need guidance to the results*
		- 3rd - specific information should be added (id)
		- 4th - missing table for dimensions 
		- 5th - wrap each area into html tags and good output
	message 
	- user prompt + system prompt
	- tiktoken
		- library for encoders which calculates the amount of tokens for some prompt and designated llm to use
	- 