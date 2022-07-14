import csv
import json
import os

from .constants import SHOP_FILE, INVENTORY_FILE, CATALOG_FILE
from .economy import Economy
from .errors import NotAnItemError


class Shop:
    _instance = None

    def __init__(self, server):
        self.econ = Economy.get_instance(server)
        self.catalog = Catalog.get_instance(server)

        # Parse the server name before creating or accessing the file for it
        parsed_server_name = ''.join(char for char in server if char.isalnum())

        self.shop_file = SHOP_FILE.replace('SERVER', parsed_server_name)
        self.items = self.load(self.shop_file) if os.path.exists(self.shop_file) else []

    @classmethod
    def get_instance(cls, server):
        if cls._instance is None:
            cls._instance = Shop(server)
        return cls._instance

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        for item in self.items:
            if key == item.id:
                return item
        return None

    def add_item(self, item):
        if not isinstance(self.items, set) and not self.items:
            self.items = set()
        if item not in self.items:
            self.items.add(item)
            self.save()

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            self.save()

    def load(self, fp):
        with open(fp, newline='') as f:
            csvreader = csv.reader(f)
            next(csvreader)  # Skip header row
            return {self.catalog[row[0]].set_quantity(row[1]) for row in csvreader}

    def save(self):
        # Generate the necessary file structure if it does not exist
        out_folder = self.shop_file[:self.shop_file.rfind('/')]
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        with open(self.shop_file, 'w', newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(['ID', 'Quantity'])  # Write header
            for item in self.items:
                csvwriter.writerow([item.id, item.quantity])


# The Item class is just an interface for items that can be bought from the shop,
# the actual item implementations should be elsewhere
class Item:
    def __init__(self, id: int = -1, name: str = '', cost: int = -1, quantity: int = 0):
        self.cost = cost
        self.name = name
        self.id = id
        self.quantity = quantity

    def __eq__(self, other):
        return other.id == self.id

    def __hash__(self):
        return hash(self.id)

    def copy(self):
        return Item(self.id, self.name, self.cost)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'cost': self.cost, 'quantity': self.quantity}

    def from_dict(self, data):
        try:
            self.id = data['id']
            self.name = data['name']
            self.cost = data['cost']
            self.quantity = data['quantity']
        except KeyError as e:
            raise NotAnItemError(f'Dictionary could not be converted to an item without key(s): {", ".join(e.args)}')
        return self

    # This function exists purely because I am lazy
    def set_quantity(self, new_quantity: int):
        self.quantity = int(new_quantity)
        return self


# Inventory representing the items a user has in a given server
class Inventory:
    def __init__(self, server, user):
        self.econ = Economy.get_instance(server)
        self.catalog = Catalog.get_instance(server)
        self.shop = Shop.get_instance(server)
        self.owner = user

        # Parse the server name before creating or accessing the file for it
        parsed_server_name = ''.join(char for char in server if char.isalnum())

        self.inventory_file = INVENTORY_FILE.replace('SERVER', parsed_server_name)
        self.items = self.load(self.inventory_file) if os.path.exists(self.inventory_file) else {}

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        for item in self.items:
            if key == item.id:
                return item
        return None

    def buy(self, item, amount: int):
        # Ensure that the inventory is a set of items
        if not isinstance(self.items, set) and not self.items:
            self.items = set()

        # Get the item from the shop
        if isinstance(item, str):
            try:
                item_id = next(i.id for i in self.shop.items if i.name == item)
            except StopIteration:
                raise NotAnItemError(f'Item {item} does not exist to be purchased')
        elif isinstance(item, int):
            item_id = item
        else:
            raise NotAnItemError('Invalid item being purchased')
        shop_item = self.shop[item_id]

        # You can only purchase the item if the shop has it in stock
        purchased_item = None
        if shop_item.quantity - amount >= 0:
            # Case: we already have the same item in the inventory
            if shop_item in self.items:
                purchased_item = self[item_id]
                self[item_id].quantity += amount
            else:  # Case: we do not have the same item in the inventory
                purchased_item = self.catalog[item_id].set_quantity(amount)
                self.items.add(purchased_item)
            shop_item.quantity -= amount

            # Subtract currency
            self.econ.scores[self.owner] -= purchased_item.cost
            self.econ.save()
            self.save()
        else:
            print(f'Unable to buy {amount} item(s) with ID {item_id}, insufficient stock.')

    def load(self, fp):
        with open(fp) as f:
            inventories = json.load(f)
            json_inventory = inventories[self.owner]
            return {self.catalog[id].set_quantity(quantity) for id, quantity in json_inventory.items()}

    def save(self):
        # Generate the necessary file structure if it does not exist
        out_folder = self.inventory_file[:self.inventory_file.rfind('/')]
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        # Open the inventories file to ONLY update the user's inventory
        with open(self.inventory_file, 'w+') as f:
            inventories = json.load(f) if os.stat(self.inventory_file).st_size > 0 else {}
            inventories[self.owner] = {item.id: item.quantity for item in self.items}
            json.dump(inventories, f)


# Catalog intended to store all item information for a given server
class Catalog:
    _instance = None

    def __init__(self, server):
        # Parse the server name before creating or accessing the file for it
        parsed_server_name = ''.join(char for char in server if char.isalnum())

        self.catalog_file = CATALOG_FILE.replace('SERVER', parsed_server_name)
        self.items = self.load(self.catalog_file) if os.path.exists(self.catalog_file) else {}

    @classmethod
    def get_instance(cls, server):
        if cls._instance is None:
            cls._instance = Catalog(server)
        return cls._instance

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key: int):
        key = int(key)
        for item in self.items:
            if key == item.id:
                return item.copy()
        return None

    def __delitem__(self, key):
        for item in self.items:
            if item.id == key:
                self.remove_item(item)
                return True
        return False

    def add_item(self, item):
        if not isinstance(self.items, set) and not self.items:
            self.items = set()
        if item not in self:
            self.items.add(item.copy().set_quantity(-1))
            self.save()

    def remove_item(self, item):
        if item in self:
            self.items.remove(item)
            self.save()

    def load(self, fp):
        with open(fp) as f:
            json_catalog = json.load(f)
            return {Item().from_dict(item) for item in json_catalog}

    def save(self):
        # Generate the necessary file structure if it does not exist
        out_folder = self.catalog_file[:self.catalog_file.rfind('/')]
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        # Open the inventories file to ONLY update the user's inventory
        with open(self.catalog_file, 'w') as f:
            json.dump([item.to_dict() for item in self.items], f)


if __name__ == '__main__':
    num_items = 11
    items = [Item(i, f'test item {i + 1}', 1, 100) for i in range(num_items)]

    catalog = Catalog.get_instance('Botland')
    shop = Shop.get_instance('Botland')

    player_inv = Inventory('Botland', 'Dark?')

    for item in items:
        catalog.add_item(item)
        shop.add_item(item)
    # player_inv.buy(1, 1)
    # player_inv.buy(2, 1)

    shop.save()
    player_inv.save()
