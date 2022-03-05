import re

from bs4 import BeautifulSoup
import chromedriver_binary
import numpy as np
import requests
from selenium import webdriver
import tensorflow_hub as hub
import tensorflow_text


# setup selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=chrome_options)

# setup universal sentence encoder
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3")


def find_max_page():
    """ Scrape the first page for search results to get the max number of pages."""
    url = "https://www.ricardocuisine.com/recherche?sort=score&searchValue=&content-type=recipe&currentPage=1"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    num = soup.find('div', {'class': 'c-pagination__pages'}).find_all('span')[-1].get_text()
    return int(num)


def get_recipes_list(url):
    """ Scrape search results page to get list of recipe urls and ids. """
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'lxml')

    recipes = []
    for item in soup.find_all('a', {'class': 'c-masonry-item__container'}):
        path = item['href']
        recipes.append({'url': 'https://www.ricardocuisine.com' + path,
                        'id': path.split('/')[-1].split('-')[0]})

    return recipes


def get_recipe_info_ricardo(url):
    """ Scrape the webpage of a specific recipe on ricardo website and collect name and list of ingredients. """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    print(url)
    # get recipe name
    name = soup.find('div', {'class': 'recipe-content'}).find('h1').get_text()
    # get ingredients
    ingredients = []
    for item in soup.find('section', {'class': 'ingredients'}).find_all('span'):
        ingredients.append(cleanup_ingredient(item.get_text()))

    return name, ingredients


def get_recipe_info_radiocan(url):
    """ Scrape the webpage of a specific recipe on radio-canada website and collect name and list of ingredients. """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    print(url)
    # get recipe name
    name = soup.find('div', {'class': 'recipe__heading'}).get_text()
    # get ingredients
    ingredients = []
    for item in soup.find_all('span', {'class': 'ingredients-list-group__list__item__title'}):
        ingredients.append(item.get_text())

    return name, ingredients


def cleanup_ingredient(ingredient):
    """ Remove numbers, units and small words from ingredient. """
    # remove numbers
    ingredient = ''.join([i for i in ingredient if not i.isdigit()])
    # remove text in parenthesis
    ingredient = "".join(re.split("\(|\)|\[|\]", ingredient)[::2])
    # remove tabs
    ingredient = ingredient.replace('\t', ' ')
    # remove measurement units
    for unit in [' ml ', ' oz ', ' g ', ' cm ', ' mm ', '%', ' kg ', ',', ' tasse ', '/', 'c. à thé', 'c. à soupe', ' tasses ', ' lb ', ' litre ']:
        ingredient = ingredient.replace(unit, '')
    # remove extra spaces
    ingredient = ' '.join(ingredient.split())
    # remove de and d' at start of ingredient
    if ingredient.startswith('de '):
        ingredient = ingredient[3:]
    if ingredient.startswith("d’"):
        ingredient = ingredient[2:]

    return ingredient


def get_vector(ingredients):
    """ Pass list of ingredients in universal sentence encoder and average resulting vectors. """
    vectors = embed(ingredients).numpy()
    avg = np.mean(vectors, axis=0)
    return list(avg)


def main():
    num_pages = find_max_page()
    print(num_pages)

    results = []
    for i in range(1, 2):
        url = f"https://www.ricardocuisine.com/recherche?sort=score&searchValue=&content-type=recipe&currentPage={i}"

        recipes = get_recipes_list(url)
        for recipe in recipes[:4]:
            try:
                recipe['name'], recipe['ingredients'] = get_recipe_info_ricardo(recipe['url'])
            except:
                recipe['name'], recipe['ingredients'] = get_recipe_info_radiocan(recipe['url'])
            recipe['vector'] = get_vector(recipe['ingredients'])
        results = results + recipes

    print(results)


main()