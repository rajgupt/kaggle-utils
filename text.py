import emoji
import re
import webcolors

# Nltk for tokenize and stopwords
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

# credits: https://www.kaggle.com/raenish/cheatsheet-text-helper-functions

def find_url(string): 
    text = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',string)
    return "".join(text) # converting return value from list to string


def find_emoji(text):
    emo_text=emoji.demojize(text)
    line=re.findall(r'\:(.*?)\:',emo_text)
    return line


def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def find_email(text):
    line = re.findall(r'[\w\.-]+@[\w\.-]+',str(text))
    return ",".join(line)


def find_hash(text):
    '''Find hashtags'''
    line=re.findall(r'(?<=#)\w+',text)
    return " ".join(line)


def find_at(text):
    '''Find @ mentions'''
    line=re.findall(r'(?<=@)\w+',text)
    return " ".join(line)


def find_number(text):
    line=re.findall(r'[0-9]+',text)
    return " ".join(line)


def find_nonalp(text):
    '''Non alphanumeric'''
    line = re.findall("[^A-Za-z0-9 ]",text)
    return line


def find_punct(text):
    line = re.findall(r'[!"\$%&\'()*+,\-.\/:;=#@?\[\\\]^_`{|}~]*', text)
    string="".join(line)
    return list(string)


def stop_word_fn(text):
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text) 
    non_stop_words = [w for w in word_tokens if not w in stop_words] 
    stop_words= [w for w in word_tokens if w in stop_words] 
    return stop_words


def ngrams_top(corpus,ngram_range,n=None):
    """
    List the top n words in a vocabulary according to occurrence in a text corpus.
    """
    vec = CountVectorizer(stop_words = 'english',ngram_range=ngram_range).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    total_list=words_freq[:n]
    df=pd.DataFrame(total_list,columns=['text','count'])
    return df


def rep(text):
    grp = text.group(0)
    if len(grp) > 1:
        return grp[0:1] # can change the value here on repetition


def unique_char(rep,sentence):
    '''
    text: "heyyy this is loong textttt sooon"
    result: "hey this is long text son"
    '''
    convert = re.sub(r'(\w)\1+', rep, sentence) 
    return convert


def find_dollar(text):
    # \$ - dollar sign followed by
    # \d+ one or more digits
    # (?:\.\d+)? - decimal which is optional
    line=re.findall(r'\$\d+(?:\.\d+)?',text)
    return " ".join(line)


def only_words(text):
    line=re.findall(r'\b[^\d\W]+\b', text)
    return " ".join(line)


def only_numbers(text):
    line=re.findall(r'\b\d+\b', text)
    return " ".join(line)


def find_capital(text):
    '''
    "World is affected by corona crisis.No one other than God can save us from it"
    ['World', 'No', 'God']
    '''
    line=re.findall(r'\b[A-Z]\w+', text)
    return line


def find_color(string): 
    '''
    "Find the color of #00FF00 and #FF4500"
    ['lime', 'orangered']
    '''
    text = re.findall('\#(?:[0-9a-fA-F]{3}){1,2}',string)
    conv_name=[]
    for i in text:
        conv_name.append(webcolors.hex_to_name(i))
    return conv_name