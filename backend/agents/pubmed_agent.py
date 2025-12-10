"""
PubMed Literature Retrieval Agent
Fetches scientific papers from PubMed via NCBI E-utilities API
"""
import httpx
from typing import List, Optional
from models.schemas import Paper, QueryIntent
from utils.logger import setup_logger
from utils.config import settings
import xmltodict

logger = setup_logger(__name__)

class PubMedAgent:
    """Agent for fetching literature from PubMed"""
    
    ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    
    def __init__(self):
        self.api_key = settings.ncbi_api_key
        self.email = settings.ncbi_email
    
    async def fetch_papers(self, query_intent: QueryIntent, max_results: int = 20) -> List[Paper]:
        """
        Fetch papers from PubMed
        
        Args:
            query_intent: Structured query
            max_results: Maximum number of papers to retrieve
            
        Returns:
            List of Paper objects
        """
        logger.info("Fetching papers from PubMed")
        
        try:
            # Build search query
            search_query = self._build_search_query(query_intent)
            
            # Search for PMIDs
            pmids = await self._search_pubmed(search_query, max_results)
            
            if not pmids:
                logger.info("No papers found")
                return []
            
            # Fetch paper details
            papers = await self._fetch_paper_details(pmids)
            
            logger.info(f"Fetched {len(papers)} papers from PubMed")
            return papers
            
        except Exception as e:
            logger.error(f"Error fetching papers: {str(e)}")
            return []
    
    def _build_search_query(self, query_intent: QueryIntent) -> str:
        """Build PubMed search query"""
        query_parts = []
        
        if query_intent.condition:
            query_parts.append(f"{query_intent.condition}[Title/Abstract]")
        
        if query_intent.intervention:
            query_parts.append(f"{query_intent.intervention}[Title/Abstract]")
        
        # Add clinical trial filter
        query_parts.append("Clinical Trial[Publication Type]")
        
        # Date range
        if query_intent.start_date:
            start_year = query_intent.start_date[:4]
            end_year = query_intent.end_date[:4] if query_intent.end_date else "2025"
            query_parts.append(f"{start_year}:{end_year}[pdat]")
        
        return " AND ".join(query_parts) if query_parts else "clinical trial"
    
    async def _search_pubmed(self, query: str, max_results: int) -> List[str]:
        """Search PubMed and return PMIDs"""
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": "relevance"
        }
        
        # Only add API key if it's a valid key (not placeholder)
        if self.api_key and not self.api_key.startswith("your_"):
            params["api_key"] = self.api_key
        if self.email and not self.email.startswith("your_"):
            params["email"] = self.email
        
        headers = {
            "User-Agent": "MedNexa/1.0 (Medical Research Platform)"
        }
        
        async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
            response = await client.get(self.ESEARCH_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            pmids = data.get("esearchresult", {}).get("idlist", [])
            
            return pmids
    
    async def _fetch_paper_details(self, pmids: List[str]) -> List[Paper]:
        """Fetch detailed information for papers"""
        if not pmids:
            return []
        
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml"
        }
        
        # Only add API key if it's a valid key (not placeholder)
        if self.api_key and not self.api_key.startswith("your_"):
            params["api_key"] = self.api_key
        
        headers = {
            "User-Agent": "MedNexa/1.0 (Medical Research Platform)"
        }
        
        async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
            response = await client.get(self.EFETCH_URL, params=params)
            response.raise_for_status()
            
            # Parse XML
            data = xmltodict.parse(response.text)
            
            papers = []
            articles = data.get("PubmedArticleSet", {}).get("PubmedArticle", [])
            
            if not isinstance(articles, list):
                articles = [articles]
            
            for article in articles:
                try:
                    paper = self._parse_article(article)
                    if paper:
                        papers.append(paper)
                except Exception as e:
                    logger.warning(f"Error parsing article: {str(e)}")
                    continue
            
            return papers
    
    def _parse_article(self, article: dict) -> Optional[Paper]:
        """Parse article XML into Paper object"""
        try:
            medline = article.get("MedlineCitation", {})
            pubmed_data = article.get("PubmedData", {})
            
            # PMID
            pmid = medline.get("PMID", {}).get("#text", "")
            
            # Article data
            article_data = medline.get("Article", {})
            
            # Title
            title = article_data.get("ArticleTitle", "")
            if isinstance(title, dict):
                title = title.get("#text", "")
            
            # Authors
            author_list = article_data.get("AuthorList", {}).get("Author", [])
            if not isinstance(author_list, list):
                author_list = [author_list]
            
            authors = []
            for author in author_list:
                if isinstance(author, dict):
                    last_name = author.get("LastName", "")
                    fore_name = author.get("ForeName", "")
                    if last_name:
                        authors.append(f"{fore_name} {last_name}".strip())
            
            # Journal
            journal_data = article_data.get("Journal", {})
            journal = journal_data.get("Title", "")
            
            # Publication date
            pub_date = article_data.get("ArticleDate", {})
            if not pub_date:
                pub_date = journal_data.get("JournalIssue", {}).get("PubDate", {})
            
            year = pub_date.get("Year", "")
            month = pub_date.get("Month", "01")
            day = pub_date.get("Day", "01")
            publication_date = f"{year}-{month:0>2}-{day:0>2}" if year else None
            
            # Abstract
            abstract_data = article_data.get("Abstract", {})
            abstract_texts = abstract_data.get("AbstractText", [])
            if not isinstance(abstract_texts, list):
                abstract_texts = [abstract_texts]
            
            abstract = " ".join([
                text if isinstance(text, str) else text.get("#text", "")
                for text in abstract_texts
            ])
            
            # DOI
            doi = None
            article_ids = pubmed_data.get("ArticleIdList", {}).get("ArticleId", [])
            if not isinstance(article_ids, list):
                article_ids = [article_ids]
            
            for aid in article_ids:
                if isinstance(aid, dict) and aid.get("@IdType") == "doi":
                    doi = aid.get("#text")
            
            # URL
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            
            # Keywords
            keyword_list = medline.get("KeywordList", {}).get("Keyword", [])
            if not isinstance(keyword_list, list):
                keyword_list = [keyword_list]
            keywords = [k if isinstance(k, str) else k.get("#text", "") for k in keyword_list]
            
            return Paper(
                pmid=pmid,
                title=title,
                authors=authors[:10],  # Limit to first 10 authors
                journal=journal,
                publication_date=publication_date,
                abstract=abstract,
                doi=doi,
                url=url,
                keywords=keywords
            )
            
        except Exception as e:
            logger.warning(f"Error parsing article: {str(e)}")
            return None
