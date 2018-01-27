


def compute_similarities(word_vec, attr_words_vec_table, only_between):
    similarity_results = {}
    for lemma in only_between:
        similarity_results[lemma] = 0
    for attr_index in word_vec:
        w1 = word_vec[attr_index]
        attr_words_vec = attr_words_vec_table[attr_index]
        for word_index in attr_words_vec:
            if word_index in only_between:
                w2 = attr_words_vec[word_index]
                similarity_results[word_index] += w1 * w2
    return similarity_results
