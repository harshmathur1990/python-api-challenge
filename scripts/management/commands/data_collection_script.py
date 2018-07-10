
import traceback
import operator
import sys

from datetime import date

import os
from django.core.management.base import BaseCommand
from django.conf import settings

from scripts.management.constants import fieldnames, filename, category, base_url, start_date
from utilities.filters import FilterChain, Filter, DateFilter
from utilities.utils import get_call, processor, change_dict_keys_to_title_case, dump_data_to_csv


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
            date_filter = DateFilter(
                'start_date',
                operator.ge,
                date(
                    year=start_date.get('year'),
                    month=start_date.get('month'),
                    day=start_date.get('day')
                )
            )
            category_filter = Filter('category', operator.eq, category)
            filter_chain.add_filter(date_filter).add_filter(category_filter)
            fetch_data_from_api_and_create_csv(url, filename, fieldnames, filter_chain)
        except Exception as e:
            err = traceback.format_exc()
            sys.stderr.write(err)
            sys.exit(1)
