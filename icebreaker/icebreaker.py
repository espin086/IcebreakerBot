"""
This file contains the code for the icebreaker. It is the main file that runs the agent. 
"""

# Standard library imports
import logging
import os

# Third-party imports
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Local application imports
from icebreaker.agents import lookup
from icebreaker.linkedin import get_linkedin_data

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables from .env file
SECRET_KEY = os.getenv("OPENAI_API_KEY")


def icebreaker(name: str):
    """
    This function is the main function that runs the icebreaker. 
    It takes a name as input and returns a summary of the LinkedIn information for the person.
    """
    logging.info("Starting icebreaker for name: %s", name)

    # TOOL: Get the LinkedIn ID of person by doing a LinkedIn search with an AI agent
    try:
        _, linkedin_id = lookup(name)
        logging.info("LinkedIn ID for %s: %s", name, linkedin_id)
    except LookupError as _:
        logging.error(
            "Error occurred during LinkedIn ID lookup for %s", name
        )
        return None

    # Use a LinkedIn function to get the LinkedIn with the ID.
    try:
        linked_info = get_linkedin_data(name=f"{linkedin_id}")
        if "message" in linked_info:
            raise LookupError(linked_info["message"])
        logging.info("LinkedIn information for %s: %s", name, linked_info)

    except LookupError as e:
        logging.error(
            "Error occurred while fetching LinkedIn data for %s: %s", name, e, exc_info=True
        )
        return None

    # Defining the prompt for the LLM to use to create a summary of the LinkedIn information
    prompt_template = PromptTemplate(
        input_variables=["information"],
        template="""
        Given the LinkedIn information {information} about a person, I want you to

        1. a short summary about the person
        2. two interesting facts about them
        3. an cold email template for the person introducing yourself and asking for a call

        If you don't have enough information, you can ask for more information. 
        Just return 'I could not find enough information to create a summary'
        """,
    )
    logging.info("Prompt template defined")

    # Creating the LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=SECRET_KEY)
    logging.info("LLM initialized")

    # llm = ChatOllama(model="llama3", temperature=0)

    chain = prompt_template | llm | StrOutputParser()
    logging.info("Chain created")

    try:
        res = chain.invoke(input={"information": linked_info})
        logging.info("Generated summary for %s: %s", name, res)
    except LookupError as e:
        logging.error(
            "Error occurred during chain invocation for %s: %s", name, e, exc_info=True
        )
        return None

    return res


if __name__ == "__main__":
    result = icebreaker(name="Fidel Vargas")
    if result:
        print(result)
    else:
        print("An error occurred during the icebreaker process.")
