from flask import Flask, render_template, request, redirect, url_for ,flash #Conectarse a al html, Direccionar en html, request trabajar en pagina, redireccionar en la pagina, enviar a algun lugar, agregar en html
#Contectarse a la base de datos con flasck
from flask_mysqldb import MySQL

#Obtener un coneccion a la red
app = Flask(__name__)#Name es el parametro

#Nombrar base de datos donde se debe conectar
app.config['MySQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin123'
app.config['MYSQL_DB'] = 'flaskcontacts'

#Configuraciones

app.secret_key = 'mysecretkey'

#Configuracion a la DB
mysql = MySQL(app)
 
#Decorador
@app.route('/')

#Crear una funcion
def Index():

    #Obtener datos al iniciar
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()

    #Enviar datos al html
    return render_template('index.html', contacts = data)

#Recibir informacion del html
@app.route('/add_contact',methods=['POST'])

def add_contact():

    if request.method == 'POST':

        #llamar datos de index
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

         #Conectarse a mysqlDB
        cur = mysql.connection
        cur1 = cur.cursor()
        cur1.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added successfully')

        #return 'recived'

        #Redireccionar a la pagina principal
        return redirect(url_for('Index'))




@app.route('/edit_contact/<id>')

def editar(id):

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE  id = %s', (id))#Selecciona el valor del id e insertalo en sql)
    data = cur.fetchall()
    print(data)
    return render_template('edit-contact.html', contact = data[0])

#Informacion para actualizar
@app.route('/update/<id>', methods = ['POST'])

def update_contact(id):
    
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
            phone = %s,
            email = %s
            WHERE id = %s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
        flash('Contact Updated Successfully')
        
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>')

def delete_contact(id):

    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'. format(id))#Donde esta el cero premplaza con una id
    mysql.connection.commit()
    
    flash('Contanct Removed Successfully')
    return redirect(url_for('Index'))

 #Verificar que se este ajecutando en app
if __name__ =='__main__':

    #Correr el programa puerto numero 3000 y debug sirve para reiniciar el servidor
    app.run(port=3000, debug=True)