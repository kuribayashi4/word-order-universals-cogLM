# modified the code from https://github.com/rycolab/artificial-languages

import argparse

def total_sentence_score(words):
    score = 0
    for w in words:
        score += float(w.split(' ')[1][1:-1])
    return score

parser = argparse.ArgumentParser(
    description = "Get sentence scores from eval output file")

parser.add_argument("-i", "--input_file", type=str, required=True, 
    help="Path to input file")

parser.add_argument("-O", "--output_file", type=str, required=True,
    help="Location of output file")

args = parser.parse_args()


file = open(args.input_file, 'r')
all_lines = file.readlines()
all_lines = [l for l in all_lines if len(l.split('|')) > 3]
word_score_lines = [l.split('|')[3][1:] for l in all_lines if l.split(
    '|')[3].split(' ')[1].isnumeric()]
word_score_lines.sort(key=lambda a:int(a.split(' ')[0]))
full_text = ""
for line in word_score_lines:
    full_text += ' '.join(line.split(' ')[1:]).strip('\n') + " "
sentences = []
start = 0
words = full_text.split("\t")
for i in range(len(words)):
    if words[i].split(' ')[0] == "</s>":
        sentences.append(words[start:i+1])
        start = i+1
sentence_scores = []
for s in sentences:
    sentence_scores.append(total_sentence_score(s))
output_file = open(args.output_file, "w")
for s in sentence_scores:
    output_file.write(str(s) + "\n")
