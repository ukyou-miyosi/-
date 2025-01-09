import os
import webbrowser
import subprocess
import sys

# 必要なパッケージがインストールされているか確認し、インストールする関数
def install_package(package):
    # 指定されたパッケージをインストールするコマンドを実行
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# speech_recognition パッケージのインポートを試みる
try:
    import speech_recognition as sr
except ImportError:
    # パッケージがインストールされていない場合、インストール処理を行う
    print("speech_recognition がインストールされていません。インストールします...")
    install_package('speechrecognition')  # インストールコマンドを実行
    import speech_recognition as sr  # インストール後、再度インポート

# pyaudio パッケージのインポートを試みる
try:
    import pyaudio
except ImportError:
    # パッケージがインストールされていない場合、インストール処理を行う
    print("pyaudio がインストールされていません。インストールします...")
    install_package('pyaudio')  # インストールコマンドを実行
    import pyaudio  # インストール後、再度インポート

# 音声認識オブジェクトの生成
recognizer = sr.Recognizer()

# マイクから音声を取得する
with sr.Microphone() as source:
    print("日本語で話してください...")  # 音声を取得する前にユーザーに指示
    audio_data = recognizer.listen(source)  # マイクから音声データを取得
    print("音声を認識しています...")  # 音声認識中に表示

# 音声データをテキストに変換する
try:
    # Googleの音声認識APIを使って音声データを日本語に変換
    text = recognizer.recognize_google(audio_data, language="ja-JP")
    print("認識結果:", text)  # 認識した音声テキストを表示

    # 音声コマンドに基づいて実行するアクションを決定
    if "メモ" in text:
        print("メモを開きます...")  # コマンドに「メモ」が含まれていた場合
        os.system("notepad")  # Windowsの場合、メモ帳を開く
    elif "ブラウザ" in text:
        print("ブラウザを開きます...")  # コマンドに「ブラウザ」が含まれていた場合
        webbrowser.open("https://www.google.com")  # Googleを開く
    elif "電卓" in text:
        print("電卓を開きます...")  # コマンドに「電卓」が含まれていた場合
        os.system("calc")  # Windowsの場合、電卓を開く
    else:
        print("該当するコマンドがありません")  # 該当するコマンドがなかった場合

# 音声認識の例外処理
except sr.UnknownValueError:
    print("音声が認識できませんでした")  # 音声が認識できなかった場合
except sr.RequestError:
    print("APIに接続できませんでした")  # APIへの接続に問題があった場合