import os
import logging
from dotenv import load_dotenv
load_dotenv()

# Loading a tool
from tools import get_profile_url_tavily

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Start of module
def lookup(name: str) -> tuple:
    logging.info(f"Starting lookup for name: {name}")

    # Defining the LLM for the agent to use
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=os.getenv('OPENAI_API_KEY')
    )
    logging.info("LLM initialized")

    # llm = ChatOllama(model="llama3", temperature=0)

    # Defining the tools for the agent to use
    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the linkedin profile page of a person"
        )
    ]
    logging.info("Tools for agent defined")

    # Creating the agent
    react_prompt = hub.pull("hwchase17/react")
    logging.info("React prompt pulled from hub")

    # Creating a react agent
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )
    logging.info("React agent created")

    # Creating the agent executor: this contains the type of agent it is and the tools it can use
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    logging.info("Agent executor created")

    # Defining the prompt (instructions) for the agent so it can run and use its tools
    prompt_template = PromptTemplate(
        input_variables=["name_of_person"],
        template="""
        given the name {name_of_person} I want you to get me a link to their linkedin profile page. 
        Your answer should contain only a URL.
    """)
    logging.info("Prompt template defined")

    # Running the agent which will use the tool to search for the linkedin profile page
    formatted_prompt = prompt_template.format_prompt(name_of_person=name)
    logging.info(f"Formatted prompt: {formatted_prompt}")

    try:
        results = agent_executor.invoke(input={"input": formatted_prompt})
        logging.info("Agent executor invoked successfully")
    except Exception as e:
        logging.error("Error occurred during agent execution", exc_info=True)
        return None, None

    # Getting the linkedin profile URL
    linkedin_profile_url = results["output"]
    logging.info(f"LinkedIn profile URL: {linkedin_profile_url}")

    # Extracting the linkedin id from the URL
    linkedin_id = linkedin_profile_url.replace("https://www.linkedin.com/in/", "").replace("/es", "")
    logging.info(f"LinkedIn ID: {linkedin_id}")

    return linkedin_profile_url, linkedin_id

if __name__ == "__main__":
    url, id = lookup("Julia Cervantes-Espinoza")
    print(url)
    print(id)