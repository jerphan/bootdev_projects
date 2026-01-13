from stats import get_num_words, count_chars, dict_to_list
import sys

def get_book_text(path): #Opens and closes a file to return the contents of the file
    with open(path) as f:
        return f.read()

def main():
    if not(len(sys.argv)==2):
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)
    file_path=sys.argv[1]
    text=get_book_text(file_path)
    num_words=get_num_words(text)
    char_dict=count_chars(text)
    sorted_list= dict_to_list(char_dict)
    print_report(file_path, num_words, sorted_list)
    

def print_report(file_path, num_words, sorted_list): #Prints a report of how many total words there are, and what characters are most common to least common
    print(f"============ BOOKBOT ============\nAnalyzing book found at {file_path}...\n----------- Word Count ----------\nFound {num_words} total words")
    for item in sorted_list:
        if not(item["char"].isalpha()):
            continue
        print(f"{item["char"]}: {item["num"]}")
    print("============= END ===============")

main()
    
