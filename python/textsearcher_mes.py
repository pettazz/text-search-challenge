import string, re

class TextSearcher(object):

    def __init__(self):
        self.word_map = {}
        self.lines = []

    def load(self, file_path:str)->bool: 
        word_regex = r'[A-z0-9\'\-]+'

        try:
            with open(file_path) as f:
                line_count = 0
                for line in f:
                    words_split = line.strip().split()
                    self.lines.append(words_split)

                    word_count = 0
                    for word_full in words_split:
                        word = re.match(word_regex, word_full).group(0)
                        # check for multiple?

                        if word in self.word_map.keys():
                            self.word_map[word].append((line_count, word_count))
                        else:
                            self.word_map[word] = [(line_count, word_count)]

                        word_count +=1 
                    line_count += 1

            return True
        except Exception as e:
            # handle errors!
            print(e)
            return False

        # split each line by words, 
        # add each word to the big ordered list of words, 
        # add each position in that array to the lookup dict referencing their indices
    
    def search(self, word:str, context:int=0)->list:
        result = []
        if word.lower() in self.word_map.keys():
            str_found = ""
            for matched_words in self.word_map[word.lower()]:
                start_line, start_idx = matched_words

                line_idx = start_line
                word_idx = start_idx - 1
                pre_words = 0
                while pre_words < context:
                    if word_idx < 0:
                        line_idx -= 1
                        if line_idx < 0:
                            break
                        word_idx = len(self.lines[line_idx])
                    str_found = self.lines[line_idx][word_idx] + " " + str_found
                    word_idx -= 1
                    pre_words += 1

                str_found += self.lines[start_line][start_idx]

                line_idx = start_line
                word_idx = start_idx + 1
                post_words = 0
                while post_words < context:
                    if word_idx >= len(self.lines[line_idx]):
                        line_idx += 1
                        if line_idx >= len(self.lines):
                            break
                        word_idx = 0
                    str_found +=  " " + self.lines[line_idx][word_idx]
                    word_idx += 1
                    post_words += 1
            result.append(str_found)

        return result

        # get all the indices from lookup dict
        # grab all the words from index i - context : i + context (check for start/end)
        

