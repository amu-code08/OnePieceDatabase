# データベースアプリケーションプログラミング演習

## 容量の確認

Flaskの環境構築は、ITCのCGI実行環境の厳密なルールに従う必要があるため、このマニュアルを逸脱しないようにしてください。Flaskはこちらが用意したPythonのバージョンを使用し、ホームディレクトリ内に仮想環境を構築する必要があります（/workなどは不可）。環境構築のため、160MB以上の空き容量が必要になります。以下のページを参考に、空き容量の確認及び不必要なファイルの移動を行ってください。

https://www.st.itc.keio.ac.jp/ja/com_ws_home_st.html#linux

## サンプルアプリのインストールとデプロイ

setupスクリプトを使用して、仮想環境の構築・サンプルアプリのインストール・ITCサーバーへのデプロイを行います。

1. ITCにRDPで接続するか`ssh ubXXXXXX@remote.educ.cc.keio.ac.jp` にSSHログインする（ITCのPCを使用する場合は不要）
2. `bash /home/kyozai/dm_flask/setup.sh` を実行
3. ~/dm_srcディレクトリにソースが展開され、http://user.keio.ac.jp/~ubXXXXXX/dm_app にデプロイされます。
4. setupスクリプトでは以下のことを設定できます。必要に応じて、setup.shをコピーして書き換えてください。
    - APP_SRC=$HOME/dm_src  ##ソースをインストールするディレクトリ。必ず$HOME内にする
    - APP_NAME=dm_app  ##デプロイ先のURI
5. サンプルアプリにはログインユーザ情報が登録されていません。最初に適当な名前でサインアップする必要があります。

## Python仮想環境の有効化

1. `cd ~/dm_src` コマンドで移動します。
2. `source venv/bin/activate` コマンドで仮想環境を起動します。
    1. ターミナルに(venv)が表示されるようになります。
    2. setup.shを使用した場合、Flaskがすでにインストールされています。
    3. 仮想環境のPythonのバージョンを使用しないとWebサーバー側で動きません！
3. 仮想環境を終了する場合、`deactivate` を実行します。

## テスト環境でのアプリケーション実行

`flask run`を使用してテスト環境でアプリケーションを実行します。

### ローカル環境（ITCのPC or Remote Desktop内）での実行

1. appディレクトリで `flask run` を実行します。
2. Webブラウザで [http://127.0.0.1:5000](http://127.0.0.1:5000/) にアクセスします。

### SSH環境での実行　※TAサポートなし

1. 別のターミナルで、 `ssh -L 5000:127.0.0.1:5000 ubXXXXXX@remoteX.educ.cc.keio.ac.jp` を実行します（ubXXX…は自分のITCアカウント、remoteXをログイン中のサーバ名に変更）
2. appディレクトリで `flask run` を実行します。
3. Webブラウザで [http://127.0.0.1:5000](http://127.0.0.1:5000/) にアクセスします。

### VSCodeでの実行　※TAサポートなし

1. VSCodeにSSH extensionをインストールします。
2. VSCode上でSSHを使用してサーバに接続します。SSH鍵を設定しておくとパスワードの入力が煩雑になりません。
3. VSCode上でディレクトリを開きます。
4. VSCodeのターミナルでappディレクトリで `flask run` を実行します。
5. ポップアップからWebブラウザを表示することができます。

## データベースの構築

database.dbはサンプルのデータベースが入っています。そのまま、`rm database.db`で削除し、自分のデータベースファイルを使用することができます。サンプルデータベースを再インストールする場合、`sqlite3 database.db < sample.sql` を実行します。

## デプロイの設定

デプロイを止めたい場合、\~/public_html/dm_app (URIを変更した場合は\~/public_html/$APP_NAME)のディレクトリを削除します。再デプロイする場合、環境構築するときに使用したsetup.shを使用します。

（注：setup.shを実行すると、ディレクトリ$APP_SRC, $APP_SRC/venvがない場合サンプルアプリが再インストールされます。 $APP_SRC/database.dbがない場合サンプルアプリのデータベースが読み込まれます。必要に応じてソースのバックアップをとってください。）

（chmod 700 ~/public_html/dm_appでデプロイ停止、chmod 755 ~/public_html/dm_appで再デプロイすることも可能です。多少のラグが生じます）


## セキュリティ上の注意

ITCのサーバはSSL/TLSによる暗号化をサポートしていません。password等は平文で通信されるので重要なパスワードを使用することは避けてください。

## FAQ

- flaskがない
    - 仮想環境に入っているか確認する(source venv/bin/activate)
- ブラウザからテスト環境にアクセスできない
    - flask runがエラーをはいていないか確認する
    - リモートの場合、Remote Desktopでローカル環境でできないかまずためす
- 変更が反映されない
    - flask run を起動しなおす
- ブラウザから本番環境にアクセスできない
    - Internal Errorが表示される
        - Flaskのアプリケーション側の問題の可能性があるので、テスト環境で動くか確かめる
        - setup.shを再実行する
    - Not foundが表示される
        - setup.shを再実行する
    - Forbiddenが表示される
        - public_html, public_html/dm_appの権限を確認する（755）
        - public_html/dm_appを削除してsetup.shを再実行する
