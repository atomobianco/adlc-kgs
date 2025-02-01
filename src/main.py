import os

from agents import Agents
from crewai import Crew
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from tasks import Tasks

load_dotenv()

default_ontology = "ontology-dispo.ttl"
default_text = "14d05-dispo.txt"
ontology = input(f"Ontology (defaults to {default_ontology}): ") or default_ontology
text = input(f"Text (defaults to {default_text}): ") or default_text

ontology_path = f"./ontologies/{ontology}"
text_path = f"./input/{text}"
output_path = f"./output/{os.path.splitext(text)[0]}.ttl"

gpt4_llm = ChatOpenAI(temperature=0.0, model_name="gpt-4-turbo")
gpt35_llm = ChatOpenAI(temperature=0.0, model_name="gpt-3.5-turbo")
# groq_llm = ChatGroq(temperature=0.0, model_name="llama3-8b-8192")
haiku_llm = ChatAnthropic(temperature=0.0, model="claude-3-haiku-20240307")
sonnet_llm = ChatAnthropic(temperature=0.0, model="claude-3-sonnet-20240229")
opus_llm = ChatAnthropic(temperature=0.0, model="claude-3-opus-20240229")
default_llm = gpt4_llm

agents = Agents()
resource_provider = agents.resource_provider(llm=gpt35_llm)
summarizer = agents.summarizer(llm=default_llm, ontology_file_path=ontology_path)
graph_extractor = agents.graph_extractor(llm=default_llm, ontology_file_path=ontology_path)
graph_correctness_reviewer = agents.graph_correctness_reviewer(llm=default_llm, ontology_file_path=ontology_path)
graph_programmatic_reviewer = agents.graph_programmatic_reviewer(llm=gpt35_llm)
graph_completeness_reviewer = agents.graph_completeness_reviewer(llm=default_llm)
graph_editor = agents.graph_editor(llm=default_llm)

tasks = Tasks()
ontology_provision_task = tasks.ontology_provision_task(resource_provider, ontology_path)
text_provision_task = tasks.text_provision_task(resource_provider, text_path)
summary_task = tasks.summary_task(
    agent=summarizer,
    context=[text_provision_task],
)
graph_extraction_task = tasks.graph_extraction_task(
    agent=graph_extractor,
    context=[text_provision_task],
)
graph_completeness_review_task = tasks.graph_completeness_review_task(
    agent=graph_completeness_reviewer,
    context=[
        ontology_provision_task,
        text_provision_task,
        summary_task,
        graph_extraction_task,
    ],
)
graph_correctness_review_task = tasks.graph_correctness_review_task(
    agent=graph_correctness_reviewer,
    context=[ontology_provision_task, graph_extraction_task],
)
graph_programmatic_review_task = tasks.graph_programmatic_review_task(
    agent=graph_programmatic_reviewer,
    context=[ontology_provision_task, graph_extraction_task],
)
graph_edit_task = tasks.graph_edit_task(
    agent=graph_editor,
    context=[
        ontology_provision_task,
        text_provision_task,
        graph_extraction_task,
        graph_correctness_review_task,
        graph_completeness_review_task,
        graph_programmatic_review_task,
    ],
)
graph_save_task = tasks.graph_save_task(
    agent=resource_provider,
    context=[graph_edit_task],
    file_path=output_path,
)

crew = Crew(
    agents=[
        resource_provider,
        # summarizer,
        graph_extractor,
        graph_completeness_reviewer,
        graph_correctness_reviewer,
        graph_programmatic_reviewer,
        graph_editor,
    ],
    tasks=[
        ontology_provision_task,
        text_provision_task,
        # summary_task,
        graph_extraction_task,
        graph_completeness_review_task,
        graph_correctness_review_task,
        graph_programmatic_review_task,
        graph_edit_task,
        graph_save_task,
    ],
    verbose=2,
    # max_rpm=30,
)

result = crew.kickoff()
print(result)
