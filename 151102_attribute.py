#-*- coding: utf-8 -*-
#cabochaを使って形容詞にかかる名詞を抽出してそのtfidf値を出力するプログラム
import CaboCha
import numpy as np
import re
import MeCab
import math
import matplotlib.pyplot as plt
import sys
import codecs
import csv

def get_word(tree, chunk):
	surface = ''
	for i in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
		token = tree.token(i)
		features = token.feature.split(',')
		if features[0] == '名詞':
			surface += token.surface
		elif features[0] == '形容詞':
			surface += features[6]
			break
		elif features[0] == '動詞':
			surface += features[6]
			break
	return surface


def get_2_words(line):
	cp = CaboCha.Parser('-f1')
	tree = cp.parse(line)
	chunk_dic = {}
	chunk_id = 0
	for i in range(0, tree.size()):
		token = tree.token(i)
		if token.chunk:
			chunk_dic[chunk_id] = token.chunk
			chunk_id += 1
 
	tuples = []
	for chunk_id, chunk in chunk_dic.items():
		if chunk.link > 0:
			from_surface =  get_word(tree, chunk)
			to_chunk = chunk_dic[chunk.link]
			to_surface = get_word(tree, to_chunk)
			tuples.append((from_surface, to_surface))
			# print from_surface,to_surface

	# for i in tuples:
	# 	print 
	return tuples

def only_calc_tf(cabo_output_result):
	tf = {}#リストをつくる
	for tfword in cabo_output_result:#名詞のリストからすべてを取り出す
		if tfword not in tf:#リストの中に今までのものが入ってないときに
			tf[tfword] = 0#ｔｆに0を入れる
		tf[tfword] += 1#数をふやす

	# for z in list1:#正規化をする
	# 	print z,tf[z]#単語と頻度の表示
		# tf[z] = 1.0*tf[z]/len(list1)#正規化シたものの表示
	nomalize_tf = {}
		#### 単語をキーとして正規化した値を保存 ####
	for k, l in tf.items():
		nomalize_tf[k] = 1.0 * l / len(cabo_output_result)

	return nomalize_tf

##############ココだけのオリジナル版コピペしないこと
def calc_df(tf):
	df = {}#dfのディクショナリを宣言
	for dfword in tf:	#tfの配列を渡してもらう
		for df2word in dfword.keys():	#tfで取り出した文字列を繰り返す
			if df2word not in df:	#ユニークをする
				df[df2word] = 0	#単語を新しく入れる
			df[df2word] += 1 #dfの値を入れる
	return df

def calc_idf(df,sentencenum):
	idf={}#idfのディクショナリを宣言
	for idfword in df.keys():#dfの単語を繰り返す
		idf[idfword] = math.log(1.0*sentencenum/df[idfword])+1#idfを求める
	return idf

##############ココだけのオリジナル版コピペしないこと
def calc_tfidf(tf,idf):
	tfidfdic = {}#ディクショナリ
	tfidf = []#リスト（結果）をいれる
	# for tfdoc in tf:#一つの文章をとりだす
	for tfword in tf.keys():# 文字に入れる。
		tfidfdic[tfword] = tf[tfword] * idf.get(tfword,0.00000001)#tfidfに値をいれる
	tfidf.append(tfidfdic)#一致した時にtfidfにいれる
	tfidfdic = {}#再初期化
	# print tf[0]["KDDI"]
	# print idf["KDDI"]
	return tfidf

#文字列を長い順にソートする関数（実行はdoc.sort(lencmp)）
def lencmp(x, y):
  a, b = len(x), len(y)
  if a == b:
    return 0
  elif a > b:
    return -1
  else:
    return 1

#係り結び関係の形容詞と名詞のペアのリストを返す関数（レビュー、上限）
def relationship(doc,limit):
	#形としてはary[0][0to7704]ここからary[0][0]で出力してみる。---------------------------------------
	m = MeCab.Tagger ("--node-format=%m\s%f[0]\\n --eos-format='' ")#メカブを使う
	# print cabocha[0][0]
	ndic=[]#名詞の数を入れるディクショナリー
	adic=[]#形容詞の数を入れるディクショナリー
	debugging_count=0#デバック用
	debugging_count_1000count=0
	# print doc[1]
	for review_num in range(limit):#レビューで回す。
		# n_buff = [] #1レビューのすべての名詞を取り出す
		# a_buff = [] #1レビューのすべての形容詞を取り出す。
		debugging_count += 1
		if debugging_count == 100:
			debugging_count_1000count+=1
			print "------------今",int(debugging_count_1000count*100),"回目のレビュー-------------------------"
			debugging_count = 0
		tuples = get_2_words(doc[review_num])
		for t in tuples:#t[0],t[1]には単語が入る
			# print(t[0] + ' => ' + t[1])
			if t[0] and t[1]:#係り受け関係となる品詞があるとき
				cd0 = m.parse(t[0])#めかぶを使う
				cd1 = m.parse(t[1])
				cp0 = cd0.split()#真ん中の空白をなくす
				cp1 = cd1.split()
				word0 = cp0[0::2] #偶数だけとるプログラム
				hinshi0 = cp0[1::2] #奇数だけ取るプログラム
				word1 = cp1[0::2] #偶数だけとるプログラム
				hinshi1 = cp1[1::2] #奇数だけ取るプログラム
				# print word0[0],word1[0]
				# print hinshi0[0],hinshi1[0]

				#係り結び関係となる形容詞をすべて取り込むという問題点があるプログラム
				#1,t[0]形容詞>=t[1]名詞の時
				reject0 = re.search("形容詞",hinshi0[0])
				reject1 = re.search("形容詞",hinshi1[0])
				if reject0:
					none1 = re.search("名詞",hinshi1[0])
					if none1:
						ndic.append(word1[0])
						adic.append(word0[0])
						# print word1[0]#確認のためのもの
						# print word0[0]
				#2,t[0]名詞>=t[1]形容詞の時
				if reject1:
					none0 = re.search("名詞",hinshi0[0])
					if none0:
						ndic.append(word0[0])
						adic.append(word1[0])
						# print word0[0]#確認のためのもの
						# print word1[0]
				
		# ndic.append(n_buff)#全体を1文書とするため、プログラムを変えた。
		# adic.append(a_buff)#[柳、クマ、ピアノ、牛乳、ピアノ…]という形で入っている。
	# print "len_ndic",len(ndic),"len_adic",len(adic)
	return ndic,adic

#係り結び関係の形容詞と名詞のペアのリストを返す関数（レビュー、上限）
def relationship_df(doc,limit):
	#形としてはary[0][0to7704]ここからary[0][0]で出力してみる。---------------------------------------
	m = MeCab.Tagger ("--node-format=%m\s%f[0]\\n --eos-format='' ")#メカブを使う
	# print cabocha[0][0]
	ndic=[]#名詞の数を入れるディクショナリー
	adic=[]#形容詞の数を入れるディクショナリー
	debugging_count=0#デバック用
	debugging_count_1000count=0
	# print doc[1]
	for review_num in range(limit):#レビューで回す。
		n_buff = [] #1レビューのすべての名詞を取り出す
		a_buff = [] #1レビューのすべての形容詞を取り出す。
		debugging_count += 1
		if debugging_count == 100:
			debugging_count_1000count+=1
			print "------------今",int(debugging_count_1000count*100),"回目のレビュー-------------------------"
			debugging_count = 0
		tuples = get_2_words(doc[review_num])
		for t in tuples:#t[0],t[1]には単語が入る
			# print(t[0] + ' => ' + t[1])
			if t[0] and t[1]:#係り受け関係となる品詞があるとき
				cd0 = m.parse(t[0])#めかぶを使う
				cd1 = m.parse(t[1])
				cp0 = cd0.split()#真ん中の空白をなくす
				cp1 = cd1.split()
				word0 = cp0[0::2] #偶数だけとるプログラム
				hinshi0 = cp0[1::2] #奇数だけ取るプログラム
				word1 = cp1[0::2] #偶数だけとるプログラム
				hinshi1 = cp1[1::2] #奇数だけ取るプログラム
				# print word0[0],word1[0]
				# print hinshi0[0],hinshi1[0]

				#係り結び関係となる形容詞をすべて取り込むという問題点があるプログラム
				#1,t[0]形容詞>=t[1]名詞の時
				reject0 = re.search("形容詞",hinshi0[0])
				reject1 = re.search("形容詞",hinshi1[0])
				if reject0:
					none1 = re.search("名詞",hinshi1[0])
					if none1:
						n_buff.append(word1[0])
						a_buff.append(word0[0])
						# print word1[0]#確認のためのもの
						# print word0[0]
				#2,t[0]名詞>=t[1]形容詞の時
				if reject1:
					none0 = re.search("名詞",hinshi0[0])
					if none0:
						n_buff.append(word0[0])
						a_buff.append(word1[0])
						# print word0[0]#確認のためのもの
						# print word1[0]
				
		ndic.append(n_buff)#全体を1文書とするため、プログラムを変えた。
		adic.append(a_buff)#[柳、クマ、ピアノ、牛乳、ピアノ…]という形で入っている。
	# print "len_ndic",len(ndic),"len_adic",len(adic)
	return ndic,adic
if __name__ == '__main__' :
	limit = 100000
	limit_cat = 1000
	f_all = open("/home/seko/text_mining/rakuten_data/alldata201001.txt","r")#1000 
	f_cat1 = open("/home/seko/text_mining/rakuten_data/only_purpose/vacuum_cleaner_review.csv","r")
	fn1 = open('/home/seko/text_mining/day_report/1511/output1/attribute_output_none_vacuum_cleaner.csv','w') 
	fa1 = open('/home/seko/text_mining/day_report/1511/output1/attribute_output_adjective_vacuum_cleaner.csv','w')
	f_cat2 = open("/home/seko/text_mining/rakuten_data/only_purpose/wine_review.csv","r")
	fn2 = open('/home/seko/text_mining/day_report/1511/output1/attribute_output_none_wine.csv','w') 
	fa2 = open('/home/seko/text_mining/day_report/1511/output1/attribute_output_adjective_wine.csv','w')

	# fp = open('/home/murahashi/text_mining/day_report/1510/output3/aaa_alldatatf.csv','w')
	print "finish_file_load------------------------------------"
	doc_all = []
	doc_cat1 = []
	doc_cat2 = []
	print "finish_makeary---------------------------------------"
	# レビューを項目ごとに分割し，各項目の内容を新たなリストに追加する
	# ary[a][b]
	# a : レビューの件数(何件目か)
	# b : レビューの項目(0～16)
	for row in f_all:
		if row:
			doc_all.append(row)
	f_all.close()

	for row in f_cat1:
		if row:
			doc_cat1.append(row)
	f_cat1.close()

	for row in f_cat2:
		if row:
			doc_cat2.append(row)
	f_cat2.close()
	#長い順にソート
	doc_all.sort(lencmp)
	doc_cat1.sort(lencmp)
	doc_cat2.sort(lencmp)
	ndic_all = {}
	adic_all = {}
	ndic_cat1 = {}
	adic_cat1 = {}
	ndic_cat2 = {}
	adic_cat2 = {}

	ndic_all,adic_all = relationship_df(doc_all,limit)
	# ndic_all,adic_all = relationship_df(doc_all,len(doc_all))
	ndic_cat1,adic_cat1 = relationship(doc_cat1,limit_cat)
	ndic_cat2,adic_cat2 = relationship(doc_cat2,limit_cat)
	# for i in range(len(ndic_all)):
	# 	for j in range(len(ndic_all[i])):
	# 		print ndic_all[i][j]
	n_tf_all=[]
	a_tf_all=[]
	n_tf_cat1 = only_calc_tf(ndic_cat1)
	a_tf_cat1 = only_calc_tf(adic_cat1)
	n_tf_cat2 = only_calc_tf(ndic_cat2)
	a_tf_cat2 = only_calc_tf(adic_cat2)
	for sentence in ndic_all:#星5のtfを求める
		n_tf_all.append(only_calc_tf(sentence))
	for sentence in adic_all:#星5のtfを求める
		a_tf_all.append(only_calc_tf(sentence))
	# for sentence in cabocha_output_result:#リストの中の結果を渡す
	# 	tf.append(only_calc_tf(sentence))
	# n_tf_all = only_calc_tf(ndic_all)
	# a_tf_all = only_calc_tf(adic_all)
	n_df = calc_df(n_tf_all) 
	a_df = calc_df(a_tf_all) 
	# n_idf = calc_idf(n_df,len(doc_all))
	# a_idf = calc_idf(a_df,len(doc_all))
	n_idf = calc_idf(n_df,limit)
	a_idf = calc_idf(a_df,limit)
	n_tfidf1 = calc_tfidf(n_tf_cat1,n_idf)
	a_tfidf1 = calc_tfidf(a_tf_cat1,a_idf)
	n_tfidf2 = calc_tfidf(n_tf_cat2,n_idf)
	a_tfidf2 = calc_tfidf(a_tf_cat2,a_idf)

	fn1.write("---------------------------名詞のtfidf---------------------------------------")
	fn1.write("\n")
	for i in n_tfidf1:
		for k,v in sorted(i.items(),key=lambda x:x[1], reverse=True):
	 		print "tfidf",k,v
	 		fn1.write(str(k))
	 		fn1.write("\t")
	 		fn1.write(str(v))
	 		fn1.write("\n")
	fn1.write("---------------------------名詞のtf---------------------------------------")
	fn1.write("\n")
	for k,v in sorted(n_tf_cat1.items(),key=lambda x:x[1], reverse=True):
		print "n_tf",k,v
		fn1.write(str(k))
		fn1.write("\t")
	 	fn1.write(str(v))
	 	fn1.write("\n")
	fa1.write("---------------------------形容詞のtfidf---------------------------------------")
	fa1.write("\n")
	for i in a_tfidf1:
		for k,v in sorted(i.items(),key=lambda x:x[1], reverse=True):
	 		print "a_tfidf",k,v
	 		fa1.write(str(k))
	 		fa1.write("\t")
	 		fa1.write(str(v))
	 		fa1.write("\n")
	fa1.write("---------------------------形容詞のtf---------------------------------------")
	fa1.write("\n")
	for k,v in sorted(a_tf_cat1.items(),key=lambda x:x[1], reverse=True):
		print "a_tf",k,v
		fa1.write(str(k))
		fa1.write("\t")
	 	fa1.write(str(v))
	 	fa1.write("\n")

	fn2.write("---------------------------名詞のtfidf---------------------------------------")
	fn2.write("\n")
	for i in n_tfidf2:
		for k,v in sorted(i.items(),key=lambda x:x[1], reverse=True):
	 		print "tfidf",k,v
	 		fn2.write(str(k))
	 		fn2.write("\t")
	 		fn2.write(str(v))
	 		fn2.write("\n")
	fn2.write("---------------------------名詞のtf---------------------------------------")
	fn2.write("\n")
	for k,v in sorted(n_tf_cat2.items(),key=lambda x:x[1], reverse=True):
		print "n_tf",k,v
		fn2.write(str(k))
		fn2.write("\t")
	 	fn2.write(str(v))
	 	fn2.write("\n")
	fa2.write("---------------------------形容詞のtfidf---------------------------------------")
	fa2.write("\n")
	for i in a_tfidf2:
		for k,v in sorted(i.items(),key=lambda x:x[1], reverse=True):
	 		print "a_tfidf",k,v
	 		fa2.write(str(k))
	 		fa2.write("\t")
	 		fa2.write(str(v))
	 		fa2.write("\n")
	fa2.write("---------------------------形容詞のtf---------------------------------------")
	fa2.write("\n")
	for k,v in sorted(a_tf_cat2.items(),key=lambda x:x[1], reverse=True):
		print "a_tf",k,v
		fa2.write(str(k))
		fa2.write("\t")
	 	fa2.write(str(v))
	 	fa2.write("\n")
#出力確認
	# for i in range(len(ndic)):
	# 	print "ndic",ndic[i]
	# for i in range(len(adic)):
	# 	print "adic",adic[i]

	# for k,v in n_tf.items():
	# 	print "tf",k,v
	# for k,v in n_idf.items():
	# 	print "idf",k,v
	# for i in n_tfidf:
	# 	for k,v in i.items():
	# 		print "tfidf",k,v