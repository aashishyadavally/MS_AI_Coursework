"""
Constructs :class: `POSTagger` which builds an n-gram part-of-speech tagger,
default of which is bigram part-of-speech tagger, and analyzes it's
performance through the frequency distribution of the wrong predictions.

Author:
-------
Aashish Yadavally
"""
import nltk
from nltk.corpus import brown, indian
from nltk import find
from nltk.corpus import TaggedCorpusReader


class POSTagger:
    """
    Builds a bigram part-of-speech tagger and analyzes it's performance
    """
    def __init__(self, corpus='brown', tagset=None, partition_ratio=0.9,
                 default_tagger='NN', lang='telugu'):
        """
        Initializes :class: `POSTagger`

        Parameters:
        -----------
            corpus (str):
                One of 'brown', 'bnc' and 'indian'
            tagset (None or str):
                Parameter for BNC Corpus - one of CLAWS5 and 'universal'
            partition_ratio (float):
                Partition ratio for Train-Test split
            default_tagger (str):
                'NN', by default - can be modified
            lang (str):
                One of the four Indian languages (Telugu, Hindi, Bangla,
                Marathi) in `nltk.corpus.indian`
        """     
        self.corpus = corpus
        self.tagset = tagset
        self.partition_ratio = partition_ratio
        self.default_tagger = default_tagger
        self.lang = lang


    def tagger(self, train_set, level):
        """
        Returns a tagger based on the level, with '0' corresponding to
        default tagger, '1' corresponding to a unigram tagger, '2'
        corresponding to a bigram tagger and '3' corresponding to a
        trigram tagger, with each of the previous levels as backoffs

        Arguments:
        ---------
            train_set (list):
                First 90% of the tagged sentences used for training
            level (int):
                Type of tagger to be returned - '0' corresponds to
        default tagger, '1' corresponds to a unigram tagger, '2'
        corresponds to a bigram tagger and '3' corresponds to a
        trigram tagger, with each of the previous levels as backoffs

        Returns:
        --------
            By default, t2 (nltk.BigramTagger)
                Uses `nltk.UnigramTagger` and 'NN' as backoff-taggers
        """
        t = []
        while len(t) <= level:
            t.append(nltk.DefaultTagger(self.default_tagger))
            t.append(nltk.UnigramTagger(train_set, backoff=t[0]))
            t.append(nltk.BigramTagger(train_set, backoff=t[1]))
            t.append(nltk.TrigramTagger(train_set, backoff=t[2]))        
        return t[level]


    def data_preparation(self):
        """
        Splits one of Brown, BNC News, Indian corpora into train set and
        test set

        Returns:
        --------
            sentences (list):
                Sentences without POS-tags
            tagged_sentences (list):
                Sentences with POS-tags
        """
        if self.corpus == 'brown':
            tagged_sentences = brown.tagged_sents(categories='news')
            sentences = brown.sents(categories='news')
        elif self.corpus == 'bnc':
            root = find('corpora/bnc')
            bncnews = TaggedCorpusReader(root, 'bnc-news-wtp.txt',
                                         tagset='en-claws')
            if self.tagset is None:
                tagged_sentences = bncnews.tagged_sents()
            elif self.tagset == 'universal':
                tagged_sentences = bncnews.tagged_sents(tagset=self.tagset)
            sentences = bncnews.sents()
        elif self.corpus == 'indian':
            if self.lang in ['telugu', 'hindi', 'marathi', 'bangla']:
                tagged_sentences = indian.tagged_sents(f'{self.lang}.pos')
                sentences = indian.sents(f'{self.lang}.pos')
            else:
                print('Language not part of Indian Corpus.')
        return sentences, tagged_sentences


    def evaluate(self, level=2):
        """
        Evaluates the trained POSTagger model on test data - computes accuracy
        and frequency distribution of wrong predictions

        Argument:
        ----------
            level (int):
                Type of tagger to be returned - '0' corresponds to
        default tagger, '1' corresponds to a unigram tagger, '2'
        corresponds to a bigram tagger and '3' corresponds to a
        trigram tagger, with each of the previous levels as backoffs

        Returns:
        --------
            fd (nltk.FreqDist):
                Frequency Distribution of wrong predictions
        """
        sentences, tagged_sentences = self.data_preparation()
        partition = int(len(tagged_sentences) * self.partition_ratio)
        train_set = tagged_sentences[:partition]
        test_set = tagged_sentences[partition:]
        print(len(train_set), len(test_set))
        tagger = self.tagger(train_set, level)
        accuracy = tagger.evaluate(test_set)

        print(f'Accuracy is {accuracy}')
        predictions = [(word, tag) for sentence in test_set for (word,
                        tag) in tagger.tag(nltk.untag(sentence))]
        wrong_predictions = [(word, tag, actual) for ((word,
                             tag), (_, actual)) in zip(predictions,[(w,
                             t) for sentence in test_set for (w,
                             t) in sentence]) if tag != actual and tag is not None]
        fd = nltk.FreqDist(wrong_predictions)
        print('Performing analysis...')
        print('Frequency Distribution of wrong predictions...')
        return fd
