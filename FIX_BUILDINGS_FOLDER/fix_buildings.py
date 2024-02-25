import re

# Caminho para o arquivo buildings.txt e error.log
buildings_file_path = 'C:/Users/ferna/Desktop/FIX_BUILDINGS_FOLDER/buildings/buildings.txt'
error_log_path = 'C:/Users/ferna/Desktop/FIX_BUILDINGS_FOLDER/error_log/error.log'

# Função para corrigir os erros no arquivo buildings.txt
def corrigir_erros_no_buildings(buildings_path, error_log_path):
    # Ler o arquivo de erros para encontrar as linhas e correções necessárias
    with open(error_log_path, 'r') as error_file:
        error_lines = error_file.readlines()
    
    # Identificar os erros específicos e armazenar as correções
    correcoes = []
    for line in error_lines:
        match = re.search(r"error at line (\d+): .+ supposed to be '(\d+)' but was '(\d+)'", line)
        if match:
            numero_linha = int(match.group(1))
            estado_correto = match.group(2)
            correcoes.append((numero_linha, estado_correto))
    
    # Se não houver correções, não é necessário modificar o arquivo
    if not correcoes:
        print("Nenhum erro encontrado que necessite correção.")
        return
    
    # Ler o conteúdo atual do arquivo buildings.txt
    with open(buildings_path, 'r') as file:
        lines = file.readlines()
    
    # Aplicar as correções no arquivo
    for numero_linha, estado_correto in correcoes:
        # Corrigir a linha específica
        line = lines[numero_linha - 1]
        lines[numero_linha - 1] = re.sub(r'state=\d+', f'state={estado_correto}', line)
    
    # Escrever as alterações de volta no arquivo
    with open(buildings_path, 'w') as file:
        file.writelines(lines)
    
    print("Correções aplicadas com sucesso.")

# Chamar a função de correção
corrigir_erros_no_buildings(buildings_file_path, error_log_path)
