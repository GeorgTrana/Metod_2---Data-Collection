#__extracting_data.py__
import pdfplumber
import os
from readability import Readability
import pandas as pd
'''
'''

l_folders = [
    'pre_cov',
    'dur_cov',
    'aft_cov',
    ]

kw1 = ["Abstract", "ABSTRACT"] # Same length, it works
kw2 = ["Keywords:", ["Key Words:", "Key words:"]] #Diff lengths, will have to do some magic later. 

'''
#To reset the DataFrame used for storage of values
df = pd.DataFrame(columns=['Titles', 'Scores']) 
df.to_csv("df_scores.csv", ';', index=False)
'''

error_list = []


for folder_name in l_folders:
    df = pd.DataFrame(columns=['Titles', 'Scores']) 
    csv_name = f"csv_{folder_name}.csv"
    df.to_csv(csv_name, ';', index=False)
    
    dir_path = os.path.abspath(folder_name)
    for filename in os.scandir(dir_path):
        if filename.is_file():
            filepath = os.path.join(dir_path, filename)
            print(filename)

            with pdfplumber.open(filepath) as pdf:
                page_2 = pdf.pages[1] #Second page has abstract, standardized by GU medicine departement

                default_bbox = pdf.pages[1].bbox #bbox=(x0, top, x1, bottom)
                a = default_bbox[0]
                b = default_bbox[1]
                c = default_bbox[2]
                d = default_bbox[3]
                
               # try:
                def pos_abstract(page_obj):
                    words = page_obj.extract_words(keep_blank_chars=True)
                    word_search = ""
                    for w in words:
                        i = 0
                        for letter in w["text"]:
                            if i < len(kw1[0]): #length of "Abstract"
                                word_search = word_search + letter
                                i += 1
                            else:
                                break
    
                        if word_search in kw1: #searched for word
                                pos_top = w["top"] + 10 #To not include the line itself
                                break 
                            
                        word_search = ""
                    return pos_top
                
                try:
                    pos_top = pos_abstract(page_2)
                except:
                    error_list.append(f"{filename}_top")
                
                def pos_keyword1(page_obj):
                    words = page_obj.extract_words(keep_blank_chars=True)
                    word_search = ""
                    for w in words:
                        flag = 0
                        i = 0
                        
                        for letter in w["text"]:
                            if i < len(kw2[0]): #Length of "Keywords:"
                                word_search = word_search + letter
                                i += 1
                            else:
                                break
                            
                        if word_search in kw2: #searched for words
                                pos_bot = w["bottom"] - 10 # Argumenterar för skillnader mellan texterna eller nått 
                                flag = 1
                                break
                        
                        word_search = ""
                    return pos_bot
                
                def pos_keyword2(page_obj):
                    words = page_obj.extract_words(keep_blank_chars=True)
                    word_search = ""
                    for w in words:
                        flag = 0
                        i = 0
                        
                        for letter in w["text"]:
                            if i < len(kw2[1][0]): #Length of "Key Words:" same as "Key words:"
                                word_search = word_search + letter
                                i += 1
                            else:
                                break
                            
                        if word_search in kw2[1]: #searched for words
                                pos_bot = w["bottom"] - 10 # Argumenterar för skillnader mellan texterna eller nått 
                                flag = 1
                                break
                        
                        word_search = ""
                    return pos_bot
                
                try:
                    pos_bot = pos_keyword1(page_2)
                except:
                    try:
                        pos_bot = pos_keyword2(page_2)
                    except:
                        error_list.append(f"{filename}_bot")
                    
                
                new_bbox = (a, pos_top, c, pos_bot)
                crop_area = page_2.crop(new_bbox, strict=False)
                abstract = crop_area.extract_text()
               
            r = Readability(abstract)
            r_score = r.dale_chall().score
            print(r_score)
            
            full_filename = os.path.basename(filepath)
            clean_filename = full_filename.replace(".pdf","")
            
            df_scores = pd.read_csv(csv_name, sep=";")
            df_scores.loc[len(df_scores.index)] = [clean_filename, r_score]
            df_scores.to_csv(csv_name, ';', index=False)

            with open("file_log.txt", "a") as txt:
                txt.write(folder_name)
                txt.write(abstract)
                txt.write("\n\n")

for error in error_list:
    print(error)
