import logging
from langchain_community.tools.tavily_search import TavilySearchResults

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_profile_url_tavily(search_query: str):
    logging.info(f"Starting search for query: {search_query}")
    
    search = TavilySearchResults()
    
    try:
        res = search.run(search_query)
        logging.info(f"Search completed successfully for query: {search_query}")
        logging.debug(f"Search results: {res}")
        if res is None:
            raise Exception("Search results returned None")
    except Exception as e:
        logging.error(f"Error occurred during search for query: {search_query}", exc_info=True)
        res = None
    except Exception as e:
        logging.error(f"Error occurred during search for query: {search_query}", exc_info=True)
        res = None
    
    return res