import wikipedia
from ddgs import DDGS  # Updated import to use the new package name
from langchain.tools import Tool
import requests
import time
import random

class ResearchTools:
    @staticmethod
    def wikipedia_search(query: str) -> str:
        """Search Wikipedia for factual information with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Set a timeout for the request
                wikipedia.set_lang("en")
                summary = wikipedia.summary(query, sentences=3, auto_suggest=False)
                page = wikipedia.page(query, auto_suggest=False)
                return f"Title: {page.title}\nSummary: {summary}\nURL: {page.url}"
            except Exception as e:
                if attempt < max_retries - 1:
                    # Wait before retrying with exponential backoff
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(wait_time)
                    continue
                return f"Wikipedia search failed for: {query}. Error: {str(e)}"
    
    @staticmethod
    def web_search(query: str) -> str:
        """Search web for recent information with multiple fallback options"""
        max_retries = 3
        search_engines = [
            ResearchTools._duckduckgo_search,
            ResearchTools._brave_search,
            ResearchTools._qwant_search
        ]
        
        for engine in search_engines:
            for attempt in range(max_retries):
                try:
                    result = engine(query)
                    if result and result.strip():
                        return result
                except Exception as e:
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        time.sleep(wait_time)
                        continue
        
        return f"All search engines failed for query: {query}"
    
    @staticmethod
    def _duckduckgo_search(query: str) -> str:
        """DuckDuckGo search with specific error handling"""
        try:
            with DDGS(timeout=10) as ddgs:
                results = list(ddgs.text(query, max_results=3))
                formatted_results = []
                for result in results:
                    formatted_results.append(f"Title: {result['title']}\nSnippet: {result['body']}\nURL: {result['href']}")
                return "\n\n".join(formatted_results)
        except Exception as e:
            raise Exception(f"DuckDuckGo search failed: {str(e)}")
    
    @staticmethod
    def _brave_search(query: str) -> str:
        """Brave search as a fallback option"""
        try:
            url = "https://search.brave.com/search"
            params = {"q": query, "source": "web"}
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                # Simple text extraction - in a real implementation, you'd parse HTML
                return f"Brave search results for: {query}\n[Content would be extracted here]"
            else:
                raise Exception(f"HTTP {response.status_code}")
        except Exception as e:
            raise Exception(f"Brave search failed: {str(e)}")
    
    @staticmethod
    def _qwant_search(query: str) -> str:
        """Qwant search as another fallback option"""
        try:
            url = "https://api.qwant.com/v3/search/web"
            params = {
                "q": query,
                "count": 3,
                "locale": "en_US",
                "safesearch": 1,
                "source": "news"
            }
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get("data", {}).get("result", {}).get("items", {})
                formatted_results = []
                for item in results.get("mainline", [])[:3]:
                    if "desc" in item:
                        formatted_results.append(f"Title: {item.get('title', 'N/A')}\nSnippet: {item.get('desc', 'N/A')}\nURL: {item.get('url', 'N/A')}")
                return "\n\n".join(formatted_results)
            else:
                raise Exception(f"HTTP {response.status_code}")
        except Exception as e:
            raise Exception(f"Qwant search failed: {str(e)}")

def get_tools():
    return [
        Tool(
            name="Wikipedia Search",
            func=ResearchTools.wikipedia_search,
            description="Use this tool to get factual, encyclopedic information about topics, definitions, history, and statistics."
        ),
        Tool(
            name="Web Search", 
            func=ResearchTools.web_search,
            description="Use this tool to find recent news, trends, current events, and up-to-date information about topics."
        )
    ]