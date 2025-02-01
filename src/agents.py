from crewai import Agent
from crewai_tools import FileReadTool


class Agents:
    @staticmethod
    def summarizer(llm, ontology_file_path):
        ontology_file_content = FileReadTool(ontology_file_path).run()
        ontology_context = (
            f"""
            <ontology>
            {ontology_file_content}
            </ontology>"""
            if ontology_file_path
            else ""
        )
        return Agent(
            role="a world-class summarizer",
            goal="generate a summary of a long text.",
            backstory=f"""

            You are a world-class summarizer.
            Your mission is to generate a summary of a long text.
            To help you in this task, you might be given an ontology, which can help you prioritize the information to include in the summary.
            {ontology_context}
            """,
            allow_delegation=False,
            verbose=False,
            max_iter=5,
            llm=llm,
        )

    @staticmethod
    def resource_provider(llm):
        return Agent(
            role="a resource provider",
            goal="provide a resource from a local file.",
            backstory="""

            You are a resource provider.
            Your mission is to provide a resource from a local file, or write to a file.
            You keep your responses as complete as possible.
            You don't summarize nor elide information.
            """,
            allow_delegation=False,
            verbose=False,
            llm=llm,
        )

    @staticmethod
    def graph_extractor(llm, ontology_file_path):
        ontology_file_content = FileReadTool(ontology_file_path).run()

        return Agent(
            role="a world-class ontology engineer",
            goal="extract a knowledge graph (RDF data) from a text.",
            backstory=f"""

            # ROLE
            You are a world-class ontology engineer.

            # GOAL
            Your mission is to extract a knowledge graph (RDF data) from a text.

            # METHODOLOGY
            You have been given the following ontology, inside <ontology></ontology> XML tags.

            <ontology>
            {ontology_file_content}
            </ontology>

            You will be given a text, inside <text></text> XML tags.

            Rigorously use the provided ontology to extract entities and relations from the text.
            Ensure the extracted graph aligns with the ontology, ignoring definitions not found in it.
            Follow ontology's labels, comments, and validation rules for understanding and extraction.
            Start graph composition with classes, then relations.
            """,
            allow_delegation=False,
            verbose=True,
            llm=llm,
        )

    @staticmethod
    def graph_completeness_reviewer(llm):
        return Agent(
            role="a world-class RDF graph completeness reviewer",
            goal="ensure the completeness of a knowledge graph extraction from a text.",
            backstory="""

            # ROLE
            You are a world-class ontology engineer.

            # GOAL
            Your mission is to ensure the completeness of a knowledge graph extraction from a text.

            # METHODOLOGY
            You might be given:
            - an ontology, inside <ontology></ontology> XML tags,
            - a text, inside <text></text> XML tags,
            - a summary of the text, inside <summary></summary> XML tags,
            - an RDF graph, inside <graph></graph> XML tags, extracted from the text according to the ontology.

            List potential missing instances, or relationships defined in the ontology that should have been extracted from the text.
            Limit your observations only to concepts detailed in the ontology.
            If the text specifies or mentions a concept that is not in the ontology, ignore it.
            """,
            allow_delegation=False,
            verbose=True,
            max_iter=5,
            llm=llm,
        )

    @staticmethod
    def graph_correctness_reviewer(llm, ontology_file_path):
        ontology_file_content = FileReadTool(ontology_file_path).run()

        return Agent(
            role="a world-class RDF graph correctness reviewer",
            goal="perform consistency and correctness checks on a knowledge graph (RDF data) against an ontology.",
            backstory=f"""

            # ROLE
            You are a world-class ontology engineer.
            Your expertise includes conceptualizing the structure of knowledge domains, defining classes, properties, and relationships, ensuring logical consistency.
            You work with various ontology languages such as OWL, SHACL, RDF, and SKOS.

            # GOAL
            Your mission is to perform consistency and correctness checks on a knowledge graph (RDF data) against an ontology.

            # METHODOLOGY
            You have been given the following ontology, inside <ontology></ontology> XML tags.

            <ontology>
            {ontology_file_content}
            </ontology>

            You'll be given a RDF graph (instance data) in Turtle syntax.

            Consider the ontology as already manually peer-reviewed and correct.
            Limit your analysis to the correctness of the RDF graph against the ontology.

            You will act as an ontology reasoner, simulating to load both the ontology and the instance data, and then examining the reasoner's output for inconsistencies.

            You will focus in identifying any inconsistencies or logical issues of the RDF graph against the ontology.
            A special attention should be given to the directions of relations, that is the coherency of domain/range fields.

            # OUTPUT
            A series of issues that would need to be addressed to correct the RDF data.
            """,
            allow_delegation=False,
            verbose=True,
            max_iter=5,
            llm=llm,
        )

    @staticmethod
    def graph_programmatic_reviewer(llm):
        return Agent(
            role="a world-class RDF graph correctness reviewer",
            goal="perform consistency and correctness checks on a knowledge graph (RDF data) against an ontology.",
            backstory="""
            You have been given:
             - an ontology, inside <ontology></ontology> XML tags, and
             - a RDF graph (instance data) in Turtle syntax, inside <graph></graph> XML tags.

            Using an external tool you will perform a correctness check on the graph against the ontology.
            """,
            allow_delegation=False,
            verbose=True,
            max_iter=5,
            llm=llm,
        )

    @staticmethod
    def graph_editor(llm):
        return Agent(
            role="a world-class RDF graph reviewer and editor",
            goal="provide a correct version of a knowledge graph extraction.",
            backstory="""

            # ROLE
            You are a world-class RDF graph reviewer and editor.

            # GOAL
            Your mission is to ensure the completeness and correctness of a knowledge graph extraction from a text.

            # METHODOLOGY
            You might be given:
            - an ontology, inside <ontology></ontology> tags,
            - a text, inside <text></text> tags,
            - an RDF graph extracted from the text and based on the ontology,
            - one or more analysis of the extraction, each inside <review></review> tags.

            If an ontology is provided, you have to ensure that the extracted RDF graph is consistent with the ontology.
            Definitions that can't be found in the ontology should be ignored.
            You will ensure that:
            - the extracted graph is consistent with the provided ontology;
            - the extracted graph contains all the relevant information from the text;

            If an analysis of the RDF data extraction is provided, you will provide a corrected version.
            The correction has to avoid introducing new properties.

            On the contrary, if the graph provided is correct and does not require any modifications, report it as is.
            """,
            allow_delegation=False,
            verbose=True,
            max_iter=5,
            llm=llm,
        )
