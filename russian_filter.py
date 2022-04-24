from pymystem3 import Mystem
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

rus_stop = stopwords.words('russian') # 151 words

def filtration(text):
    m = Mystem()
    lemmas = m.lemmatize(text)
    return list(filter(lambda word: word not in rus_stop and word.isalnum(), lemmas))
