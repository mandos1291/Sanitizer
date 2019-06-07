import re
from collections import Counter

"""
    Name: SanitizerTokenizer
    Description: This method contains only static methods that help to sanitize a text. Some methods also tokenize the text.
    Author: Matthias Christe
    Date: 07.06.2019

"""

class SanitizerTokenizer:
    """
        This class contains one public method sanitize_sentences which will clean the sentences following the rules decided by the class
        That means:
            - removing non-letter, but keeping dots and commas
            - removing non usefull spaces
            - lowercase
    """

    PUNKT_STR = "<PUNKT>"
    PUNCTUATION = ".,!?;:\)\]"
    BRACKETS_OPENING ="\(\["

    @classmethod
    def keep_dashes(cls, sentence: str) -> str:
        # regex rule for removing non-letter but keeping dashes, keep only letters and dashes
        regex = "[^\w \-]|\d|_"
        return re.sub(regex, " ", sentence)

    @classmethod
    def remove_manyspaces(cls, sentence: str) -> str:
        return re.sub(r'\s+', ' ', sentence)

    @classmethod
    def lowercase_sentences(cls, sentence: str) -> str:
        return sentence.lower()

    @classmethod
    def replace_numbers(cls, sentence: str) -> str:
        """
        replace every number '10', '213', '21.3' ... by N
        """
        text = re.sub('[0-9]+',  'N', sentence) # converting number to char N

        # the following replace N.N with N, however if it's N.N.N.N..., it will not be replaced
        regexNN = "(?<!N\.)N\.N(?!\.N)"
        return re.sub(regexNN,  'N', text)

    @classmethod
    def replace_dots(cls, sentence: str) -> str:
        """
        replace dots with <PUNKT>, only those thare are followed by a letter or a number
        """
        return re.sub(r"(\.)(\w)", cls.PUNKT_STR+"\g<2>", sentence)

    @classmethod
    def split_perfect(cls, sentence: str) -> str:
        """
        split the sentences by keeping punctuation, but separate them from the words
        """
        regex = r"[\w'-]+|[" + cls.PUNCTUATION + cls.BRACKETS_OPENING + "]|"+cls.PUNKT_STR
        return re.findall(regex, sentence)

    @classmethod
    def join_remove_space_for_punctuation(cls, tokens: list) -> str:
        """
        remove spaces before any punctuation but keep it after
        """
        joint = " ".join(tokens)
        #remove space before punctuation for following symbols
        regex = r"\s([" + cls.PUNCTUATION + "](?:\s|$))"
        space_after_removed = re.sub(regex, r'\1', joint)
        #remove space after punctuation for following symbols
        regex = r"([" + cls.BRACKETS_OPENING + "])(?:\s|$)"
        space_before_removed = re.sub(regex, r'\1', space_after_removed)
        return space_before_removed

    @classmethod
    def replace_dots_back(cls, sentence: str) -> str:
        """
        replace <PUNKT> with .
        """
        return re.sub(" "+cls.PUNKT_STR+" ", ".", sentence)

    @classmethod
    def keep_most_common_words(cls, sentences: list, n_mostcommon=10000, unk_symbol="<unk>", verbose=False) -> list:
        """
        list the n most common words and replace the others words by <unk>. Punctuation should remain
        """
        #-------------------------------------------------------------------------------------------------------------#
        #-------------------------- Creation of the most common words Vocabulary -------------------------------------#
        #-------------------------------------------------------------------------------------------------------------#
        # use sanitization method to find words: words are lowercase, no punctuation and no unnecessary whitespaces
        san_sentences = [cls.sanitize_hard(sen) for sen in sentences]
        san_sentences_tokens = [sen.split(" ") for sen in san_sentences]
        san_sentences_tokens_flatten = [token for sen in san_sentences_tokens for token in sen ]
        # word counter
        counter_words = Counter()
        counter_words.update(san_sentences_tokens_flatten)
        # keep most common words
        counter_most_common_words = dict(counter_words.most_common(n_mostcommon))

        if verbose:
            tupleList_words_in = counter_words.most_common(n_mostcommon)
            all_words_count = sum([cnt for el, cnt in counter_words.most_common()])
            coverage = sum([cnt for el, cnt in tupleList_words_in])
            coverage_percentage = coverage/all_words_count * 100
            print("Coverage from most common words %d/%d (%.2f%%)" % (coverage, all_words_count, coverage_percentage))
            dictionary_size_most_common = len(counter_most_common_words.keys())
            dictionary_size_all = len(counter_words.keys())
            dictionary_usage_percentage = dictionary_size_most_common / dictionary_size_all * 100
            print("Dictionary size reduced from %d => %d (%.2f%%)" % (dictionary_size_all, dictionary_size_most_common, dictionary_usage_percentage))

        #-------------------------------------------------------------------------------------------------------------#
        #------------------------------ Replace non common words with unk_symbol -------------------------------------#
        #-------------------------------------------------------------------------------------------------------------#
        # replace special dots with symbol
        punkts_sentences = [cls.replace_dots(sen) for sen in sentences]
        # split the sentences by keeping punctuation, but separate them from the words
        perfect_splitted_sentences = [cls.split_perfect(sen) for sen in punkts_sentences]

        # keep punctuation and most common words only
        sentences_most_common = []
        for si, sen in enumerate(perfect_splitted_sentences):
            word_ack = []
            for word in sen:
                if word in cls.PUNCTUATION+cls.BRACKETS_OPENING:
                    # check punctuation
                    word_ack.append(word)
                elif word == cls.PUNKT_STR:
                    word_ack.append(word)
                elif word.lower() in counter_most_common_words:
                    # word in vocabulary, uppercase or lowercase not important
                    word_ack.append(word)
                else:
                    # word not in vocabulary replace non-common words with <unk>
                    word_ack.append(unk_symbol)

            # convert list of tokens to a string and remove spaces before punctuation
            word_ack = cls.join_remove_space_for_punctuation(word_ack)
            # convert <PUNKT> back to .
            word_ack = cls.replace_dots_back(word_ack)
            sentences_most_common.append(word_ack)

        return sentences_most_common

    @classmethod
    def sanitize_hard(cls, sentence: str) -> str:
        """
            - remove punctuation except dashes
            - unify whitespaces
            - lowercase sentences
        """
        sentence = cls.keep_dashes(sentence)
        sentence = cls.remove_manyspaces(sentence)
        sentence = cls.lowercase_sentences(sentence)
        return sentence

    @classmethod
    def sanitize_numbers(cls, sentence: str) -> str:
        """
            - unify whitespaces
            - replace numbers with N
        """
        sentence = cls.remove_manyspaces(sentence)
        sentence = cls.replace_numbers(sentence)
        return sentence

    @classmethod
    def sanitize_numbers_limit_commonwords(cls, sentences: list, n_mostcommon=10000, verbose=False) -> str:
        """
            - unify whitespaces
            - replace numbers with N
            - keep n most common words and replace other with <unk>
        """
        # sanitize every sentence
        sentences =  [cls.sanitize_numbers(s) for s in sentences]
        # this can only be done with all sentences in order to find the most common words
        sentences = cls.keep_most_common_words(sentences, n_mostcommon=n_mostcommon, verbose=verbose, unk_symbol="<unk>")
        return sentences

    @classmethod
    def sanitize_and_tokenize(cls, sen, sanitize_method):
        if isinstance(sen, str):
            return sanitize_method(sen).split()
        else:
            return [sanitize_method(s).split() for s in sen]
