import json
from json_storage_manager import atomic, utils

# with open("../../../data/data-100k.json", "r") as products_file_r:
#     products_data = json.load(products_file_r)


# products_data.append(
#     {'UUID': "2299d69e-deba-11e8-bded-680715cce955",
#      'price': "77",
#      'name': "Brand New Product"
#      })


# with open("../../../data/data-100k.json", "w") as products_file_w:
#     json.dump(products_data, products_file_w)


# def create_data():
#     """
#     """
#     import json
#     import lorem
#     import uuid
#     import random

#     products_data = []

#     for i in range(5000000):
#         products_data.append(
#             {'uuid': str(uuid.uuid1()),
#              'name': str(lorem.sentence()),
#              'price': str(round(random.uniform(5.0, 6000.0), 2))
#              }
#             )

#     with open("data-5m.json", "w") as products_file_w:
#         json.dump(products_data, products_file_w, sort_keys=True, indent=2)


# filename = "tests/dummy_products.json"

# with fatomic.atomic_write(filename) as temp_file:
#     with open(filename, "r") as products_file:
#         # get the JSON data into memory
#         _products_data = json.load(products_file)
#     # now process the JSON data
#     _products_data.append(
#         {'UUID': "2299d69e-deba-11e8-bded-680715cce955",
#          'price': "77",
#          'name': "New Product"
#          })
#     json.dump(_products_data, temp_file)


def test_is_file_ok():
    filename = "tests/data/dummy_products.json"

    assert utils.is_file(filename) is True


def test_is_file_not_ok():
    invalid_filename = "tests/data/invalid.json"

    assert utils.is_file(invalid_filename) is None


def test_json_read_object():
    filename = "tests/data/dummy_products.json"
    with open(filename, "r") as f:
        products_data = json.load(f)
    test = [i for i in products_data if i["uuid"] == "e4eaefcd-e128-11e8-87d5-680715cce921"]
    assert test[0]["special_price"] == '1654.03'


def test_json_add_object():
    filename = "tests/data/dummy_products.json"

    with atomic.atomic_write(filename) as temp_file:
        with open(filename, "r") as products_file:
            # get the JSON data into memory
            products_data = json.load(products_file)
        # now process the JSON data
        products_data.append(
            {'uuid': "2299d69e-deba-11e8-bded-680715cce955",
             'special_price': "111.0",
             'name': "Test Product"
             })
        json.dump(products_data, temp_file)

    with open(filename, "r") as f:
        products_data = json.load(f)
    test = [i for i in products_data if i["uuid"] == "2299d69e-deba-11e8-bded-680715cce955"]
    assert test[0]["name"] == 'Test Product'
