
# Vector Search

*"The copier is smoking"* and *"printer on fire"* have no word in common, but mean almost the same thing.
A vector database finds such similarities.

## Embeddings

An **embedding** is a vector that describes the meaning of a text.
A model maps similar texts to vectors that lie close to each other.
The search then simply calculates distances.

### Exercise 1: Look at embeddings

Open the [TensorFlow Embedding Projector](https://projector.tensorflow.org/).
Search for a word and look at its nearest neighbours.

----

## Exercise 2: Find similar incidents

We use **ChromaDB**: a vector database that can be installed as a Python library and comes with an embedding model.

```bash
uv add chromadb
```

On the first call, ChromaDB downloads a small embedding model (approx. 80 MB).

### Step 1: Load data

Run the code in [code/incident_search.py](code/incident_search.py).
It requires a CSV file with incidents: [code/incidents.csv](code/incidents.csv)


Enter a text and look at the documents found and their distances. The smaller the distance, the more similar.

### Step 2: Turn it into an MCP tool

Write a tool `search_similar_incidents(text: str, n: int = 3) -> list[dict]`.

### Step 3: Try it with an LLM

> My laptop can't find any Wi-Fi. Has this happened before?

- Does the LLM find the matching old incident?
- What happens with a search for which there is no match?
