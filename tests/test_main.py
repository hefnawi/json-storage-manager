# -*- coding: utf-8 -*-

import json
import pytest
import random
import uuid
from json_storage_manager import atomic, utils


def test_is_file_not_ok():
    invalid_filename = "tests/data.json"
    assert not utils.is_file(invalid_filename)


def test_is_file_ok():
    invalid_filename = "tests/test_main.py"
    assert utils.is_file(invalid_filename)


@pytest.fixture(scope='session')
def create_json_data():

    def _create_json_data(product_name):
        return {
            "uuid": str(uuid.uuid4()),
            "name": str(product_name),
            "price": str(round(random.uniform(5.0, 6000.0), 2))
        }

    return _create_json_data


@pytest.fixture(scope='session')
def json_file(tmpdir_factory, create_json_data):
    json_1 = create_json_data("Alpha Product MK-1000")
    json_2 = create_json_data("Bravo Product MK-2000")
    json_3 = create_json_data("Charlie Product MK-3000")
    json_list = []
    json_list.append(json_1)
    json_list.append(json_2)
    json_list.append(json_3)
    fn = tmpdir_factory.mktemp('data').join('products.json')
    fn.write(json.dumps(json_list))
    return fn


# read contents of json file
def test_read_json(json_file):
    with open(str(json_file)) as f:
        products_data = json.load(f)
    for item in products_data:
        assert item["uuid"]
        assert item["name"]
        assert item["price"]


# add to contents of json file
def test_write_json(json_file):
    with atomic.atomic_write(str(json_file)) as temp_file:
        with open(str(json_file)) as products_file:
            # get the JSON data into memory
            products_data = json.load(products_file)
        # now process the JSON data
        products_data.append(
            {'uuid': "2299d69e-deba-11e8-bded-680715cce955",
             'price': 111.0,
             'name': "Test Product"
             })
        json.dump(products_data, temp_file)

    with open(str(json_file)) as f:
        products_data = json.load(f)
    test = [i for i in products_data if i["uuid"] == "2299d69e-deba-11e8-bded-680715cce955"]
    assert test[0]["name"] == 'Test Product'


def test_get_item(json_file):
    results = atomic.get_item(
        str(json_file), "2299d69e-deba-11e8-bded-680715cce955")
    assert results
    assert results[0]["name"] == 'Test Product'


def test_get_no_item(json_file):
    results = atomic.get_item(
        str(json_file), "xxxxxxxx-deba-11e8-bded-680715cce955")
    assert not results


def test_set_item(json_file):
    new_item = {'uuid': "1144d69e-joya-33e8-bdfd-680688cce955",
                'price': 333.0,
                'name': "Test Product via set_item"
                }
    results = atomic.set_item(str(json_file), new_item)
    results_get = atomic.get_item(
        str(json_file), "1144d69e-joya-33e8-bdfd-680688cce955")
    assert results
    assert results_get[0]["name"] == 'Test Product via set_item'


def test_update_item(json_file):
    mod_item = {'price': 777.0,
                'name': "Test Product via update_item"
                }
    results = atomic.update_item(str(json_file), mod_item, "1144d69e-joya-33e8-bdfd-680688cce955")
    results_get = atomic.get_item(
        str(json_file), "1144d69e-joya-33e8-bdfd-680688cce955")
    assert results
    assert results_get[0]["name"] == 'Test Product via update_item'
    assert results_get[0]["price"] == 777.0


def test_set_item_fail(json_file):
    new_item = {'uuid': "1144d69e-joya-33e8-bdfd-680688cce955",
                'price': 333.0,
                'name': "Test Product via set_item"
                }
    results = atomic.set_item(str(json_file), new_item)
    assert not results
