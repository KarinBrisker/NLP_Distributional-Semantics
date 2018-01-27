
import numpy as np
import sys


def most_similar(word, k):
    word_index = lemmas[word]
    word_vector = words2vec_matrix[word_index]
    k_similar = []

    distances = np.dot(words2vec_matrix, word_vector)

    distances[word_index] = -float('inf')
    for i in range(k):
        min_dist_index = np.argmax(distances)
        k_similar.append(int2lemma[min_dist_index])
        distances[min_dist_index] = -float('inf')
    return k_similar


if __name__ == '__main__':
    words_file = sys.argv[1]
    context_file = sys.argv[2]

    print '### Loading word vectors ###'
    lemmas = {}
    f_words = open(words_file, 'r')
    num_words = 0
    for line in f_words:
        line = line.strip()
        vector = line.split(' ')
        lemmas[vector[0]] = np.array(vector[1:], dtype=np.float)
        num_words += 1
        if num_words % 25000 == 0:
            print num_words, ' words loaded...'
    f_words.close()

    vec_size = 0
    for lemma in lemmas:
        vec_size = len(lemmas[lemma])
        break

    words2vec_matrix = np.zeros((len(lemmas) ,vec_size))
    int2lemma = {}
    curr_word = 0
    for lemma in lemmas:
        vec = lemmas[lemma]
        vec /= np.linalg.norm(vec)
        words2vec_matrix[curr_word] = vec
        lemmas[lemma] = curr_word
        int2lemma[curr_word] = lemma
        curr_word += 1

    words_to_check = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb',
                      'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']
    for word in words_to_check:
        k_sim = most_similar(word, 20)
        print '###', word, '###'
        for lem2 in k_sim:
            print lem2, ',',
        print ''

    print '\n### Saving vectors of the 12 words to check on, and deleting everthing else ###\n'
    words2vecs = np.zeros((len(words_to_check), vec_size))
    max_distances = {}
    for i in range(len(words_to_check)):
        words2vecs[i, :] = words2vec_matrix[lemmas[words_to_check[i]]]
        max_distances[i] = []

    del words2vec_matrix
    del lemmas
    del int2lemma

    print '### Loading Context vectors ###'
    contexts = {}
    f_contexts = open(context_file, 'r')
    num_words = 0
    holds_n_distances = 0
    for line in f_contexts:
        line = line.strip()
        vector = line.split(' ')
        context = vector[0]
        context_vector = np.array(vector[1:], dtype=np.float)

        distances = np.dot(words2vecs, context_vector)
        for i in range(len(distances)):
            max_distances[i].append([distances[i], context])
        holds_n_distances += 1

        if holds_n_distances == 10000:
            holds_n_distances = 0
            for i in range(len(max_distances)):
                max_distances[i] = sorted(max_distances[i], reverse=True)[0:11]

        num_words += 1
        if num_words % 25000 == 0:
            print num_words, ' contexts checked...'
    f_contexts.close()

    for i in range(len(max_distances)):
        max_distances[i] = sorted(max_distances[i], reverse=True)[1:11]
        print '###', words_to_check[i], '###'
        for j in range(10):
            print max_distances[i][j][1], ',',
        print ''
