# -- coding: utf-8 --
import sys,re,collections,nltk
import os 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# patterns that used to find or/and replace particular chars or words
# to find chars that are not a letter, a blank or a quotation
pat_letter = re.compile(r'[^a-zA-Z \']+')
# to find the 's following the pronouns. re.I is refers to ignore case
pat_is = re.compile("(it|he|she|that|this|there|here)(\'s)", re.I)
# to find the 's following the letters
pat_s = re.compile("(?<=[a-zA-Z])\'s")
# to find the ' following the words ending by s
pat_s2 = re.compile("(?<=s)\'s?")
# to find the abbreviation of not
pat_not = re.compile("(?<=[a-zA-Z])n\'t")
# to find the abbreviation of would
pat_would = re.compile("(?<=[a-zA-Z])\'d")
# to find the abbreviation of will
pat_will = re.compile("(?<=[a-zA-Z])\'ll")
# to find the abbreviation of am
pat_am = re.compile("(?<=[I|i])\'m")
# to find the abbreviation of are
pat_are = re.compile("(?<=[a-zA-Z])\'re")
# to find the abbreviation of have
pat_ve = re.compile("(?<=[a-zA-Z])\'ve")


function_words = ['of','to','in', 'and','as','from','for','with', 'that', 'have', 'by', 'on','upon','about', 'above', 'across', 'among', 'ahead', 'after', 'a', 'an','although','at','also', 'along', 'around','always', 'away', 'any','up', 'under', 'until','before','be','you','your', 'between', 'beyond', 'behind', 'because','what', 'when', 'would', 'could', 'who' ,'whom', 'whose','which', 'where', 'why', 'without', 'whether','down', 'during', 'despite', 'over', 'off', 'only', 'other', 'out', 'than', 'the', 'then','through', 'throughout', 'that' ,'these', 'this', 'those', 'there', 'therefore', 'till','some', 'such', 'since', 'so', 'can','many', 'much', 'more', 'may', 'might', 'must','ever', 'even', 'every', 'each']
lmtzr = WordNetLemmatizer()





def get_words(files):  
    path = "./spam/"
    co = 1
    words_box=[]
    for spamFile in files: #遍历文件
        print co
        with open (path+spamFile) as f:  
            pat = re.compile(r'[^a-zA-Z \']+')
            for line in f:                           
                #if re.match(r'[a-zA-Z]*',line): 
                #    words_box.extend(line.strip().strip('\'\"\.,').lower().split())
                # words_box.extend(pat.sub(' ', line).strip().lower().split())
                words_box.extend(merge(replace_abbreviations(line).split()))
            co = co + 1
    return collections.Counter(words_box)  


def merge(words):
    new_words = []
    for word in words:
        if word:
            tag = nltk.pos_tag(word_tokenize(word)) # tag is like [('bigger', 'JJR')]
            pos = get_wordnet_pos(tag[0][1])
            if pos:
                lemmatized_word = lmtzr.lemmatize(word, pos)
                new_words.append(lemmatized_word)
            else:
                new_words.append(word)
    return new_words


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return ''


def replace_abbreviations(text):
    new_text = text
    new_text = pat_letter.sub(' ', text).strip().lower()
    new_text = pat_is.sub(r"\1 is", new_text)
    new_text = pat_s.sub("", new_text)
    new_text = pat_s2.sub("", new_text)
    new_text = pat_not.sub(" not", new_text)
    new_text = pat_would.sub(" would", new_text)
    new_text = pat_will.sub(" will", new_text)
    new_text = pat_am.sub(" am", new_text)
    new_text = pat_are.sub(" are", new_text)
    new_text = pat_ve.sub(" have", new_text)
    new_text = new_text.replace('\'', ' ')
    return new_text


def append_ext(words):
    new_words = []
    for item in words:
        word, count = item
        tag = nltk.pos_tag(word_tokenize(word))[0][1] # tag is like [('bigger', 'JJR')]
        new_words.append((word, count, tag))
    return new_words

def write_to_file(words, file='results.txt'):
    f = open(file, 'w')
    j = 1
    for item in words:
        i = 0
        if item[0] not in function_words:
            f.write(str(j) + '  ')
        else:
            continue
        for field in item:
            if(i == 1):
                break   
            if field not in function_words:
                f.write(str(field))
                i = i + 1
            else:
                break
        j = j + 1
        f.write('\n')

if __name__=='__main__':
    print "counting..."
    path = "./spam/"
    files= os.listdir(path)
    words = get_words(files)
    print "writing file..."
    write_to_file(append_ext(words.most_common()))
    
