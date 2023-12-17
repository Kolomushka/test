import requests
from bs4 import BeautifulSoup
import pandas as pd

# Функция для сбора информации о каждой новости
def parse_news(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлечение даты
        date = soup.find('time').get_text()

        # Извлечение заголовка
        title = soup.find('h1').get_text()
        
        # Извлечение текста новости
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])

        # Извлечение автора
        author_tag = soup.find('a', {'rel': 'author'})
        author = author_tag.get_text() if author_tag else None


        # Извлечение категорий
        categories = [a.get_text() for a in soup.find_all('a', {'rel': 'category tag'})]


        return {'Date': date, 'Title': title, 'Text': text, 'Author': author, 'Categories': categories}
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Ссылки на страницы с новостями
all_pages = ['https://sysblok.ru', 'https://sysblok.ru/page/2', 'https://sysblok.ru/page/16']

# Собираем все ссылки на отдельные новости
all_links = []
for page_url in all_pages:
    try:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.select('.entry-title a')]
        all_links.extend(links)
    except Exception as e:
        print(f"An error occurred: {e}")

# Собираем информацию о каждой новости
all_news = []
for link in all_links:
    news_info = parse_news(link)
    if news_info:
        all_news.append(news_info)

# Создаем датафрейм
df = pd.DataFrame(all_news)

# Сохраняем датафрейм в csv
df.to_csv('news_data.csv', index=False)
