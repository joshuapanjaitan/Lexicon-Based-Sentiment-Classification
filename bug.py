import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.stem import PorterStemmer
import read as read


def penn_to_wn(tag):
    """
    Convert between the PennTreebank tags to simple Wordnet tags
    """
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None


lemmatizer = WordNetLemmatizer()


def get_sentiment(word, tag):
    """ returns list of pos neg and objective score. But returns empty list if not present in senti wordnet. """

    wn_tag = penn_to_wn(tag)
    if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
        return []

    lemma = lemmatizer.lemmatize(word, pos=wn_tag)
    if not lemma:
        return []

    synsets = wn.synsets(word, pos=wn_tag)
    if not synsets:
        return []

    # Take the first sense, the most common
    synset = synsets[0]
    swn_synset = swn.senti_synset(synset.name())

    return [swn_synset.pos_score(), swn_synset.neg_score()]


# driver
data = read.read()
# data[0][0] = 'nice'  # indentasi

for i in range(len(data)):
    for x in range(len(data[i])):
        ps = PorterStemmer()
        words_data = nltk.word_tokenize(data[i][x])
        pos_val = nltk.pos_tag(words_data)
        senti_val = [get_sentiment(x, y) for (x, y) in pos_val]
        # handle 1 kata
        if len(senti_val) == 1 and len(senti_val[0]) != 0:
            pos = senti_val[0][0]
            neg = senti_val[0][1]
            tot = pos - neg
            if tot != 0:
                if pos > neg:
                    data[i][x] = 'Positive'
                elif neg > pos:
                    data[i][x] = 'Negative'
        # handle 2 kata
        elif len(senti_val) == 2:
            if len(senti_val[1]) != 0:
                pos1 = senti_val[0][0]
                neg1 = senti_val[0][1]
                pos2 = senti_val[1][0]
                neg2 = senti_val[1][1]

                pos = pos1 + pos2
                neg = neg1 + neg2
                if pos > neg:
                    data[i][x] = 'Positive'
                elif neg > pos:
                    data[i][x] = 'Negative'
            elif len(senti_val[1]) == 0 and len(senti_val[0]) != 0:
                pos = senti_val[0][0]
                neg = senti_val[0][1]
                tot = pos - neg
                if tot != 0:
                    if pos > neg:
                        data[i][x] = 'Positive'
                    elif neg > pos:
                        data[i][x] = 'Negative'
            elif len(senti_val[0]) == 0 and len(senti_val[1]) != 0:
                pos = senti_val[1][0]
                neg = senti_val[1][1]
                tot = pos - neg
                if tot != 0:
                    if pos > neg:
                        data[i][x] = 'Positive'
                    elif neg > pos:
                        data[i][x] = 'Negative'

# Driver write file
f = open('ClassificationCanonG3.csv', 'w')
for item in data:
    for i in range(len(item)):
        if i == 0:
            f.write(str(item[i]))
        else:
            f.write(',' + str(item[i]))
    f.write('\n')
f.close()
