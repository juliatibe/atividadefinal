from flask import Flask, render_template,  request, flash, url_for, redirect
import fdb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ua_chave_secreta_aqui'

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\BANCO (2)\BANCO.FDB'
user = 'sysdba'
password = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=password)


class Cadastro:
    def __int__(self, id_cadastro, nome, email, senha):
        self.id_cadastro = id_cadastro
        self.nome = nome
        self.email = email
        self.senha = senha

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')



@app.route('/abrir_cadastro')
def abrir_cadastro():
    return render_template('cadastro.html')

@app.route('/criar_cadastro', methods=['POST'])
def criar_cadastro():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Criando o cursor
    cursor = con.cursor()

    try:
        # Verificar se o livro já existe
        cursor.execute("SELECT 1 FROM CADASTRO c WHERE EMAIL = ?", (email,))
        if cursor.fetchone():  # Se existir algum registro
            flash("Erro: Email já cadastrado.", "error")
            return redirect(url_for('abrir_cadastro'))

        # Inserir o novo livro (sem capturar o ID)
        cursor.execute("INSERT INTO CADASTRO (NOME, EMAIL, SENHA) VALUES(?, ?, ?)",
                       (name, email, password))
        con.commit()
    finally:
        # Fechar o cursor manualmente, mesmo que haja erro
        cursor.close()

    flash("Veterinário cadastrado com sucesso!", "success")
    return redirect(url_for('index'))



@app.route('/cadastro')
def cadastro():
    cursor = con.cursor()
    cursor.execute('SELECT id_cadastro, nome, email, senha FROM cadastro')
    cadastro = cursor.fetchall()
    cursor.close()
    return render_template('cadastro.html', cadastro=cadastro)


@app.route('/veterinario')
def veterinario():
    return render_template('veterinario.html')



if __name__ == '__main__':
    app.run(debug=True)










