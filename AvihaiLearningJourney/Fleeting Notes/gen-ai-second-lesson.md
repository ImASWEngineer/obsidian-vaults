[[DB+Liron Ratzabi+generative-ai-course]]
# Langchain
## Chains
- langfuse?!
- langchain.com
- ecosystem w tools for enhancing AI workflow for complex solutions
- agnostic code
- abstract layer agnostic to LLM providers
- running the code over azure etc.
- agents w mcp support - [search] "langchain - azure openai" for all documentation
``` langchain python
pip install openai
pip install langchain
pip install langchain-openai #wrapper for openai

llm=ChatOpenAI(...)

messages = [
("message")
]

print(llm.invoke(messages)) #agnostic wrapper 
```
- same goes for hugging face local llm
``` langchain
from langchain_huggingface
llm = HuggingFaceLLM()
#same as above - agnostic invocation
```
- must use langcahin!!!!!!!
- Prompt templates
- object template to use with langchain
- "PromptTemplate"
- "From langchain.chains import LLMChain"
- "Sequential chain" - to concat 2 chains of messages into one result

## Agents and tools
- supply tools to agents in order to recive external information which is more reliable (as humans using tools)
- load_tools
- llm = openai(temperature=0)
- agent = initialize-agents (tool , model )
- agent.run
- Google Search API - search engine to be used using the llm - formatted to json
- search over colab = local / web api ide
- checkk wikipedia api!!!! - good for the zettlekasten system!!! hop between notes using the api
- 
## Memory
- agnostic model cross LLM Provider
- "lanchain.memory from conversationbuffermomry"
- adding memory to the chain = llmchain(... memory = memory) - use this for the llm memory when processing the notes - you can limit the session length of the model interaction
- you can ask for summary and not the whole conversation
- you can combine - save 1 hr before above it save the information as summary (token usage save)

## Document Loaders
- working with organizationl documents
- !pip install pypdf - python pdf lib - "PyPDFLoacder"
- "tiktoken ?!"
- "create_pandas_dataframe_agent - works with tabular information (tables)"
- agent.run("how many total rows?")

## Incorporating Domain Knowledge
- fine tuning
	- coupling model to knowldege base - coupling
	
### RAG - retrieval augmented generation
- Learn new facts
- Rag Architecture
- fusion of RAG and LLM
- Add model type which embedded the content!!!!
	- float number vector for the embedding
- openai models > embeddings
- data > embedding model > vector
- dimensions per document input
- vector per document creation in the vector db
- clustering and distance functions to retrieve the relevant documents
- retireval by the cluster of the rag relevant to the prompt vector
- SVM process -> look in google -> seems like the RAG workflow similar
- pinecone vectordb - cloud service - scale rag
- faiss - facebook ai vectordb - in process rag
- chromadb - vectordb - opensource - *onprem running !!*
- we can also abstract this RAG layer using langchain
- mongodb - embeddings builting in the db with this ai solution
- postgress etc.
- azure ai search / google vertex ai (ANN, KNN, ScaNN) - scalable vector embedding db oriented
 ```langchain pyhton
!pip install pinecone
!pip install langchain-community
from langchain.text_splitter #recursivecharacterbasedsplitter - for chunking the data
...
loader = pyPDFLocader
data= loader.load()
recursivecharactertextsplitter(chunksize=500)
docs = text_splitter
os.environment['pineconeapikey'] = sdfsdfsd...
#we can set the dimensions of the vector
embeddings=  openAIEmbeddings (model="text-embedding-3-large")
index_name='demo-index-1' #from pinecone - for embedding configs
Pineconevectordtore.fromDocuments(docs,embeddings,index-...)
#run the embeddings for the PDF document
```
- we can use embeddings also for inner pictures
```embeddings python
quert = "how to close the lights"
docs=docsearch.similarity_search(query)
llm_chain.invoke(...);

```
- semantic information is very accurate, numbering or non semantic data is problematic
- chromadb - creating a vectordb locally on prem
- you can give langchain the ability to load document and tell him the langauge of documents
- "Chroma.from_documet(...text, embeddings,..)"
- "Chroma.persist" flush to disk
- -add memory etc.
### langchain indexing api 
- working with live rag system - not only retireval!!!! upsert to db
- incremental all the new code information is updating the index db
- full is full mirror include the delete
- knows how to not insert existing documents into the rag
- searching not rag search by vector but by non semantix search (searchin numbers e.g. 1243)
	- full keyword search
	- *hybrid search*
	- fusion - keyword and vector search (BM25 - keyword search)
	- use this with tags search - good for filtering the search
- trag - finetuned llm for our system domain - if getting the rag to the trag to add the domain knowledge
- graph rag - neo4j - entity relationship
	- graphql
	- prompt "hop inside the graph and extract information related from A for B"\
	- neo4j langchain  api!!!!
	- we can use llm model > extract text > use this with context and embed the whole info with the picture!!!

# Task
- use rss feed which is an xml format , creating fact checker
- ynet - rss feed - rag all the rss feeds
- true or not with link to the fact in the rss
- rss parser -> create for reading the items 
- text item which we use to embedd the vector
- add meta data to the vector (non semantic)
- use rb.gy/ehrncf