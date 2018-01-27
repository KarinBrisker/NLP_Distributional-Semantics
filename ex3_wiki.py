
import sys
import math
import gc
import data_reader as dr
import sparse_vectors_similarity as svs


if __name__ == '__main__':
    wiki_corpus_file = sys.argv[1]
    att_type = sys.argv[2]

    if att_type == 'b':
        lemma2index, index2lemma, index2lemma_big, lemma_counter, depend2index, context_lemma_counter, num_cont = \
            dr.depparse_to_window_co_occurring(wiki_corpus_file)
        attr_counter = lemma_counter
    elif att_type == 'a':
        lemma2index, index2lemma, index2lemma_big, lemma_counter, depend2index, context_lemma_counter, num_cont = \
            dr.depparse_to_sentence_co_occurring(wiki_corpus_file)
        attr_counter = lemma_counter
    elif att_type == 'c':
        lemma2index, index2lemma, index2lemma_big, lemma_counter, attr_counter, depend2index, context_lemma_counter, num_cont = \
            dr.depparse_to_dependencies_co_occurring(wiki_corpus_file)
    else:
        print 'incorrect given option, enter {a,b} as the second param.'
        exit()
    gc.collect()

    words_to_check = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb',
                      'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']

    smoothed_p_w = 0
    p_w = 0
    for lemma in lemma_counter:
        p_w += lemma_counter[lemma]
        smoothed_p_w += lemma_counter[lemma] ** 0.75

    print '### Turning counts to PMIs ###'
    for context in context_lemma_counter:
        # clc = context_lemma_counter[context]
        for lemma in context_lemma_counter[context]:
            p_wc = context_lemma_counter[context][lemma] / float(num_cont)
            p_w = (lemma_counter[lemma] ** 0.75) / float(smoothed_p_w)
            p_c = attr_counter[context] / float(num_cont)
            if p_wc == 0:
                context_lemma_counter[context][lemma] = 0
            else:
                # print p_wc, p_w, p_c
                context_lemma_counter[context][lemma] = math.log(p_wc / (p_w * p_c), math.e)
            if context_lemma_counter[context][lemma] < 0:
                context_lemma_counter[context][lemma] = 0
    gc.collect()

    print '### Calculating sqrt(V^2) for the lemmas that passed the threshold ###\n'
    sqr_sums = {}
    for lemma in index2lemma:
        sqr_sums[lemma] = 0
    total = len(context_lemma_counter)
    prog = total / 10
    curr = 0
    for attr in context_lemma_counter:
        for lemma in context_lemma_counter[attr]:
            sqr_sums[lemma] += context_lemma_counter[attr][lemma]**2
        curr += 1
        if prog > 0:
            if curr % prog == 0:
                print curr, 'out of', total, 'complete...'
    for lemma in sqr_sums:
        sqr_sums[lemma] = math.sqrt(sqr_sums[lemma])

    print '### Creating lemma_context vectors for the 12 words to check for ###\n'
    lemma_context_counter = {}
    for word in words_to_check:
        lemma = lemma2index[word]
        lemma_context_counter[lemma] = {}
        for context in context_lemma_counter:
            if lemma in context_lemma_counter[context]:
                lemma_context_counter[lemma][context] = context_lemma_counter[context][lemma]
    gc.collect()

    def keywithmaxval(d):
        v = list(d.values())
        k = list(d.keys())
        return k[v.index(max(v))]

    print '### Calculating cosine distances ###\n'
    for i in range(len(words_to_check)):
        lemma = lemma2index[words_to_check[i]]
        sims = svs.compute_similarities(lemma_context_counter[lemma], context_lemma_counter, index2lemma)
        lemma_norm = sqr_sums[lemma]
        for lemma2 in sims:
            sims[lemma2] /= (lemma_norm * sqr_sums[lemma2])
        sims[lemma] = -float('inf')
        print '\n####', words_to_check[i], '####'
        for l in range(20):
            m = keywithmaxval(sims)
            print index2lemma[m], ',',
            sims[m] = -float('inf')

    print '\n\n### CONTEXTS ###\n'

    for word in words_to_check:
        lemma = lemma2index[word]
        vec_dict = lemma_context_counter[lemma]
        print '\n####', word, '####'
        for l in range(20):
            m = keywithmaxval(vec_dict)
            vec_dict[m] = -float('inf')
            if att_type == 'c':
                m = index2lemma_big[int(m.split('|')[0])] + ' ' + m.split('|')[1]
            if att_type == 'b' or att_type == 'a':
                m = index2lemma_big[int(m)]
            print m, ',',