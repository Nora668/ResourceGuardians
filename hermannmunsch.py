# Implementation of the Hermann-Munsch algorithm to calculate similarity between two alphanumeric strings.
# Questions? Contact me @carthussandworm on Discord.
import numpy as np
import re

# Big ugly array, using approximate 2-norm values between each alphanumeric key on the keyboard, excluding the numpad.
# Indexes 0-9 represent numberic keys, indexes 10-35 represent alphabetical keys.
difference = np.array([[0, 9, 8, 7, 6, 5, 4, 3, 2, 1, 8, 5, 7, 7, 7, 6, 5, 4, 2, 3, 2, 2, 3, 4, 1, 1, 9, 6, 8, 5, 3, 6, 8, 7, 4, 8],
                       [9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 2, 6, 4, 3, 3, 4, 5, 6, 8, 7, 8, 9, 8, 7, 9, 10, 1, 4, 3, 5, 7, 5, 2, 4, 6, 3],
                       [8, 1, 0, 1, 2, 3, 4, 5, 6, 7, 2, 5, 4, 3, 2, 3, 4, 5, 7, 6, 7, 8, 7, 6, 8, 9, 1, 3, 2, 4, 6, 4, 1, 3, 5, 3],
                       [7, 2, 1, 0, 1, 2, 3, 4, 5, 6, 2, 4, 3, 2, 1, 3, 3, 4, 6, 5, 6, 7, 6, 5, 7, 8, 2, 2, 2, 3, 5, 4, 1, 3, 4, 3],
                       [6, 3, 2, 1, 0, 1, 2, 3, 4, 5, 3, 4, 3, 2, 1, 2, 3, 3, 5, 4, 5, 6, 5, 4, 6, 7, 3, 1, 2, 2, 4, 2, 2, 3, 3, 3],
                       [5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 4, 3, 3, 2, 2, 2, 2, 3, 4, 3, 4, 5, 4, 4, 5, 6, 4, 1, 3, 1, 3, 2, 3, 4, 2, 4],
                       [4, 5, 4, 3, 2, 1, 0, 1, 2, 3, 5, 3, 3, 3, 3, 2, 2, 2, 3, 3, 3, 4, 4, 3, 4, 5, 5, 2, 4, 1, 2, 2, 4, 4, 1, 5],
                       [3, 6, 5, 4, 3, 2, 1, 0, 1, 2, 6, 3, 4, 4, 4, 3, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 6, 3, 5, 2, 1, 3, 5, 5, 1, 6],
                       [2, 7, 6, 5, 4, 3, 2, 1, 0, 1, 7, 3, 5, 5, 5, 4, 3, 2, 1, 2, 2, 3, 3, 3, 2, 3, 7, 4, 6, 3, 1, 3, 6, 6, 2, 6],
                       [1, 8, 7, 6, 5, 4, 3, 2, 1, 0, 8, 4, 6, 6, 6, 5, 4, 3, 1, 2, 2, 2, 3, 3, 1, 2, 8, 5, 7, 4, 2, 4, 7, 7, 3, 7],
                       [8, 2, 2, 2, 3, 4, 5, 6, 7, 8, 0, 5, 3, 2, 2, 3, 4, 5, 7, 6, 7, 8, 7, 6, 8, 9, 1, 3, 1, 4, 6, 4, 1, 2, 5, 1],
                       [5, 6, 5, 4, 4, 3, 3, 3, 3, 4, 5, 0, 2, 3, 3, 2, 1, 1, 1, 2, 3, 4, 2, 1, 4, 5, 5, 3, 4, 2, 2, 1, 4, 3, 2, 4],
                       [7, 4, 4, 3, 3, 3, 3, 4, 5, 6, 3, 2, 0, 1, 2, 1, 2, 3, 5, 4, 5, 6, 4, 3, 6, 7, 3, 2, 2, 2, 4, 1, 3, 1, 3, 2],
                       [7, 3, 3, 2, 2, 2, 3, 4, 5, 6, 2, 3, 1, 0, 1, 1, 2, 3, 5, 4, 5, 6, 5, 4, 6, 7, 3, 1, 1, 2, 4, 2, 2, 1, 3, 2],
                       [7, 3, 2, 1, 1, 2, 3, 4, 5, 6, 2, 3, 2, 1, 0, 2, 3, 3, 5, 4, 5, 6, 5, 4, 6, 7, 2, 1, 1, 2, 4, 3, 1, 2, 3, 2],
                       [6, 4, 3, 3, 2, 2, 2, 3, 4, 5, 3, 2, 1, 1, 2, 0, 1, 2, 4, 3, 4, 5, 4, 3, 5, 6, 4, 1, 2, 1, 3, 1, 3, 2, 2, 3],
                       [5, 5, 4, 3, 3, 2, 2, 2, 3, 4, 4, 1, 2, 2, 3, 1, 0, 1, 3, 2, 3, 4, 3, 2, 4, 5, 4, 2, 3, 1, 2, 1, 3, 3, 1, 4],
                       [4, 6, 5, 4, 3, 3, 2, 2, 2, 3, 5, 1, 3, 3, 3, 2, 1, 0, 2, 1, 2, 3, 2, 1, 3, 4, 5, 3, 4, 2, 1, 2, 4, 4, 1, 5],
                       [2, 8, 7, 6, 5, 4, 3, 2, 1, 1, 7, 1, 5, 5, 5, 4, 3, 2, 0, 1, 1, 2, 2, 2, 1, 2, 7, 4, 6, 3, 1, 4, 6, 6, 2, 7],
                       [3, 7, 6, 5, 4, 3, 3, 2, 2, 2, 6, 2, 4, 4, 4, 3, 2, 1, 1, 0, 1, 2, 1, 1, 2, 3, 6, 3, 5, 3, 1, 3, 5, 5, 2, 6],
                       [2, 8, 7, 6, 5, 4, 3, 3, 2, 2, 7, 3, 5, 5, 5, 4, 3, 2, 1, 1, 0, 1, 1, 2, 1, 2, 7, 4, 6, 3, 2, 4, 6, 6, 3, 7],
                       [2, 9, 8, 7, 6, 5, 4, 3, 3, 2, 8, 4, 6, 6, 6, 5, 4, 3, 2, 2, 1, 0, 2, 3, 1, 1, 8, 5, 7, 4, 3, 5, 7, 7, 3, 8],
                       [3, 8, 7, 6, 5, 4, 4, 3, 3, 3, 7, 2, 4, 5, 5, 4, 3, 2, 2, 1, 1, 2, 0, 1, 2, 3, 7, 4, 6, 3, 2, 3, 6, 5, 3, 6],
                       [4, 7, 6, 5, 4, 4, 3, 3, 3, 3, 6, 1, 3, 4, 4, 3, 2, 1, 2, 1, 2, 3, 1, 0, 3, 4, 6, 3, 5, 3, 2, 2, 5, 4, 2, 5],
                       [1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 8, 4, 6, 6, 6, 5, 4, 3, 1, 2, 1, 1, 2, 3, 0, 1, 8, 5, 7, 4, 2, 5, 7, 7, 3, 8],
                       [1, 10, 9, 8, 7, 6, 5, 4, 3, 2, 9, 5, 7, 7, 7, 6, 5, 4, 2, 3, 2, 1, 3, 4, 1, 0, 9, 6, 8, 5, 3, 6, 8, 8, 4, 9],
                       [9, 1, 1, 2, 3, 4, 5, 6, 7, 8, 1, 5, 3, 3, 2, 4, 4, 5, 7, 6, 7, 8, 7, 6, 8, 9, 0, 3, 2, 4, 6, 4, 1, 3, 5, 2],
                       [6, 4, 3, 2, 1, 1, 2, 3, 4, 5, 3, 3, 2, 1, 1, 1, 2, 3, 4, 3, 4, 5, 4, 3, 5, 6, 3, 0, 2, 1, 3, 2, 2, 3, 2, 4],
                       [8, 3, 2, 2, 2, 3, 4, 5, 6, 7, 1, 4, 2, 1, 1, 2, 3, 4, 6, 5, 6, 7, 6, 5, 7, 8, 2, 2, 0, 3, 5, 3, 1, 1, 4, 1],
                       [5, 5, 4, 3, 2, 1, 1, 2, 3, 4, 4, 2, 2, 2, 2, 1, 1, 2, 3, 3, 3, 4, 3, 3, 4, 5, 4, 1, 3, 0, 2, 2, 3, 3, 1, 4],
                       [3, 7, 6, 5, 4, 3, 2, 1, 1, 2, 6, 2, 4, 4, 4, 3, 2, 1, 1, 1, 2, 3, 2, 2, 2, 3, 6, 3, 5, 2, 0, 3, 5, 5, 1, 6],
                       [6, 5, 4, 4, 2, 2, 2, 3, 3, 4, 4, 1, 1, 2, 3, 1, 1, 2, 4, 3, 4, 5, 3, 2, 5, 6, 4, 2, 3, 2, 3, 0, 4, 2, 3, 3],
                       [8, 2, 1, 1, 2, 3, 4, 5, 6, 7, 1, 4, 3, 2, 1, 3, 3, 4, 6, 5, 6, 7, 6, 5, 7, 8, 1, 2, 1, 3, 5, 4, 0, 2, 4, 2],
                       [7, 4, 3, 3, 3, 4, 4, 5, 6, 7, 2, 3, 1, 1, 2, 2, 3, 4, 6, 5, 6, 7, 5, 4, 7, 8, 3, 3, 1, 3, 5, 2, 2, 0, 4, 1],
                       [4, 6, 5, 4, 3, 2, 1, 1, 2, 3, 5, 2, 3, 3, 3, 2, 1, 1, 2, 2, 3, 3, 3, 2, 3, 4, 5, 2, 4, 1, 1, 3, 4, 4, 0, 5],
                       [8, 3, 3, 3, 3, 4, 5, 6, 6, 7, 1, 4, 2, 2, 2, 3, 4, 5, 7, 6, 7, 8, 6, 5, 8, 9, 2, 4, 1, 4, 6, 3, 2, 1, 5, 0]])

# The function takes three parameters: a string representing the input, a list of known strings that the first one could represent,
# and a cost representing how severe the gap penalty should be.
def hermannMunsch(inputStr, comparedStrs, gapCost):

    # Removes all non-alphanumeric characters from the string, and sets all alphabetic characters to lowercase.
    pattern = re.compile('\W')
    inputAN = re.sub(pattern, '', inputStr)
    inputAN = inputAN.lower()

    # Take the length of the input string and the number of strings to be compared.
    inputLen = len(inputAN)
    numStrs = len(comparedStrs)

    # Create an array to hold the final comparison values.
    values = np.zeros((numStrs, 1))

    # Iterate through each of the strings in the list of strings to be compared
    i = 0
    for compStr in comparedStrs:

        # Remove non-alphanumeric characters and set to lowercase.
        strAN = re.sub(pattern, '', compStr)
        strAN = strAN.lower()
        strLen = len(strAN)

        # Create the dynamic programming table.
        table = np.zeros((inputLen + 1, strLen + 1))

        # Fill out the origin row and column with the gap penalty.
        j = 0
        while j < max(inputLen, strLen):
            if j < inputLen:
                table[j, 0] = j * gapCost * -1
            if j < strLen:
                table[0, j] = j * gapCost * -1
            j += 1

        # Iterate over the remaining values in the table.
        k = 1
        while k < inputLen + 1:
            l = 1
            while l < strLen + 1:

                # Access the previous values in the strings.
                prevK = k - 1
                prevL = l - 1

                # Get the unicode value of the characters in the string.
                origVal = ord(inputAN[prevK])
                compVal = ord(strAN[prevL])

                # Should the character be alphabetic, reduce the value so that the gap is seamless.
                if origVal > 9:
                    origVal -= 87
                if compVal > 9:
                    compVal -= 87
                
                # Access the character in the difference table, and set the value in the dynamic programming table to be equal to the best transition outcome.
                transitionCost = difference[origVal, compVal]
                table[k, l] = max((table[prevK, l] - gapCost), (table[k, prevL] - gapCost), (table[prevK, prevL] - transitionCost))
                l += 1
            k += 1
        # Uncomment the line below to see each iteration of the dynamic programming table.
        # print(table)
        # Enter the final value in the table to the values list.
        values[i] = table[inputLen, strLen]
        i += 1

    # Set the target value to be the least negative value, then find its location in the values array.
    target = max(values)
    m = 0
    while m < len(values):
        if values[m] == target:
            break
        m += 1
    
    # Return that value in the original list of strings.
    return comparedStrs[m]

# A simple example using protein chains. The difference array is designed with a gap penalty of 10 in mind.
print(hermannMunsch('Dober', ['Dover', 'Newark', 'Wilmington'], 10))