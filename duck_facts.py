import random

from helpers.unsplash_image import get_random_image


def get_fact():
    with open('duck-facts/duck_facts.txt', 'r', encoding='utf8') as file:
        fact = file.readlines()
        fact_num = random.randint(1, len(fact)) - 1

    return fact[fact_num], fact_num + 1


# Obtain a random (duck) image from Unsplash
async def get_image(client_key, query='duck', orientation='landscape'):
    return await get_random_image(client_key, query, orientation)
