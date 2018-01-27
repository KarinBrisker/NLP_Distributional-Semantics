
import math


def pmi_calc(word, context, context_word_counter, context_counter, word_counter, num_cont):
    p_wc = context_word_counter[context][word]
    p_w = word_counter[word]
    p_c = context_counter[context]
    if p_wc == 0:
        return 0
    res = math.log((p_wc * num_cont) / (p_w * p_c), math.e)
    if res < 0:
        return 0
    return res
