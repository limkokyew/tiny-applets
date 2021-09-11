# -*- coding: utf-8 -*-
import codecs
import random

STATUS_MAP = {
    "AWAITING_CHAPTER_QUESTION": 0,
    "AWAITING_CONTENT": 1
}

CHAPTER_DELIMITER = "====================================================================================================================\r\n"
QUESTION_DELIMITER = "--------------------------------------------------------------------------------------------------------------------\r\n"

def questionnaire(file_name):
    lines = None
    content = {}
    
    status = STATUS_MAP["AWAITING_CHAPTER_QUESTION"]
    cached_content = []
    current_chapter = ""
    current_question = ""
    current_content = ""
    
    with codecs.open(file_name, "r", "utf-8") as f:
        lines = f.readlines()
    
    lines = "".join(lines)
    
    while lines != "":
        if status == STATUS_MAP["AWAITING_CHAPTER_QUESTION"]:
            if current_chapter == "":
                s = lines.partition(CHAPTER_DELIMITER)
                current_chapter = s[0][:-2]
                content[current_chapter] = {}
                lines = s[2]
            else:
                s = lines.partition(QUESTION_DELIMITER)
                current_question = s[0][:-2]
                lines = s[2]
                status = STATUS_MAP["AWAITING_CONTENT"]
        else:
            s = lines.partition(QUESTION_DELIMITER)
            if CHAPTER_DELIMITER in s[0]:
                next_chapter = s[0][:s[0].index(CHAPTER_DELIMITER)]
                next_chapter = next_chapter[::-1]
                next_chapter = next_chapter[2:]
                next_chapter = next_chapter.partition("\n\r")[0][::-1]
                
                next_question = s[0][::-1]
                next_question = next_question[2:]
                next_question = next_question.partition("\n\r")[0][::-1]
                
                remaining_content = s[0][:s[0].index(next_chapter)]
                content[current_chapter][current_question] = remaining_content
                
                current_chapter = next_chapter[:]
                current_question = next_question[:]
                content[current_chapter] = {}
                
                lines = s[2]
            else:
                next_question = s[0][::-1]
                next_question = next_question[2:]
                next_question = next_question.partition("\n\r")[0][::-1]
                
                content[current_chapter][current_question] = s[0][:s[0].index(next_question)]
                current_question = next_question[:]
                
                lines = s[2]
    
    # Question!
    chapters = list(content.keys())
    shuffle = True
    
    while True:
        print("\nCurrent chapters:\n")
        for chapter in chapters:
            print(chapter)
        print("Please type 'fin' if ready or the title of a chapter to remove it.")
        if shuffle:
            print("Additionally, type 'sequential' to disable randomization of both chapters and questions.")
        user_input = input()
        if user_input == "fin":
            break
        elif shuffle and user_input == "sequential":
            shuffle = False
        else:
            try:
                user_input = int(user_input)
                del chapters[user_input]
            except Exception:
                print("Something went wrong.")
                # if user_input in chapters:
                    # chapters.remove(user_input)
    
    if shuffle:
        random.shuffle(chapters)
    
    for chapter in chapters:
        questions = list(content[chapter].keys())
        # random.shuffle(questions)
        while questions:
            question = ""
            if shuffle:
                question = random.choice(questions)
            else:
                question = questions[0]
        
            print("\nCHAPTER:", chapter)
            print("QUESTION:", question)
            
            print("Input answer (enter 'fin' to complete answer):\n")
            while True:
                user_input = input()
                if user_input == "fin":
                    break
            
            print("----------\nThe answer as listed in your notes:\n----------\n")
            print(content[chapter][question], end="\n\n")
            
            print("Is your answer sufficient? (y/n)")
            user_input = input()
            
            while not (user_input == "y" or user_input == "n"):
                print("Please enter 'y' or 'n'.")
                user_input = input()
    
            if user_input == "y":
                questions.remove(question)
    

if __name__ == "__main__":
    questionnaire("Zusammenfassung.txt")
