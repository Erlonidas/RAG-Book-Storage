import logging
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_article_metadata(dolphin_json: dict, book_id: str) -> Optional[dict]:
    """
    Extracts metadata from a scientific article from Dolphin JSON.
    
    Searches the first pages for elements containing:
    - Title (sec_0 from the first page)
    - Abstract (element with tags containing 'abstract', 'paper_abstract', 'Abstract')
    - Authors (element with tags containing 'author', 'authors', 'author_affili')
    
    Args:
        dolphin_json: Dictionary with Dolphin JSON structure
        book_id: Unique article identifier
    
    Returns:
        Dictionary with format:
        {
            "book_id": str,
            "title": str,
            "abstract": str,
            "authors": str | None,
            "combined_text": str
        }
        Returns None if title or abstract not found
    """
    title = None
    abstract = None
    authors = None
    
    pages = dolphin_json.get('pages', [])
    
    # Search in the first 3 pages (abstract is usually at the beginning)
    max_pages_to_search = min(3, len(pages))
    
    for page_idx in range(max_pages_to_search):
        page = pages[page_idx]
        elements = page.get('elements', [])
        
        for element in elements:
            label = element.get('label', '')
            text = element.get('text', '').strip()
            tags = element.get('tags', [])
            
            # Capture title (first sec_0 found)
            if label == 'sec_0' and title is None and text:
                title = text
                logger.debug(f"Title found on page {page_idx + 1}: {title[:50]}...")
            
            # Capture abstract (search for related tags)
            if abstract is None and tags:
                # Check if any tag contains 'abstract' (case-insensitive)
                abstract_tags = [tag for tag in tags if 'abstract' in tag.lower()]
                if abstract_tags and text:
                    abstract = text
                    logger.debug(f"Abstract found on page {page_idx + 1} with tag: {abstract_tags}")
            
            # Capture authors (search for related tags)
            if authors is None and tags:
                # Check if any tag contains 'author' (case-insensitive)
                author_tags = [tag for tag in tags if 'author' in tag.lower()]
                if author_tags and text:
                    authors = text
                    logger.debug(f"Authors found on page {page_idx + 1} with tag: {author_tags}")
        
        # If title, abstract and authors are found, can stop
        if title and abstract and authors:
            break
    
    # Validation
    if not title:
        logger.warning(f"book_id='{book_id}': Title not found")
        return None
    
    if not abstract:
        logger.warning(f"book_id='{book_id}': Abstract not found")
        return None
    
    # Authors are optional
    if not authors:
        logger.info(f"book_id='{book_id}': Authors not found (may be omitted in PDF)")
    
    # Build combined_text
    combined_text = f"{title}\n\nAbstract: {abstract}"
    
    result = {
        "book_id": book_id,
        "title": title,
        "abstract": abstract,
        "authors": authors,
        "combined_text": combined_text
    }
    
    logger.info(f"book_id='{book_id}': Metadata extracted successfully")
    return result
