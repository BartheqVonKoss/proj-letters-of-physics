from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import nltk



nltk.download('stopwords')
nltk.download('punkt')

class FrequencySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        """
         Initilize the text summarizer.
         Words that have a frequency term lower than min_cut 
         or higer than max_cut will be ignored.
        """
        self._min_cut = min_cut
        self._max_cut = max_cut 
        self._stopwords = set(stopwords.words('english') + list(punctuation))


    def compute_freq(self, word_sent):
        """ 
          Compute the frequency of each of word.
          Input: 
           word_sent, a list of sentences already tokenized.
          Output: 
           freq, a dictionary where freq[w] is the frequency of w.
        """
        freq = defaultdict(int)
        for item in word_sent:
            for word in item:
                if word not in self._stopwords:
                    freq[word] += 1
        m = float(max(freq.values()))
        freq2 = freq.copy()
        for w in freq.keys():
            freq[w] = freq[w]/m
            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                del freq2[w]
        return freq2
    
    def summarize(self, text, n):
        """
          return a list of n sentences 
          that present summary of the text.
        """
        sents = nltk.sent_tokenize(text)
        assert n <= len(sents)
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self.compute_freq(word_sent)
        ranking = defaultdict(int)
        for i,sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self.rank(ranking, n)    
        return [sents[j] for j in sents_idx]

    def rank(self, ranking, n):
        """ 
          return the first n sentences with highest ranking
        """
        return nlargest(n, ranking, key=ranking.get)
    
    def clean(self, text):
        text = text.replace('\r', ' ').replace('\n', ' ').replace('\t',' ').replace('\xa0',' ')
        text = text.replace('Physics Today', ' ')
        return text