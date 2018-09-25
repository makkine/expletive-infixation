#!/usr/bin/python
import sys
import random

global phones
global vocab
global vowels

#Given CMU's phonetic dictionary, creates a python dict
#dict keys are words in all-caps, vals are phonetic representation
def create_dict(txtfile):
	vocab = {}
	with open(txtfile) as f:
		for line in f:
			vocab[line.split(" ", 1)[0]] = line.split(" ", 1)[1]
	return vocab

def create_phdict(txtfile):
	vocab = {}
	with open(txtfile) as f:
		for line in f:
			vocab[line.split("	", 1)[0]] = line.split("	", 1)[1]
	vocab[""] = ""
	return vocab

##Finds the last stressed vowel
def find_stress(word):
	if word not in vocab:
		return
	w = vocab[word].split(" ")
	i = -1
	j = -1
	l = -1
	for ph in w:
		if ph == "":
			continue
		if phones[ph[0]] == "vowel\n":
			i += 1
			if ph[-1] == "1":
				j = i 
			elif ph[-1] == "2":
				l = i
	return (j, l) 

#finds the indexes of the vowels
def vowel_idx(word): 
	vowel_idx = []
	for l in range(len(word)):
		if word[l] in vowels:
			if l > 0:
				if word[l-1] not in vowels:
					vowel_idx.append(l)
			else:
				vowel_idx.append(l)

	return vowel_idx

def split_onset(word, stress, vidx, infix):
	onsets = ["sh", "pl", "bl", "gl", "cl", "tr", "dr", "pr", "br", "cr", "gr", "tw", "dw",
				"fl", "sl", "fr", "sw", "sp", "st", "sk", "th", "ch", "sm", "sn", "ph", 
				"spl", "spr", "str", "q", "r", "t", "y", "p", "s", "d", "f", "g", "h", "j", "k", 
				"l", "z", "x", "c", "v", "b", "n", "m", "scr", "w"]

	i = 1

	while(word[vidx[stress-1]+i : vidx[stress]] != ""):
		if word[vidx[stress-1]+i : vidx[stress]].lower() in onsets:
			return word[:vidx[stress-1]+i ] + infix + word[vidx[stress-1]+i :]
		else: 
			i+= 1

def infix(word, sent):
	onsets = ["sh", "pl", "bl", "gl", "cl", "tr", "dr", "pr", "br", "cr", "gr", "tw", "dw",
				"fl", "sl", "fr", "sw", "sp", "sc", "st", "sk", "th", "ch", "sm", "sn", "ph", 
				"spl", "spr", "str", "q", "r", "t", "y", "p", "s", "d", "f", "g", "h", "j", "k", 
				"l", "z", "x", "c", "v", "b", "n", "m", "scr", "w"]

	infixes = ["-fucking-", "-motherfucking-", "-goddamn-", "-bloody-"]

	infix = random.choice(infixes)

	stress = find_stress(word.upper())
	vidx = vowel_idx(word.upper())

	if stress == None:
		return (word, 0)

	if len(vidx) == 0:
		return (word, 0)

	i = 0

	if stress[0] > 0:
		#Case one: (best case). Primary stress in the second+ syllable
		return (split_onset(word, stress[0], vidx, infix), 1)

	else:
		#case two: Secondary stress 
		if stress[1] > 0:
			return (split_onset(word, stress[1], vidx, infix), .8)
		else:
			#Case three: Infix after onset
			if vidx[0] != 0:
				return (word[:vidx[0]] + infix + word[vidx[0]:], .3)
			#case four: no secondary stress, word starts in vowel, primary stress on the 
			#first syllable (e.g - "apple"). No infixation is possible
			else:
				if sent:
					return (word, 0)
				return ("I couldn't find a point for infix-goddamn-ation, you smart-fucking-ass. \
					Learn some English phono-motherfucking-tactics then get back to me.", 0)

def sentence_analysis(sent):
	st = ""
	s = sent.split(" ")

	if len(s) == 1:
		return(infix(sent, False)[0])
	else: 
		for w in s:
			inf = infix(w, True)
			if random.random() < inf[1]:
				st += inf[0] + " "
			else: 
				st += w + " "
	return st


def main(argv):
	global vocab
	vocab = create_dict("./cmudict.0.6d.txt")
	txtphones = "./phones.txt"

	global phones
	phones = create_phdict(txtphones)

	global vowels
	vowels = ["A", "E", "I", "O", "U"]

	s = ""
	while s != "QUIT" and s != "Q":
		s = input('--->	')
		print(sentence_analysis(s))


if __name__ == "__main__":
	main(sys.argv[1:])