import imaplib
import email

UserName = "" #メールアドレス
PassName = "" #パスワード（Gmailの場合アプリパスワード推奨）

gmail = imaplib.IMAP4_SSL("imap.gmail.com", '993') #サーバ指定
gmail.login(UserName, PassName) #ログイン
gmail.select() #ラベル指定、空なら全て

head, data = gmail.search(None, 'UNSEEN') #UNSEEN（未読）でサーチ

# 取得したメール一覧の処理
for num in data[0].split():
    h, d = gmail.fetch(num, '(RFC822)')
    raw_email = d[0][1]
    # 文字コードを判別、なければiso-2022-jpとして処理
    msg = email.message_from_string(raw_email.decode('utf-8'))
    msg_encoding = email.header.decode_header(msg.get('Subject'))[0][1] or 'iso-2022-jp' 
    # メールタイトルを取得
    msg_subject = email.header.decode_header(msg.get('Subject'))[0][0]
    # エンコーディング
    subject = str(msg_subject.decode(msg_encoding))
    print(subject)

    # 本文抽出（シングルパート？マルチパート？なんそれ？ってなったらじっくり調べてみてね！）
    if msg.is_multipart() is False: # シングルパートなら
        payload = msg.get_payload(decode=True)
        charset = msg.get_content_charset()
        if charset is not None:
            payload = payload.decode(charset, "ignore")
        print(payload)
        print()
    else: #マルチパートなら
        for part in msg.walk():
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            charset = part.get_content_charset()
            if charset is not None:
                payload = payload.decode(charset, "ignore")
            print(payload)
            print()

# 終了処理
gmail.close()
gmail.logout()

print("完了")