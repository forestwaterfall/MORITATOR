# MORITATOR
人工衛星地上局　アンテナ制御ソフト

## 使用ライブラリ

* ephem 軌道計算
* wxPython GUI作成
* serial ローテーター制御マイコンとのシリアル通信用
* openpyxl エクセル操作用

## 各ファイル概要

* [main.py](#main.py)  
    フロントエンド部の大枠。moritator_main_class.pyを呼び出し
* [main_class.py](#main_class.py)  
　　　　　　　　GUIの基本構成を構築しているクラス
    wxFormBuilder というGUIを作成するためのGUIソフト上でGUIの構成を決定し，コードを自動生成したもの．（wxFormBuilder側の保存ファイル消失後は手修正している）
    wxFormBuilder側の保存ファイルもあれば良いのだが，ファイル破損のため消失．
* [MORITATOR.bat](#MORITATOR.bat)  
    main.pyを呼び出し
* [MORITATOR.vbs](#MORITATOR.vbs)  
    MORITATOR.batを呼び出し
* [moritator_main_class.py](#moritator_main_class.py)  
    フロントエンドとPID制御部
    main_class.pyのクラスを継承している
    継承して作成している理由はwxFormBuilderが理由（wxFormBuilderがmain_classを作成し，それを継承したクラスで人間が処理を記述するという方法．人間はmain_classには手をつけず，GUIを変更する必要があるときはwxFormBuilder上で編集し，コードを生成することで変更するという方法．なお，MORITATORではwxFormBuilder側の保存ファイルが破損したためこの方法は守っていない．）
* [ope_voltage.py](#ope_voltage.py)  
    AzimuthとElevationへの出力電圧算出？
* [orbit.py](#orbit.py)  
    軌道計算関数。TLEと時刻から、AzimuthとElevationの角度を算出する
* [req.py](#req.py)  
    衛星番号と衛星名の紐づけ、space-trackからのTLE取得プログラム
    TLE取得の予備手段として，space-trackが使用できない場合は自動的にcelestrakから取得
    ひろがりの運用時は最後に取得したTLEを保存し，space-trackとcelestakのいずれにもアクセスできない場合にバックアップのものを使用
* [setting.py](#seting.py)  
    ユーザー設定ファイル(他の衛星の番号など)関係の関数、シリアルのポート一覧取得関数
* [south_judge.py](south_judge.py)  
    大旋回の判定部

## 複数衛星追跡機能について
    複数衛星追跡機能は，設定ファイルで指定した複数の衛星を追跡対象とする機能である．
    追跡対象の衛星を追加するには，setting/background_sat.txt に1行ずつ，"衛星名,NORAD_ID" のようなカンマ区切りの形式で衛星の情報を記入する．
    GUI上で，Track Multiple Satelliteのチェックボックスにチェックを入れるとこの機能が有効になる．
    この機能を有効にしている際に他の衛星を手動で選択すると，この機能はオフとなり，手動で選択した衛星の追尾を開始する．
