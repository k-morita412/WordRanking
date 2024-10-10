import MeCab
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

mecabTagger = MeCab.Tagger()
noun_count = {}

# CSVファイルを読み込む
df = pd.read_csv("bad-izakaya.csv")

# 各店名を処理する
for text in df["店名"]:
    # MeCabで形態素解析を実行
    node = mecabTagger.parseToNode(text)
    
    while node:
        # nodeを単語に分割
        word = node.surface

        # nodeから品詞情報を取り出す
        hinshi = node.feature.split(",")[0]
        
        # 品詞が名詞であるとき
        if hinshi == "名詞" and word:
            if word in noun_count:
                noun_count[word] += 1
            else:
                noun_count[word] = 1
        
        node = node.next

# 名詞の出現頻度を降順にソート
noun_count = sorted(noun_count.items(), key=lambda x: x[1], reverse=True)
print(noun_count)

# 出現頻度が3以下の単語を除外
filtered_noun_count = {word: count for word, count in noun_count if count > 2}

# 円グラフを作成
if filtered_noun_count:
    words = list(filtered_noun_count.keys())
    counts = list(filtered_noun_count.values())

    # 円グラフの描画
    plt.figure(figsize=(10, 7))
    plt.pie(counts, labels=words, autopct='%1.1f%%', startangle=90, counterclock=False)
    plt.title('名詞の出現頻度（出現頻度が3以上の単語）')
    plt.show()
else:
    print("出現頻度が3以上の単語はありません。")
