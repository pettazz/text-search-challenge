import re


class TextSearcher(object):

    def __init__(self):
        # a map of search terms to word list indices 
        self.word_map = {}
        # ordered list of all the source text words as-is
        self.words = []

    @staticmethod
    def __tokenize(word: str, default: str = "") -> str:
        word_regex = r"([A-z0-9\'\-]+)"
        matches = re.findall(word_regex, word.lower())

        # if the search contains multiple words with punctuation
        # between, ignore that and make a single searchable term
        return "".join(matches) if matches else default

    def load(self, file_path: str) -> bool:
        self.word_map = {}
        self.words = []

        try:
            with open(file_path) as f:
                for line in f:
                    for full_word in line.strip().split():
                        self.words.append(full_word)
                        idx = len(self.words) - 1
                        search_word = self.__tokenize(full_word)

                        if search_word in self.word_map:
                            self.word_map[search_word].append(idx)
                        else:
                            self.word_map[search_word] = [idx]

            return True
        except Exception as e:
            print(e) # insert actual error handling here
            return False

    def search(self, word: str, context: int = 0) -> list:
        result = []
        search_word = self.__tokenize(word, None)
        if search_word and search_word in self.word_map:
            for match_idx in self.word_map[search_word]:
                # ensure we don't go beyond start/end
                pre_idx = max(match_idx - context, 0)
                post_idx = min(match_idx + context + 1, len(self.words))

                found_str = " ".join(self.words[pre_idx:post_idx])
                result.append(found_str)

        return result
