import random

# Your secret word
secretWord = "tere"
secretWordLength = len(secretWord)

# Initialize a dictionary to count the occurrences of each letter
letter_counts = {}

# Initialize a list to store the guessed letters
guessed_letters = []

# Open the text file for reading
with open("lemmad.txt", "r") as file:
    # Read each line (word) from the file and filter words that have the same length as secretWord
    for line in file:
        word = line.strip()  # Remove leading/trailing whitespace and newline characters
        if len(word) == secretWordLength:
            # Count the occurrences of each letter in the word
            for letter in word:
                letter_counts[letter] = letter_counts.get(letter, 0) + 1

# Sort the letters by count in descending order
sorted_letters = sorted(letter_counts, key=lambda x: letter_counts[x], reverse=True)

# Initialize a list to store words matching the revealed characters
matching_words = []

# Main game loop
while True:
    # Check if there are any remaining letters to guess
    if not sorted_letters:
        print("No more letters to guess. You win!")
        break
    
    # Get the next most common letter to guess
    next_letter = sorted_letters.pop(0)
    
    # Check if the letter has not been guessed before
    if next_letter not in guessed_letters:
        guessed_letters.append(next_letter)
        
        # Check if the guessed letter is in the secret word
        if next_letter in secretWord:
            print(f"The letter '{next_letter}' is in the secret word.")
            
            # Update the secret word with the revealed letter(s)
            secretWord = ''.join([c if c in guessed_letters else '_' for c in secretWord])
            print(f"Current state of the secret word: {secretWord}")
            break
        
        # Find words that match the revealed characters
        matching_words = [word for word in matching_words if all(letter in guessed_letters or letter == '_' for letter in word)]
        matching_words = [word for word in matching_words if len(word) == secretWordLength]
        
        # Print matching words
        print(f"Matching words: {', '.join(matching_words)}")

    else:
        print(f"The letter '{next_letter}' is not in the secret word.")

# End of the game
