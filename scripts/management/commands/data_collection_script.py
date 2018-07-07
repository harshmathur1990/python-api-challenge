
import traceback
import operator
import sys

from datetime import date
from django.core.management.base import BaseCommand

from utilities.filters import FilterChain, Filter, DateFilter
from utilities.utils import get_call, processor, change_dict_keys_to_title_case, dump_data_to_csv

base_url = 'http://127.0.0.1:8000'


def fetch_data_from_api_and_create_csv(url, filename, fieldnames, filter_chain=None):
    next = True
    while next:
        data = get_call(url, processor)
        results = data.get('results')
        if filter_chain:
            results = filter_chain.filter(results)
        filtered_data_with_keys_in_title_case = change_dict_keys_to_title_case(results)
        dump_data_to_csv(filename, filtered_data_with_keys_in_title_case, fieldnames)
        sys.stdout.write('Successfully Wrote data for the page {}\n'.format(url))
        if data.get('next'):
            next = True
            url = data.get('next')
            continue
        next = False


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = base_url + '/departures'
        try:
            filter_chain = FilterChain()
            date_filter = DateFilter('start_date', operator.ge, date(year=2018, month=6, day=1))
            category_filter = Filter('category', operator.eq, 'Adventurous')
            filter_chain.add_filter(date_filter).add_filter(category_filter)
            fieldnames = ['Name', 'Start Date', 'Finish Date', 'Category']
            fetch_data_from_api_and_create_csv(url, 'adventurous_data.csv', fieldnames, filter_chain)
        except Exception as e:
            err = traceback.format_exc()
            sys.stderr.write(err)
