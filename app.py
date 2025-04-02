# app.py
import os
import psycopg2
from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
# É importante ter uma secret key para usar flash messages
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'uma-chave-secreta-padrao-mude-isso')

def get_db_connection():
    """Estabelece a conexão com o banco de dados."""
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'mydatabase'),
            user=os.environ.get('DB_USER', 'user'),
            password=os.environ.get('DB_PASSWORD', 'password'),
            port=os.environ.get('DB_PORT', '5432') # Porta padrão do PostgreSQL
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        # Em um app real, você poderia tentar reconectar ou logar o erro
        # Para este exemplo, vamos retornar None para indicar falha
        return None

def init_db():
    """Cria a tabela se ela não existir (para demonstração)."""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS items (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL
                    );
                """)
                # Adiciona alguns dados iniciais se a tabela estiver vazia (opcional)
                cur.execute("SELECT COUNT(*) FROM items;")
                if cur.fetchone()[0] == 0:
                     cur.execute("INSERT INTO items (name) VALUES (%s), (%s);",
                                 ('Item Inicial 1', 'Item Inicial 2'))
                conn.commit()
        except psycopg2.Error as e:
            print(f"Erro ao inicializar tabela: {e}")
            conn.rollback() # Desfaz alterações em caso de erro
        finally:
            conn.close()
    else:
        print("Não foi possível conectar ao BD para inicialização.")


@app.route('/')
def index():
    """Exibe os itens do banco de dados."""
    items = []
    conn = get_db_connection()
    error_message = None
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name FROM items ORDER BY id;")
                items = cur.fetchall() # Retorna uma lista de tuplas
        except psycopg2.Error as e:
            error_message = f"Erro ao buscar itens: {e}"
            print(error_message)
        finally:
            conn.close()
    else:
        error_message = "Não foi possível conectar ao banco de dados."

    return render_template('index.html', items=items, error_message=error_message)

@app.route('/add', methods=['POST'])
def add_item():
    """Adiciona um novo item ao banco de dados."""
    item_name = request.form.get('item_name')
    conn = get_db_connection()
    error_message = None

    if not item_name:
        flash("Nome do item não pode ser vazio!", "error")
        return redirect(url_for('index'))

    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO items (name) VALUES (%s);", (item_name,))
                conn.commit()
            flash(f"Item '{item_name}' adicionado com sucesso!", "success")
        except psycopg2.Error as e:
            error_message = f"Erro ao adicionar item: {e}"
            flash(error_message, "error")
            print(error_message)
            conn.rollback()
        finally:
            conn.close()
    else:
         error_message = "Não foi possível conectar ao banco de dados para adicionar o item."
         flash(error_message, "error")

    return redirect(url_for('index')) # Redireciona de volta para a página inicial

if __name__ == '__main__':
    print("Inicializando o banco de dados (se necessário)...")
    init_db()
    print("Iniciando a aplicação Flask...")
    # O host 0.0.0.0 torna a aplicação acessível externamente (necessário para Docker)
    app.run(host='0.0.0.0', port=5000, debug=True) # debug=True é útil para desenvolvimento