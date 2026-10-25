"""
Vector search over incidents.

    uv add chromadb
"""
import csv
from pprint import pprint

import chromadb


db = chromadb.PersistentClient(path="incident_db")
collection = db.get_or_create_collection("incidents")


def load_examples(filename: str = "incidents.csv") -> None:
    with open(filename) as f:
        for i, row in enumerate(csv.DictReader(f), start=1):
            collection.upsert(
                ids=[str(i)],
                documents=[f"{row['title']}: {row['description']}"],
                metadatas=[{"location": row["location"]}],
            )
    print(f"{i} incidents loaded")


def search_similar_incidents(text: str, n: int = 3) -> list[dict]:
    """Finds earlier incidents that are similar in meaning to the given text.

    Args:
        text: a description of the current problem
        n: number of results
    """
    result = collection.query(query_texts=[text], n_results=n)
    return [
        {"id": id_, "incident": doc, "location": meta["location"], "distance": round(dist, 3)}
        for id_, doc, meta, dist in zip(
            result["ids"][0],
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
        )
    ]


if __name__ == "__main__":
    load_examples()
    text = input("enter an incident: ")
    pprint(search_similar_incidents(text))
