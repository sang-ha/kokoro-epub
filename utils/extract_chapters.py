from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

def extract_chapters(epub_path):
    """Extract chapter titles and text content from an EPUB file."""

    book = epub.read_epub(epub_path)
    chapters = []
    
    for idref, _ in book.spine:
        item = book.get_item_with_id(idref)
        if item.get_type() == ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text = soup.get_text().strip()
            if not text:
                continue

            # Find all chapter headings
            headings = soup.find_all(["h1", "h2", "h3"])
            
            if headings:
                # If there's only one heading, treat the entire document as one chapter
                if len(headings) == 1:
                    title = headings[0].get_text(strip=True)
                    # Get all text content from the document (includes the heading)
                    chapter_text = soup.get_text(" ", strip=True)
                    
                    # Add period after the title if it doesn't already have punctuation
                    if chapter_text.startswith(title):
                        if not title.endswith(('.', '!', '?', ':')):
                            chapter_text = chapter_text.replace(title, title + ".", 1)
                    
                    if chapter_text and not any(title.lower().startswith(s) for s in get_skip_titles()):
                        chapters.append((title, chapter_text))
                
                else:
                    # Multiple headings - split content between them
                    for i, heading in enumerate(headings):
                        title = heading.get_text(strip=True)
                        
                        # Find the next heading to determine where this chapter ends
                        next_heading = headings[i + 1] if i + 1 < len(headings) else None
                        
                        # Get all elements starting from this heading to the next
                        content_elements = [title + "."]  # Include the heading text with period
                        current = heading.next_element
                        
                        while current and current != next_heading:
                            # If we hit the next heading, stop
                            if next_heading and current == next_heading:
                                break
                            
                            # If this is a text element or has text content
                            if hasattr(current, 'get_text'):
                                text_content = current.get_text(" ", strip=True)
                                if text_content and text_content not in [h.get_text(strip=True) for h in headings]:
                                    content_elements.append(text_content)
                            elif hasattr(current, 'string') and current.string:
                                text_content = current.string.strip()
                                if text_content:
                                    content_elements.append(text_content)
                            
                            current = current.next_element
                        
                        chapter_text = " ".join(content_elements).strip()
                        
                        # Clean up the text - remove duplicate whitespace
                        chapter_text = " ".join(chapter_text.split())
                        
                        if chapter_text and not any(title.lower().startswith(s) for s in get_skip_titles()):
                            chapters.append((title, chapter_text))
            else:
                # No headings found - treat entire document as one chapter
                chapters.append((item.file_name, text))
    
    return chapters

def get_skip_titles():
    """Return list of title prefixes to skip."""
    return [
        "the project gutenberg", 
        "table of contents", 
        "the full project gutenberg license",
        "produced by",
        "end of the project gutenberg",
        "*** start of this project gutenberg",
        "*** end of this project gutenberg"
    ]