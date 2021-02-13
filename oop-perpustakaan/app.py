from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from MySQLdb.connections import Connection

app = Flask(__name__, static_url_path="")

# fungsi koneksi database

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'perpustakaan'
mysql = MySQL(app)

# menampilkan index


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# menampilkan anggota


@app.route('/anggota')
def anggota():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM anggota")
    rv = cur.fetchall()
    cur.close()
    return render_template('anggota.html', anggota=rv)

# menampilkan daftar buku


@app.route('/daftarbuku')
def buku():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM buku")
    rv = cur.fetchall()
    cur.close()
    return render_template('daftarbuku.html', buku=rv)

# menampilkan daftar peminjam


@app.route('/daftarpeminjambuku')
def peminjam():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pinjam")
    rv = cur.fetchall()
    cur.close()
    return render_template('daftarpeminjambuku.html', peminjam=rv)

# menampilkan aboutus


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

# fungsi view tambah() untuk membuat form tambah


@app.route('/tambahbuku', methods=['GET', 'POST'])
def tambahbuku():
    if request.method == 'POST':
        judul = request.form['JUDUL']
        pengarang = request.form['PENGARANG']
        tahun_terbit = request.form['TAHUN_TERBIT']
        val = (judul, pengarang, tahun_terbit)
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO buku (JUDUL, PENGARANG, TAHUN_TERBIT) VALUES (%s, %s, %s)", val)
        mysql.connection.commit()
        return redirect(url_for('daftarbuku'))
    else:
        return render_template('tambahbuku.html')
# fungsi view edit() untuk form edit


@app.route('/editbuku/<KD_BUKU>', methods=['GET', 'POST'])
def edit_buku(KD_BUKU):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM buku WHERE KD_BUKU=%s', (KD_BUKU,))
    data = cur.fetchone()
    if request.method == 'POST':
        buku = request.form['KD_BUKU']
        judul = request.form['JUDUL']
        pengarang = request.form['PENGARANG']
        tahun_terbit = request.form['TAHUN_TERBIT']
        val = (judul, pengarang, tahun_terbit, buku)
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE buku SET JUDUL=%s, PENGARANG=%s, TAHUN_TERBIT=%s WHERE KD_BUKU=%s", val)
        mysql.connection.commit()
        return redirect(url_for('daftarbuku'))
    else:
        return render_template('editbuku.html', data=data)
# fungsi untuk menghapus data


@app.route('/hapus/<KD_BUKU>', methods=['GET', 'POST'])
def hapus(KD_BUKU):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM buku WHERE KD_BUKU=%s', (KD_BUKU,))
    mysql.connection.commit()
    return redirect(url_for('daftarbuku'))


if __name__ == '__main__':
    app.run(debug=True)
