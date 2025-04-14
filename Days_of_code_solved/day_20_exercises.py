import requests
import re
from collections import Counter
import statistics
from bs4 import BeautifulSoup

stop_words = ['i','me','my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up','down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

##########################################################################################
print('\nExercise number 1:')

''' Exercise number 1 //
Read this url and find the 10 most frequent words. 
romeo_and_juliet = 'http://www.gutenberg.org/files/1112/1112.txt (The link dont work)
I replaced it with 'https://www.gutenberg.org/files/1112/1112-0.txt (the same, but new)' '''

url1 = 'https://www.gutenberg.org/files/1112/1112-0.txt'

def the_most_frequent_words(text):
    clean_text = re.sub(r'[^\w\s]','',text)
    list_of_words = clean_text.split() #Create a List of words in text
    list_of_words_cleaned_of_sw =  [word for word in list_of_words if word not in stop_words]
    counted_words = Counter(list_of_words).most_common(10)
    counted_cleaned_words = Counter(list_of_words_cleaned_of_sw).most_common(10)
    
    print(f'the 10 most common word in all the book are:\n{counted_words}')
    print(f'the 10 most common word take ot the stop words all the book are:\n{counted_cleaned_words}')

try:
    response = requests.get(url1)
    response.raise_for_status()  # Throws an error if the status code is not 200 (OK)
    print("Request was successful!")
    book = response.text  # store all the text
    the_most_frequent_words(book.lower())

except requests.exceptions.RequestException as e:
    print(f"Error al obtener los datos: {e}")


#######################################################################
print('\nExercise number 2')

''' Exercise number 2 //
Read the cats API and cats_api = 'https://api.thecatapi.com/v1/breeds' and find :
i.   the min, max, mean, median, standard deviation of cats' weight in metric units.
ii.  the min, max, mean, median, standard deviation of cats' lifespan in years.
iii. Create a frequency table of country and breed of cats '''

url2 = 'https://api.thecatapi.com/v1/breeds'



def frequency_table_operations(data):
    frequency_table = {}
    for breed in data:
        origin = breed.get('origin', 'Unknown')  # Extrae el país de origen
        if origin in frequency_table:
            frequency_table[origin] += 1
        else:
            frequency_table[origin] = 1
    return frequency_table

def clear_data(data, required_data): 
    numbers_data = []

    # Gets a list of weights in the format ['3 - 6', 'x - y'] and transform [3.0, 6.0, x, y]
    if required_data == 'weight': 
        obtained_data = [cat['weight']['metric'] for cat in data] # this is the weight data
    elif required_data == 'lifespan':
        obtained_data = [cat['life_span'] for cat in data] #this is the life data
    else:
        print('Argument not correct')
        return []

    for range_str in obtained_data:
        if isinstance(range_str, str):  # Extra safety
            # Split on any dash with optional spaces
            parts = re.split(r'\s*[-–—]\s*', range_str)
            for part in parts:
                try:
                    number = float(part.strip())
                    numbers_data.append(number)
                except:
                    print(f'Could not convert: {part}')
        else:
            print(f"Invalid entry: {range_str}")
            return []
    return numbers_data

def calc_result(list_numbers): # this function calculates the min, max, mean, median, standard deviation.
    min_result = int(min(list_numbers))
    max_result = int(max(list_numbers))
    mean_result = round(statistics.mean(list_numbers), 2)
    median_result = int(statistics.median(list_numbers))
    standar_desviation = round(statistics.stdev(list_numbers), 2)
    result = {
        'min': min_result,
        'max': max_result,
        'mean': mean_result,
        'median': median_result,
        'std_desv': standar_desviation
    }
    return result

try:
    response = requests.get(url2)
    response.raise_for_status()  # Throws an error if the status code is not 200 (OK)
    print("Request was successful!")
    breeds = response.json()

    # We save the returned results
    weight_data = clear_data(breeds, 'weight')
    lifespan_data = clear_data(breeds, 'lifespan')
    frequency_data = frequency_table_operations(breeds)

    weight_stats = calc_result(weight_data)
    lifespan_stats = calc_result(lifespan_data)

    # print result
    print("\n📊 Frequency table by origin:")
    for origin, count in frequency_data.items():
        print(f"{origin}: {count}")

    print("\n📈 Weight Statistics:")
    for key, value in weight_stats.items():
        print(f"{key.capitalize()}: {value}")

    print("\n📈 Lifespan Statistics:")
    for key, value in lifespan_stats.items():
        print(f"{key.capitalize()}: {value}")

except requests.exceptions.RequestException as e:
    print(f"Error al obtener los datos: {e}")


#######################################################################
print('\nExercise number 3')

''' Exercise number 3 //
Read the countries API and find
i.   the 10 largest countries.
ii.  the 10 most spoken languages.
iii. the total number of languages in the countries API.'''

url3 = 'https://restcountries.com/v3.1/all'

def the_ten_largest_country(countries_data):
    # We create a list of tuples (name, area)
    list_countries_area = [(country['name']['common'], country.get('area',0)) for country in countries_data]
    sorted_list = sorted(list_countries_area, key=lambda x: x[1] , reverse = True)
    return sorted_list[:10]

    # We get a list of all the languages ​​and then count how many times it is repeated.
def languages_operations(countries_data):
    language_counter = Counter(lang for country in countries_data for lang in country.get('languages', {}).values())
    most_common_languages = language_counter.most_common(10)
    amount_languages = len(language_counter)
    return most_common_languages, amount_languages


try:
    response = requests.get(url3)
    response.raise_for_status()
    print("Request was successful!")
    countries = response.json()
    
    
    # We save the returned results
    largest_countries =  the_ten_largest_country(countries)
    most_spoken , total_languages = languages_operations(countries)
  

    # print result
    print("\n📊 The 10 most largest countries:")
    for country, area in largest_countries:
      print(f"{country}: {area} km²")

    print("\n🗣️ The 10 most spoken languages:")
    for language, count in most_spoken:
       print(f"{language}: {count} countries")

    print(f'\nthe number of languages are: {total_languages}')

except requests.exceptions.RequestException as e:
    print(f"Error al obtener los datos: {e}")

#######################################################################

''' Exercise number 4 //
UCI is one of the most common places to get data sets for data science and machine learning. 
Read the content of UCL (https://archive.ics.uci.edu/ml/datasets.php). 
Without additional libraries it will be difficult, so you may try it with BeautifulSoup4'''

#I don't understand the last exercise because the link is broken.