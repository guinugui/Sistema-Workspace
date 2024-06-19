from flask import Flask, render_template, redirect, url_for
from services.database import connect_to_oracle

app = Flask(__name__)


# Função para conectar ao banco de dados Oracle
def get_db_cursor():
    connection = connect_to_oracle()
    return connection.cursor()


@app.route('/')
def index():
    try:
        cursor = get_db_cursor()

        # Obtenha todos os workspaces do banco de dados, incluindo a cor HEX
        cursor.execute('SELECT ID_WORKSPACE, NOME, IMAGEM FROM PBI_WORKSPACES')
        workspaces = cursor.fetchall()

        # Converta os resultados para uma lista de dicionários para facilitar o uso no template
        workspace_list = [{'ID_WORKSPACE': row[0], 'NOME': row[1], 'IMAGEM': row[2]} for row in workspaces]

        # Feche o cursor
        cursor.close()

        # Renderize a página principal com os workspaces
        return render_template('index.html', workspaces=workspace_list)
    except Exception as e:
        return f'Erro ao conectar ao banco de dados: {e}', 500

@app.route('/relatorios/<int:workspace_id>/')
def relatorios(workspace_id):
    
    try:
        cursor = get_db_cursor()

        # Obtenha os dados do workspace usando parâmetros para prevenir injeção SQL
        cursor.execute('SELECT NOME, LINK, IMAGEM FROM PBI_RELATORIOS WHERE ID_WORKSPACE = :id', {'id': workspace_id})
        workspace_row = cursor.fetchone()

        
        # Obtenha a imagem do workspace correspondente
        cursor.execute('SELECT IMAGEM, NOME, COR_HEX FROM PBI_WORKSPACES WHERE ID_WORKSPACE = :id', {'id': workspace_id})
        workspace_img, workspace_nome, worksapce_cor = cursor.fetchone()
         # Verifique se o workspace foi encontrado
        if not workspace_row:
            # Feche o cursor
            cursor.close()
            # Renderize a página com a mensagem de nenhum relatório encontrado
            return render_template('Sem_Relatorios/index.html', workspace_img=workspace_img, workspace_nome=workspace_nome, worksapce_cor=worksapce_cor)
        
        

        # Obtenha os relatórios para o workspace selecionado
        cursor.execute('SELECT ID_RELATORIO, NOME, LINK, IMAGEM FROM PBI_RELATORIOS WHERE ID_WORKSPACE = :id ORDER BY ID_RELATORIO DESC', {'id': workspace_id})
        rows = cursor.fetchall()

        # Converta os resultados para uma lista de dicionários para facilitar o uso no template
        link_relatorio = [{'ID_RELATORIO': row[0], 'NOME': row[1], 'LINK': row[2], 'IMAGEM': row[3]} for row in rows]

        # Feche o cursor
        cursor.close()

        return render_template('relatorios/index.html', workspace_id=workspace_id, workspace=workspace_row, workspace_img=workspace_img, workspace_nome=workspace_nome,
                               worksapce_cor= worksapce_cor, link_relatorio=link_relatorio)
    except Exception as e:
        return f'Erro ao conectar ao banco de dados ou executar a consulta: {e}', 500

if __name__ == '__main__':
    app.run(debug=True)
