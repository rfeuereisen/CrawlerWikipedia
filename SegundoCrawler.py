import requests
from bs4 import BeautifulSoup
import random
import time

def scrapeWikiArticle(url, num_links_to_scrape):
    start_time = time.time()

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading").text
    print(f"Buscaste el artículo: {title}\n")

    allLinks = soup.find(id="bodyContent").find_all("a")
    random.shuffle(allLinks)

    links_scraped = 0
    link_number = 1

    index_size = 0

    for link in allLinks:
        if links_scraped == num_links_to_scrape:
            break

        if 'href' in link.attrs and link['href'].startswith("/wiki/") and ":" not in link['href']:
            link_title = link.get("title")
            link_url = "https://es.wikipedia.org" + link['href']
            if link_title is None:
                continue

            print(f"{link_number}. {link_title}")
            print(f"   URL: {link_url}\n")
            links_scraped += 1
            link_number += 1

            response = requests.get(link_url)
            index_size += len(response.content)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {execution_time} segundos")
    print(f"Velocidad de crawling: {num_links_to_scrape / execution_time} páginas por segundo")
    print(f"Tasa de éxito: {(links_scraped / num_links_to_scrape) * 100}%")
    print(f"Tamaño de la cola: {len(allLinks)}")
    print(f"Tamaño del índice: {index_size} bytes")

scrapeWikiArticle("https://en.wikipedia.org/wiki/Justin_Bieber", 50)
