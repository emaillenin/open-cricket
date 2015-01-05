# Natural Language Toolkit: Cricket Player Corpus Reader
#
# Copyright (C) 2014 - The Open Cricket Project
# Author: Lenin Raj Rajasekaran <emaillenin@gmail.com>
# URL: <http://duggout.com/open-cricket/>

import nltk


class TrainCricketPlayers():

    def __init__(self, trained_picke_file_path):
        self.tagger = nltk.data.load(trained_picke_file_path)

    def get_names(self, input):
        tokens = nltk.word_tokenize(input)
        return self.tagger.tag(tokens)