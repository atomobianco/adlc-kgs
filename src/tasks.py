from crewai import Task
from crewai_tools import FileReadTool
from tools import (
    save_graph_to_file,
    validate_graph_with_ontology,
)

with open("./examples/09d04-intro.txt") as f:
    example_1_input = f.read()
with open("./examples/09d04-intro.ttl") as f:
    example_1_output = f.read()
with open("./examples/09d04-dispo.txt") as f:
    example_2_input = f.read()
with open("./examples/09d04-dispo.ttl") as f:
    example_2_output = f.read()
with open("./examples/05d09-dispo.txt") as f:
    example_3_input = f.read()
with open("./examples/05d09-dispo.ttl") as f:
    example_3_output = f.read()

expected_output_turtle = f"""
An RDF graph written in Turtle syntax, inside <graph></graph> XML tags.

# EXAMPLES

## EXAMPLE 1
### INPUT
<text>
{example_1_input}
</text>

### OUTPUT
<graph>
{example_1_output}
</graph>

## EXAMPLE 2
### INPUT
<text>
{example_2_input}
</text>

### OUTPUT
<graph>
{example_2_output}
</graph>

## EXAMPLE 3
### INPUT
<text>
{example_3_input}
</text>

### OUTPUT
<graph>
{example_3_output}
</graph>
"""

expected_output_review = """
Raw text, bullet point list, wrapped by <review></review> tags.

Example Output:
<review>
- The graph...
- The instance...
...
</review>
"""


class Tasks:
    @staticmethod
    def summary_task(agent, context):
        return Task(
            description="Provide a summary of the given text, in the same language of the original.",
            agent=agent,
            context=context,
            expected_output="A summary of the text, inside <summary></summary> XML tags.",
        )

    @staticmethod
    def ontology_provision_task(agent, file_path):
        return Task(
            description="Provide the ontology",
            agent=agent,
            tools=[FileReadTool(file_path)],
            async_execution=True,
            expected_output="The content of the ontology file enclosed in <ontology></ontology> XML tags.",
        )

    @staticmethod
    def text_provision_task(agent, file_path):
        return Task(
            description="Provide the text",
            agent=agent,
            tools=[FileReadTool(file_path)],
            async_execution=True,
            expected_output="The content of the text file enclosed in <text></text> XML tags.",
        )

    @staticmethod
    def graph_extraction_task(agent, context):
        return Task(
            description="Extract RDF",
            agent=agent,
            context=context,
            expected_output=expected_output_turtle,
        )

    @staticmethod
    def graph_review_task(agent, context):
        return Task(
            description="Analyze if extracted RDF data is coherent with a provided ontology.",
            agent=agent,
            context=context,
            expected_output=expected_output_review,
        )

    @staticmethod
    def graph_completeness_review_task(agent, context):
        return Task(
            description="Check for missing instances or relations.",
            agent=agent,
            context=context,
            expected_output=expected_output_review,
        )

    @staticmethod
    def graph_correctness_review_task(agent, context):
        return Task(
            description="Analyze if the extracted RDF graph is coherent with the ontology.",
            agent=agent,
            context=context,
            expected_output=expected_output_review,
        )

    @staticmethod
    def graph_programmatic_review_task(agent, context):
        return Task(
            description="Programmatically validate the extracted RDF graph against the ontology.",
            agent=agent,
            context=context,
            tools=[validate_graph_with_ontology],
            expected_output=expected_output_review,
        )

    @staticmethod
    def graph_edit_task(agent, context):
        return Task(
            description="Provide a corrected version of the RDF graph.",
            agent=agent,
            context=context,
            expected_output=expected_output_turtle,
        )

    @staticmethod
    def graph_save_task(agent, context, file_path):
        return Task(
            description=f"Save the graph to file {file_path}.",
            agent=agent,
            context=context,
            expected_output="Confirmation that data was saved.",
            tools=[save_graph_to_file],
        )
