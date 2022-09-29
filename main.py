from flask import Flask, redirect, url_for, render_template, request, flash
from datetime import datetime
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_cbw'

mysql = MySQL(app)


@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM emergencia ORDER BY id DESC")
    emergencias = cursor.fetchall()
    cursor.close()
    return render_template('index.html', emergencias=emergencias)
   

@app.route('/crear-emergencia', methods=['GET', 'POST'])
def crear_emergencia():
    
    if request.method == 'POST':

        clave = request.form['clave']
        direc = request.form['direccion']
        fecha = request.form['fecha']
        desc = request.form['descripcion']
        estado = request.form['estado']

        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO emergencia VALUES(NULL, %s, %s, %s, %s, %s)", (clave, direc, fecha, desc, estado))
        cursor.connection.commit()
        
        return redirect(url_for('index'))
    
    return render_template('create_emer.html')


@app.route('/editar-emergencia/<emergencia_id>', methods=['GET', 'POST'])
def editar_emergencia(emergencia_id):

    if request.method == 'POST':

        clave = request.form['clave']
        direc = request.form['direccion']
        fecha = request.form['fecha']
        desc = request.form['descripcion']
        estado = request.form['estado']
        
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE emergencia
            SET clave = %s,
                direccion = %s,
                fecha = %s,
                descripcion = %s,
                estado = %s
            WHERE id = %s
        
        """, (clave, direc, fecha, desc, estado, emergencia_id))
        cursor.connection.commit()
        
        #flash('Haz editado el coche correctamente!!')
        return redirect(url_for('index'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM emergencia WHERE id=%s", (emergencia_id))
    emer = cursor.fetchall()
    cursor.close()

    return render_template('create_emer.html', emer=emer[0])


if __name__ == '__main__':
    app.run(debug=True)