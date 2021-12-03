# TODO Implement shop to buy items for points
class Shop:
    def __init__(self):
        self.items = []

# The Item class is just an interface for items that can be bought from the shop,
# the actual item implementations should be elsewhere
class Item:
    def __init__(self, id, name, cost):
        self.cost = cost
        self.name = name
        self.id = id

    def __eq__(self, other):
        return other.id == self.id

    def __hash__(self):
        return hash((self.id, self.name))