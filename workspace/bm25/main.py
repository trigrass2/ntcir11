#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import hymlab.text as ht

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../helper')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../config')
import helper
import config

def bm25(tf, query_words, idf, avg_length, k=2.0, b=0.75):
    """
    tf : normaliszeされていないtf vector
    bm25 @hara 
    """
    score = 0.0
    tf_unknown = 0
    idf_unknown = 0

    for word in query_words:
        # get なかったときに0に初期化
        score += idf.get(word, idf_unknown) * ( tf.vec.get(word, tf_unknown) * (k+1) ) / (tf.vec.get(word, tf_unknown) + k*( (1-b) + b*(len(tf.text) / avg_length) ) )
    return score

if __name__ == '__main__':
    import unittest

    # class Bm25TestCase(unittest.TestCase):
    #     def setUp(self):
    #         self.tc1 = ht.TextCollection([u"猫ほしい。銅像だ。"]) 
    #         self.tc2 = ht.TextCollection([u"我が輩は猫である", u"名前はまだ無い", u"我が輩は猫である"]) 
    #         self.tc2_tf = ht.TfIdf(self.tc2).tf(False)
    #         self.tc2_idf = ht.TfIdf(self.tc2).idf()
    #    
    #     def tearDown(self):
    #         pass

    #     def test_ave_lenge(self):
    #         l = self.tc2.ave_doc_length()
    #         self.assertEquals(l, float(2+1+2)/3)

    #     def test_bm25(self):
    #         """
    #         bm25のテスト
    #         """
    #         tf = self.tc2_tf[0]
    #         # idf is OK 
    #         idf = self.tc2_idf
    #         avg_length = self.tc2.ave_doc_length()
    #         query_words = self.tc1.words_list()[0]
    #         bm = bm25(tf, query_words, idf, avg_length)
    #         d = 2
    #         b = 0.75
    #         k = 2.0 
    #         self.assertEquals(bm, (idf[u'猫']*(k+1))/(1+k*((1-b)+b*(d/avg_length))))
    # unittest.main()

    conf = config.Config("bm25")

    DOC_TF_PATH = conf.TMP_PATH + "/doc_tf"
    DOC_IDF_PATH = conf.TMP_PATH + "/doc_idf"
    DOC_TMP_PATH = conf.TMP_PATH + "/doc"

    QUERY_PATH = conf.SPOKEN_QUERY_PATH
    DOC_PATH = conf.SPOKEN_DOC_PATH

    # クエリを読み込み
    query = ht.file_read(QUERY_PATH).split("\n")
    query.pop()

    q_tc = ht.TextCollection(query)

    # ドキュメントを読み込み
    doc_tf = None
    if (os.path.exists(DOC_TF_PATH) == False):
        doc_tc = ht.TextCollection(DOC_PATH)
        ht.pickle_save(doc_tc, DOC_TMP_PATH)

        doc_tf = ht.TfIdf(doc_tc).tf(False)
        ht.pickle_save(doc_tf, DOC_TF_PATH)

        doc_idf = ht.TfIdf(doc_tc).idf()
        ht.pickle_save(doc_idf, DOC_IDF_PATH)

    else:
        doc_tc = ht.pickle_load(DOC_TMP_PATH)
        doc_tf = ht.pickle_load(DOC_TF_PATH)
        doc_idf = ht.pickle_load(DOC_IDF_PATH)

    query_texts = q_tc.list()
    avg_length = doc_tc.ave_doc_length() 

    # bm25 計算
    res = []
    for i, q_text in enumerate(query_texts):
        query_res = []
        query_words = q_text.words()

        for vsm in doc_tf: # doc loop
            bm = bm25(vsm, query_words, doc_idf, avg_length)
            query_res.append((vsm.text, bm))

        res.append(query_res)

    # fileのアウトプット
    helper.output_result(res, conf.RESULT_PATH)
