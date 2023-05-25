import string


### DO NOT MODIFY THIS FUNCTION ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list


### DO NOT MODIFY THIS FUNCTION ###
def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### DO NOT MODIFY THIS FUNCTION ###
def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


WORDLIST_FILENAME = 'words.txt'


class Message(object):
    ### DO NOT MODIFY THIS METHOD ###
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    ### DO NOT MODIFY THIS METHOD ###
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        # Create two variable to store a list of lower alphabet keys and lower shifted values.
        lower_keys = list(string.ascii_lowercase)
        lower_shifted = list(string.ascii_lowercase)

        # Create two variable to store a list of upper alphabet keys and upper shifted values.
        upper_keys = list(string.ascii_uppercase)
        upper_shifted = list(string.ascii_uppercase)

        # Create variable that store list of lower_keys and upper_keys
        keys = lower_keys + upper_keys

        # Find shifted values of lower alphabet
        lower_shifted = lower_shifted[shift:] + lower_shifted[:shift]

        # Find shifted values of lower alphabet
        upper_shifted = upper_shifted[shift:] + upper_shifted[:shift]

        # Create variable that store list of lower_shifted and upper_shifted
        shifted_values = lower_shifted + upper_shifted

        # Create a dictionary mapping a letter (string) to another letter (string).
        self.mapping_dict = dict(zip(keys, shifted_values))

        return self.mapping_dict







    def apply_shift(self, shift):
        '''
            Applies the Caesar Cipher to self.message_text with the input shift.
            Creates a new string that is self.message_text shifted down the
            alphabet by some number of characters determined by the input shift

            shift (integer): the shift with which to encrypt the message.
            0 <= shift < 26

            Returns: the message text (string) in which every character is shifted
                 down the alphabet by the input shift
            '''
        self.encrypted_text = ""
        mapping_dict = self.build_shift_dict(shift)
        for letter in self.message_text:
            if letter not in mapping_dict:
                self.encrypted_text += letter
            else:
                self.encrypted_text += mapping_dict[letter]
        return self.encrypted_text



class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        Hint: consider using the parent class constructor so less 
        code is repeated
        '''
        super().__init__(text)
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encrypting_dict(self):
        '''
        Used to safely access a copy self.encrypting_dict outside of the class
        
        Returns: a COPY of self.encrypting_dict
        '''
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        while 0 > self.shift >= 26:
            if self.shift >= 26:
                self.shift -= 26
            else:
                self.shift += 26
        self.encrypting_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)
        self.valid_words = load_words(WORDLIST_FILENAME)
    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create 
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        max_word_count = 0
        best_shift_value = 0
        for shift in range(26):
            word_count = 0
            for word in list(self.apply_shift(shift).split(" ")):
                if is_word(self.valid_words, word):
                    word_count += 1
            if word_count > max_word_count:
                best_shift_value = shift
                max_word_count = word_count
        return (best_shift_value, self.apply_shift(best_shift_value))


if __name__ == '__main__':
    s = get_story_string()
    ciphertext = CiphertextMessage(s)
    print(ciphertext.decrypt_message())

# Example test case (PlaintextMessage)
plaintext = PlaintextMessage('hello', 2)
print('Expected Output: jgnnq')
print('Actual Output:', plaintext.get_message_text_encrypted())

"""print("___________________________________________________")
print("Test 1")
encrypted1 = Message("hello")
print(encrypted1.build_shift_dict(2))
print(encrypted1.apply_shift(2))
print("___________________________________________________")"""


# Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('jgnnq, yqtnf!')
print('Expected Output:', (24, 'hello, world!'))
print('Actual Output:', ciphertext.decrypt_message())
