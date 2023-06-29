from flask import Flask, render_template, request, g, redirect, url_for, session, flash
import uuid
import hashlib
import sqlite3
import os, datetime
from dataclasses import dataclass
from datetime import timedelta

DATABASE = "database.db"
app = Flask(__name__, static_folder='./static')
app.config['SECRET_KEY'] = '1234'

@app.before_request
def before_request():
    # リクエストのたびにセッションの寿命を更新する
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)
    session.modified = True

"""
データベース接続
"""
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

"""
ビュー
"""
@app.route('/')
def home():
    # セッションにuser_idがない場合、未ログインなのでusernameを渡さずにHTMLをレンダリング
    if 'user_id' not in session:
        return render_template('home.html')
    # ユーザ情報がある場合、データベースに接続しuser_idからユーザ名を検索して渡す
    conn = get_db()
    cur = conn.cursor()
    user = cur.execute('SELECT * FROM LoginUser WHERE username = ?', (session['user_id'],)).fetchone()
    return render_template('home.html', username=user['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    error = None
    # POSTはこの関数の一番下のlogin.htmlから呼ばれ、その中のフォームを送信する。フォームの内容に基づき、ユーザ情報を照合する
    if request.method == 'POST':
        # フォームの内容を取得する
        username = request.form['username']
        password = request.form['password']
        # パスワードは平文ではなくハッシュ値で照合する
        h = hashlib.md5(password.encode())
        conn = get_db()
        cur = conn.cursor()
        user = cur.execute('SELECT * FROM LoginUser WHERE username = ? AND password = ?', (username, h.hexdigest())).fetchone()
        if user is None:
            # ユーザ認証されなかった場合、エラーメッセージをレンダリングする。メッセージはこのように引数で渡すこともできるし、else以下のようにflashを使用することもできる。
            error = 'Invalid username or password'
        else:
            # ユーザ認証された場合、セッションに記録する
            session['user_id'] = username 
            # flashメッセージを設定する
            flash("Logged in")
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = get_db()
    cur = conn.cursor()
    request_valid = True
    if request.method == 'POST':
        # フォームの内容を取得し、バリデーションを行う。エラーがあればflashメッセージで通知する
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        if not username:
            flash('Username is required')
            request_valid = False
        if not password:
            flash('Password is required')
            request_valid = False
        if password != confirm:
            flash('Passwords do not match')
            request_valid = False
        if cur.execute('SELECT * FROM LoginUser WHERE username = ?',(username,)).fetchone():
            # ユーザーがすでに存在している場合はエラーを表示する
            flash('This username is already taken')
            request_valid = False
        if request_valid:
            # 新しいユーザーを作成する
            h = hashlib.md5(password.encode())
            cur.execute('INSERT INTO LoginUser (username, password) VALUES (?, ?)', (username, h.hexdigest()))
            conn.commit()
            # ログインページにリダイレクトする
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    if session.pop('user_id', None):
        flash("Logged out")
    return redirect(url_for('home'))


@app.route("/employee", methods=["GET", "POST"])
def employee():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    # POSTは検索をするとリクエストされる
    if request.method == "POST":
        elist = cur.execute("SELECT e.*, m.name as manager_name FROM employee e, employee m WHERE m.id = e.manager AND e.name LIKE ? ORDER BY e.id", ('%'+request.form["name"]+'%', )).fetchall()
        return render_template("employee.html", counts=len(elist), elist=elist, query_name=request.form["name"])
    else:
        # GETの場合全件のデータベースルックアップをする。返ってくるテーブルの属性名で属性にアクセスするので、SQLで属性名を適切に設定する
        elist = cur.execute("SELECT e.*, m.name as manager_name FROM employee e, employee m WHERE m.id = e.manager ORDER BY e.id").fetchall() ## XXX: managerがいないと表示されない。managerがいない人も表示させるにはouter joinする。
        return render_template("employee.html", counts=len(elist), elist=elist)
    

@app.route("/employee/<id>")
def emp_master(id):
    # 各従業員（idは従業員番号）の詳細情報
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee e WHERE e.id = ?", (id,))
    emp = cur.fetchone()
    if not emp:
        flash(f"Error: No employee entry {id}", "error")
        return redirect(url_for("employee"))
    return render_template("emp_detail.html", emp=emp)


@app.route("/onboard", methods=["GET", "POST"])
def emp_new():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    if request.method == "POST":
        request_valid = True
        return_data = { "form": request.form } # エラーメッセージなどを渡すためレンダラに渡すデータが大きくなる。よって辞書として管理する。

        ## idを確認（数値である＆被りがない）
        entry = cur.execute('SELECT name FROM employee e WHERE e.id = ?', (request.form['id'],)).fetchone()
        if not request.form['id'].isdigit() or entry:
            request_valid = False
            return_data["id_invalid"] = "IDが不正です。"
        else:
            id = int(request.form['id'])

        ## managerを確認
        manager_entry = cur.execute('SELECT name FROM employee e WHERE e.id = ?', (request.form["manager"],)).fetchone()
        if  request.form["manager"] != "0" and not manager_entry:
            request_valid = False
            return_data["manager_invalid"] = "Manager IDが不正です。"

        ## 名前と誕生年の確認
        if not (request.form['byear'] and request.form['byear'].isdigit()):
            request_valid = False
            return_data['byear_invalid'] = "誕生年を記入してください。"
        if not request.form['name']:
            request_valid = False
            return_data['name_invalid'] = "名前を記入してください。"

        ## Fileを確認
        if 'pict' not in request.files:
            request_valid = False
            return_data["pict_invalid"] = "画像が添付されていないか、拡張子が不正です。"
        else:
            file = request.files["pict"]
            if file.filename == "" or not file.filename.endswith(('jpg', 'jpeg', 'png')):
                request_valid = False
                return_data["pict_invalid"] = "画像が添付されていないか、拡張子が不正です。"
            elif request_valid:
                # 他の情報も正しい場合、送信されたファイルをidにリネームして保存する。
                filename = str(id) + os.path.splitext(file.filename)[1]
                file.save(os.path.join('./static/pict', filename))

        ## Insertを行う
        if request_valid:
            try:
                cur.execute('INSERT INTO employee (id,name,salary,manager,byear,syear,pict) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        [id, request.form['name'], 100, request.form['manager'],
                        request.form['byear'], datetime.date.today().year, filename])
            except sqlite3.Error as e:
                print('sqlite3.Error occurred:', e.args[0])
                request_valid = False
                return_data['db_error'] = True
            conn.commit() ## 更新はcommitが必要

        if request_valid:
            flash("Registered. ID:{} NAME:{}（Manager:{}）".format(id, request.form['name'], manager_entry['name']))
            return redirect(url_for("employee"))
        else:
            return render_template("emp_new.html" ,**return_data)

    else:
        return render_template("emp_new.html", form={})


@app.route("/employee/<id>/edit", methods=["GET", "POST"])
def emp_edit(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    emp = cur.execute('SELECT * FROM employee e WHERE e.id = ?',[id]).fetchone()
    if not emp:
        flash(f"Invalid id {id}", "error")
        return redirect(url_for("employee"))

    if request.method == "GET":
        return render_template('emp_edit.html', emp=emp)

    if request.method == "POST":
        request_valid = True
        return_data = { "emp": {**emp, **request.form} }

        ## managerを確認
        manager_entry =cur.execute('SELECT name FROM employee e WHERE e.id = ?',[request.form["manager"]]).fetchone() 
        if request.form["manager"] != "0" and not manager_entry:
            request_valid = False
            return_data["manager_invalid"] = "Manager IDが不正です。"

        ## Fileを確認
        file = request.files["pict"] if 'pict' in request.files else None
        if not file:
            filename = emp["pict"]
        elif not file.filename.endswith(('jpg', 'jpeg', 'png')):
            request_valid = False
            return_data["pict_invalid"] = "画像の拡張子が不正です。"
        elif request_valid:
            filename = str(id) + os.path.splitext(file.filename)[1]
            file.save(os.path.join('./static/pict', filename))

        ## Insertを行う
        if request_valid:
            try:
                cur.execute('UPDATE employee SET  name=?, salary=?, manager=? ,pict=? WHERE id=?',
                        [request.form['name'], request.form['salary'], request.form['manager'],filename,id])
            except sqlite3.Error as e:
                print('sqlite3.Error occurred:', e.args[0])
                request_valid = False
                return_data['db_error'] = True
            conn.commit() ## 更新はcommitが必要

        if request_valid:
            flash(f"Updated {emp['name']} (Id:{id})")
            return redirect(url_for("employee"))
        else:
            return render_template("emp_edit.html", id=id, **return_data)


@app.route("/employee/<id>/delete", methods=["GET", "POST"])
def emp_delete(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == "GET":
        return emp_master(id)

    conn = get_db()
    cur = conn.cursor()
    request_valid = True

    ## マネージャかどうか確認
    is_manager = cur.execute('SELECT e.name FROM employee e WHERE e.manager = ?', (id,)).fetchone()
    if not is_manager:
        emp = cur.execute('SELECT name FROM employee e WHERE e.id = ?',(id,)).fetchone()
        ## Deleteを行う
        try:
            cur.execute('DELETE FROM employee WHERE id = ?',(id,))
        except sqlite3.Error as e:
            print('sqlite3.Error occurred:', e.args[0])
            request_valid = False
        if request_valid:
            conn.commit()
            flash(f"Deleted {emp['name']} (ID:{id})")
            return redirect(url_for("employee"))
        else:
            return redirect(url_for("emp_master", id=id))
    else:
        flash('Managerとして登録されています', "error")
        return redirect(url_for('emp_master', id=id))

# pythonを直接実行したときでもflask run --debugと同じ挙動となるようにする
if __name__ == '__main__':
    app.run(debug=True)
