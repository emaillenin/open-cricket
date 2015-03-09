#!/usr/bin/python
import fnmatch

import sys
import codecs
import os
import nltk
import collections
import json


def enrich_full_name(players):
    for i, s in enumerate(players):
        for p in players:
            if len(p) > len(s) and s in p:  # Different string
                # TODO In this step, make a learning that s refers to p. Machine learning ;)
                players[i] = p
                break
    return players


config = {}


def archive_file(root, filename, archive_dir):
    os.rename(os.path.join(root, filename), os.path.join(archive_dir + root.split('/')[-1], filename))


def create_dir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def main():
    if len(sys.argv) == 2:
        config = json.load(open(sys.argv[1], 'r'))

    if len(config) == 0:
        print('No Data directory. Exiting...')
        exit(2)
    elif not os.path.isdir(config['input_dir']):
        print('Data directory does not exist. Exiting...')
        exit(2)

    for root, dirnames, filenames in os.walk(config['input_dir']):
        if 'feed_' in root.split('/')[-1]:
            print("Scanning " + root)

            # Create archive directory
            create_dir_if_not_exists(config['archive_dir'] + root.split('/')[-1])

            # Create input directory for impressions
            impressions_input_dir = config['input_dir'] + 'impressions_' + root.split('/')[-1].split('_')[1]
            create_dir_if_not_exists(impressions_input_dir)

            for fpath in fnmatch.filter(filenames, '*.txt'):
                f = os.path.join(root, fpath)
                sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                fpeople = []
                with codecs.open(f, "r",encoding='utf-8') as fdata:
                    data = fdata.read().replace('\n', '').strip()
                    sents = sent_tokenizer.tokenize(data)
                    for s in sents:
                        chunks = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(s)))
                        people = [c for c in chunks if c.__class__.__name__ == 'Tree' and c.label() == 'PERSON']
                        if len(people) > 0:
                            for p in people:
                                fpeople.append(' '.join([e[0] for e in p]))
                with codecs.open(os.path.join(impressions_input_dir, os.path.basename(f)), 'w', encoding='utf-8') as fwrite:
                    fwrite.write(json.dumps((collections.Counter(enrich_full_name(fpeople)))))
                print('Completed processing ' + f)
                archive_file(root, os.path.basename(f), config['archive_dir'])
    else:
        print('No input files found. Exiting...')
        exit(0)


if __name__ == '__main__':
    main()
