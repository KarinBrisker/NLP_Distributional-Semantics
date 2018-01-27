

tags_set = set()
tags_set.update(
    ['RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
     'WRB', 'JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS'])


def check_tag(tag):
    if tag in tags_set:
        return True
    return False


def analyze_wiki_file(filename, onlyContextWords):
    lemma2index = {}
    index2lemma = {}
    depend2index = {}
    lemma_counter = {}
    num_lemmas = 0
    num_dependencies = 0

    print '### Going over \'', filename, '\' 1/2 times to learn lemma counter dict ###'
    f = open(filename, 'r')
    for line in f:
        line = line.strip()
        if line != '':
            fields = line.split('\t')
            lemma = fields[2]
            dependency = fields[7]
            pos_tag = fields[3]
            if onlyContextWords and not check_tag(pos_tag):
                continue
            if lemma not in lemma2index:
                lemma2index[lemma] = num_lemmas
                index2lemma[num_lemmas] = lemma
                lemma_counter[num_lemmas] = 0
                num_lemmas += 1
            lemma_counter[lemma2index[lemma]] += 1
            if dependency not in depend2index:
                depend2index[dependency] = num_dependencies
                num_dependencies += 1
    f.close()
    print '### Finished going over \'', filename, '\' 1/2 times ###\n'
    return lemma2index, index2lemma, lemma_counter, depend2index


def depparse_to_sentence_co_occurring(filename):
    lemma2index, index2lemma_big, lemma_counter, depend2index = analyze_wiki_file(filename, True)
    index2lemma = {}
    context_lemma_counter = {}
    for lemma in lemma_counter:
        if lemma_counter[lemma] > 2:
            context_lemma_counter[lemma] = {}
        if lemma_counter[lemma] >= 100:
            index2lemma[lemma] = index2lemma_big[lemma]
    print len(context_lemma_counter), len(index2lemma)

    print '### going over \'', filename, '\' 2/2 times to create sentence co occurrence matrix ###'
    f = open(filename, 'r')
    num_cont = 0
    sen_c = 0
    sentence = []
    for line in f:
        line = line.strip()
        if line == '':
            num_words = len(sentence)
            for i in range(num_words - 1):
                lemma1 = sentence[i]
                for j in range(i + 1, num_words, 1):
                    lemma2 = sentence[j]
                    if lemma2 in index2lemma:
                        if lemma2 not in context_lemma_counter[lemma1]:
                            context_lemma_counter[lemma1][lemma2] = 0
                        context_lemma_counter[lemma1][lemma2] += 1
                    if lemma1 in index2lemma:
                        if lemma1 not in context_lemma_counter[lemma2]:
                            context_lemma_counter[lemma2][lemma1] = 0
                        context_lemma_counter[lemma2][lemma1] += 1
                    num_cont += 1
            sentence = []
            sen_c += 1
            # if sen_c % 80000 == 0:
            #     print sen_c / 800000.0, 'complete...'
        else:
            fields = line.split('\t')
            tag = fields[3]
            if check_tag(tag):
                lemma = lemma2index[fields[2]]
                if lemma_counter[lemma] > 2:
                    sentence.append(lemma)
    f.close()
    print '\n### Finished going over \'', filename, '\' 2/2 times ###\n'
    return lemma2index, index2lemma, index2lemma_big, lemma_counter, depend2index, context_lemma_counter, num_cont


def depparse_to_window_co_occurring(filename):
    lemma2index, index2lemma_big, lemma_counter, depend2index = analyze_wiki_file(filename, True)
    index2lemma = {}
    context_lemma_counter = {}
    for lemma in lemma_counter:
        if lemma_counter[lemma] > 2:
            context_lemma_counter[lemma] = {}
        if lemma_counter[lemma] >= 100:
            index2lemma[lemma] = index2lemma_big[lemma]
    print len(context_lemma_counter), len(index2lemma)

    print '### going over \'', filename, '\' 2/2 times to create sentence co occurrence matrix ###'
    f = open(filename, 'r')
    num_cont = 0
    sen_c = 0
    sentence = []
    for line in f:
        line = line.strip()
        if line == '':
            num_words = len(sentence)
            for i in range(num_words):
                lemma1 = sentence[i]
                sub_sent = sentence[i-2:i]
                for lemma2 in sub_sent:
                    if lemma2 in index2lemma:
                        if lemma2 not in context_lemma_counter[lemma1]:
                            context_lemma_counter[lemma1][lemma2] = 0
                        context_lemma_counter[lemma1][lemma2] += 1
                    num_cont += 1
                sub_sent = sentence[i + 1:i + 3]
                for lemma2 in sub_sent:
                    if lemma2 in index2lemma:
                        if lemma2 not in context_lemma_counter[lemma1]:
                            context_lemma_counter[lemma1][lemma2] = 0
                        context_lemma_counter[lemma1][lemma2] += 1
                    num_cont += 1
            sentence = []
            sen_c += 1
            if sen_c % 80000 == 0:
                print sen_c / 800000.0, 'complete...'
        else:
            fields = line.split('\t')
            tag = fields[3]
            if check_tag(tag):
                lemma = lemma2index[fields[2]]
                if lemma_counter[lemma] > 2:
                    sentence.append(lemma)
    f.close()
    print '\n### Finished going over \'', filename, '\' 2/2 times ###\n'
    return lemma2index, index2lemma, index2lemma_big, lemma_counter, depend2index, context_lemma_counter, num_cont

def depparse_to_dependencies_co_occurring(filename):
    lemma2index, index2lemma_big, lemma_counter, depend2index = analyze_wiki_file(filename, True)
    index2lemma = {}
    attr_counter = {}
    attr_lemma_counter = {}
    for lemma in lemma_counter:
        if lemma_counter[lemma] >= 100:
            index2lemma[lemma] = index2lemma_big[lemma]
    print len(index2lemma)

    print '### going over \'', filename, '\' 2/2 times to create sentence co occurrence matrix ###'
    f = open(filename, 'r')
    num_cont = 0
    sen_c = 0
    sentence = []
    for line in f:
        line = line.strip()
        if line == '':
            sentence = remove_prepositions(sentence)
            for lemma_data in sentence:
                lemma, _, head, depend, children, isPrep = lemma_data
                if not isPrep:
                    lemma = lemma2index[lemma]
                    if lemma in index2lemma:
                        if head != 0:
                            if sentence[head - 1][0] in lemma2index:
                                headLemma = lemma2index[sentence[head - 1][0]]
                                if lemma_counter[lemma] > 2:
                                    headAttr = str(headLemma) + '|+' + depend
                                    if headAttr not in attr_lemma_counter:
                                        attr_lemma_counter[headAttr] = {}
                                    if lemma not in attr_lemma_counter[headAttr]:
                                        attr_lemma_counter[headAttr][lemma] = 0
                                    attr_lemma_counter[headAttr][lemma] += 1
                                    num_cont += 1
                        for child in children:
                            cLemma = lemma2index[sentence[child][0]]
                            if lemma_counter[lemma] > 2:
                                cDepend = sentence[child][3]
                                chAttr = str(cLemma) + '|-' + cDepend
                                if chAttr not in attr_lemma_counter:
                                    attr_lemma_counter[chAttr] = {}
                                if lemma not in attr_lemma_counter[chAttr]:
                                    attr_lemma_counter[chAttr][lemma] = 0
                                attr_lemma_counter[chAttr][lemma] += 1
                                num_cont += 1
            sentence = []
            sen_c += 1
            # if sen_c % 80000 == 0:
            #     print sen_c / 800000.0, 'complete...'
        else:
            fields = line.split('\t')
            tag = fields[3]
            lemma = fields[2]
            head = int(fields[6])
            depend_to_head = fields[7]
            data = [lemma, tag, head, depend_to_head, [], False]
            sentence.append(data)
    f.close()
    print '\n### Finished going over \'', filename, '\' 2/2 times ###\n'
    for attr in attr_lemma_counter:
        attr_counter[attr] = 0
        for lemma in attr_lemma_counter[attr]:
            attr_counter[attr] += attr_lemma_counter[attr][lemma]
    print 'number of attributes:', len(attr_lemma_counter)
    return lemma2index, index2lemma, index2lemma_big, lemma_counter, attr_counter, depend2index, attr_lemma_counter, num_cont


def remove_prepositions(sentence):
    for i in range(len(sentence)):
        head = sentence[i][2]
        tag = sentence[i][1]
        if check_tag(tag):
            if head == 0:
                continue
            sentence[head - 1][4].append(i)
        else:
            sentence[i][5] = True

    for i in range(len(sentence)):
        lemma, tag, head, depend, children, _ = sentence[i]
        if head == 0:
            continue
        if not check_tag(tag):
            for c in children:
                sentence[head - 1][4].append(c)
                sentence[c][2] = head
                sentence[c][3] = lemma + ' ' + sentence[c][3]
    return sentence
