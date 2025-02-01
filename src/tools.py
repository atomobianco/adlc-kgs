from crewai_tools import tool
from ontologist import validate
from utils import list_files, parse_graph


@tool("Validate graph with ontology")
def validate_graph_with_ontology(graph: str, ontology: str) -> str:
    """
    Takes a graph and an ontology as string contents.
    Then it parses them into graphs, and reports eventual errors in the graph for non respecting the ontology.

    :param graph: The graph to validate. Without delimiters, just the content.
    :param ontology: The ontology to validate against. Without delimiters, just the content.
    """
    _, _, report = validate(data_graph=parse_graph(graph), ont_graph=parse_graph(ontology))
    return report


@tool("Save graph to file")
def save_graph_to_file(graph: str, file_path: str):
    """
    Takes a graph and a file name and saves the content of the graph into the file.

    :param graph: The graph to save. Without delimiters, just the content.
    :param file_path: The path of file.
    """
    with open(file_path, "w") as file:
        file.write(__clean_graph_content(graph))


def __clean_graph_content(graph: str):
    return graph.replace("<graph>", "").replace("</graph>", "").strip()


@tool("List files in directory")
def list_files_in_directory(directory_path: str) -> list:
    """
    Lists all files in a given directory.

    :param directory_path: Path to the directory
    :return: List of filenames in the directory
    """
    return list_files(directory_path)
