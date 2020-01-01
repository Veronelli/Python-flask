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



@app.route('/edit_contact')

def editar():

    return 'Edit contact'

@app.route('/delete')

def delete_contact():

    return 'Delete Contact'

 #Verificar que se este ajecutando en app
if __name__ =='__main__':

    #Correr el programa puerto numero 3000 y debug sirve para reiniciar el servidor
    app.run(port=3000, debug=True)