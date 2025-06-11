import streamlit as st
import pandas as pd
import os

st.title("📝 ダイエット診断アプリ")

st.write("あなたの現在の生活習慣に基づいて、ダイエットに役立つアドバイスを提供します。")

# --- 入力セクション ---
st.header("あなたの基本情報")

gender = st.selectbox("性別を選んでください:", ["男性", "女性", "その他"])
age = st.number_input("年齢:", min_value=10, max_value=100, value=25, step=1)
height = st.number_input("身長（cm）:", min_value=100, max_value=250, value=170)
weight = st.number_input("体重（kg）:", min_value=30, max_value=200, value=70)

body_type = st.selectbox("あなたの骨格タイプを選んでください:", ["ウェーブ", "ナチュラル", "ストレート", "わからない"])
exercise = st.radio("週にどのくらい運動していますか？", ["ほとんどしない", "週1〜2回", "週3〜4回", "週5回以上"])
diet = st.radio("普段の食生活について教えてください:", ["バランス良い", "偏りがち", "外食が多い", "間食が多い"])
sleep_hours = st.slider("平均睡眠時間（1日あたり）:", 3.0, 12.0, 7.0, 0.5)


# --- 診断・結果表示 ---
if st.button("診断する"):
    # サイドバーに基本情報を表示
    with st.sidebar:
        st.header("📋 入力された基本情報")
        st.write(f"性別: {gender}")
        st.write(f"年齢: {age} 歳")
        st.write(f"身長: {height} cm")
        st.write(f"体重: {weight} kg")
        st.write(f"骨格タイプ: {body_type}")
        st.write(f"運動頻度: {exercise}")
        st.write(f"食生活: {diet}")
        st.write(f"睡眠時間: {sleep_hours} 時間")

    # ユーザーデータをCSVに追記保存
    user_data = {
        "性別": gender,
        "年齢": age,
        "身長": height,
        "体重": weight,
        "骨格タイプ": body_type,
        "運動頻度": exercise,
        "食生活": diet,
        "睡眠時間": sleep_hours
    }
    df = pd.DataFrame([user_data])
    if os.path.exists("user_data.csv"):
        df.to_csv("user_data.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("user_data.csv", index=False)
    st.success("基本情報が保存されました！")

    st.header("診断結果")

    bmi = weight / ((height / 100) ** 2)

    

    # フィードバックはカテゴリごとにリストで保持
    feedback = {"体型": [], "骨格": [], "運動": [], "食事": [], "睡眠": []}

    # BMI判定とフィードバック
    if bmi < 18.5:
        feedback["体型"].append(f"あなたのBMIは {bmi:.1f} で「やせ型」です。健康的な体重を目指して、栄養バランスの良い食事を心がけましょう。")
    elif 18.5 <= bmi < 25:
        feedback["体型"].append(f"あなたのBMIは {bmi:.1f} で「標準体型」です。この体型を維持するために、今後も運動や食生活に気を配りましょう。")
    elif 25 <= bmi < 30:
        feedback["体型"].append(f"あなたのBMIは {bmi:.1f} で「肥満（1度）」です。体重を減らすことで健康リスクを下げられます。運動と食事改善を心がけましょう。")
    else:
        feedback["体型"].append(f"あなたのBMIは {bmi:.1f} で「肥満（2度以上）」です。医師や栄養士に相談し、無理のない範囲で生活改善を始めましょう。")

    # 骨格別アドバイス
    if body_type == "ウェーブ":
        feedback["骨格"].append("脂肪を抑えてたんぱく質を多めに摂取しましょう。また、有酸素運動をメインに行うとよいです。")
    elif body_type == "ナチュラル":
        feedback["骨格"].append("腸内環境を整えることが大切です。また、全身を使った運動や姿勢改善を行うとよいです。")
    elif body_type == "ストレート":
        feedback["骨格"].append("水分をしっかりととり、脂質と糖質の取りすぎに注意しましょう。また、短時間・高強度のトレーニングを行うとよいです。")

    # 運動習慣に関するアドバイス
    if exercise == "ほとんどしない":
        feedback["運動"].append("運動の習慣を少しずつ取り入れると、基礎代謝が上がり脂肪燃焼につながります。")
    elif exercise == "週5回以上":
        feedback["運動"].append("週に5回以上運動していて素晴らしいですね！継続することが大切です。")

    # 食事習慣に関するアドバイス
    if diet != "バランス良い":
        feedback["食事"].append("食事のバランスに注意が必要です。野菜、タンパク質、炭水化物をバランスよく摂るようにしましょう。")

    # 睡眠時間に関するアドバイス
    if sleep_hours < 6:
        feedback["睡眠"].append("睡眠時間が短めです。睡眠不足は食欲の乱れや代謝低下を引き起こすため、もう少し睡眠を確保しましょう。")
    elif sleep_hours > 9:
        feedback["睡眠"].append("睡眠時間がやや長めです。適度な睡眠（6〜8時間）が理想的です。")






    # アドバイス結果の表示（expander付き）
    st.subheader("🧾 あなたへのアドバイス")
    for category, items in feedback.items():
        if items:
            with st.expander(f"▶ {category}に関するアドバイス"):
                for item in items:
                    st.markdown(f"- {item}")

    # 健康的な生活者へのメッセージ
    if 18.5 <= bmi < 25 and exercise in ["週3〜4回", "週5回以上"] and diet == "バランス良い" and 6 <= sleep_hours <= 8:
        st.success("とても健康的な生活を送っていますね！この調子で続けましょう！")
        st.balloons()

    
    # --- 特化アドバイスデータ ---
     # フィードバックはカテゴリごとにリストで保持
    feedback = {"体型": [], "骨格": [], "運動": [], "食事": [], "睡眠": []}

   

    # 骨格別アドバイス
    if body_type == "ウェーブ":
        feedback["骨格"].append("""〇向いている運動
                              
・リズム系有酸素運動：ダンス、エアロビクス
                              
・軽めの筋トレ（特にインナーマッスル）
                              
・ストレッチやヨガ
→ 血流を促進して代謝を上げることがカギ

                              
✖向いていない運動
                              
・過度な筋トレ（特に下半身）
→ 太ももやふくらはぎがたくましく見えやすい
                              
・長時間のハード有酸素運動
→ 疲れやすく、筋肉が分解されやすい傾向""")
        
    elif body_type == "ナチュラル":
        feedback["骨格"].append("""〇向いている運動
                              
・スポーツ全般：バスケ、テニスなど動きのあるもの

・サーキットトレーニング：筋トレ×有酸素の組み合わせ

・中〜高負荷の筋トレ
→ 骨格がしっかりしているので、筋肉をつけてもバランスがとれる

                              
✖向いていない運動
                              
・単調な軽めの運動のみ（ウォーキングだけ、など）
→ 筋肉や骨格が強いので、軽すぎる運動は効果が出にくい

・過度なストレッチのみ
→ 体が元々しなやかではない場合、ストレッチだけでは整わない""")
        
    elif body_type == "ストレート":
        feedback["骨格"].append("""〇向いている運動
                              
・有酸素運動（軽め）：ウォーキング、スイミング

・ストレッチ系：ヨガ、ピラティス

・体幹トレーニング：プランク、バランスボール
→ 筋肉がつきやすいので、激しい筋トレより「整える」系が◎

                              
✖向いていない運動
                              
・ハードな筋トレ（スクワット・ダンベルなど高負荷）

・ハイインパクト系の運動（HIIT、ジャンプを多用するもの）
→ 筋肉太りしやすく、ゴツく見えがちになる可能性

""")

    elif body_type == "わからない":
        feedback["骨格"].append("""以下のURLから骨格診断を行ってみましょう！
\n https://www.vivi.tv/shindan-skeletalframe-rm22syx6gb6f/""")


    # アドバイス結果の表示（expander付き）
    st.subheader("🧾 詳しいアドバイス(運動)")
    for category, items in feedback.items():
        if items:
            with st.expander("あなたの骨格に効果のある運動は？"):
                for item in items:
                    st.code(item)

 # --- 特化アドバイスデータ食事 ---
     # フィードバックはカテゴリごとにリストで保持
    feedback = {"体型": [], "骨格": [], "運動": [], "食事": [], "睡眠": []}

   

    # 骨格別アドバイス
    if body_type == "ウェーブ":
        feedback["骨格"].append("""〇太りにくい食べ物
                              
・体を温める食材（生姜、根菜、味噌汁）

・低GIの炭水化物（玄米、全粒粉パン、オートミール）

・煮物・蒸し物など温かい和食

・魚や大豆製品、白身肉（脂肪少なめで消化にやさしい）

                              
✖太りやすい食べ物
                              
・冷たいもの（アイス、冷たいドリンク、生野菜中心のサラダ）

・甘いお菓子やパン、ケーキなど糖質が高いもの

・カフェインやアルコール（代謝を乱しやすい）

・脂質の多い洋菓子（バタークッキー、クロワッサンなど）""")
        
    elif body_type == "ナチュラル":
        feedback["骨格"].append("""〇太りにくい食べ物
                              
・ナッツや全粒粉など自然な食材（適量ならOK）

・良質なタンパク源（卵、納豆、鮭など）

・シンプルでナチュラルな食事（和食中心）

・野菜や海藻を多く取り入れたバランス食事
                              
                              
✖太りやすい食べ物
                              
・ジャンクフード、加工食品（ポテチ、ファストフードなど）

・味が濃いものや塩分多めの食品（ラーメン、漬物など）

・食べ過ぎ（腹八分を超える食事）""")
        
    elif body_type == "ストレート":
        feedback["骨格"].append(""" 〇太りにくい食べ物
                              
・高たんぱく・低脂質な食材（鶏胸肉、豆腐、卵白）

・食物繊維の多い野菜（キャベツ、ブロッコリー、きのこ類）

・良質な炭水化物（玄米、雑穀米、さつまいも）

・スープや蒸し料理など脂を使わない調理法が◎
                              

✖太りやすい食べ物
                              
・脂質の多いもの（とんかつ、唐揚げ、揚げ物全般）

・油を多く使った料理（中華、カルボナーラなど）

・生クリームやチーズなどの乳脂肪分

・高GI値の白ご飯・パンを大量に食べる
""")

    elif body_type == "わからない":
        feedback["骨格"].append("""以下のURLから骨格診断を行ってみましょう！
\n https://www.vivi.tv/shindan-skeletalframe-rm22syx6gb6f/""")

    # アドバイス結果の表示（expander付き）
    st.subheader("🧾 詳しいアドバイス（食事）")
    for category, items in feedback.items():
        if items:
            with st.expander("あなたの骨格に影響を与える食事は？"):
                for item in items:
                    st.code(item)

    

      

  