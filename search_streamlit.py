import re
import sys
import os
import shutil
import itertools
import math
import time
from Stemmer import Stemmer
from collections import defaultdict, Counter
from tqdm import tqdm
import streamlit as st


def preprocess_text(text_data):
    
    text_data = text_data.strip().lower()
    
    # Replacing characters which are not alphabets and digits with space.
    # Non-ascii characters, Special symbols, punctuations etc. will be replaced with space.
    modified_text = re.sub('[^a-z0-9 ]+',' ', text_data) 
  
    # Tokenizing the text.
    tokenized_text = modified_text.split()
    
    # Considering non-stop words only.
    words_list = [word for word in tokenized_text if word not in stop_words_list]
    
    # Apply stemming on text.
    final_text = stemmer.stemWords(words_list)
    
    return final_text


def get_id_title(doc_id):
    doc_id = int(doc_id)
    file_pointer = open('./char_wise_files/id_title_info.txt', 'r', encoding='utf-8')
    start_line = 1
    end_line = len(file_pointer.readlines())
    title = ""
    while(True):
        file_pointer.seek(0)
        offset_value = int((end_line - start_line)/2)
        mid_line = start_line + offset_value
        if mid_line==0:
            line = file_pointer.readline()
        else:
            line = list(itertools.islice(file_pointer, mid_line-1, mid_line))[0]
        current_id, title = line.strip().split("-")
        current_id = int(current_id)
        #print("s:",start_line, 'off:', offset_value, "m:", mid_line,"e:", end_line, "current_token:",current_id)
        if current_id==doc_id:
            break
        elif(end_line<=start_line):
            break
        elif current_id < doc_id:
            start_line = mid_line + 1
        else:
            end_line = mid_line
            
    if current_id < doc_id:
        mid_line = mid_line+1
        
    file_pointer.close()
    return mid_line




def binary_search_title(file_id,doc_id):
    doc_id = int(doc_id)
    file_pointer = open('./char_wise_files/id_title_' + str(file_id) + ".txt", 'r', encoding='utf-8')
    print("file-id:",file_id)
    start_line = 0
    end_line = len(file_pointer.readlines())
    posting_list = []
    while(True):
        file_pointer.seek(0)
        offset_value = int((end_line - start_line)/2)
        mid_line = start_line + offset_value
        if mid_line==0:
            line = file_pointer.readline()
        else:
            line = list(itertools.islice(file_pointer, mid_line-1, mid_line))[0]
        current_id , title = [i for i in line.split('-') if i.strip()!=""]
        current_id = int(current_id)
        
        if current_id==doc_id:
            return title.strip()
        elif end_line<=start_line:
            title = ""
            break
        elif current_id < doc_id:
            title = ""
            start_line = mid_line + 1
        else:
            title = ""
            end_line = mid_line
            
    file_pointer.close()
    return title.strip()


def get_char_file_for_posting(token):
    file_pointer = open('./char_wise_files/token_'+ token[0] +'_info.txt', 'r', encoding='utf-8')
    start_line = 0
    end_line = len(file_pointer.readlines())
    while(True):
        file_pointer.seek(0)
        offset_value = int((end_line - start_line)/2)
        mid_line = start_line + offset_value
        if mid_line==0:
            line = file_pointer.readline()
        else:
            line = list(itertools.islice(file_pointer, mid_line-1, mid_line))[0] # This will point to the mid line.
        current_token = line.strip()
        
        #print("s:",start_line, 'off:', offset_value, "m:", mid_line,"e:", end_line, "current_token:",current_token)
        if current_token==token:
            break
        elif(end_line<=start_line):
            break
        elif current_token < token: # if input_token is greater than the current token, move down. 
            start_line = mid_line + 1
        else:
            end_line = mid_line
            
    if current_token > token:
        mid_line = mid_line - 1
        
    file_pointer.close()
    return mid_line



def binary_search_posting(file_id,token):
    if token[0].isalpha():
        file_pointer = open('./char_wise_files/token_' + token[0] + '_' + str(file_id) + ".txt", 'r', encoding='utf-8')
    else:
        file_pointer = open('./char_wise_files/token_' + token[0] + ".txt", 'r', encoding='utf-8')
    start_line = 0
    end_line = len(file_pointer.readlines())
    posting_list = []
    while(True):
        posting_list = []
        file_pointer.seek(0)
        offset_value = int((end_line - start_line)/2)
        mid_line = start_line + offset_value
        
        if mid_line==0:
            line = file_pointer.readline()
        else:
            line = list(itertools.islice(file_pointer, mid_line-1, mid_line))[0]
        current_token, word_postings = line.split(':')
        
        #print("s:",start_line,"m:", mid_line,"e:", end_line, "current_token: ", current_token)
        if current_token==token:
            posting_list = [word for word in word_postings.strip().rstrip('|').split('|') if word!='']
            break
        elif(end_line<=start_line):
            break
        elif current_token < token:
            start_line = mid_line + 1
        else:
            end_line = mid_line
            
    file_pointer.close()
    return posting_list



def parse_posting(posting):
    postings_dict = {'t':{}, 'b':{}, 'c':{}, 'i':{}, 'r':{}, 'l':{}}
    for line in posting:
        doc_no, fields_str = line.split('-')
        fields_freq = {field[0]:int(field[1:]) for field in re.sub(r'([tbcirl]\d+)', r' \1', fields_str).strip().split(' ')}
        for key in postings_dict:
            if key in fields_freq:
                postings_dict[key][doc_no] = fields_freq[key]
    return postings_dict


def process_query(query,query_type,field_query_pattern):
    if query_type=="plain":
        tokens = preprocess_text(query)
        final_postings = {}
        for token in (tokens):
            if token[0].isalpha():
                file_id = get_char_file_for_posting(token)
                postings = binary_search_posting(file_id,token)
            else:
                postings = binary_search_posting(-1,token)
            #print(postings)
            postings = parse_posting(postings)
            final_postings[token] = postings
        return final_postings
    else:
        query = re.sub(r'([tbicrl]:)', r';\1', query)
        matches = [match for match in query.split(';') if match!='']
        final_postings = defaultdict(dict)
        for match in matches:
            field_name, text = match.split(':', 1)
            preprocessed_tokens = preprocess_text(text)
            for each_word in preprocessed_tokens:
                if each_word[0].isalpha():
                    file_id = get_char_file_for_posting(each_word)
                    postings = binary_search_posting(file_id,each_word)
                else:
                    postings = binary_search_posting(-1,each_word)
                postings = parse_posting(postings)
                final_postings[each_word][field_name] = postings[field_name]
        return final_postings

def get_type_of_query(query):
    if 't:' in query or 'b:' in query or 'c:' in query or 'i:' in query or 'l:' in query or 'r:' in query:
        return "field"

    else:
        return "plain"


def apply_tf_idf_ranking(findings,no_tot_docs):
    weightage_dict = {'t':1.0, 'b':0.6, 'c':0.4, 'i':0.75, 'l':0.20, 'r':0.25}
    modified_findings = defaultdict(dict)
    for token,posting_list in findings.items():
        for field,post_list in posting_list.items():
            modified_findings[token][field] = {}
            for doc_id,freq in post_list.items():
                score = weightage_dict[field]*(1+math.log(freq))*math.log((no_tot_docs-len(findings[token][field]))/len(findings[token][field]))
                modified_findings[token][field][doc_id] = score
    return modified_findings


def get_final_postings(postings_with_ranking_scores,query_type):
    
    if query_type == "field":
        final_postings = {}
        for token in postings_with_ranking_scores:
            for category, postings in postings_with_ranking_scores[token].items():
                if category not in final_postings:
                    final_postings[category] = postings
                else:
                    intersection = set(list(final_postings[category].keys())) & set(list(postings.keys()))
                    temp = final_postings[category]
                    final_postings[category] = {}
                    for doc_no in intersection:
                        final_postings[category][doc_no] = temp[doc_no] + postings[doc_no]
        return final_postings
    
    else:
        final_tok_post_dict = {}
        for token, posting_list in postings_with_ranking_scores.items():
            final_tok_post_dict[token] = {}
            for field,post_list in posting_list.items():
                for doc_id,score in post_list.items():
                    if doc_id not in final_tok_post_dict[token]:
                        final_tok_post_dict[token][doc_id] = score
                    else:
                        final_tok_post_dict[token][doc_id] += score
        return final_tok_post_dict

def get_top_resutls(final_postings):
    result = {}
    for field, posting_list in final_postings.items():
        for doc_id,score in posting_list.items():
            if doc_id not in result:
                result[doc_id]=score
            else:
                result[doc_id]+=score
    sorted_result = sorted(result.items(), key=lambda item:item[1],reverse=True)
    top_10_docs = {doc:score for doc,score in sorted_result[:10]}
    
    return top_10_docs


def get_common_docs(final_tok_post_dict):
    common_docs = set()
    i = 0
    for token, posting_list in final_tok_post_dict.items():
        if posting_list!={}:
            doc_ids = set(final_tok_post_dict[token].keys())
            if i==0 or len(common_docs)==0:
                common_docs = doc_ids
            else:
                common_docs = doc_ids & common_docs
        i+=1

    new_dic = {}
    for token in final_tok_post_dict.keys():
        for each_doc in common_docs:
            score = final_tok_post_dict[token].get(each_doc, 0)
            if each_doc not in new_dic:
                new_dic[each_doc] = score
            else:
                new_dic[each_doc] += score
    
    ### Sorting the docs based on scores
    final_sorted = sorted(new_dic.items(), key = lambda item : item[1], reverse=True)
    return final_sorted[:10]




if __name__=='__main__':


    N = 16745002
    file_start_time = time.time()
    stop_words_list = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"}
    stemmer = Stemmer('english')
    field_query_pattern = re.compile(r'[tbicrl]:[\w ]*[^tbicrl:]')

    
    start_time = time.time()
    st.title('English Wikipedia Search Engine')
    query = st.text_input('Enter your query')
    print("Input_query : ",query)
    print("\n")
    query_type = get_type_of_query(query)
    findings = process_query(query,query_type,field_query_pattern)
    postings_with_ranking_scores =  apply_tf_idf_ranking(findings,N)
    final_postings = get_final_postings(postings_with_ranking_scores,query_type)
    if query_type!="field":
        f = 0
        top_docs = get_common_docs(final_postings)
        for doc_id,score in top_docs:
            file_id = get_id_title(doc_id)
            title = binary_search_title(file_id,doc_id)
            print(doc_id," - ",title)
            #st.write(doc_id, " - ", title)
            title_words = []
            for each_word in title.split():
                word = each_word[0].upper() + each_word[1:].lower()
                title_words.append(word)
            modified_title = "_".join(title_words)
            #link = 'https://en.wikipedia.org/wiki/' + modified_title
            g_title = title.replace(' ','+') + ' wikipedia' 
            link = 'https://www.google.com/search?q=' + g_title
            h_link = str(doc_id) + f' - <a target="_blank" href="{link}">{title}</a>'
            st.markdown(h_link, unsafe_allow_html=True)
            f = 1
        end_time = time.time()
        print("\n Time(Sec) :",end_time-start_time)
        if f==1:
            st.write("Search finished in ",end_time-start_time)

    
    else:
        f = 0
        top_docs = get_top_resutls(final_postings)
        for doc_id in top_docs:
            file_id = get_id_title(doc_id)
            title = binary_search_title(file_id,doc_id)
            print(doc_id," - ",title)
            title_words = []
            for each_word in title.split():
                word = each_word[0].upper() + each_word[1:].lower()
                title_words.append(word)
            modified_title = "_".join(title_words)
            #link = 'https://en.wikipedia.org/wiki/' + modified_title 
            g_title = title.replace(' ','+') + ' wikipedia' 
            link = 'https://www.google.com/search?q=' + g_title
            h_link = str(doc_id) + f' - <a target="_blank" href="{link}">{title}</a>'
            st.markdown(h_link, unsafe_allow_html=True)
            f=1
        end_time = time.time()
        print("\n Time(Sec) :",end_time-start_time)
        if f==1:
            st.write("Search finished in ",end_time-start_time)
    print("---------------------------------------------------------")

    
    file_end_time = time.time()

    print("Total time taken to complete the search_process : ",file_end_time-file_start_time)