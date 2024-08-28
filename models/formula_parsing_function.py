import pandas as pd
import os
import regex as re
import numpy as np

# Important patterns
usd_pattern = re.compile(r'\b(?:usd|usdollar|usdollars|\$)\b')
eur_pattern = re.compile(r'\b(?:eur|euro|euros|\€)\b')
perc_pattern = re.compile(r'(?:%|\bpercent\b)')
plus_pattern = re.compile(r'\s(?:\+|plus)\s')
minus_pattern = re.compile(r'\s(?:\-|minus)\s')
mul_pattern = re.compile(r'\s(?:\*|x|times)\s')
div_pattern = re.compile(r'\s(?:\/|divided by)\s')
currency_per_mt_pattern = re.compile(r'\b(?:usd\/mt|usd per mt|usdollar per mt|usdollars per mt|eur\/mt|eur per mt|euro per mt|euros per mt)\b')
index_pattern = re.compile(r'\b(?:lme|london metal exchange|bdsv)\b')
# Find all constant values indluding with thousands or decimal separator
constant_pattern = re.compile(r'\b(?:\d{1,3}(?:,\d{3})*(?:\.\d+)*|\d+\.\d*)\b')
unit_pattern = re.compile(r'\b(?:mt|metric ton|metric tons|ton|tons|kg|kilogram|kilograms \
                          |lb|pound|pounds|oz|ounce|ounces|g|gram|grams|mg|milligram|milligrams \
                          |t|metric tonne|metric tonnes|tonne|tonnes)\b')


def detect_currency(text):
    if usd_pattern.search(text):
        return 'usd'
    elif eur_pattern.search(text):
        return 'eur'
    else:
        return None
    
def detect_operator(text):
    if plus_pattern.search(text):
        return 'addition'
    elif minus_pattern.search(text):
        return 'subtraction'
    elif mul_pattern.search(text):
        return 'multiplication'
    elif div_pattern.search(text):
        return 'division'
    elif perc_pattern.search(text):
        return 'percentage'
    else:
        return None

def detect_index(text):
    if index_pattern.search(text):
        return index_pattern.search(text).group(0)
    else:
        return None

def detect_constant(text):
    if constant_pattern.search(text):
        return constant_pattern.search(text).group(0)
    else:
        return None
    
def detect_unit(text):
    if unit_pattern.search(text):
        return unit_pattern.search(text).group(0)
    else:
        return None

def convert_constant(number_str):
    """This function converts the string constant to numeric.
    Because this is used in several geographies without any structure, the values can be written in many different ways
    with different thousands and decimal separators. This function tries to convert them to float
    """
    if number_str is None:
        return float('nan')
    else:
        try:
            if ',' in number_str and '.' in number_str:
                comma_pos = number_str.rfind(',')
                dot_pos = number_str.rfind('.')
                if comma_pos < dot_pos:
                    # Comma as thousand separator
                    number_str = number_str.replace(',', '')
                else:
                    # Comma as decimal separator
                    number_str = number_str.replace('.', '').replace(',', '.')
            elif ',' in number_str:
                if number_str.count(',') > 1:
                    # Comma as thousand separator
                    number_str = number_str.replace(',', '')
                # Check if there are more than three digits after the comma
                elif len(number_str[number_str.rfind(',')+1:]) > 2:
                    # Comma as thousand separator
                    number_str = number_str.replace(',', '')
                else:
                    # Comma as decimal separator
                    number_str = number_str.replace(',', '.')
            elif '.' in number_str:
                if number_str.count('.') > 1:
                    # Dot as thousand separator
                    number_str = number_str.replace('.', '')
                # Check if there are more than three digits after the dot
                elif len(number_str[number_str.rfind('.')+1:]) > 2:
                    # Dot as thousand separator
                    number_str = number_str.replace('.', '')
                else:
                # Dot as decimal separator
                    pass
            return float(number_str)
        except ValueError:
            return float('nan')
