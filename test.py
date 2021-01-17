# program randomly generates a number and prompts the user to guess the number until they guess correctly

import random # import random module
print('Choose a range to pick a number from.')

# while loop for user to input an integer for the upper and lower range
while True: 
    try:
        first_value = int(input('Enter the first value: '))  
        second_value = int(input('Enter the second value: '))
        break
    except: # throw an exception if user input is not an integer
        print('Input needs to be an integer.')

# identifying and defining upper and lower range using the given 2 integer inputs
if first_value > second_value:
    lower_range = second_value
    upper_range = first_value
else:
    lower_range = first_value
    upper_range = second_value

# randomly generated number
answer = random.randint(lower_range, upper_range)
guess = None

# while loop for user to input correct number
while guess != answer:
    try:
        guess = int(input('Guess a number between ' + str(lower_range) + ' and ' + str(upper_range) + ': '))
        if guess > answer:
            print('Incorrect. The number is lower')
        elif guess < answer:
            print('Incorrect. The number is higher')
    except: # throw exception if user guess input is not an integer
        print('Error. Only integers are allowed')

print('Congratulations! You guessed the number!')