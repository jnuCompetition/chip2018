import pandas as pd
import numpy as np
from config import opt
import pickle

# 文本处理
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tqdm import tqdm

def read_data_as_word():
    question = pd.read_csv(opt.raw_data_root + 'question_id.csv')
    question = question[['qid', 'wid', 'cid']]
    train = pd.read_csv(opt.raw_data_root + 'train.csv')
    test = pd.read_csv(opt.raw_data_root + 'test.csv')

    train = pd.merge(train, question, left_on=['qid1'], right_on=['qid'], how='left').drop(['qid'], axis=1)
    train = pd.merge(train, question, left_on=['qid2'], right_on=['qid'], how='left').drop(['qid'], axis=1)
    test = pd.merge(test, question, left_on=['qid1'], right_on=['qid'], how='left').drop(['qid'], axis=1)
    test = pd.merge(test, question, left_on=['qid2'], right_on=['qid'], how='left').drop(['qid'], axis=1)

    tokenizer = Tokenizer(num_words=opt.MAX_NB_WORDS)
    tokenizer.fit_on_texts(question['wid'])
    train_q1_word_seq = tokenizer.texts_to_sequences(train['wid_x'])
    train_q2_word_seq = tokenizer.texts_to_sequences(train['wid_y'])
    test_q1_word_seq = tokenizer.texts_to_sequences(test['wid_x'])
    test_q2_word_seq = tokenizer.texts_to_sequences(test['wid_y'])

    embeddings_index = {}
    with open(opt.raw_data_root + 'word_embedding.txt', 'r') as f:
        wordmat = f.read().split('\n')
        if wordmat[-1] == '': wordmat = wordmat[:-1]
        if wordmat[0] == '':  wordmat = wordmat[1:]

    for line in tqdm(wordmat):
        wvec = line.strip('\n').strip(' ').split('\t')
        embeddings_index[wvec[0]] = np.asarray(wvec[1:], dtype='float')
    # print('word embedding', len(embeddings_index))

    word_index = tokenizer.word_index
    nb_words = min(opt.MAX_NB_WORDS, len(word_index))
    word_embedding_matrix = np.zeros((nb_words + 1, opt.EMBEDDING_DIM))
    for word, i in word_index.items():
        if i > opt.MAX_NB_WORDS: continue
        embedding_vector = embeddings_index.get(str(word).upper())
        if embedding_vector is not None:
            word_embedding_matrix[i] = embedding_vector

    MAX_WORD_SEQUENCE_LENGTH = opt.MAX_WORD_SEQUENCE_LENGTH
    train_q1_word_seq = pad_sequences(train_q1_word_seq, maxlen=MAX_WORD_SEQUENCE_LENGTH, truncating='post', value=0)
    train_q2_word_seq = pad_sequences(train_q2_word_seq, maxlen=MAX_WORD_SEQUENCE_LENGTH, truncating='post', value=0)

    test_q1_word_seq = pad_sequences(test_q1_word_seq, maxlen=MAX_WORD_SEQUENCE_LENGTH, truncating='post', value=0)
    test_q2_word_seq = pad_sequences(test_q2_word_seq, maxlen=MAX_WORD_SEQUENCE_LENGTH, truncating='post', value=0)

    y = train.label.values

    with open(opt.processed_data_root+'train_word.pkl','wb') as f:
        pickle.dump([train_q1_word_seq, train_q2_word_seq,y],f)
    with open(opt.processed_data_root+'test_word.pkl','wb') as f:
        pickle.dump([test_q1_word_seq, test_q2_word_seq],f)
    with open(opt.processed_data_root + 'word_embedding_matrix.pkl','wb') as f:
        pickle.dump(word_embedding_matrix, f)

    # return [train_q1_word_seq, train_q2_word_seq,y], [test_q1_word_seq, test_q2_word_seq]

def read_data_as_char():
    question = pd.read_csv(opt.raw_data_root + 'question_id.csv')
    question = question[['qid', 'wid', 'cid']]
    train = pd.read_csv(opt.raw_data_root + 'train.csv')
    test = pd.read_csv(opt.raw_data_root + 'test.csv')

    train = pd.merge(train, question, left_on=['qid1'], right_on=['qid'], how='left').drop(['qid'], axis=1)
    train = pd.merge(train, question, left_on=['qid2'], right_on=['qid'], how='left').drop(['qid'], axis=1)
    test = pd.merge(test, question, left_on=['qid1'], right_on=['qid'], how='left').drop(['qid'], axis=1)
    test = pd.merge(test, question, left_on=['qid2'], right_on=['qid'], how='left').drop(['qid'], axis=1)

    tokenizer = Tokenizer(num_words=opt.MAX_NB_WORDS)
    tokenizer.fit_on_texts(question['cid'])
    train_q1_word_seq = tokenizer.texts_to_sequences(train['cid_x'])
    train_q2_word_seq = tokenizer.texts_to_sequences(train['cid_y'])
    test_q1_word_seq = tokenizer.texts_to_sequences(test['cid_x'])
    test_q2_word_seq = tokenizer.texts_to_sequences(test['cid_y'])

    embeddings_index = {}
    with open(opt.raw_data_root + 'char_embedding.txt', 'r') as f:
        wordmat = f.read().split('\n')
        if wordmat[-1] == '': wordmat = wordmat[:-1]
        if wordmat[0] == '':  wordmat = wordmat[1:]

    for line in tqdm(wordmat):
        wvec = line.strip('\n').strip(' ').split('\t')
        embeddings_index[wvec[0]] = np.asarray(wvec[1:], dtype='float')
    # print('word embedding', len(embeddings_index))

    word_index = tokenizer.word_index
    nb_words = min(opt.MAX_NB_WORDS, len(word_index))
    word_embedding_matrix = np.zeros((nb_words + 1, opt.EMBEDDING_DIM))
    for word, i in word_index.items():
        if i > opt.MAX_NB_WORDS: continue
        embedding_vector = embeddings_index.get(str(word).upper())
        if embedding_vector is not None:
            word_embedding_matrix[i] = embedding_vector

    # MAX_WORD_SEQUENCE_LENGTH = opt.MAX_WORD_SEQUENCE_LENGTH
    MAX_CHAR_SEQUENCE_LENGTH = opt.MAX_CHAR_SEQUENCE_LENGTH
    train_q1_word_seq = pad_sequences(train_q1_word_seq, maxlen=MAX_CHAR_SEQUENCE_LENGTH, truncating='post', value=0)
    train_q2_word_seq = pad_sequences(train_q2_word_seq, maxlen=MAX_CHAR_SEQUENCE_LENGTH, truncating='post', value=0)

    test_q1_word_seq = pad_sequences(test_q1_word_seq, maxlen=MAX_CHAR_SEQUENCE_LENGTH, truncating='post', value=0)
    test_q2_word_seq = pad_sequences(test_q2_word_seq, maxlen=MAX_CHAR_SEQUENCE_LENGTH, truncating='post', value=0)

    y = train.label.values

    with open(opt.processed_data_root+'train_char.pkl','wb') as f:
        pickle.dump([train_q1_word_seq, train_q2_word_seq,y],f)
    with open(opt.processed_data_root+'test_char.pkl','wb') as f:
        pickle.dump([test_q1_word_seq, test_q2_word_seq],f)
    with open(opt.processed_data_root + 'char_embedding_matrix.pkl','wb') as f:
        pickle.dump(word_embedding_matrix, f)


if __name__ == '__main__':
    read_data_as_char()
    # read_data_as_word()