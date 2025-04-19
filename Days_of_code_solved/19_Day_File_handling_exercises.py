import re
from collections import Counter
import math
import csv

#####################################################################################
print('\nExercise number 7:')

'Exercise number 7 // Need to perform validation before attempting to open a file.'

'''Write a python application that checks similarity between two texts. It takes a file or a 
string as a parameter and it will evaluate the similarity of the two texts. For instance check 
the similarity between the transcripts of Michelle's and Melina's speech. You may need a 
couple of functions, function to clean the text(clean_text), function to remove support words(remove_support_words)
and finally to check the similarity(check_text_similarity). List of stop words are in the data directory'''

stop_words = ['i','me','my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up','down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

def cleantext(filename):
    with open(f'./data/{filename}_speech.txt', 'r', encoding='utf-8') as file:
        cleaned = file.read().lower()
        cleaned = re.sub(rf'[^\w\s]', '', cleaned)
        list_of_words = cleaned.split()
        list_cleaned_sw = [word for word in list_of_words if word not in stop_words]
    return list_cleaned_sw

# Function to create frequency vectors
def create_frequency_vector(words, vocabulary):
    word_count = Counter(words)
    return [word_count.get(word, 0) for word in vocabulary]


# Function to calculate cosine similarity
def cosine_similarity_manual(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a ** 2 for a in vec1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def similarity(first_speech,second_speech):
    words1 = cleantext(first_speech)
    words2 = cleantext(second_speech)

    vocabulary = list(set(words1 + words2))

     # Create vectors
    vec1 = create_frequency_vector(words1, vocabulary)
    vec2 = create_frequency_vector(words2, vocabulary)

     # Calculate similarity
    similarity_score = cosine_similarity_manual(vec1, vec2)

    return f"Similarity between '{first_speech}' and '{second_speech}' speeches: {similarity_score:.2f}"


print(similarity('michelle','melina'))

#####################################################################################
print('\nExercise number 8:')

'''Exercise number 8 // Find the 10 most repeated words in the romeo_and_juliet.txt.'''

with open('./data/romeo_and_juliet.txt') as text_book:
    complete_book = text_book.read().lower()
    clean_book = re.sub(r'[^\w\s]','',complete_book)
    list_of_words = clean_book.split()
    list_of_words_cleaned_of_sw = [word for word in list_of_words if word not in stop_words]
    counted_words = Counter(list_of_words_cleaned_of_sw).most_common(10)
print(counted_words)

#####################################################################################
print('\nExercise number 9:')

'''Exercise number 9 // Read the hacker news csv file and find out: 
a) Count the number of lines containing python or Python 
b) Count the number lines containing JavaScript, javascript or Javascript 
c) Count the number lines containing Java and not JavaScript'''

searched_word = ['python','javascript','java']

# Initialize the counters with the keywords as keys
word_counts = {key: 0 for key in searched_word}
java_not_javascript_count = 0



try:
    with open('./data/hacker_news.csv') as hacker_news:
        cvs_reader = csv.reader(hacker_news, delimiter=',')
        for row in cvs_reader:
            line = ' '.join(row) # merge fields and convert to lowercase
            for word in searched_word:
                 if word in line:
                    word_counts[word] += 1
            # Count lines that contain 'java' but NOT 'javascript'
            if 'java' in line and 'javascript' not in line:
                java_not_javascript_count += 1
    
    print(f"a) Lines with 'python' or 'Python': {word_counts['python']}")
    print(f"b) Lines with 'JavaScript', 'javascript', or 'Javascript': {word_counts['javascript']}")
    print(f"c) Lines with 'Java' but not 'JavaScript': {java_not_javascript_count}")
                    
except IOError:
        print("Error opening or reading input file")

        