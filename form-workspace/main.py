from flask import Flask, render_template, request, redirect, url_for, flash
from services.database import connect_to_oracle, oracledb



app = Flask(__name__)
#dados mais seguros
app.secret_key = 'your_unique_and_secret_key'

#Puxar todos os dados cadastrados OK
@app.route('/')
def Index():
    connection = connect_to_oracle()
    if not connection:
        return "Failed to connect to Oracle database!", 500

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM PBI_WORKSPACES ORDER BY NR_SEQUENCIA")
        imprimir_todos_workspace = cursor.fetchall()
    finally:
        # Ensure cursor and connection are closed even on errors
        cursor.close()
        connection.close()

    return render_template('index.html', dados=imprimir_todos_workspace)

#Essa classe adiciona la dentro do banco de dados
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Workspace inserido com sucesso")
        nome = request.form['nome']
        descricao = request.form['descricao']
        imagem = request.form['imagem']
        sequencia = request.form['sequencia']  # Add semicolon here
        cor = request.form['cor']  # Add semicolon here

        connection = connect_to_oracle()
        if not connection:
            return "Failed to connect to Oracle database!", 500

        cursor = connection.cursor()
        try:
            # Use Oracle-specific placeholder syntax for values
            cursor.execute("INSERT INTO PBI_WORKSPACES (NOME, DESCRICAO, IMAGEM, NR_SEQUENCIA, COR_HEX) VALUES (:nome, :descricao, :imagem, :sequencia, :cor)",
                           {'nome': nome, 'descricao': descricao, 'imagem': imagem, 'sequencia': sequencia, 'cor': cor})
            connection.commit()
        except oracledb.Error as err:
            print("Error inserting data:", err)
            return "Error inserting data!", 500
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('Index'))



@app.route('/delete/<int:ID_WORKSPACE>', methods=['GET'])
def delete(ID_WORKSPACE):
    flash("Deletado com Sucesso")

    connection = connect_to_oracle()
    if not connection:
        return "Failed to connect to Oracle database!", 500

    cursor = connection.cursor()
    try:
        # Use Oracle's parameter binding for security
        cursor.execute("DELETE FROM PBI_WORKSPACES WHERE ID_WORKSPACE = :id", {'id': ID_WORKSPACE})
        connection.commit()
    except oracledb.Error as err:  # Catch oracledb.Error specifically
        print("Error deleting data:", err)
        return "Error deleting data!", 500
    finally:
        # Ensure cursor and connection are closed even on errors
        cursor.close()
        connection.close()

    return redirect(url_for('Index'))




@app.route('/update', methods=['POST'])
def update():
    connection = connect_to_oracle()
    if not connection:
        return "Failed to connect to Oracle database!", 500

    if request.method == 'POST':
        ID_WORKSPACE = request.form['ID_WORKSPACE']
        nome = request.form['nome']
        descricao = request.form['descricao']
        imagem = request.form['imagem']
        sequencia = request.form['sequencia']
        cor = request.form['cor']
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE PBI_WORKSPACES
                SET NOME = :nome, DESCRICAO = :descricao, IMAGEM = :imagem, NR_SEQUENCIA = :sequencia, COR_HEX = :cor
                WHERE ID_WORKSPACE = :id
            """, {'nome': nome, 'descricao': descricao, 'imagem': imagem, 'sequencia': sequencia, 'cor': cor, 'id': ID_WORKSPACE})
            connection.commit()
            flash("Workspace atualizado")
        except oracledb.Error as err:
            print("Error updating data:", err)
            return "Error updating data!", 500
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('Index'))
    
    
@app.route('/relatorios/index/<int:workspace_id>')
def relatorios(workspace_id):
    connection = connect_to_oracle()
    if not connection:
        return "Failed to connect to Oracle database!", 500

    cursor = connection.cursor()
    try:
         # Fetch the workspace name
        cursor.execute("SELECT NOME FROM PBI_WORKSPACES WHERE ID_WORKSPACE = :id", {'id': workspace_id})
        nome = cursor.fetchone()
        if nome:
            nome = nome[0]  # Extract the name from the tuple
        
        cursor.execute("SELECT * FROM PBI_RELATORIOS WHERE ID_WORKSPACE = :id", {'id': workspace_id})
        relatorios = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('relatorios/index.html', relatorios=relatorios, workspace_id=workspace_id, nome=nome)



#Essa classe adiciona la dentro do banco de dados
@app.route('/relatorios/insert', methods=['POST'])
def insert_relatorio():
    if request.method == "POST":
        nome = request.form['nome']
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        caminho = request.form['caminho']
        link = request.form['link']
        imagem = request.form['imagem']
        sequencia = request.form['sequencia']
        
        # Conectar ao banco de dados
        connection = connect_to_oracle()
        if not connection:
            return "Falha ao conectar ao banco de dados Oracle!", 500

        try:
            cursor = connection.cursor()

            # Exemplo para obter o último ID_WORKSPACE - ajuste conforme sua lógica
            cursor.execute("SELECT ID_WORKSPACE FROM PBI_WORKSPACES ORDER BY ID_WORKSPACE DESC")
            last_workspace_id = cursor.fetchone()[0]  # Assume que o ID_WORKSPACE é o primeiro campo

            # Inserir o novo relatório na tabela PBI_RELATORIOS
            cursor.execute("""
                INSERT INTO PBI_RELATORIOS (ID_WORKSPACE, NOME, DESCRICAO, TIPO, CAMINHO, LINK, IMAGEM, NR_SEQUENCIA)
                VALUES (:id_workspace, :nome, :descricao, :tipo, :caminho, :link, :imagem, :sequencia)
            """, {'id_workspace': last_workspace_id, 'nome': nome, 'descricao': descricao, 'tipo': tipo,
                  'caminho': caminho, 'link': link, 'imagem': imagem, 'sequencia': sequencia})
            
            connection.commit()

        
        except oracledb.Error as err:
            print("Erro ao inserir os dados:", err)
            return "Erro ao inserir os dados!", 500
        
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'connection' in locals() and connection is not None:
                connection.close()

        # Redirecionar para 'relatorios' com o parâmetro ID_WORKSPACE
        return redirect(url_for('relatorios', ID_WORKSPACE=last_workspace_id))





@app.route('/relatorios/update', methods=['POST'])
def editar_relatorio():
    connection = connect_to_oracle()
    if not connection:
        return "Failed to connect to Oracle database!", 500

    if request.method == 'POST':
        ID_RELATORIO = request.form['ID_RELATORIO']
        nome = request.form['nome']
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        caminho = request.form['caminho']
        link = request.form['link']
        imagem = request.form['imagem']
        sequencia = request.form['sequencia']

        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE PBI_RELATORIOS
                SET NOME = :nome, DESCRICAO = :descricao, TIPO = :tipo, LINK = :link, CAMINHO = :caminho,
                    IMAGEM = :imagem, NR_SEQUENCIA = :sequencia
                WHERE ID_RELATORIO = :id
            """, {'nome': nome, 'descricao': descricao, 'tipo': tipo, 'link': link, 'caminho': caminho,
                  'imagem': imagem, 'sequencia': sequencia, 'id': ID_RELATORIO})
            connection.commit()
            flash("Relatório atualizado com sucesso")
        except oracledb.Error as err:
            print("Oracle Database Error:", err)
            return "Error updating data!", 500
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('relatorios', ID_RELATORIO=ID_RELATORIO))










if __name__ == "__main__":
    app.run(debug=True)
