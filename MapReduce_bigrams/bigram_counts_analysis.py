#!/usr/bin/python


from mrjob.job import MRJob
import re


word_pattern = re.compile(r"\b[\w']+\b")


class BiGramFreqCount(MRJob):

    def mapper_step1(self, _, line):
        lines = word_pattern.findall(line)
        for i in range(len(lines)-1):
            yield (lines[i].lower()+' '+lines[i+1].lower(), 1)

    def reducer_step1(self, key, values):
        yield (key, sum(values))

    def mapper_step2(self, bigram, count):
        split_words = word_pattern.findall(bigram)
        yield (split_words[0], [split_words[1], float(count)])

    def reducer_step2(self, first_word, sec_words_counts):
        second_words = []
        second_counts = []
        total_count = 0
        for value in sec_words_counts:
            second_words.append(value[0])
            second_counts.append(int(value[1]))
            total_count = total_count + value[1]
        probs = [float(count)/total_count for count in second_counts]
        values_list = zip(second_words, second_counts, probs)
        values_list_sort = sorted(values_list, key=lambda x: -x[2])
        yield (first_word, values_list_sort)

    def steps(self):
        return [
            self.mr(mapper=self.mapper_step1, reducer=self.reducer_step1),
            self.mr(mapper=self.mapper_step2, reducer=self.reducer_step2)
        ]


if __name__ == '__main__':
    BiGramFreqCount.run()
