#-*- coding: utf-8 -*-
#cabochaを使って形容詞にかかる名詞を抽出して多く出現したものを知るプログラム
#なぜか動かないため改良が必要
import numpy as np
import re
import csv

def purse(doc, ary, item1, item2, item3):

	# データの有無を管理するフラグ
	data_flag1 = 0
	data_flag2 = 0
	data_flag3 = 0

	sub_ary = []
	ary_purse = []

	# 指定した項目のデータを抽出して，ファイルに書き込む(リストに追加する)
	for i in range(len(doc)):

		sub_ary = [] # リストの初期化

		# 抽出したい項目のとき，その項目の内容をファイルに書き込む
		for j in range(0, 3):
			# print i,ary[j][i]

			# 項目が13のとき
			if (j == item1): #13

				# データがある場合を検出する
				searchOb1 = re.search(".", ary[i][item1])
				if searchOb1:
					data_flag1 = 1

			# 項目が15のとき
			if (j == item2): #15
				
				# データがある場合を検出する
				searchOb2 = re.search(".", ary[i][item2])
				if searchOb2:
					data_flag2 = 1

			# 項目が15のとき
			if (j == item3): #15
				
				# データがある場合を検出する
				searchOb3 = re.search(".", ary[i][item3])
				if searchOb3:
					data_flag3 = 1		
		
		# 欲しい項目がすべて存在するレビューであった場合，sub_aryに各項目を格納する
		if data_flag1 == 1 and data_flag2 == 1 and data_flag3 == 1:
			sub_ary.append(ary[i][item1])
			sub_ary.append(ary[i][item2])
			sub_ary.append(ary[i][item3])

			# 欲しい項目のみが格納されたリストを，新たなリストに格納する
			ary_purse.append(sub_ary)

		# フラグの初期化
		data_flag1 = 0
		data_flag2 = 0

	return ary_purse


def make_ary(fl):

	doc = [] # レビューを件ごとに入れるリスト
	ary = [] # レビューを項目ごとに入れるリスト

	# 一つのrowは，0(投稿者)～16(投稿日時)までのデータをひとまとまりにしたもの(レビュー1件)である
	# そのレビュー1件を順番に，リストに追加する
	# 追加するレビュー数は，2000件までとする
	for row in fl:

		# if (review_num % 2) == 0 and review_num < 1000:
		doc.append(row)   # レビューをリストに追加する

	# レビューを項目ごとに分割し，各項目の内容を新たなリストに追加する
	# ary[a][b]
	# a : レビューの件数(何件目か)
	# b : レビューの項目(0～16)
	# 17個にスプリットしたものを一気にいれていくため，二次元配列として扱う？
	# 17個の項目を，1つのリストとしてリストに追加している
	# つまり，17個の項目のリストを要素とするリストがaryである
	for i in range(len(doc)):

		# すべての項目の情報があるレビューのみをリストに追加する
		if len(doc[i].split("	")) == 10:
			# 表示された項目がタブで区切られていたため，タブでスプリットしている？
			ary.append(doc[i].split("	")) # 本文を分けるためのもの

	return ary


# if __name__ == "__main__":
def genre_purse():

	f1 = open("/home/murahashi/text_mining/rakuten_data/ichiba03_genre_20140221.tsv","r") # 2361件
	genre_num = 0  # レビューの件数をカウントするための変数
	doc = [] # レビューを件ごとに入れるリスト
	ary = [] # レビューを項目ごとに入れるリスト

	ary1 = [] # 特定の項目を格納するリスト
	ary2 = []
	# sub_ary = [] # 項目を格納するためのリスト

	# # データの有無を管理するフラグ
	# data_flag1 = 0
	# data_flag2 = 0

	# 欲しい項目の指定
	item1 = 0
	item2 = 1
	item3 = 2

	# 一つのrowは，0(ジャンルID)～2(親ジャンルID)までのデータをひとまとまりにしたものである
	# そのジャンル1件を順番に，リストに追加する
	for row in f1:
		doc.append(row)   # ジャンルをリストに追加する
		genre_num = genre_num + 1 # ジャンル数数のカウント

	# ジャンルを項目ごとに分割し，各項目の内容を新たなリストに追加する
	# ary[a][b]
	# a : ジャンルの数(何件目か)
	# b : ジャンルの項目(0～2)
	for i in range(len(doc)):
		# 表示された項目がタブで区切られていたため，タブでスプリットしている？
		ary.append(doc[i].split("	")) # 本文を分けるためのもの
	ary1 = purse(doc, ary, item1, item2, item3)

	# 親ジャンルIDの改行を消す
	for i in range(len(ary1)):
		searchOb_kaigyou = re.search("\d+", ary1[i][2])
		if searchOb_kaigyou:
			ary1[i][2] = searchOb_kaigyou.group()
	f1.close()

	return ary1

# レビューデータをジャンルごとに分類し，特定のジャンルのレビューデータのみを集める関数
def genreclassify(genre_ary, ary):

	genre_dic = {}
	top_genre = []
	first_genre = "" # 最初のジャンルを保存するための変数
	first_flag = 0 # 最初だけジャンルを保存するようにするための変数
	top_genre_id = ""
	new_ary = [] #特定のジャンルのみのレビューを格納するリスト
	new_ary1 = []
	new_ary2 = []
	new_ary3 = []
	new_ary4 = []
	new_ary5 = []
	new_ary6 = [] 
	new_ary7 = []
	new_ary8 = []
	new_ary9 = []
	new_ary10 = []
	new_ary11 = []
	new_ary12 = []
	new_ary13 = []
	new_ary14 = []
	new_ary15 = []
	new_ary16 = [] 
	new_ary17 = []
	new_ary18 = []
	new_ary19 = []
	new_ary20 = []

	now_count = 0 # ここまでのデータ数を確認する数
	not_topgenre_num = 0 # トップジャンルがなかった数


	flag = 0
	not_flag = 0
	not_num = 0
	# ジャンルIDから，トップジャンルを抽出する
	for i in range(len(ary)):

		# ここまでのデータ数のカウント
		now_count += 1
		if now_count == 10000:
			print "-------------------------------------", i+1, "番目まで終了-------------------------------------------"
			now_count = 0

		flag = 0
		not_flag = 0
		not_num = 0
		top_genre_id = ary[i][10]#商品ジャンルのID、、、、のちのち書品データで使うときはここを10にする。reviewは7
		first_flag = 0
		while flag < 1:#flagが立てば（flag=1）親ジャンル探しが終わり！次のレビューに移動
			flag2 = 0
			j = 0

			while flag2 < 1 and j < len(genre_ary):#flag2が立つか（flag2=1）ひと通り回したら(j)小ジャンル一致探し終わり！

				if int(genre_ary[j][0]) == int(top_genre_id):#小ジャンルが一致した時

					# 最初に出てきたジャンルを保存し，記憶しておく
					if first_flag == 0:
						first_genre = genre_ary[j][1]
						first_flag = 1

					top_genre_id = genre_ary[j][2]#探すジャンルIDの移動
					not_flag = 1#見つかったから見つからなかったフラグを下ろす
					notgenreclassify_num = j#genrefineの行数を保存
					flag2 = 1

					searchOb_gr = re.search("洗濯機",genre_ary[j][1])
					if searchOb_gr:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary.append(ary[i])
						
					searchOb_gr1 = re.search("ミュージック",genre_ary[j][1])
					if searchOb_gr1:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary1.append(ary[i])

					searchOb_gr2 = re.search("ジャズ",genre_ary[j][1])
					if searchOb_gr2:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary2.append(ary[i])

					searchOb_gr3 = re.search("メンズインナー",genre_ary[j][1])
					if searchOb_gr3:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary3.append(ary[i])

					searchOb_gr4 = re.search("おもちゃ",genre_ary[j][1])
					if searchOb_gr4:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary4.append(ary[i])

					searchOb_gr5 = re.search("スピーカー",genre_ary[j][1])
					if searchOb_gr5:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary5.append(ary[i])

					searchOb_gr6 = re.search("ミシン",genre_ary[j][1])
					if searchOb_gr6:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary6.append(ary[i])

					searchOb_gr7 = re.search("ヘッドホン・イヤホン",genre_ary[j][1])
					if searchOb_gr7:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary7.append(ary[i])

					searchOb_gr8 = re.search("デジタルカメラ",genre_ary[j][1])
					if searchOb_gr8:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary8.append(ary[i])

					searchOb_gr9 = re.search("テレビ",genre_ary[j][1])
					if searchOb_gr9:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary9.append(ary[i])

					searchOb_gr10 = re.search("オフィスチェア",genre_ary[j][1])
					if searchOb_gr10:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary10.append(ary[i])

					searchOb_gr11 = re.search("テレビゲーム",genre_ary[j][1])
					if searchOb_gr11:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary11.append(ary[i])

					searchOb_gr12 = re.search("調味料",genre_ary[j][1])
					if searchOb_gr12:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary12.append(ary[i])

					searchOb_gr13 = re.search("ノートパソコン",genre_ary[j][1])
					if searchOb_gr13:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary13.append(ary[i])

					searchOb_gr14 = re.search("デスクトップパソコン",genre_ary[j][1])
					if searchOb_gr14:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary14.append(ary[i])

					searchOb_gr15 = re.search("赤ワイン",genre_ary[j][1])
					if searchOb_gr15:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary15.append(ary[i])

					searchOb_gr16 = re.search("小説・エッセイ",genre_ary[j][1])
					if searchOb_gr16:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary16.append(ary[i])

					searchOb_gr17 = re.search("エアコン",genre_ary[j][1])
					if searchOb_gr17:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary17.append(ary[i])

					searchOb_gr18 = re.search("炊飯器",genre_ary[j][1])
					if searchOb_gr18:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary18.append(ary[i])

					searchOb_gr19 = re.search("冷蔵庫",genre_ary[j][1])
					if searchOb_gr19:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary19.append(ary[i])

					searchOb_gr20 = re.search("掃除機",genre_ary[j][1])
					if searchOb_gr20:
						flag = 1
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)
						new_ary20.append(ary[i])

					if int(top_genre_id) == 0:#親ジャンルが0（目的）にたどり着いた時
						flag = 1#見つかったフラグ、次のレビューに移動
						top_genre.append(genre_ary[j][1])#目的の親ジャンルの名前を取得(食品、靴、服、家電)

						# # 目的のジャンルがあった場合，そのレビューデータをリストに追加する
						# searchOb_gr1 = re.search("家電", genre_ary[j][1])
						# if searchOb_gr1:
						# 	new_ary.append(ary[i])
						# 	flag1 = 1
						# 	# print "match consumer electronics"
				j += 1
			
			# 本来のトップジャンル（IDが0）が得られなかった場合でも，トップジャンルのリストに入れる
			if not_flag == 0:
				flag = 1
				top_genre.append(genre_ary[not_num][1])
				# print "not match topgenre"
				not_topgenre_num += 1
	print "finish"

	# 各トップジャンルの内訳を知るためのディクショナリを作成する
	for i in range(len(top_genre)):
		if top_genre[i] not in genre_dic:
			genre_dic[top_genre[i]] = 0
		genre_dic[top_genre[i]] += 1

	return genre_dic, new_ary, new_ary1, new_ary2, new_ary3, new_ary4, new_ary5, new_ary6, new_ary7, new_ary8, new_ary9, new_ary10, new_ary11, new_ary12, new_ary13, new_ary14, new_ary15, new_ary16, new_ary17, new_ary18, new_ary19, new_ary20, not_topgenre_num



if __name__ == "__main__":

	f1 = open("/home/murahashi/text_mining/rakuten_data/ichiba01_item-html260_20140221.tsv","r") # 2361件
	print "finish_file_load------------------------------------"
	ary = []
	ary = make_ary(f1)
	print "ary",len(ary)
	# print "ary[0]",len(ary[0])
	print "finish_makeary---------------------------------------"
	# レビューを項目ごとに分割し，各項目の内容を新たなリストに追加する
	# ary[a][b]
	# a : レビューの件数(何件目か)
	# b : レビューの項目(0～16)
	f1.close()


	# ジャンルマスタの情報を取得する
	genre_ary = []
	genre_ary = genre_purse()
	print "finish_genre_file_load----------------------------------"

	gr_dic = {}  # トップジャンルの内訳を保存するディクショナリ
	gr_ary = []  # 特定のジャンルのみを抽出したレビューデータを格納するリスト1
	gr_ary1 = [] # 特定のジャンルのみを抽出したレビューデータを格納するリスト1
	gr_ary2 = [] # 特定のジャンルのみを抽出したレビューデータを格納するリスト2
	gr_ary3 = [] # 以下同様
	gr_ary4 = []
	gr_ary5 = []
	gr_ary6 = []
	gr_ary7 = []
	gr_ary8 = []
	gr_ary9 = []
	gr_ary10 = []
	gr_ary11 = [] # 特定のジャンルのみを抽出したレビューデータを格納するリスト1
	gr_ary12 = [] # 特定のジャンルのみを抽出したレビューデータを格納するリスト2
	gr_ary13 = [] # 以下同様
	gr_ary14 = []
	gr_ary15 = []
	gr_ary16 = []
	gr_ary17 = []
	gr_ary18 = []
	gr_ary19 = []
	gr_ary20 = []

	not_gr_num = 0 # トップジャンルが取れなかったデータ数
	gr_dic, gr_ary, gr_ary1, gr_ary2, gr_ary3, gr_ary4, gr_ary5, gr_ary6, gr_ary7, gr_ary8, gr_ary9, gr_ary10, gr_ary11, gr_ary12, gr_ary13, gr_ary14, gr_ary15, gr_ary16, gr_ary17, gr_ary18, gr_ary19, gr_ary20, not_gr_num = genreclassify(genre_ary, ary)
	print "--------------------------finish_classify----------------------"

	for k,l in gr_dic.items():
		print k,l

	# for i in gr_ary[0]:
	# 	print i

	print "トップジャンルが取れなかったデータ数：", not_gr_num


	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv = open("/home/murahashi/text_mining/rakuten_data/washing_machine_html_.csv", "ab")
	csvWriter = csv.writer(f_csv)
	csvWriter.writerows(gr_ary)
	f_csv.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv1 = open("/home/murahashi/text_mining/rakuten_data/music_html_.csv", "ab")
	csvWriter1 = csv.writer(f_csv1)
	csvWriter1.writerows(gr_ary1)
	f_csv1.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv2 = open("/home/murahashi/text_mining/rakuten_data/jazz_html_.csv", "ab")
	csvWriter2 = csv.writer(f_csv2)
	csvWriter2.writerows(gr_ary2)
	f_csv2.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv3 = open("/home/murahashi/text_mining/rakuten_data/mansunderwear_html_.csv", "ab")
	csvWriter3 = csv.writer(f_csv3)
	csvWriter3.writerows(gr_ary3)
	f_csv3.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv4 = open("/home/murahashi/text_mining/rakuten_data/toy_html_.csv", "ab")
	csvWriter4 = csv.writer(f_csv4)
	csvWriter4.writerows(gr_ary4)
	f_csv4.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv5 = open("/home/murahashi/text_mining/rakuten_data/speaker_html_.csv", "ab")
	csvWriter5 = csv.writer(f_csv5)
	csvWriter5.writerows(gr_ary5)
	f_csv5.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv6 = open("/home/murahashi/text_mining/rakuten_data/sewing_machine_html_.csv", "ab")
	csvWriter6 = csv.writer(f_csv6)
	csvWriter6.writerows(gr_ary6)
	f_csv6.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv7 = open("/home/murahashi/text_mining/rakuten_data/headphones_earphone_html_.csv", "ab")
	csvWriter7 = csv.writer(f_csv7)
	csvWriter7.writerows(gr_ary7)
	f_csv7.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv8 = open("/home/murahashi/text_mining/rakuten_data/digital_camera_html_.csv", "ab")
	csvWriter8 = csv.writer(f_csv8)
	csvWriter8.writerows(gr_ary8)
	f_csv8.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv9 = open("/home/murahashi/text_mining/rakuten_data/TV_html_.csv", "ab")
	csvWriter9 = csv.writer(f_csv9)
	csvWriter9.writerows(gr_ary9)
	f_csv9.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv10 = open("/home/murahashi/text_mining/rakuten_data/office_chair_html_.csv", "ab")
	csvWriter10 = csv.writer(f_csv10)
	csvWriter10.writerows(gr_ary10)
	f_csv10.close()

		# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv11 = open("/home/murahashi/text_mining/rakuten_data/game_html_.csv", "ab")
	csvWriter11 = csv.writer(f_csv11)
	csvWriter11.writerows(gr_ary11)
	f_csv11.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv12 = open("/home/murahashi/text_mining/rakuten_data/seasoning_html_.csv", "ab")
	csvWriter12 = csv.writer(f_csv12)
	csvWriter12.writerows(gr_ary12)
	f_csv12.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv13 = open("/home/murahashi/text_mining/rakuten_data/notePC_html_.csv", "ab")
	csvWriter13 = csv.writer(f_csv13)
	csvWriter13.writerows(gr_ary13)
	f_csv13.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv14 = open("/home/murahashi/text_mining/rakuten_data/desktop_PC_html_.csv", "ab")
	csvWriter14 = csv.writer(f_csv14)
	csvWriter14.writerows(gr_ary14)
	f_csv14.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv15 = open("/home/murahashi/text_mining/rakuten_data/red_wine.csv", "ab")
	csvWriter15 = csv.writer(f_csv15)
	csvWriter15.writerows(gr_ary15)
	f_csv15.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv16 = open("/home/murahashi/text_mining/rakuten_data/novel_html_.csv", "ab")
	csvWriter16 = csv.writer(f_csv16)
	csvWriter16.writerows(gr_ary16)
	f_csv16.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv17 = open("/home/murahashi/text_mining/rakuten_data/air_conditioner_html_.csv", "ab")
	csvWriter17 = csv.writer(f_csv17)
	csvWriter17.writerows(gr_ary17)
	f_csv17.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv18 = open("/home/murahashi/text_mining/rakuten_data/rice_cooker_html_.csv", "ab")
	csvWriter18 = csv.writer(f_csv18)
	csvWriter18.writerows(gr_ary18)
	f_csv18.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv19 = open("/home/murahashi/text_mining/rakuten_data/fridge_html_.csv", "ab")
	csvWriter19 = csv.writer(f_csv19)
	csvWriter19.writerows(gr_ary19)
	f_csv19.close()

	# csvファイルに，必要なジャンルのレビューデータだけを書き込む
	f_csv20 = open("/home/murahashi/text_mining/rakuten_data/vacuum_cleaner_html_.csv", "ab")
	csvWriter20 = csv.writer(f_csv20)
	csvWriter20.writerows(gr_ary20)
	f_csv20.close()