import math
import itertools
import copy

class ngram_score(object):
    def __init__(self, ngramfile, sep=' '):
        self.ngrams = {}
        f = open(ngramfile, 'r')
        for line in f:
            line = line.lower()
            gram, count = line.split(sep)
            self.ngrams[gram] = int(count)
        self.L = len(gram)
        self.N = sum(self.ngrams.values())
        for key in self.ngrams.keys():
            self.ngrams[key] = math.log10(float(self.ngrams[key]) / self.N)
        self.minval = math.log10(0.01 / self.N)

    def score(self, text):
        score = 0
        for i in range(len(text) - self.L + 1):
            if text[i:i+self.L] in self.ngrams:
                # print('%s %d' %(text[i:i+self.L], score))
                score += self.ngrams[text[i:i+self.L]]
            else:
                score += self.minval
        return score


bigram_score = ngram_score('bigram_freq.txt')
trigram_score = ngram_score('trigram_freq.txt')
quadgram_score = ngram_score('quadgram_freq.txt')
time = 5


def scoring(key, text):
    decypher_text = ""
    for i in text:
        decypher_text += key[i]
    score = trigram_score.score(decypher_text)
    return score


if __name__ == '__main__':
    ciphertext_file = 'ciphertext.txt'
    cipher_flag = ""
    with open(ciphertext_file, 'r') as ctf:
        ciphertext = ctf.readline()
    for i in ciphertext:
        cipher_flag += i
        if i == '}':
            break
    ciphertext = ciphertext[len(cipher_flag):-1].lower()
    table = [w for w in "etaonrishdlfcmugypwbvkjxqz"]
    # table = [w for w in "etaoinshrdlcumwfgypbvkjxqz"]
    transfer = {}
    unifreq = {}
    bifreq = {}
    trifreq = {}
    bigram = ""
    trigram = ""
    for i in table:
        unifreq[i] = 0
    for i in ciphertext:
        unifreq[i] += 1
        if len(bigram) < 2:
            bigram += i
        else:
            if bigram not in bifreq:
                bifreq[bigram] = 1
            else:
                bifreq[bigram] += 1
            bigram = ""
        if len(trigram) < 3:
            trigram += i
        else:
            if trigram not in trifreq:
                trifreq[trigram] = 1
            else:
                trifreq[trigram] += 1
            trigram = ""

    uni_sort_list = sorted(unifreq.items(), key=lambda x: x[1], reverse=True)
    bi_sort_list = sorted(bifreq.items(), key=lambda x: x[1], reverse=True)
    tri_sort_list = sorted(trifreq.items(), key=lambda x: x[1], reverse=True)
    print("================")
    print(uni_sort_list)
    print(bi_sort_list)
    print(tri_sort_list)
    index = 0
    for w in uni_sort_list:
        transfer[w[0]] = table[index]
        index += 1
    print("================")
    print(transfer)
    
    key_list = list(transfer.keys())
    value_list = list(transfer.values())
    test = 0
    for w, v in bi_sort_list:
        # solve 'he' or 'th'
        if transfer[w[1]] == 'e':
            temp = copy.deepcopy(transfer[w[0]])
            if temp != 'h':   
                transfer[w[0]] = 'h'
                transfer[key_list[value_list.index('h')]] = temp
        else:
            temp = copy.deepcopy(transfer[w[0]])
            if temp != 't':
                transfer[w[0]] = 't'
                transfer[key_list[value_list.index('t')]] = temp

            temp = copy.deepcopy(transfer[w[1]])
            if temp != 'h':
                transfer[w[1]] = 'h'
                transfer[key_list[value_list.index('h')]] = temp
        break

    print("================")
    print(transfer)
    score = scoring(transfer, ciphertext)
    print(score)
    for epoch in range(time):
        for i in 'abcdefghijklmnopqrstuvwxyz':
            for j in 'abcdefghijklmnopqrstuvwxyz':
                cur_key = copy.deepcopy(transfer)
                cur_key[i] = transfer[j]
                cur_key[j] = transfer[i]
                cur_score = scoring(cur_key, ciphertext)
                if cur_score > score:
                    score = cur_score
                    transfer = cur_key
            print(score)
            print(transfer)

    decrypte_flag = ""
    decrypte_text = ""
    for i in cipher_flag.lower():
        if i in transfer:
            decrypte_flag += transfer[i].upper()
        else:
            decrypte_flag += i
    print(decrypte_flag)
    for i in ciphertext:
        decrypte_text += transfer[i]
    print("=============================")
    print(ciphertext[:300])
    print("============================")
    print(decrypte_text[:300])
    print("============================")
    key = ""
    for i in 'abcdefghijklmnopqrstuvwxyz':
        for j in transfer:
            if transfer[j] == i:
                key += j
    print(key)