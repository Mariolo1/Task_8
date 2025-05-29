import time
import random
import requests
from bs4 import BeautifulSoup

class JobFetcher:
    def __init__(self, base_url="https://justjoin.it/"):
        self.base_url = base_url

    def get_job_links(self, limit=10):
        job_links = set ()
        page = 1
        
        while len(job_links) < limit:
            url = f"{self.base_url}?page={page}"
            try:
                response = requests.get(url,timeout=1000)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Błąd podczas pobierania strony {url}: {e}")
                break
                
        
            soup = BeautifulSoup(response.text, 'html.parser')
            found_links = ["https://justjoin.it" + link["href"] for link in soup.find_all("a", href=(True)) if "/job-offer/" in link["href"]]
            job_links.update(found_links)
        
            if not found_links:
                break #jeśli nie ma ofert konczymy paginację
            
            page += 1
            time.sleep(random.uniform(1, 2)) #unikanie blokady
        
        return list(job_links)[:limit]
        
    def get_job_details(self, job_url):
        try:
            response = requests.get(job_url, timeout=1000)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Błąd pobierania oferty {job_url}: {e}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return {
            "url": job_url,
            "title": self._get_text(soup, "h1", "Brak tytułu"),
            "description": self._get_text(soup, "div", "Brak opisu", "MuiBox-root css-1p81rs"),
            "add_info": self._get_text(soup, "div", "Brak opisu", "MuiBox-root css-17h1y7k"),
            "company_location": self._get_text(soup, "div", "Brak opisu", "MuiBox-root css-yd5zxy"),
            "salary": self._get_text(soup, "div", "Brak opisu", "MuiBox-root css-1km0bek"),
            "tech_stack" : self._get_text(soup, "div", "Brak opisu", "MuiBox-root css-qal8sw")
            
               
        
        }
                  
        
    
    def _get_text(self, soup, tag, default, class_name=None):
        element = soup.find(tag, class_=class_name) if class_name else soup.find(tag)
        return element.text.strip() if element else default

    def fetch_offers(self, limit =10):
        job_links = self.get_job_links(limit)
        all_job_details = []
        
        for link in job_links:
            time.sleep(random.uniform(1, 3))  # Randomizowanie opóźnienia między 1 a 3 sekundy
            job_details = self.get_job_details(link)
            if job_details:
                all_job_details.append(job_details)
                print("\n", job_details)
        
        return all_job_details
