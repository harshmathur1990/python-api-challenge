# Generated by Django 2.0.2 on 2018-07-06 12:34

import ijson.backends.yajl2_cffi as ijson
from django.db import migrations


def insert_from_json(apps, schema_editor):

    Departure = apps.get_model('departures', 'Departure')

    f = open('departures.json', 'rb')
    parser = ijson.parse(f)

    count = 0
    departure_obj_list = list()

    for prefix, event, value in parser:
        if event == 'start_map':
            _departure_obj = Departure()
        elif prefix.endswith('name'):
            _departure_obj.name = value
        elif prefix.endswith('start_date'):
            _departure_obj.start_date = value
        elif prefix.endswith('finish_date'):
            _departure_obj.finish_date = value
        elif prefix.endswith('category'):
            _departure_obj.category = value
        elif event == 'end_map':
            departure_obj_list.append(_departure_obj)
            count += 1
            if count == 50:
                Departure.objects.bulk_create(departure_obj_list)
                departure_obj_list = list()
                count = 0

    if departure_obj_list:
        Departure.objects.bulk_create(departure_obj_list)

class Migration(migrations.Migration):

    dependencies = [
        ('departures', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_from_json),
    ]
