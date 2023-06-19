import requests
import time
import sys

def get_related_articles(url, num_articles):
    base_url = "https://en.wikipedia.org/w/api.php"

    # Extract the page title from the URL
    page_title = url.split("/")[-1]

    articles = []
    continue_param = ""
    while len(articles) < num_articles:
        # Make a request to the Wikipedia API to fetch the related articles
        params = {
            "action": "query",
            "format": "json",
            "prop": "info",
            "generator": "search",
            "gsrsearch": f"morelike:{page_title}",
            "gsrnamespace": 0,
            "gsrlimit": num_articles,
            "gsroffset": len(articles),
            "continue": continue_param
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if "query" in data and "pages" in data["query"]:
            pages = data["query"]["pages"]
            for page_id, page_data in pages.items():
                if ":" in page_data.get("title", ""):
                    continue
                article_info = get_article_info(page_id)
                articles.append(article_info)

        if "continue" in data:
            continue_param = data["continue"]["continue"]
        else:
            break

    return articles[:num_articles]

def get_article_info(page_id):
    base_url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "pageids": page_id
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    article_data = {}
    if "query" in data and "pages" in data["query"]:
        page_data = data["query"]["pages"].get(page_id)

        if page_data:
            article_title = page_data.get("title", "")
            article_intro = page_data.get("extract", "")
            article_link = f"https://en.wikipedia.org/?curid={page_id}"
            article_data = {
                "title": article_title,
                "link": article_link,
                "introduction": article_intro
            }

    return article_data

def calculate_execution_time(start_time, end_time):
    execution_time = end_time - start_time
    return execution_time

def calculate_crawling_speed(num_articles, execution_time):
    crawling_speed = num_articles / execution_time
    return crawling_speed

def calculate_success_rate(related_articles, num_articles):
    success_rate = len(related_articles) / num_articles * 100
    return success_rate

def calculate_queue_size(related_articles):
    queue_size = len(related_articles)
    return queue_size

def calculate_index_size(related_articles):
    index_size = sys.getsizeof(related_articles)
    return index_size

def main():
    url = input("Enter the URL of the Wikipedia article: ")
    num_articles = int(input("Enter the number of related articles to retrieve: "))

    start_time = time.time()

    related_articles = get_related_articles(url, num_articles)

    end_time = time.time()
    execution_time = calculate_execution_time(start_time, end_time)
    crawling_speed = calculate_crawling_speed(num_articles, execution_time)
    success_rate = calculate_success_rate(related_articles, num_articles)
    queue_size = calculate_queue_size(related_articles)
    index_size = calculate_index_size(related_articles)

    print("\nRelated Articles:")
    with open('related_articles.txt', 'w', encoding='utf-8') as file:
        for i, article in enumerate(related_articles, 1):
            file.write(f"\nRelated Article {i}:\n")
            file.write(f"Title: {article['title']}\n")
            file.write(f"Link: {article['link']}\n")
            file.write(f"Introduction:\n{article['introduction']}\n")

            print(f"\nRelated Article {i}:")
            print(f"Title: {article['title']}")
            print(f"Link: {article['link']}")
            print(f"Introduction:\n{article['introduction']}")

    print(f"\nExecution Time: {execution_time} seconds")
    print(f"Crawling Speed: {crawling_speed:.2f} pages per second")
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"Queue Size: {queue_size}")
    print(f"Index Size: {index_size} bytes")

if __name__ == '__main__':
    main()