import os
import oracledb
import json
import pandas as pd

conexao = False  # Conexão com o banco de dados

try:
    conn = oracledb.connect(user='rm567175', password='060995', dsn='oracle.fiap.com.br:1521/ORCL')
    # Cursores para cada operação (CRUD)
    cursor_insert = conn.cursor()
    cursor_select = conn.cursor()
    cursor_update = conn.cursor()
    cursor_delete = conn.cursor()
    conexao = True

except Exception as e:
    print("Erro de conexão com o banco de dados Oracle:", e)
    print("Verifique se o Oracle SQL Developer está instalado e a sua conexão foi configurada.")
    print("Aplicação encerrada devido a falha de conexão.")
    conexao = False

#colunas
colunas_display = ['ID', 'COLHEITADEIRA', 'HECTARES', 'PERDAS_HA', 'PREJUIZO_ESTIMADO']

#arquivo Jason
arquivo_json = 'relatorio_colheita.json'


# ==============================================================================
# 2. SUBALGORITMOS (FUNÇÕES E PROCEDIMENTOS)
# ==============================================================================

#limpar terminal
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

#exibir menu
def exibe_menu() -> int:

    print("=" * 40)
    print("      SISTEMA DE GESTÃO DE COLHEITA AGRO")
    print("=" * 40)
    print("1. Registrar nova colheita")
    print("2. Listar histórico de colheitas")
    print("3. Atualizar registro de colheita")
    print("4. Excluir registro de colheita")
    print("5. Excluir TODOS os registros")
    print("6. Sair")
    print("=" * 40)

    while True:
        try:
            escolha = int(input("Escolha uma opção: "))
            if 1 <= escolha <= 6:
                return escolha
            else:
                print("Opção inválida. Digite um número de 1 a 6.")
        except ValueError:
            print("Entrada inválida. Digite um número.")


#validar entrada de números reais.
def valida_float(pergunta: str) -> float:
    while True:
        try:
            valor = float(input(pergunta))
            if valor >= 0:
                return valor
            else:
                print("Valor deve ser maior ou igual a zero.")
        except ValueError:
            print("Entrada inválida. Digite um número real (casa decimal com ponto '.' ao invés de vírgula ',').")


#salvar o Jason
def salvar_em_json(dados_json):
    with open(arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(dados_json, f, ensure_ascii=False, indent=4)
    print("\nRelatório de colheitas salvo em", arquivo_json)


#carregar dados no Jason
def carregar_do_json() -> list:
    try:
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


#registrar nova colheita no Oracle e no Jason
def registrar_colheita():
    print("\n░█▀▄░█▀▀░█▀▀░▀█▀░█▀▀░▀█▀░█▀▄░█▀█░█▀▄░░░█▀█░█▀█░█░█░█▀█░░░█▀▀░█▀█░█░░░█░█░█▀▀░▀█▀░▀█▀░█▀█")
    print("░█▀▄░█▀▀░█░█░░█░░▀▀█░░█░░█▀▄░█▀█░█▀▄░░░█░█░█░█░▀▄▀░█▀█░░░█░░░█░█░█░░░█▀█░█▀▀░░█░░░█░░█▀█")
    print("░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀░▀░▀░▀░▀░▀░░░▀░▀░▀▀▀░░▀░░▀░▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀░▀\n")
    try:
        id_colheitadeira = input("ID da Colheitadeira: ")
        hectares = valida_float("Área colhida (ha): ")
        perdas_por_ha = valida_float("Perdas por hectare (kg): ")

        #simulação cálculo de prejuízo (50cent por kg)
        prejuizo_estimado = hectares * perdas_por_ha * 0.5

        #coloca no oracle
        insert_sql = "INSERT INTO TBL_COLHEITA (ID_COLHEITADEIRA, HECTARES_COLHIDOS, PERDAS_POR_HA, PREJUIZO_ESTIMADO) VALUES (:1, :2, :3, :4)"
        cursor_insert.execute(insert_sql, [id_colheitadeira, hectares, perdas_por_ha, prejuizo_estimado])
        conn.commit()

        #adicionar novo registro no Jason
        dados_json = carregar_do_json()
        novo_registro = {
            'id': cursor_insert.lastrowid,  #captura o id gerado automaticamente
            'id_colheitadeira': id_colheitadeira,
            'hectares': hectares,
            'perdas_por_ha': perdas_por_ha,
            'prejuizo_estimado': prejuizo_estimado
        }
        dados_json.append(novo_registro)
        salvar_em_json(dados_json)

        print("\nRegistro de colheita realizado com sucesso!")

    except Exception as e:
        print("Erro ao registrar colheita:", e)
        conn.rollback()


#lista toas as colheitas presentes no Oracle
def listar_colheitas():
    print("░█░█░▀█▀░█▀▀░▀█▀░█▀█░█▀▄░▀█▀░█▀▀░█▀█░░░█▀▄░█▀▀░░░█▀▀░█▀█░█░░░█░█░█▀▀░▀█▀░▀█▀░█▀█░█▀▀")
    print("░█▀█░░█░░▀▀█░░█░░█░█░█▀▄░░█░░█░░░█░█░░░█░█░█▀▀░░░█░░░█░█░█░░░█▀█░█▀▀░░█░░░█░░█▀█░▀▀█")
    print("░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀░░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀░▀░▀▀▀")
    try:
        cursor_select.execute(
            "SELECT ID, ID_COLHEITADEIRA, HECTARES_COLHIDOS, PERDAS_POR_HA, PREJUIZO_ESTIMADO FROM TBL_COLHEITA ORDER BY ID")
        registros = cursor_select.fetchall()

        if not registros:
            print("Não há registros de colheita cadastrados.")
        else:
            df = pd.DataFrame(registros, columns=colunas_display)
            print(df.to_string(index=False))  #exibe de forma limpa e formatada

        print("--- FIM DA LISTAGEM ---")
    except Exception as e:
        print("Erro ao listar colheitas:", e)

#função utilizada apenas em "atualizar_colheitas" pra tela não ficar poluída com ASCII
def listar_colheitas_sem_ASCII():
    try:
        cursor_select.execute(
            "SELECT ID, ID_COLHEITADEIRA, HECTARES_COLHIDOS, PERDAS_POR_HA, PREJUIZO_ESTIMADO FROM TBL_COLHEITA ORDER BY ID")
        registros = cursor_select.fetchall()

        if not registros:
            print("Não há registros de colheita cadastrados.")
        else:
            df = pd.DataFrame(registros, columns=colunas_display)
            print(df.to_string(index=False))  #exibe de forma limpa e formatada

        print("--- FIM DA LISTAGEM ---")
    except Exception as e:
        print("Erro ao listar colheitas:", e)

#atualizar colheitas
def atualizar_colheita():
    print("░█▀█░▀█▀░█░█░█▀█░█░░░▀█▀░▀▀█░█▀█░█▀▄░░░█▀▄░█▀▀░█▀▀░▀█▀░█▀▀░▀█▀░█▀▄░█▀█")
    print("░█▀█░░█░░█░█░█▀█░█░░░░█░░▄▀░░█▀█░█▀▄░░░█▀▄░█▀▀░█░█░░█░░▀▀█░░█░░█▀▄░█░█")
    print("░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀░▀░▀▀▀")
    listar_colheitas_sem_ASCII()

    try:
        id_registro = int(input("\nDigite o ID do registro que deseja atualizar: "))

        # Verificar se o registro existe
        cursor_select.execute("SELECT * FROM TBL_COLHEITA WHERE ID = :1", [id_registro])
        if not cursor_select.fetchone():
            print(f"Não foi encontrado nenhum registro com o ID {id_registro}.")
            return

        print("Preencha as novas informações:")
        novo_id_colheitadeira = input(f"Novo ID da Colheitadeira: ")
        novos_hectares = valida_float(f"Nova área (ha): ")
        novas_perdas_por_ha = valida_float(f"Novas perdas por hectare (kg): ")

        # Recalcular prejuízo
        novo_prejuizo = novos_hectares * novas_perdas_por_ha * 0.15

        update_sql = "UPDATE TBL_COLHEITA SET ID_COLHEITADEIRA = :1, HECTARES_COLHIDOS = :2, PERDAS_POR_HA = :3, PREJUIZO_ESTIMADO = :4 WHERE ID = :5"
        cursor_update.execute(update_sql,
                              [novo_id_colheitadeira, novos_hectares, novas_perdas_por_ha, novo_prejuizo, id_registro])
        conn.commit()

        print(f"\nRegistro com ID {id_registro} atualizado com sucesso!")

    except ValueError:
        print("Entrada inválida. O ID deve ser um número inteiro.")
    except Exception as e:
        print("Erro ao atualizar registro:", e)
        conn.rollback()

#excluir um registro
def excluir_colheita():
    print("░█▀▀░█░█░█▀▀░█░░░█░█░▀█▀░█▀▄░░░█▀▄░█▀▀░█▀▀░▀█▀░█▀▀░▀█▀░█▀▄░█▀█")
    print("░█▀▀░▄▀▄░█░░░█░░░█░█░░█░░█▀▄░░░█▀▄░█▀▀░█░█░░█░░▀▀█░░█░░█▀▄░█░█")
    print("░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀░▀░▀▀▀")
    listar_colheitas()

    try:
        id_registro = int(input("\nDigite o ID do registro que deseja excluir: "))

        # Verificar se o registro existe
        cursor_select.execute("SELECT * FROM TBL_COLHEITA WHERE ID = :1", [id_registro])
        if not cursor_select.fetchone():
            print(f"Não foi encontrado nenhum registro com o ID {id_registro}.")
            return

        delete_sql = "DELETE FROM TBL_COLHEITA WHERE ID = :1"
        cursor_delete.execute(delete_sql, [id_registro])
        conn.commit()

        print(f"\nRegistro com ID {id_registro} excluído com sucesso!")

    except ValueError:
        print("Entrada inválida. O ID deve ser um número inteiro.")
    except Exception as e:
        print("Erro ao excluir registro:", e)
        conn.rollback()


#excluir todos os registros da tabela --PRERIGO--
def excluir_todos_registros():
    print("░█▀▀░█░█░█▀▀░█░░░█░█░▀█▀░█▀▄░░░▀█▀░█▀█░█▀▄░█▀█░█▀▀░░░█▀█░█▀▀░░░█▀▄░█▀▀░█▀▀░▀█▀░█▀▀░▀█▀░█▀▄░█▀█░█▀▀")
    print("░█▀▀░▄▀▄░█░░░█░░░█░█░░█░░█▀▄░░░░█░░█░█░█░█░█░█░▀▀█░░░█░█░▀▀█░░░█▀▄░█▀▀░█░█░░█░░▀▀█░░█░░█▀▄░█░█░▀▀█")
    print("░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░░░▀░░▀▀▀░▀▀░░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀░▀░▀▀▀░▀▀▀")
    confirmacao = input("TEM CERTEZA? Esta ação é irreversível! (S/N): ").upper()
    if confirmacao == 'S':
        try:
            #apagar todos os registros
            cursor_delete.execute("DELETE FROM TBL_COLHEITA")

            #reset na sequência de ID
            cursor_delete.execute("ALTER TABLE TBL_COLHEITA MODIFY (ID GENERATED AS IDENTITY (START WITH 1))")
            conn.commit()

            #limpar o Jason
            salvar_em_json([])

            print("\nTodos os registros foram excluídos com sucesso.")
        except Exception as e:
            print("Erro ao excluir todos os registros:", e)
            conn.rollback()
    else:
        print("\nOperação de exclusão cancelada.")


# =======================================================================
# ===============    3. LÓGICA PRINCIPAL =========================
# ==============================================================================
if conexao:
    while True:
        limpar_tela()
        escolha = exibe_menu()

        if escolha == 1:
            registrar_colheita()
        elif escolha == 2:
            listar_colheitas()
        elif escolha == 3:
            atualizar_colheita()
        elif escolha == 4:
            excluir_colheita()
        elif escolha == 5:
            excluir_todos_registros()
        elif escolha == 6:
            print("Saindo da aplicação. Obrigado por usar!")
            break

        input("\nPressione ENTER para continuar...")

    # Fechar a conexão ao sair do programa
    if conn:
        conn.close()