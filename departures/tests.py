import os

from datetime import date
import operator
from django.test import TestCase
import responses
# Create your tests here.
from scripts.management.commands.data_collection_script import \
    dump_data_to_csv, \
    fetch_data_from_api_and_create_csv, change_dict_keys_to_title_case
from utilities.filters import FilterChain, DateFilter, Filter


class DeparturesTest(TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000'
        super(DeparturesTest, self).setUp()

    def tearDown(self):
        super(DeparturesTest, self).tearDown()

    def test_filter_data(self):
        data = [
        {
            "name": "New Zealand Safari",
            "start_date": "2018-04-03",
            "finish_date": "2018-04-13",
            "category": "Marine"
        },
        {
            "name": "New Zealand Encompassed",
            "start_date": "2018-08-31",
            "finish_date": "2018-09-10",
            "category": "Adventurous"
        },
        {
            "name": "Bali Overland",
            "start_date": "2018-04-03",
            "finish_date": "2018-04-13",
            "category": "Classic"
        },
        {
            "name": "Galapagos Overland",
            "start_date": "2018-08-31",
            "finish_date": "2018-09-10",
            "category": "Marine"
        },
        {
            "name": "Galapagos Discovery",
            "start_date": "2018-04-03",
            "finish_date": "2018-04-13",
            "category": "Adventurous"
        },
        {
            "name": "Brazil Adventure",
            "start_date": "2018-04-03",
            "finish_date": "2018-04-13",
            "category": "Classic"
        },
        {
            "name": "Vietnam Encompassed",
            "start_date": "2018-04-03",
            "finish_date": "2018-04-13",
            "category": "Marine"
        }]


        expected_data = [
            {
                "name": "New Zealand Safari",
                "start_date": "2018-04-03",
                "finish_date": "2018-04-13",
                "category": "Marine"
            },
            {
                "name": "Vietnam Encompassed",
                "start_date": "2018-04-03",
                "finish_date": "2018-04-13",
                "category": "Marine"
            }
        ]

        filter_chain = FilterChain()
        date_filter = DateFilter('finish_date', operator.le, date(year=2018, month=6, day=1))
        category_filter = Filter('category', operator.eq, 'Marine')
        filter_chain.add_filter(date_filter).add_filter(category_filter)

        filtered_data = filter_chain.filter(data)

        assert len(filtered_data)==len(expected_data)

        for _filtered, _expected in zip(filtered_data, expected_data):
            for k, v in _filtered.items():
                assert _expected[k]==v

    def test_create_csv_file(self):
        data = [
            {
                "name": "New Zealand Encompassed",
                "start_date": "2018-08-31",
                "finish_date": "2018-09-10",
                "category": "Adventurous"
            },
            {
                "name": "Galapagos Discovery",
                "start_date": "2018-04-03",
                "finish_date": "2018-04-13",
                "category": "Adventurous"
            }
        ]

        filename = 'test_csv_data_output.csv'
        data = change_dict_keys_to_title_case(data)
        fieldnames = ['Name', 'Start Date', 'Finish Date', 'Category']
        dump_data_to_csv(filename, data, fieldnames)

        assert self._compare_csv_file(filename, 'test_csv_data_sample.csv') is True

        if os.path.exists(filename):
            os.remove(filename)

    def _compare_csv_file(self, file_one, file_two):
        with open(file_one, 'r') as t1, open(file_two, 'r') as t2:
            _file_one = t1.readlines()
            _file_two = t2.readlines()

            for line in _file_two:
                if line not in _file_one:
                    return False

            return True

    @responses.activate
    def test_pagination(self):
        first_page_data = {
            "count": 20,
            "next": "http://127.0.0.1:8000/departures/?limit=10&offset=10",
            "previous": None,
            "results": [
                {
                    "name": "New Zealand Safari",
                    "start_date": "2018-04-03",
                    "finish_date": "2018-04-13",
                    "category": "Marine"
                },
                {
                    "name": "New Zealand Encompassed",
                    "start_date": "2018-08-31",
                    "finish_date": "2018-09-10",
                    "category": "Adventurous"
                },
                {
                    "name": "Bali Overland",
                    "start_date": "2018-04-03",
                    "finish_date": "2018-04-13",
                    "category": "Classic"
                },
                {
                    "name": "Galapagos Overland",
                    "start_date": "2018-08-31",
                    "finish_date": "2018-09-10",
                    "category": "Marine"
                },
                {
                    "name": "Galapagos Discovery",
                    "start_date": "2018-04-03",
                    "finish_date": "2018-04-13",
                    "category": "Adventurous"
                },
                {
                    "name": "Brazil Adventure",
                    "start_date": "2018-04-03",
                    "finish_date": "2018-04-13",
                    "category": "Classic"
                },
                {
                    "name": "Vietnam Encompassed",
                    "start_date": "2018-04-03",
                    "finish_date": "2018-04-13",
                    "category": "Marine"
                },
                {
                    "name": "Cambodia Safari",
                    "start_date": "2018-08-31",
                    "finish_date": "2018-09-10",
                    "category": "Marine"
                },
                {
                    "name": "Peru Multisport",
                    "start_date": "2018-04-03",
                    "finish_date": "2018-04-13",
                    "category": "Classic"
                },
                {
                    "name": "Galapagos Encompassed",
                    "start_date": "2018-04-03",
                    "finish_date": "2018-04-13",
                    "category": "Marine"
                }
            ]
        }
        second_page_data = {
            "count": 20,
            "next": None,
            "previous": "http://127.0.0.1:8000/departures/?limit=10",
            "results": [
                {
                    "name": "South Africa Discovery",
                    "start_date": "2018-08-31",
                    "finish_date": "2018-09-10",
                    "category": "Marine"
                },
                {
                    "name": "Bali Overland",
                    "start_date": "2018-04-03",
                    "finish_date": "2018-04-13",
                    "category": "Marine"
                },
                {
                    "name": "New Zealand Encompassed",
                    "start_date": "2018-04-03",
                    "finish_date": "2018-04-13",
                    "category": "Marine"
                },
                {
                    "name": "Cambodia Overland",
                    "start_date": "2018-08-31",
                    "finish_date": "2018-09-10",
                    "category": "Adventurous"
                },
                {
                    "name": "Bali Encompassed",
                    "start_date": "2018-08-31",
                    "finish_date": "2018-09-10",
                    "category": "Marine"
                },
                {
                    "name": "South Africa Encompassed",
                    "start_date": "2018-08-31",
                    "finish_date": "2018-09-10",
                    "category": "Marine"
                },
                {
                    "name": "Ethopia Multisport",
                    "start_date": "2018-04-03",
                    "finish_date": "2018-04-13",
                    "category": "Marine"
                },
                {
                    "name": "Cambodia Adventure",
                    "start_date": "2018-08-31",
                    "finish_date": "2018-09-10",
                    "category": "Classic"
                },
                {
                    "name": "Kenya Overland",
                    "start_date": "2018-08-31",
                    "finish_date": "2018-09-10",
                    "category": "Marine"
                },
                {
                    "name": "Cambodia Trek",
                    "start_date": "2018-08-31",
                    "finish_date": "2018-09-10",
                    "category": "Marine"
                }
            ]
        }
        first_url = self.base_url + '/departures/?limit=10'
        second_url = self.base_url + '/departures/?limit=10&offset=10'
        responses.add(responses.GET, first_url,
                  json=first_page_data, status=200)
        responses.add(responses.GET, second_url,
                  json=second_page_data, status=200)

        filename = 'test_pagination_output.csv'
        fieldnames = ['Name', 'Start Date', 'Finish Date', 'Category']

        filter_chain = FilterChain()
        date_filter = DateFilter('start_date', operator.ge, date(year=2018, month=6, day=1))
        category_filter = Filter('category', operator.eq, 'Adventurous')
        filter_chain.add_filter(date_filter).add_filter(category_filter)
        fetch_data_from_api_and_create_csv(first_url, filename, fieldnames, filter_chain)

        assert self._compare_csv_file(filename, 'test_pagination_sample.csv') is True

        if os.path.exists(filename):
            os.remove(filename)
