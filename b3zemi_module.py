#-*- coding: utf-8 -*-
import os
def get_file_contents(path):
	file = os.listdir(path)
	doc = []
	for i in sorted(file):
		f = open(path+"/"+i,'r')#""でそのフォルダの中を探せでiでファイルを指定
		doc.append(f.read())
	# f = open("data/p601.json",'r')
	# doc.append(f.read())
	# file = os.listdir("pos_data")
	# for i in sorted(file):
	# 	f = open("pos_data/"+i,'r')#""でそのフォルダの中を探せでiでファイルを指定
	# 	doc.append(f.read())
	return doc

#引数(tfidfのリスト（単語、tfidf値）、書き込むファイル名、単語ディクショナリー、タグ、クラス番号)
#単語ディクショナリー、タグはメイン文に初期化で宣言してください。
#tag=0,words={}
def svm_data(tfidf,fp,words,attrs,tag,classnum):
	num = tag
	for title in tfidf:	#tfidf1の配列を渡してもらう
		for title_word in title.keys():	#tfidfで取り出した文字列を繰り返す
			# print title1_word, title1[title1_word]#tfidfの単語と状態表示
			if title_word not in words:#言葉にタグをつけるプログラム
				words[title_word] = num
				num = num + 1

	for title in tfidf:
		# fp.write('-1 ')
		fp.write(str(classnum))#クラス名を書く
		fp.write(' ')
		for title_word in title.keys():
			if title_word not in words.keys():#もし、単語が入ってないとき
				break
			tag = words[title_word]#タグを取り出す
			attrs[tag] = title[title_word]
			# if tag in attrs:#
			# 	attrs[tag] = attrs[tag] + 1
			# else:
			# 	attrs[tag] = 1
			# print title5_word,tag
		for ak in sorted(attrs.keys()):
			if attrs[ak] != 0:
			# print str(ak) + ":" + str(attrs[ak])
				fp.write(str(ak+1))
				fp.write(':')
				fp.write(str(attrs[ak]))
				fp.write(' ')
		for i in range(len(attrs)):
			attrs[i] = 0
		fp.write('\n')
	return words,tag+1

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

def calc_tf(sentence):
	m = MeCab.Tagger ("--node-format=%m\s%f[0]\\n --eos-format='' ")#メカブを使う
	# f = open(file_pass, 'r')#00000370.txtフィアルを開く
	# doc=f.read()#ファイルの内容をdocにいれる
	nobe = 0
	hinshinobe = 0
	# doc.decode("utf-8")
	# print doc
	# print m.parse(doc)
	cd = m.parse(sentence)#メカブを使用したものをcdに入れる
	full = []#隙間を詰めるために使うリスト
	list1 = []#名詞のみを入れるリスト
	cp2 = cd.split()#真ん中の空白をなくす
	# # for i in range(len(cp2)):#
	# # 	j = i%2
	# # 	if j == 0:
	# # 		print cp2[i], cp2[i+1]
	# print "異なり語数"
	word = cp2[0::2] #偶数だけとるプログラム
	hinshi = cp2[1::2] #奇数だけ取るプログラム
	# for i in range(len(word)):#メカブの情報を取り出すがエラーをはく
	# 	# print word[i],hinshi[i]

	for i in range(len(hinshi)):#1から品詞の数分繰り返す
		noun = re.search("名詞",hinshi[i])#名詞と書いているものを取り出す
		verb = re.search("動詞",hinshi[i])
		adjective = re.search("形容詞",hinshi[i])
		if noun or verb or adjective:#一致した時
			list1.append(word[i])#wordの配列に入れる
	tf = {}#リストをつくる
	for tfword in list1:#名詞のリストからすべてを取り出す
		if tfword not in tf:#リストの中に今までのものが入ってないときに
			tf[tfword] = 0#ｔｆに0を入れる
		tf[tfword] += 1#数をふやす

	# for z in list1:#正規化をする
	# 	print z,tf[z]#単語と頻度の表示
		# tf[z] = 1.0*tf[z]/len(list1)#正規化シたものの表示
	nomalize_tf = {}
		#### 単語をキーとして正規化した値を保存 ####
	for k, l in tf.items():
		nomalize_tf[k] = 1.0 * l / len(list1)

	return nomalize_tf


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

def calc_tfidf(tf,idf):
	tfidfdic = {}#ディクショナリ
	tfidf = []#リスト（結果）をいれる
	for tfdoc in tf:#一つの文章をとりだす
		for tfword in tfdoc.keys():# 文字に入れる。
			tfidfdic[tfword] = tfdoc[tfword] * idf[tfword]#tfidfに値をいれる
		tfidf.append(tfidfdic)#一致した時にtfidfにいれる
		tfidfdic = {}#再初期化
	# print tf[0]["KDDI"]
	# print idf["KDDI"]
	return tfidf

def tfidf_process(body_file):
	tf5=[]
	df5=[]
	idf5=[]
	tfidf5=[]
	tfdic = {}
	for sentence in body_file:#星5のtfを求める
		if calc_tf(sentence):
			tf5.append(calc_tf(sentence))
		# if tfdic:
		# 	tf5.append(tfdic)
	df5 = calc_df(tf5)
	idf5 = calc_idf(df5,len(body_file))
	tfidf5 = calc_tfidf(tf5,idf5)
	return tfidf5


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
    return tuples

def cabocha_tfidf_process(body_file):#引数はリストに一文が入っている状態["大きいです。","お勧めです！","これはちょっと…"]
	cabocha_output_result=[]
	c_out=[]
	# print "body_file",body_file
	for sentence in body_file:#一文を取り出す
		# print "sentence",sentence
		tuples = get_2_words(sentence)#cabochaに入れる
		c_out = []
		for t in tuples:
			# print t[0],t[1]
			c_out.append(t[0]+t[1])
		if c_out:
			cabocha_output_result.append(c_out)#cabochaの結果だけ入ったリストを作成する
	# for i in c_out:
	# 	print i
	# for i in range(len(cabocha_output_result)):
	# 	for j in range(len(cabocha_output_result[i])):
	# 		print "cabocha_output_result",cabocha_output_result[i][j]
	#以下tfidfの計算
	tf=[]
	df=[]
	idf=[]
	tfidf=[]
	for sentence in cabocha_output_result:#リストの中の結果を渡す
		tf.append(only_calc_tf(sentence))
	# print "tf",tf
	# for i in tf:
	# 	for k,v in i.items():
	# 		print k,v
	df = calc_df(tf)
	# for k,v in df.items():
	# 	print k,v
	idf = calc_idf(df,len(cabocha_output_result))
	tfidf = calc_tfidf(tf,idf)
	# for i in tfidf:
	# 	for k,v in i.items():
	# 		print "tfidf",k,v
	return tfidf

def divide(body_file,order,quotient):#配列をquotientこに分割して1個と9個の分割を返す。orderが1からquotientが入る。
	num = int(len(body_file)/quotient)
	extract_data = []
	rest_data = []
	count = 0
	for i in body_file:
		if not order == quotient:
			if count>=(order-1)*num and count<order*num:
				extract_data.append(i)
				print count,i
			else:
				rest_data.append(i)
				# print i
			count+=1
		else:
			if count>=(order-1)*num:
				extract_data.append(i)
				print count,i
			else:
				rest_data.append(i)
			count+=1
	return [extract_data,rest_data]