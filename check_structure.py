# check_structure.py
import os

print("--- INICIANDO DIAGNÓSTICO DO PROJETO ---")

# --- Verificação de Arquivos Essenciais ---
files_to_check = [
    os.path.join('app', '__init__.py'),
    os.path.join('app', 'main.py'),
    os.path.join('app', 'api', '__init__.py'),
    os.path.join('app', 'api', 'endpoints', '__init__.py'),
    os.path.join('app', 'api', 'endpoints', 'users.py'),
]

print("\n[1] Verificando se os arquivos existem...")
all_files_ok = True
for file_path in files_to_check:
    if os.path.exists(file_path):
        print(f"  OK: Arquivo encontrado em '{file_path}'")
    else:
        print(f"  ERRO: Arquivo NÃO encontrado em '{file_path}'")
        all_files_ok = False

if not all_files_ok:
    print("\nERRO CRÍTICO: Um ou mais arquivos essenciais não foram encontrados. Verifique a estrutura de pastas.")
    exit()

# --- Verificação do Conteúdo do main.py ---
print("\n[2] Verificando o conteúdo de 'app/main.py'...")
try:
    with open(os.path.join('app', 'main.py'), 'r', encoding='utf-8') as f:
        main_content = f.read()
        
        print("\n--- CONTEÚDO DE app/main.py ---")
        print(main_content)
        print("-------------------------------\n")

        import_line = "from app.api.endpoints import login, users, students, classes"
        if import_line in main_content:
            print("  OK: A linha de importação em 'main.py' parece estar correta.")
        else:
            print("  ERRO: A linha de importação em 'main.py' está INCORRETA ou não foi salva.")
            print(f"       Esperado: '{import_line}'")

except Exception as e:
    print(f"  ERRO: Não foi possível ler o arquivo 'app/main.py': {e}")


print("\n--- DIAGNÓSTICO FINALIZADO ---")