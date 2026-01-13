def get_num_words(text): #Returns the number of words in the text
    return len(text.split())

def count_chars(text): #Returns a dictonary of every unique character in the text as a key, and the number of times they are in the text as a value
    chars = {}
    for char in text:
        lowered = char.lower()
        if lowered in chars:
            chars[lowered] += 1
        else:
            chars[lowered] = 1
    return chars

def sort_dict(text): #Returns the value of the num key of the given dictionary. Used as a sorting kekey
    return text["num"]

def dict_to_list(num_char_dict): #Converts a dictionary into a sorted list
    sorted_list=[] 
    for ch in num_char_dict: #For each character in the original dictionary, it splits the character portion as a value to the char key, and the number portion to a num key
        sorted_list.append({"char": ch, "num": num_char_dict[ch]})
    sorted_list.sort(reverse= True, key=sort_dict)
    return sorted_list