import re
import sys
import os
import shutil
import math
import itertools
import xml.sax
import time
from Stemmer import Stemmer
from collections import defaultdict, Counter
from tqdm import tqdm


## Merging id_to_title files into single file.
def merge_id_files(num_of_files):
    id_to_title_dic = {}
    print("1.Running merge_id_files function:[op files will be created in char_wise_files directory]")
    for each_file in (range(1,num_of_files+1)):
        with open("./id_to_title_files/id_to_title_" + str(each_file)) as fp:
            data = fp.readlines()
            for each_line in data:
                each_line = each_line.strip().split("-")
                article_id = int(each_line[0])
                title = each_line[1]
                id_to_title_dic[article_id] = title
        del data
    sorted_id_to_dict = sorted(id_to_title_dic.items(), key=lambda item:item[0])
    with open('./char_wise_files/id_to_title.txt', 'w') as fp:
        for article_id, title in sorted_id_to_dict:
            fp.write(str(article_id) + "-" + title + "\n")
    del id_to_title_dic


## This creates character and number wise individual files. Ex. token_a.txt file will contain all the tokens
## started with 'a' and their corresponding posting lists.
def create_char_wise_files(num_of_files):
    global char_list
    global num_list
    print("2.Running create_char_wise_files function:[op files will be created in final_files directory]")
    for each_file in range(1,num_of_files+1):
        with open('./inverted_indexes_files/inv_index_'+str(each_file), 'r') as fp:
            data = fp.readlines()
        dic = defaultdict(list)
        for each_line in (data):
            each_line = each_line.strip()
            token = each_line.split(":")[0]
            if token[0] in char_list:
                dic[token[0]].append(each_line)
            elif token[0] in num_list:
                dic[token[0]].append(each_line)

        # writing the data to file:
        del data
        for each_char in char_list:
            if len(dic[each_char])!=0:
                with open('./final_files/token_'+ each_char + ".txt", "a") as fp1:
                    fp1.write("\n".join(dic[each_char]))
                    fp1.write("\n")
        for each_num in num_list:
            if len(dic[each_num])!=0:
                with open('./final_files/token_'+ each_num + ".txt", "a") as fp2:
                    fp2.write("\n".join(dic[each_num]))
                    fp2.write("\n")
        del dic
        #print("No.of files completed :", each_file)



# creating unique 'token-posting_list' for each individual file in sorted order.
def create_final_char_files(data_list,output_path):
    print("3.Running create_final_char_files function:[op files will be created in {0} ]".format(output_path))
    for each_char in range(len(data_list)):
        with open('./final_files/token_'+ data_list[each_char] + ".txt", 'r') as fp:
            data = fp.readlines()
        tok_pos_dict = {}
        for each_line in (data):
            each_line = each_line.strip("\n").split(":")
            token = each_line[0]
            posting_list = each_line[1].strip()
            if token not in tok_pos_dict:
                tok_pos_dict[token] = posting_list
            else:
                tok_pos_dict[token] += "|" + posting_list

        # sorting the dictionary
        sorted_tok_pos_dict = sorted(tok_pos_dict.items(), key = lambda item : item[0])
        with open('./'+ output_path +'/token_' + data_list[each_char] + ".txt", 'w') as fp:
            for token,posting_list in sorted_tok_pos_dict:
                if posting_list[-1]=="|":
                    fp.write(token + ":" + posting_list[:-1] + "\n")
                else:
                    fp.write(token + ":" + posting_list + "\n")
        #print("No.of files completed :", each_char+1)
    del sorted_tok_pos_dict, tok_pos_dict




# This function divides each_character file into multiple files.
def divide_char_file_to_multiple_files(n_files_count):
    print("4.Running divide_char_to_multiple_files function:[op files will be created in char_wise_files directory]")
    global char_list
    for each_char in range(len(char_list)):
        with open('./final_files/token_'+ char_list[each_char] + ".txt", 'r') as fp:
            data = fp.readlines()
        total_lines_count = len(data)
        part_size = int(total_lines_count/n_files_count)
        i = 1
        j = 1
        number_of_files = 1
        for each_line in (data):
            with open('./char_wise_files/token_' + char_list[each_char] + "_" + str(number_of_files) + ".txt", 'a') as fp:
                if i==part_size:
                    fp.write(each_line.strip("\n"))
                elif j==len(data):
                    fp.write(each_line.strip("\n"))
                else:
                    fp.write(each_line)
            if i==part_size:
                number_of_files+=1
                i = 0
            i+=1
            j+=1


def create_char_wise_info_files(n_files_count):
    print("5.Running create_char_wise_info_files:[op files will be created in char_wise_files directory]")
    global char_list
    for each_char in char_list:
        for i in range(1,n_files_count+2):
            with open('./char_wise_files/token_'+ each_char +'_' + str(i) + ".txt",'r') as fp:
                first_token = fp.readline().split(":")[0]
                with open('./char_wise_files/token_'+ each_char +'_info.txt', 'a') as fp1:
                    if i != n_files_count+1:
                        fp1.write(first_token + "\n")
                    else:
                        fp1.write(first_token)

def divide_id_title_file_to_multiple_files(n_files_count):
    print("6.Running divide_id_title_to_multiple_files function:[op files will be created in char_wise_files directory]")
    with open('./char_wise_files/id_to_title.txt', 'r') as fp:
        data = fp.readlines()
    total_lines_count = len(data)
    part_size = int(total_lines_count/n_files_count)
    i = 1
    j = 1
    number_of_files = 1
    for each_line in tqdm(data):
        with open('./char_wise_files/id_title_' + str(number_of_files) + ".txt", 'a') as fp:
            if i==part_size:
                fp.write(each_line.strip("\n"))
            elif j==len(data):
                fp.write(each_line.strip("\n"))
            else:
                fp.write(each_line)
        if i==part_size:
            number_of_files+=1
            i = 0
        i+=1
        j+=1


def create_id_title_file_wise_info_files(n_files_count):
    print("7.Running create_id_title_wise_info_files:[op files will be created in char_wise_files directory]")
    for i in range(1,n_files_count+2):
        with open('./char_wise_files/id_title_'+ str(i) + ".txt",'r') as fp:
            last_line = fp.readlines()[-1]
            with open('./char_wise_files/id_title_info.txt', 'a') as fp1:
                if i != n_files_count+1:
                    fp1.write(last_line + "\n")
                else:
                    fp1.write(last_line)
                        







def index_creation(doc_id, title_words_list,body_words_list, category_words_list, infobox_words_list, external_links_words_list, reference_words_list):
    
        total_words = set()
        global word_posting_dict
        
        title_word_freq_dict = Counter(title_words_list)
        total_words.update(title_word_freq_dict.keys())

        body_word_freq_dict = Counter(body_words_list)
        total_words.update(body_word_freq_dict.keys())

        category_word_freq_dict = Counter(category_words_list)
        total_words.update(category_word_freq_dict.keys())

        infobox_word_freq_dict = Counter(infobox_words_list)
        total_words.update(infobox_word_freq_dict.keys())

        ext_links_word_freq_dict = Counter(external_links_words_list)
        total_words.update(ext_links_word_freq_dict.keys())

        ref_word_freq_dict = Counter(reference_words_list)
        total_words.update(ref_word_freq_dict.keys())


        
        for word in total_words:
            if len(word)>1:
                posting = str(doc_id)+'-'

                if word in title_word_freq_dict:
                    posting += 't'+str(title_word_freq_dict[word])

                if word in body_word_freq_dict:
                    posting += 'b'+str(body_word_freq_dict[word])

                if word in category_word_freq_dict:
                    posting += 'c'+str(category_word_freq_dict[word])

                if word in infobox_word_freq_dict:
                    posting += 'i'+str(infobox_word_freq_dict[word])

                if word in ext_links_word_freq_dict:
                    posting += 'l'+str(ext_links_word_freq_dict[word])

                if word in ref_word_freq_dict:
                    posting += 'r'+str(ref_word_freq_dict[word])

                posting+='|'

                word_posting_dict[word]+=posting


def preprocess_text(text_data):
    
    #global total_tokens_in_dump

    text_data = text_data.strip().lower()
    
    # Replacing characters which are not alphabets and digits with space.
    # Non-ascii characters, Special symbols, punctuations etc. will be replaced with space.
    modified_text = re.sub('[^a-z0-9 ]+',' ', text_data) 
  
    # Tokenizing the text.
    tokenized_text = modified_text.split()
    # total_tokens_in_dump+=len(tokenized_text)
    
    # Considering non-stop words only.
    words_list = [word for word in tokenized_text if word not in stop_words_list]
    
    # Apply stemming on text.
    final_text = stemmer.stemWords(words_list)
    
    return final_text

def get_field_wise_data(title,text_data):
    
    lines = text_data.split("\n")
    flag = 0
    body_flag = 1
    cat_text = ""
    info_text = ""
    links_text = ""
    ref_text = ""
    b_text = ""
    for each_line in lines:
        
        each_line = each_line.strip()
        ### Infobox text
        if '{{Infobox' in each_line:
            info_text+= each_line + " "
            if not each_line.endswith('}}'):
                flag=1      
        elif flag==1:
            info_text+= each_line + " "
            if each_line.strip()=='}}':
                flag=0

        ### Category text
        elif '[[Category:' in each_line:
            body_flag = 0
            cat_text+= each_line + " "
            if not each_line.endswith(']]'):
                flag=2      
        elif flag==2:
            cat_text+= each_line + " "
            if each_line.strip().endswith(']]'):
                flag=0


        ### External links and See Also
        elif '==External links==' in each_line or '== External links ==' in each_line or '==See also==' in each_line or '== See also ==' in each_line:
            flag=3
            body_flag = 0
        elif flag==3 and each_line.startswith("*"):
            line = each_line.split(" ")
            links_text+= ' '.join([each_word for each_word in line if "http" not in each_word]) + " "
        elif flag==3 and each_line=="":
            flag = 0

        ### References
        elif '==References==' in each_line or '== References ==' in each_line or '==Bibliography==' in each_line or '== Bibliography ==' in each_line:
            flag=4
            body_flag = 0
        elif flag==4 and each_line.startswith("*"):
            line = each_line.split(" ")
            ref_text+= ' '.join([each_word for each_word in line if "http" not in each_word]) + " "
        elif flag==4 and each_line=="":
            flag = 0

        ### Body text
        elif body_flag==1:
            if each_line!="":
                if "#redirect" not in each_line.lower():
                    b_text+=each_line+ " "

    info_text = info_text.replace('{{Infobox','').replace("}}",'')
    cat_text = cat_text.replace('[[Category:','').replace("]]",'')
    if b_text.strip()!="":
        body_text = re.sub(r'(&lt;.*?&gt;)','',b_text)
        body_text = re.sub('(http[s]?://[^ ]+)', '', b_text)
        body_text = re.sub('\{.*?\}|\=\=.*?\=\=|\[.*?\]', '', body_text)
        final_body_text    = preprocess_text(body_text)
    else:
        final_body_text    = []
    
        ### Preprocessed data ###
    final_cat_text     = preprocess_text(cat_text)
    final_info_text    = preprocess_text(info_text)
    final_links_text   = preprocess_text(links_text)
    final_ref_text     = preprocess_text(ref_text)
    final_title_text   = preprocess_text(title)
    
    return final_title_text, final_body_text,final_cat_text, final_info_text, final_links_text, final_ref_text

class XMLParser(xml.sax.ContentHandler):
    
    """
        A custom class XMLParser is defined that inherits from xml.sax.ContentHandler. This class is used for handling XML events.
    """

    def __init__(self):

        """
            The constructor initializes several instance variables, including self.tag, self.doc_id, self.title, self.text, self.namespa, self.page_count, and self.start_time.
            These variables will be used to store information extracted from the XML content.
        """
        
        self.tag = ''
        self.doc_id = ''
        self.title = ''
        self.text = ''
        self.namespa = ''
        self.page_count = 0   
        self.start_time = time.time()

    def startElement(self,name,attrs):
        """
            This method is called when the parser encounters the start of an XML element. It sets the self.tag to the name of the current element.
            when the parser encounters the opening tag of an element (e.g., <id>), it records the name of the tag in self.tag.
            This is how the parser keeps track of which element it is currently processing.
            
        """

        self.tag=name
        
    def endElement(self,name):
        """
            This method is called when the parser encounters the end of an XML element. It handles the processing of specific elements within a <page> element.
            For example, when the parser encounters the closing tag of an element (e.g., </id>), it invokes the endElement method.  
            
        """
        
        global id2title_dict
        global word_posting_dict
        global index_files_count
        if name=='page':
            self.page_count+=1
            if self.page_count%100000==0:
                print("page_count : {0}, time : {1}".format(self.page_count,time.time()-start_time))
            self.doc_id = self.doc_id.split("\n")[0]
            if self.namespa.strip() == "0":
                id2title_dict[self.doc_id] = self.title.lower().strip()
                final_title_text, final_body_text,final_cat_text, final_info_text, final_links_text, final_ref_text = get_field_wise_data(self.title,self.text)
                index_creation(self.doc_id,final_title_text, final_body_text,final_cat_text, final_info_text, final_links_text, final_ref_text)

            if self.page_count%500000==0:
                index_files_count+=1
                print("Writing index file")
                
                ## Writing index file
                folder_path_1 = "./inverted_indexes_files"
                if not os.path.exists(folder_path_1):
                    os.makedirs(folder_path_1)
                sorted_word_posting_dict = sorted(word_posting_dict.items(), key = lambda item : item[0])
                with open(folder_path_1 + "/inv_index_"+ str(index_files_count) + ".txt", 'w') as fp:
                    for token, posting_list in sorted_word_posting_dict:
                        if posting_list[-1]=="|":
                            fp.write(token + ':' + posting_list[:-1] + "\n")
                        
                ## Writing article_id to title dict file:
                folder_path_2 = "./id_to_title_files"
                if not os.path.exists(folder_path_2):
                    os.makedirs(folder_path_2)
                sorted_id2title_dict = sorted(id2title_dict.items(), key = lambda item : item[0])
                with open(folder_path_2 + "/id_to_title_" + str(index_files_count) + ".txt", 'w') as fp:
                    for article_id, article_title in sorted_id2title_dict:
                        fp.write(article_id + "-" + article_title + "\n")
                        
                word_posting_dict = defaultdict(str)
                id2title_dict = {}
                del sorted_word_posting_dict
                del sorted_id2title_dict


            self.tag = ""
            self.title = ""
            self.text = ""
            self.doc_id =""
            self.namespa = ""

    def characters(self, content):
        
        """
             When the parser encounters the character data within an element (e.g., the content of <id>), it checks the value of self.tag to determine which element is currently being processed.
             For example, if it's <id>, it appends the character data to self.doc_id.
        """
        
        if self.tag == 'id':
            self.doc_id += content
        
        if self.tag == "ns":
            self.namespa += content
        
        if self.tag == 'title':
            self.title += content
        
        if self.tag == 'text':
            self.text += content




if __name__=='__main__':

    start_time = time.time()
    stop_words_list = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"}
    stemmer = Stemmer('english')
    id2title_dict = {}
    word_posting_dict = defaultdict(str)
    index_files_count = 0
    char_list = [chr(i) for i in range(97,123)]
    num_list = [str(i) for i in range(0,10)]
    num_of_files = 45  # Total no.of inverted indices files.
    n_files_count = 100 # No.of files we want to divide each character into.

    parser = xml.sax.make_parser()
    xml_parser = XMLParser()
    parser.setContentHandler(xml_parser)

    # sys.argv[1] ---> wiki dump path
    # sys.argv[2] ---> path for inverted index file creation
    # sys.argv[3] ---> path for invertedindex_stat txt file creation

    # output=parser.parse(sys.argv[1])
    # inverted_index_path = sys.argv[2]
    # invertedindex_stat_path = sys.argv[3]
    dump_path = "./enwiki-20220820-pages-articles-multistream.xml"
    output = parser.parse(dump_path)

    ## Writing index file
    index_files_count+=1
    folder_path_1 = "./inverted_indexes_files"
    sorted_word_posting_dict = sorted(word_posting_dict.items(), key = lambda item : item[0])
    with open(folder_path_1 + "/inv_index_"+ str(index_files_count) + ".txt", 'w') as fp:
        for token, posting_list in sorted_word_posting_dict:
            if posting_list[-1]=="|":
                fp.write(token + ':' + posting_list[:-1] + "\n")
            
    ## Writing article_id to title dict file:
    folder_path_2 = "./id_to_title_files"
    sorted_id2title_dict = sorted(id2title_dict.items(), key = lambda item : item[0])
    with open(folder_path_2 + "/id_to_title_" + str(index_files_count) + ".txt", 'w') as fp:
        for article_id, article_title in sorted_id2title_dict:
            fp.write(article_id + "-" + article_title + "\n")


    ############################### File Operations starts ######################################################
    path = "./final_files"
    if not os.path.exists(path):
        os.makedirs(path)
    path = "./char_wise_files"
    if not os.path.exists(path):
        os.makedirs(path)


    s_time = time.time()
    merge_id_files(num_of_files)
    create_char_wise_files(num_of_files)
    create_final_char_files(char_list,'final_files')
    create_final_char_files(num_list,'char_wise_files')
    divide_char_file_to_multiple_files(n_files_count)
    create_char_wise_info_files(n_files_count)
    divide_id_title_file_to_multiple_files(n_files_count)
    create_id_title_file_wise_info_files(n_files_count)
    os.remove('./char_wise_files/id_to_title.txt')
    shutil.rmtree('./final_files')
    e_time = time.time()
    print("Time taken to complete the file operations :", e_time-s_time)


    ####################################### Creating stats.txt file ##################################################
    total_no_of_tokens_in_inv_index = 0
    index_size = "15.1 GB"
    total_files = 128
    '''
    ID to title secondary index files = 101
    ID to secondary index file map    = 1
    Index files starts with digit     = 10
    A-Z secondary index file map      = 26
    ----------------------------------------
    Total files                       = 128
    '''
    for i in range(len(char_list)):
        for j in range(1,102):
            with open('./char_wise_files/token_'+str(char_list[i])+"_"+str(j)+".txt", "r") as fp:
                total_no_of_tokens_in_inv_index += len(fp.readlines())
                total_files += 1

    for i in range(len(num_list)):
        with open('./char_wise_files/token_'+str(num_list[i])+".txt", "r") as fp:
            total_no_of_tokens_in_inv_index += len(fp.readlines())
            total_files += 1

    with open("./stats.txt", 'w') as fp:
        fp.write(index_size+"\n")
        fp.write(str(total_files)+"\n")
        fp.write(str(total_no_of_tokens_in_inv_index))



    end_time = time.time()

    print("Total time taken for creating inverted index file : ",end_time-start_time)