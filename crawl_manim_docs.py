import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
import time

class ManimDocsCrawler:
    def __init__(self):
        self.base_url = "https://docs.manim.community/en/stable/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
    def get_code_snippets(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            snippets = []
            
            # Find all code blocks with class 'highlight-python'
            code_blocks = soup.find_all('div', class_='highlight-python')
            
            for block in code_blocks:
                # Get the actual code
                code = block.find('pre').text if block.find('pre') else ""
                
                # Get the context (description) from nearby elements
                context = ""
                prev_p = block.find_previous('p')
                if prev_p:
                    context = prev_p.text.strip()
                
                if code.strip():  # Only add non-empty code blocks
                    snippet = {
                        "source_url": url,
                        "code": code.strip(),
                        "context": context,
                        "section": self._get_section_title(block, soup),
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    snippets.append(snippet)
            
            return snippets
        
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return []
    
    def _get_section_title(self, element, soup):
        # Try to find the nearest heading above the code block
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            heading = element.find_previous(tag)
            if heading:
                return heading.text.strip()
        return ""
    
    def save_snippets(self, snippets, filename):
        with open(filename, 'a', encoding='utf-8') as f:
            for snippet in snippets:
                f.write(json.dumps(snippet, ensure_ascii=False) + '\n')
    
    def crawl_url(self, url, output_file):
        print(f"Crawling: {url}")
        snippets = self.get_code_snippets(url)
        if snippets:
            self.save_snippets(snippets, output_file)
            print(f"Saved {len(snippets)} snippets from {url}")
        else:
            print(f"No snippets found in {url}")
        time.sleep(2)  # Be nice to the server

# URLs to crawl
urls = [
    "https://docs.manim.community/en/stable/tutorials/building_blocks.html",
    "https://docs.manim.community/en/stable/guides/configuration.html",
    "https://docs.manim.community/en/stable/guides/deep_dive.html",
    "https://docs.manim.community/en/stable/guides/using_text.html",
    "https://docs.manim.community/en/stable/reference/manim.animation.animation.html",
    "https://docs.manim.community/en/stable/reference/manim.animation.changing.AnimatedBoundary.html",
    "https://docs.manim.community/en/stable/reference/manim.animation.changing.TracedPath.html"
]

def main():
    crawler = ManimDocsCrawler()
    output_file = "manim_docs_snippets.jsonl"
    
    for url in urls:
        crawler.crawl_url(url, output_file)
        print("-" * 50)

if __name__ == "__main__":
    main()