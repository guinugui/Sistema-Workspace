import os
os.environ['TNS_ADMIN'] = r'C:\app\client\administrator\product\12.2.0\client_2\network\admin'

import oracledb

# Inicialização do cliente Oracle (substitua o caminho com o seu cliente Oracle)
oracledb.init_oracle_client(lib_dir=r'C:\app\client\administrator\product\12.2.0\client_2')

# Oracle database connection details
db_username = ''
db_password = ''
db_service_name = ''

# Função para conectar ao banco de dados Oracle
def connect_to_oracle():
    return oracledb.connect(user=db_username, password=db_password, dsn=db_service_name)
