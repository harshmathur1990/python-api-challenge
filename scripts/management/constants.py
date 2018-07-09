import os


base_url = os.getenv('BASE_URL')
fieldnames = os.getenv('FIELDNAMES').split('  ')
filename = os.getenv('FILENAME')
category = os.getenv('CATEGORY')
start_date = {item.split('.')[0]:int(item.split('.')[1]) for item in os.getenv('STARTDATE').split(' ')}