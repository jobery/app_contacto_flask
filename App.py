from flask import Flask,render_template,request,url_for,redirect,flash
from pymysql import *

app = Flask(__name__)

#Coneccion
conexion = connect(host='localhost', user = 'admin', password ='admin', database = 'contacts')

#Configuraciones
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM contact ')
    data = cursor.fetchall()
    return render_template('index.html',contacts = data)

@app.route('/add_contact',methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']        
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO contact(fullname,phone,email)VALUES(%s,%s,%s)',(fullname,phone,email))
        conexion.commit()
        flash('Contacto Registrado con Exito')
        return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def get_contact(id):
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM contact WHERE id = %s',(id))
    data = cursor.fetchall()
    print(data)
    return render_template('editar.html',contact=data[0])

@app.route('/editar_contacto/<int:id>',methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cursor = conexion.cursor()
        cursor.execute('UPDATE contact SET fullname = %s,phone = %s,email = %s WHERE id = %s',(fullname,phone,email,id))
        conexion.commit()
        flash('Registro Actualizado con Exito')
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM contact WHERE id = {0}'.format(id))
    conexion.commit()
    flash(message='Contacto Eliminado con Exito')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=3000,debug=True)