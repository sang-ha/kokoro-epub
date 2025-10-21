import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_chapters(epub_path):
    """
    Extract all chapters and their content from an EPUB file.
    
    Args:
        epub_path (str): Path to the EPUB file
        
    Returns:
        list: Array of tuples (title, content)
    """
    # Read the EPUB file
    book = epub.read_epub(epub_path)
    
    chapters = []
    
    # Iterate through all items in the book
    for item in book.get_items():
        # Filter only document items (chapters)
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            
            # Extract title (try to get from h1, h2, or title tag)
            title = None
            if soup.find('h1'):
                title = soup.find('h1').get_text(strip=True)
            elif soup.find('h2'):
                title = soup.find('h2').get_text(strip=True)
            elif soup.find('title'):
                title = soup.find('title').get_text(strip=True)
            else:
                # Use the item's file name as fallback
                title = item.get_name()
            
            # Extract text content
            content = soup.get_text(separator='\n', strip=True)
            
            # Only add chapters with actual content
            if content:
                # Include title in content followed by a period
                full_content = f"{title}. {content}"
                chapters.append((title, full_content))
    
    return chapters
