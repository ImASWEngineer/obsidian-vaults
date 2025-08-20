# azure ai search
- data ingestion simplied via embeddings
- 100 vectors and up supported scale of customers
# hybrid search
- vector rag search
- keyword search
- hybrid + semantic ranker
- llm checks the prompt and the result to give rank to the accuracy
- we can have db vector with the following colums - vector , summary, tags, link, rank-> to text - > ranking on the summary
- graph rag with hybrid search and ranker -> ultimate solution!!!!!
- in our dbms zettlekasten -> add prunning and merging api
# vector quantization
- binary quanization - each dimension will be 0 or 1
- scalar quant from float 32 to int 8 -> need research
# data ingestion
- add to pipline ingestion
- add compression policy for vector in the json - quantized_data_type -> key
- build in oversampling 
	- ScalarQuantizationCompressionConfguration( .... below ...)
	- rerank_with_original_vectors = True
	- default_oversampling = 10
- mathemics calculation and vector retireval index is from the compressed info
- the ranking on the raw data
# azure ai-search
- import and vectorize data
	- data source
	- ingestion data pipeline shows all configuration to insert (onelake) of data sources
	- azure Fabric service -> data analysis
# LLM ops
- Building llm apps for production
- criterias model selection
	- speed of response
	- task completion
	- does model solve my problem?
	- cost - per query? task, user, day
- need to adjust output to the best format the llm can act upon and process the best possible way!!!!!!! -> relevant to dbms
- pipeline for production development of LLM - integrating LLM into a software system (SDLC???)
	- take snapshot from phone (Attachment workflow)
- LLMOps Challanges
	- Monitoring the ll, prompting workflow and data flow ->>> laggraph (observabilty) / langsmith !!!! langfuse  - open source langsmith
	- training
	- fine running
	- storage
	- latency
	- LLM app arch (attachment workflow from phone!!!)
	- LLM Ops workflow
		- check the result relevant to prompt
		- iterative fixing of improvement loop
		- monitoring / evaluation -> monitoring of the logs etc. to see issues in the llm integration - drifting
			- data drift -> data changed for the llm -> change in model quality
			- model drift -> llm changed
			- embeddding drift -> if changes the vectors similarity also changes -> consider revectoring or A/B testing!!!
	- Security
		- Top 10 LLM Risks for app security
			- prompt injection
			- insecure output handling
			- trainin data poisnining
			- DDOS attack
			- data leakage -> private data goes out to external prompts
			- insecure plugins
			- too much autonomy
	- LLM guardrails!!!
		- checking input vs output
		- defining the pattern of the system use case and where the llm can do and cannot do
		- feedback loop on the llm result and insert the guardrails also after the llm result!!!! - colang!!!! defines the conversation flow!!!! the model should be very determinstic according to the colang definitions!!!!
	- 
# langfuse (llm ops service free!)
- using docker for observability
- tracing should show you the communication to the web api with all infomration and metadata
- settings > api keys for supplying the langfuse chain of llms

# Caching prompts
- saves tokens

# Task
- we need to analize .net apps with 

# Agentic AI
- genrativa AI vs Agentic ai
	- generative
		- LLM
		- create 
		- analysis 
		- customization
		- transformation of data
	- agentic
		- decision making
		- probloem solving
		- autonomy
		- interactivity
		- planning
		- human in /out of the loop
	- what are ai agents?
		- live in hes own domain
		- single or team player in the system
		- plans
		- orchastrate tasks
		- sync / async - qna with async system of execution
		- human in the loop - tools for observing the llm plans etc.
	- client > infra > models > platform > {customer agent, employee agent , etc.}
# Agent Dev Kit (ADK)
- google dev kit
- multi agent focus
- DEV oriented
- model agnostic and deployemnt agnostic
- tools + actions etc. by design
- by design MCP and A2A support
- in python
# MCP
- model context protocol 
- external tools
- MCP Server < tools with description
# Agent to Agent (A2A)
- communicate between different agents
- creating agent infra
- the agent found in somewhere else in the world
- Agent card on the whole agent capabilities using json formats
- a2a uses async and sync communication (push events or messages services)
- identification, authorization
- agent scope (public ..)
- curated agents (orgazniation agents repo with roles and permissions and policies)
- private agents (card is blocked)
	- auth, jwt
# A2A (LOVE) MCP
- agent written with a2a have its own mcp client
- Agent A
	- local agents
	- llm
	- agent framework
	- mcp
	- API and enterp apps
- A2A to:
- Agent B
	- local agents
	- vertex au 
	- ADK
	- MCP
	- API and enterp apps
- 
- FAST MCP to create mcp servers
- create an a2a agent which runs this mcp library
- AgentSpace - create ultimate organizations RAG
- AutoGen - microsoft python multi agent infra without a2a
	- archastrater -> multi agent types review -> feedback loop -> user output
- lnagchain / crewai / lamaindex