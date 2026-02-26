"""
🌐 Web Tools Module
=================
Tools for web search, scraping, and online information gathering.
"""

import os
import requests
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

try:
    from serpapi import GoogleSearch
    SERPAPI_AVAILABLE = True
except ImportError:
    SERPAPI_AVAILABLE = False

try:
    from duckduckgo_search import DDGS
    DUCKDUCKGO_AVAILABLE = True
except ImportError:
    try:
        from ddgs import DDGS
        DUCKDUCKGO_AVAILABLE = True  
    except ImportError:
        DUCKDUCKGO_AVAILABLE = False

try:
    import arxiv
    ARXIV_AVAILABLE = True
except ImportError:
    ARXIV_AVAILABLE = False

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)

class WebSearchTool:
    """
    🔍 Web Search Tool
    Searches the internet using DuckDuckGo (free, no API key required)
    """
    
    def __init__(self):
        self.serpapi_key = os.getenv("SERPAPI_API_KEY", "")
        self.use_serpapi = SERPAPI_AVAILABLE and bool(self.serpapi_key)
        self.use_duckduckgo = DUCKDUCKGO_AVAILABLE
        
    def search_web(self, query: str, num_results: int = 5) -> str:
        """
        Search the web for information using DuckDuckGo (primary) with SerpAPI fallback
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            Formatted search results string
        """
        # Try DuckDuckGo first (free, no API key required)
        if self.use_duckduckgo:
            try:
                result = self._search_duckduckgo(query, num_results)
                # Check if DuckDuckGo returned an error or no results
                if "error" not in result.lower() and "no results found" not in result.lower():
                    return result
                else:
                    logger.warning(f"DuckDuckGo search failed: {result}")
            except Exception as e:
                logger.warning(f"DuckDuckGo search failed with exception: {str(e)}")
        
        # Fallback to SerpAPI if DuckDuckGo failed and SerpAPI is available
        if self.use_serpapi:
            try:
                logger.info("Falling back to SerpAPI search")
                return self._search_serpapi(query, num_results)
            except Exception as e:
                logger.warning(f"SerpAPI search also failed: {str(e)}")
        
        # Final fallback to basic web scraping
        try:
            logger.info("Using basic web scraping as final fallback")
            return self._search_basic(query, num_results)
        except Exception as e:
            logger.error(f"All search methods failed: {str(e)}")
            return f"Search error: All search methods failed. DuckDuckGo: rate limited, SerpAPI: {('not available' if not self.use_serpapi else 'failed')}, Basic search: {str(e)}"
    
    def _search_duckduckgo(self, query: str, num_results: int) -> str:
        """Search using DuckDuckGo (free, no API key required)"""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=num_results))
            
            if not results:
                return f"No results found for: {query}"
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                body = result.get('body', 'No description')
                url = result.get('href', '')
                
                formatted_results.append(f"""
**🔍 Result {i}: {title}**
{body}
🌐 Source: {url}
""")
            
            header = f"🦆 DuckDuckGo Search Results for '{query}':\n"
            return header + "\n".join(formatted_results)
            
        except Exception as e:
            error_msg = str(e).lower()
            if "ratelimit" in error_msg or "rate limit" in error_msg or "429" in error_msg:
                logger.warning(f"DuckDuckGo rate limited for query: {query}")
                return f"DuckDuckGo search error: Rate limited - trying fallback method"
            else:
                logger.error(f"DuckDuckGo search error: {str(e)}")
                return f"DuckDuckGo search error: {str(e)} - trying fallback method"
    
    def _search_serpapi(self, query: str, num_results: int) -> str:
        """Search using SerpAPI (more reliable but requires API key)"""
        try:
            search = GoogleSearch({
                "q": query,
                "location": "United States",
                "hl": "en",
                "gl": "us",
                "google_domain": "google.com",
                "num": str(num_results),
                "api_key": self.serpapi_key
            })
            
            results = search.get_dict()
            organic_results = results.get("organic_results", [])
            
            if not organic_results:
                return f"No results found for: {query}"
            
            formatted_results = []
            for i, result in enumerate(organic_results[:num_results], 1):
                title = result.get('title', 'No title')
                snippet = result.get('snippet', 'No description')
                link = result.get('link', '')
                
                formatted_results.append(f"""
**🔍 Result {i}: {title}**
{snippet}
🔗 Source: {link}
""")
            
            return f"🐍 SerpAPI Search Results for '{query}':\n" + "\n".join(formatted_results)
            
        except Exception as e:
            return f"SerpAPI search error: {str(e)}"
    
    def _search_basic(self, query: str, num_results: int) -> str:
        """Basic search using web scraping (fallback method)"""
        try:
            # Simulate search using a basic approach
            # In a real implementation, you might use DuckDuckGo API or similar
            search_url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # This is a simplified example - actual implementation would be more complex
            results = soup.find_all('div', class_='result', limit=num_results)
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                title_elem = result.find('a', class_='result__a')
                title = title_elem.text if title_elem else "No title"
                
                snippet_elem = result.find('div', class_='result__snippet')
                snippet = snippet_elem.text if snippet_elem else "No description"
                
                formatted_results.append(f"""
**Result {i}: {title}**
{snippet}
""")
            
            if not formatted_results:
                return f"No search results found for: {query} (using basic search)"
            
            return f"🔍 Search results for '{query}':\n" + "\n".join(formatted_results)
            
        except Exception as e:
            return f"Basic search error: {str(e)}"

class WebScrapingTool:
    """
    🌐 Web Scraping Tool
    Extracts content from web pages.
    """
    
    def scrape_webpage(self, url: str) -> str:
        """
        Scrape content from a webpage
        
        Args:
            url: URL to scrape
            
        Returns:
            Extracted text content
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            # Extract text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit text length
            if len(text) > 2000:
                text = text[:2000] + "..."
            
            return f"📰 Content from {url}:\n\n{text}"
            
        except requests.exceptions.RequestException as e:
            return f"Error accessing webpage: {str(e)}"
        except Exception as e:
            return f"Error scraping webpage: {str(e)}"

class NewsSearchTool:
    """
    📰 News Search Tool
    Searches for recent news articles.
    """
    
    def __init__(self):
        self.web_search = WebSearchTool()
    
    def search_news(self, topic: str, days: int = 7) -> str:
        """
        Search for recent news about a topic
        
        Args:
            topic: News topic to search for
            days: Number of recent days to search
            
        Returns:
            News search results
        """
        try:
            # Enhance query with news-specific terms and date filtering
            news_query = f"{topic} news recent {days} days"
            
            results = self.web_search.search_web(news_query, num_results=5)
            
            # Add news-specific formatting
            formatted_results = f"📰 Recent news about '{topic}' (last {days} days):\n\n{results}"
            
            return formatted_results
            
        except Exception as e:
            return f"News search error: {str(e)}"

class AcademicSearchTool:
    """
    🎓 Academic Search Tool
    Searches academic papers and research.
    """
    
    def search_papers(self, query: str, max_results: int = 5) -> str:
        """
        Search academic papers on arXiv
        
        Args:
            query: Research topic to search
            max_results: Maximum number of papers to return
            
        Returns:
            Academic paper search results
        """
        if not ARXIV_AVAILABLE:
            return "Academic search not available. Please install arxiv package: pip install arxiv"
        
        try:
            # Search arXiv
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = []
            for paper in search.results():
                papers.append({
                    'title': paper.title,
                    'authors': [str(author) for author in paper.authors],
                    'summary': paper.summary[:400] + "..." if len(paper.summary) > 400 else paper.summary,
                    'url': paper.entry_id,
                    'published': paper.published.strftime('%Y-%m-%d')
                })
            
            if not papers:
                return f"No academic papers found for: {query}"
            
            formatted_results = []
            for i, paper in enumerate(papers, 1):
                formatted_results.append(f"""
**Paper {i}: {paper['title']}**
👥 Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}
📅 Published: {paper['published']}
📝 Summary: {paper['summary']}
🔗 Link: {paper['url']}
""")
            
            return f"🎓 Academic papers for '{query}':\n" + "\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"Academic search error: {str(e)}")
            return f"Academic search error: {str(e)}"
    
    def get_paper_details(self, arxiv_id: str) -> str:
        """
        Get detailed information about a specific paper
        
        Args:
            arxiv_id: arXiv ID of the paper
            
        Returns:
            Detailed paper information
        """
        if not ARXIV_AVAILABLE:
            return "Academic search not available. Please install arxiv package."
        
        try:
            paper = next(arxiv.Search(id_list=[arxiv_id]).results())
            
            details = f"""
📄 **Paper Details**

**Title:** {paper.title}

**Authors:** {', '.join([str(author) for author in paper.authors])}

**Published:** {paper.published.strftime('%Y-%m-%d')}

**Abstract:**
{paper.summary}

**Categories:** {', '.join(paper.categories)}

**Link:** {paper.entry_id}

**PDF:** {paper.pdf_url}
"""
            
            return details
            
        except Exception as e:
            return f"Error getting paper details: {str(e)}"

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Web Tools...")
    
    # Test Web Search
    web_search = WebSearchTool()
    print("\n1. Testing Web Search:")
    result = web_search.search_web("artificial intelligence trends 2024", 3)
    print(result)
    
    # Test Web Scraping
    web_scraper = WebScrapingTool()
    print("\n2. Testing Web Scraping:")
    # Use a simple, reliable website for testing
    scrape_result = web_scraper.scrape_webpage("https://httpbin.org/html")
    print(scrape_result[:500] + "..." if len(scrape_result) > 500 else scrape_result)
    
    # Test News Search
    news_search = NewsSearchTool()
    print("\n3. Testing News Search:")
    news_result = news_search.search_news("artificial intelligence", 7)
    print(news_result)
    
    # Test Academic Search
    academic_search = AcademicSearchTool()
    print("\n4. Testing Academic Search:")
    academic_result = academic_search.search_papers("machine learning", 3)
    print(academic_result)