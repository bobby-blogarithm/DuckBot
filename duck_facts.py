import random

from helpers.unsplash_image import get_random_image

DUCK_IMAGES_FILE = 'duck-facts/image_links.txt'
DUCK_FACTS_FILE = 'duck-facts/duck_facts.txt'


class DuckFact:
    def __init__(self):
        self.images = DUCK_IMAGES_FILE
        self.facts = DUCK_FACTS_FILE

    def get_fact(self):
        with open(self.facts, 'r', encoding='utf8') as file:
            fact = file.readlines()
            fact_num = random.randint(1, len(fact)) - 1

        return fact[fact_num], fact_num + 1

    def get_image(self):
        with open(self.images, 'r', encoding='utf8') as file:
            image = file.readlines()
            image_num = random.randint(1, len(image)) - 1

        return image[image_num]

    # Obtain a random (duck) image from Unsplash
    async def get_image_unsplash(self, client_key, query='duck', orientation='landscape'):
        return await get_random_image(client_key, query, orientation)

    def add_fact(self, fact):
        fact += '\n' if fact[-1] != '\n' else ''
        with open(self.facts, 'a', encoding='utf8') as file:
            file.write(fact)

    def add_image(self, image_link):
        image_link += '\n' if image_link[-1] != '\n' else ''
        with open(self.images, 'a', encoding='utf8') as file:
            file.write(image_link)
