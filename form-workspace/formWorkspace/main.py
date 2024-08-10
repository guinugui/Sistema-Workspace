from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from services.database import connect_to_oracle, oracledb
import logging

logging.basicConfig(level=logging.DEBUG)  # Define o nível de logging como DEBUG ou outro nível desejado
main_bp = Blueprint('main', __name__)

img_dashboard = "https://objectstorage.sa-vinhedo-1.oraclecloud.com/n/axcdkt1qdgsl/b/powerbi/o/workspaces%2Frelatorios%2Fwindow-maximize_white.svg"
img_relatorio = "https://objectstorage.sa-vinhedo-1.oraclecloud.com/n/axcdkt1qdgsl/b/powerbi/o/workspaces%2Frelatorios%2Ffile_white.svg"

@main_bp.route('/')
@login_required
def Index():
    connection = connect_to_oracle()
    if not connection:
        return "Failed to connect to Oracle database!", 500

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM PBI_WORKSPACE ORDER BY NR_SEQUENCIA")
        imprimir_todos_workspace = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('formWorkspaceTemplates/index.html', dados=imprimir_todos_workspace)

# Outras rotas seguem a mesma estrutura, adicionando o decorador @login_required onde necessário
@main_bp.route('/insert', methods=['POST'])
@login_required
def insert():
    if request.method == "POST":
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
            cursor.execute("INSERT INTO PBI_WORKSPACE (NOME, DESCRICAO, IMAGEM, NR_SEQUENCIA, COR_HEX) VALUES (:nome, :descricao, :imagem, :sequencia, :cor)",
                           {'nome': nome, 'descricao': descricao, 'imagem': imagem, 'sequencia': sequencia, 'cor': cor})
            connection.commit()
        except oracledb.Error as err:
            error_message = "Error inserting data: {}".format(err)
            print(error_message)
            return error_message, 500

        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('main.Index'))



@main_bp.route('/delete/<int:ID_WORKSPACE>', methods=['GET'])
@login_required
def delete(ID_WORKSPACE):

    connection = connect_to_oracle()
    if not connection:
        return "Failed to connect to Oracle database!", 500

    cursor = connection.cursor()
    try:
        # Use Oracle's parameter binding for security
        cursor.execute("DELETE FROM PBI_WORKSPACE WHERE ID_WORKSPACE = :id", {'id': ID_WORKSPACE})
        connection.commit()
    except oracledb.Error as err:  # Catch oracledb.Error specifically
        print("Error deleting data: Causa: tem relatorios dentro desse Workspace", err)
        return "Error deleting data!, Causa: tem relatorios dentro desse Workspace", 500
    finally:
        # Ensure cursor and connection are closed even on errors
        cursor.close()
        connection.close()

    return redirect(url_for('main.Index'))




@main_bp.route('/update', methods=['POST'])
@login_required
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
                UPDATE PBI_WORKSPACE
                SET NOME = :nome, DESCRICAO = :descricao, IMAGEM = :imagem, NR_SEQUENCIA = :sequencia, COR_HEX = :cor
                WHERE ID_WORKSPACE = :id
            """, {'nome': nome, 'descricao': descricao, 'imagem': imagem, 'sequencia': sequencia, 'cor': cor, 'id': ID_WORKSPACE})
            connection.commit()
        except oracledb.Error as err:
            print("Error updating data:", err)
            return "Error updating data!", 500
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('main.Index'))
    
    
@main_bp.route('/relatorios/index/<int:workspace_id>')
@login_required
def relatorios(workspace_id):
    connection = connect_to_oracle()
    if not connection:
        return "Failed to connect to Oracle database!", 500

    cursor = connection.cursor()
    try:
         # Fetch the workspace name
        cursor.execute("SELECT NOME FROM PBI_WORKSPACE WHERE ID_WORKSPACE = :id", {'id': workspace_id})
        nome = cursor.fetchone()
        if nome:
            nome = nome[0]  # Extract the name from the tuple
        
        cursor.execute("SELECT * FROM PBI_WORKSPACE_RELATORIO WHERE ID_WORKSPACE = :id ORDER BY ID_RELATORIO ASC ", {'id': workspace_id})
        relatorios = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
        
        

    return render_template('formWorkspaceTemplates/relatorios/index.html', relatorios=relatorios, workspace_id=workspace_id, nome=nome, img_dashboard = img_dashboard , img_relatorio=img_relatorio)



#Essa classe adiciona la dentro do banco de dados
@main_bp.route('/relatorios/insert', methods=['POST'])
@login_required
def insert_relatorio():
    if request.method == "POST":
        nome = request.form['nome']
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        link = request.form['link']
        imagem = request.form['imagem']
        sequencia = request.form['sequencia']
        workspace_id = request.form['workspace_id']

        # Conectar ao banco de dados
        connection = connect_to_oracle()
        if not connection:
            return "Falha ao conectar ao banco de dados Oracle!", 500

        try:
            cursor = connection.cursor()

            # Inserir o novo relatório na tabela PBI_WORKSPACE_RELATORIO
            cursor.execute("""
                INSERT INTO PBI_WORKSPACE_RELATORIO (ID_WORKSPACE, NOME, DESCRICAO, TIPO, LINK, IMAGEM, NR_SEQUENCIA)
                VALUES (:id_workspace, :nome, :descricao, :tipo, :link, :imagem, :sequencia)
            """, {'id_workspace': workspace_id, 'nome': nome, 'descricao': descricao, 'tipo': tipo, 'link': link, 'imagem': imagem, 'sequencia': sequencia})
            
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
        return redirect(url_for('main.relatorios', workspace_id=workspace_id))










@main_bp.route('/relatorios/delete/<int:ID_RELATORIO>', methods=['POST'])
@login_required
def delete_relatorio(ID_RELATORIO):
    id_workspace = request.form.get('ID_WORKSPACE')

    if not id_workspace:
        return "ID_WORKSPACE não fornecido!", 400

    connection = connect_to_oracle()
    if not connection:
        return "Failed to connect to Oracle database!", 500

    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM PBI_WORKSPACE_RELATORIO WHERE ID_RELATORIO = :id_relatorio AND ID_WORKSPACE = :id_workspace",
                       {'id_relatorio': ID_RELATORIO, 'id_workspace': id_workspace})
        connection.commit()
    except oracledb.Error as err:
        logging.error(f"Error deleting data: {err}", exc_info=True)  # Registra o erro com traceback completo
        return "Error deleting data!", 500
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('main.relatorios', workspace_id=id_workspace))






@main_bp.route('/editar_relatorio', methods=['POST'])
@login_required
def editar_relatorio():
    connection = connect_to_oracle()
    if not connection:
        return "Falha ao conectar ao banco de dados Oracle!", 500

    if request.method == 'POST':
        ID_RELATORIO = request.form['ID_RELATORIO']
        ID_WORKSPACE = request.form['ID_WORKSPACE']
        nome = request.form['nome']
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        link = request.form['link']
        imagem = request.form['imagem']
        sequencia = request.form['sequencia']

        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE PBI_WORKSPACE_RELATORIO
                SET NOME = :nome, DESCRICAO = :descricao, TIPO = :tipo, LINK = :link, IMAGEM = :imagem, NR_SEQUENCIA = :sequencia
                WHERE ID_RELATORIO = :id
            """, {'nome': nome, 'descricao': descricao, 'tipo': tipo, 'link': link,
                  'imagem': imagem, 'sequencia': sequencia, 'id': ID_RELATORIO})
            connection.commit()
        except oracledb.Error as err:
            print("Erro no Oracle Database:", err)
            return "Erro ao atualizar os dados!", 500
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('main.relatorios', relatorios_id=ID_RELATORIO, workspace_id=ID_WORKSPACE))