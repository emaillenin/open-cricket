# Natural Language Toolkit: Cricket Player Corpus Reader
#
# Copyright (C) 2014 - The Open Cricket Project
# Author: Lenin Raj Rajasekaran <emaillenin@gmail.com>
# URL: <http://duggout.com/open-cricket/>

import nltk


class TrainCricketPlayers():

    def __init__(self, trained_pickle_file_path):
        self.tagger = nltk.data.load(trained_pickle_file_path)

    def get_names(self, input):
        tokens = nltk.word_tokenize(input)
        tags = self.tagger.tag(tokens)
        return [p[0] for p in tags if p[1] == 'NNP']