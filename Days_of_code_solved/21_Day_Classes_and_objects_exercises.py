from collections import Counter
import math
#####################################################################################
print('\nExercise number 1:')

'''Exercise number 1 // Python has the module called statistics and we can use 
this module to do all the statistical calculations. However, to learn how to make 
function and reuse function let us try to develop a program, which calculates 
the measure of central tendency of a sample (mean, median, mode) and measure of variability 
(range, variance, standard deviation). 
In addition to those measures, find the min, max, count, percentile, and frequency distribution of the sample. 
You can create a class called Statistics and create all the functions 
that do statistical calculations as methods for the Statistics class. Check the output below.'''

class Statisticsnew:
    def __init__(self, data):
        self.data = sorted(data)
    
    def count(self):
        return len(self.data)

    def sum(self):
        return sum(self.data)
    
    def minimum(self):
        return min(self.data)
    
    def maximum(self):
        return max(self.data)
    
    def range(self):
        return self.maximum() - self.minimum()
    
    def mean(self):
        return self.sum() / (self.count())
    
    def median(self):
        n = self.count()
        mid = n // 2
        if n % 2 == 0:
            return (self.data[mid - 1] + self.data[mid]) / 2
        else:
            return self.data[mid]
    
    def mode(self):
        counts = Counter(self.data)  # Count the frequency of each number
        max_count = max(counts.values())  # Find the highest frequency
        mode_values = [k for k, v in counts.items() if v == max_count]  # Find all values ​​with that frequency

        # If there is only one mode, we return it as a number, if there are several, as a list
        return {
            'mode': mode_values if len(mode_values) > 1 else mode_values[0],
            'count': max_count
        }
    
    def std(self):
        return round(math.sqrt(self.var()), 1)
    
    def var(self):
        mean_val = self.mean()
        return round(sum((x - mean_val) ** 2 for x in self.data) / self.count(), 1)

    def freq_dist(self):
        freq = Counter(self.data)
        return dict(sorted(freq.items()))  # Sorted by number
        

    def describe(self):
        print('Count:', data.count()) # 25
        print('Sum: ', data.sum()) # 744
        print('Min: ', data.minimum()) # 24
        print('Max: ', data.maximum()) # 38
        print('Range: ', data.range()) # 14
        print('Mean: ', data.mean()) # 29.76
        print('Median: ', data.median()) # 29
        print('Mode: ', data.mode()) # {'mode': 26, 'count': 5}
        print('Standard Deviation: ', data.std()) # 4.2
        print('Variance: ', data.var()) # 17.5
        print('Frequency Distribution: ', data.freq_dist()) # [(20.0, 26), (16.0, 27), (12.0, 32), (8.0, 37), (8.0, 34), (8.0, 33), (8.0, 31), (8.0, 24), (4.0, 38), (4.0, 29), (4.0, 25)]
    
ages = [31, 26, 34, 37, 27, 26, 32, 32, 26, 27, 27, 24, 32, 33, 27, 25, 26, 38, 37, 31, 34, 24, 33, 29, 26]
                
data = Statisticsnew(ages)
data.describe()

#####################################################################################
print('\nExercise number 2:')

'''Exercise number 2 // Create a class called PersonAccount. 
It has firstname, lastname, incomes, expenses properties and it has 
total_income, total_expense, account_info, add_income, add_expense and account_balance methods.
Incomes is a set of incomes and its description. The same goes for expenses.'''

class PersonAccount:
    def __init__(self, firstname, lastname, incomes= 0, expenses = 0):
        self.firstname = firstname
        self.lastname = lastname
        self.incomes = incomes
        self.expenses = expenses
        print(f'\n[{firstname},{lastname},{incomes},{expenses}]')

    def add_income(self, amount):
        self.incomes += amount
        print(f'New income of:{amount}\nthe new total income are: {self.incomes}')

    def add_expenses(self, amount):
        self.expenses += amount
        print(f'New expense of:{amount}\nthe new total expense are: {self.expenses}')

    def total_incomes(self):
        print(f'the total incomes are:{self.incomes}')
        
    def total_expenses(self):
        print(f'the total expenses are:{self.expenses}')

    def account_info(self):
        print(f'''\n👤 Account Info:
Name: {self.firstname} {self.lastname}
Total Income: ${self.incomes}
Total Expense: ${self.expenses}
Balance: ${self.account_balance()}
''')

    def account_balance(self):
        balance = self.incomes - self.expenses
        return balance


#test the methods
#person1
person1 = PersonAccount('Kevin', 'Alonso', 1200, 700)
person1.add_income(400)
person1.add_expenses(100)
person1.total_incomes()
person1.total_expenses()
person1.account_info()
person1.account_balance()

#person2
person2 = PersonAccount('Elma', 'Rino', 800, 520)
person2.add_income(200)
person2.add_expenses(100)
person2.total_incomes()
person2.total_expenses()
person2.account_info()
person2.account_balance()
