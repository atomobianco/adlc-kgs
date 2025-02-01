import os

import rdflib
from rdflib import Graph


def list_files(directory_path: str) -> list:
    try:
        files = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                files.append(filename)
        return sorted(files)
    except (FileNotFoundError, PermissionError, OSError):
        return []


def parse_graph(text: str) -> Graph:
    graph = rdflib.Graph()
    graph.parse(data=text, format="text/turtle")
    return graph
