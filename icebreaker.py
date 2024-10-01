import os
import logging
from dotenv import load_dotenv
load_dotenv()

# Loading AI modules
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

# Custom code
from agents import lookup
from linkedin import get_linkedin_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
SECRET_KEY = os.getenv('OPENAI_API_KEY')

def icebreaker(name: str):
    logging.info(f"Starting icebreaker for name: {name}")

    # TOOL: Get the LinkedIn ID of person by doing a LinkedIn search with an AI agent
    try:
        _, id = lookup(name)
        logging.info(f"LinkedIn ID for {name}: {id}")
    except Exception as e:
        logging.error(f"Error occurred during LinkedIn ID lookup for {name}", exc_info=True)
        return None

    # Use a LinkedIn function to get the LinkedIn information by LinkedIn ID found by the lookup function and fed into the LinkedIn function
    try:
        linked_info = get_linkedin_data(name=f"{id}")
        if 'message' in linked_info:
            raise Exception(linked_info['message'])
        logging.info(f"LinkedIn information for {name}: {linked_info}")

    except Exception as e:
        logging.error(f"Error occurred while fetching LinkedIn data for {name}", exc_info=True)
        return None

    # Defining the prompt for the LLM to use to create a summary of the LinkedIn information
    prompt_template = PromptTemplate(
        input_variables=["information"], 
        template="""
        Given the LinkedIn information {information} about a person, I want you to
        create: 

        1. a short summary about the person
        2. two interesting facts about them

        If you don't have enough information, you can ask for more information. 
        Just return 'I could not find enough information to create a summary'
        """
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
        logging.info(f"Generated summary for {name}: {res}")
    except Exception as e:
        logging.error(f"Error occurred during chain invocation for {name}", exc_info=True)
        return None

    return res

if __name__ == "__main__":
    result = icebreaker(name="Fidel Vargas")
    if result:
        print(result)
    else:
        print("An error occurred during the icebreaker process.")