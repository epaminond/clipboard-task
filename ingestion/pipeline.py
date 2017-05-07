from os.path import join, dirname
import pandas as pd
import numpy as np
from pymongo import MongoClient
import datetime
import re

mongo_url = 'mongodb://localhost:27017/'
mondo_database = 'clipboardinterview'

hours_in_week = 40
hours_in_biweek = hours_in_week * 2
hours_in_month = hours_in_week * 4.35
hours_in_year = hours_in_week * 52.14
valid_hourly_rates = range(7, 200)

"""

Use this file to read in the project nurse data, perform text pre-processing
and store data in mongo. The fields we're interested in storing are:

  'How many years of experience do you have?' -> experience,
  'What's your highest level of education?' -> education,
  'What is your hourly rate ($/hr)?' -> salary,
  'Department' -> department,
  'What (City, State) are you located in?' -> location,
  'What is the Nurse - Patient Ratio?' -> patientNurseRatio

Check server/models/Record.js for an example of the schema.

"""

def main():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['clipboardinterview']
    df = pd.read_csv(join(dirname(__file__), '../data/projectnurse.csv'))

    client = MongoClient(mongo_url)
    db = client[mondo_database]
    db.records.delete_many({})

    valid_departments = open('data/types.txt').read().split('\n')

    for i, row in df.iterrows():
      shift_answer = row["What's Your Shift Length?"]
      shift = extract_number(shift_answer) if type(shift_answer) is str else 8

      nurse = {"salary": parse_hourly_rate(row['What is your hourly rate ($/hr)?'], shift),
               "patientNurseRatio": parse_nurse_patient_ratio(row['What is the Nurse - Patient Ratio?']),
               "department": parse_department(row['Department'], valid_departments),
               "education": row["What's your highest level of education?"],
               "createdAt": datetime.datetime.utcnow()}

      db.records.insert_one(nurse)

def parse_hourly_rate(answer, shift):
    number = extract_number(answer)

    if number is None or len(answer.split(' ')) > 4: return

    if is_number(answer) or is_mentioned(['/h', 'hr', 'hour'], answer):
      hourly_rate = number
    elif is_mentioned(['yr', 'year', 'annual'], answer):
      hourly_rate = number / hours_in_year
    elif is_mentioned(['month'], answer):
      hourly_rate = number / hours_in_month
    elif is_mentioned(['2 weeks', 'biweek', 'bi week'], answer):
      hourly_rate = number / hours_in_biweek
    elif is_mentioned(['week'], answer):
      hourly_rate = number / hours_in_week
    elif is_mentioned(['day', 'diem'], answer):
      hourly_rate = number / shift
    else:
      return None 

    return round(hourly_rate, 2) if hourly_rate in valid_hourly_rates else None

def parse_department(answer, valid_departments):
    if answer in valid_departments: # TODO needs searching by synonims
      return answer
    else:
      return None


def parse_nurse_patient_ratio(answer):
    if type(answer) is not str: return None
    ratios = list(map(calculate_ratio, re.findall(r"(\d+\.?\-?\\?\d*\:?(?:\sto\s)?\d*)", answer)))
    return average(ratios)

def calculate_ratio(phrase):
    if is_number(phrase):
      return float(phrase)

    splitter = ':' if is_mentioned([':'], phrase) else 'to'
    parts = map(normalize_ratio_part, phrase.split(splitter))

    return max(filter_empty(parts))

def normalize_ratio_part(ratio_part):
    if '-' in ratio_part or'/' in ratio_part:
      splitter = '-' if '-' in ratio_part else '/'
      return average(list(map(lambda ratio: to_float_or_none(ratio), ratio_part.split('-'))))
    else:
      return to_float_or_none(ratio_part)

def average(items):
    clean_items = filter_empty(items)
    return round(sum(clean_items) / float(len(clean_items)), 2) if len(clean_items) > 0 else None

def filter_empty(items):
    return list(filter(lambda item: item is not None, items))

def is_number(string):
    clean_string = string.replace(',', '').replace('$', '').replace(' ', '')
    return re.match("^\d+?\.?\d*?$", clean_string)

def to_float_or_none(string):
    return float(string) if is_number(string) else None

def is_mentioned(keywords, phrase):
    return any(word in phrase.lower() for word in keywords)

def extract_number(answer):
    numbers_list = re.findall("(\d+((.|,)\d+)?)", answer)
    if len(numbers_list) > 0:
      return float(numbers_list[0][0].replace(',', ''))

if __name__ == "__main__":
    main()
