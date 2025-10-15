# create_init_files.py
import os

# Definir estrutura
init_files = {
    'database': 'configuração do banco de dados',
    'models': 'modelos de dados',
    'schemas': 'schemas de validação',
    'services': 'serviços e lógica de negócio',
    'tests': 'testes'
}

# Criar arquivos
for folder, description in init_files.items():
    # Criar diretório se não existir
    os.makedirs(folder, exist_ok=True)
    
    # Criar __init__.py
    init_path = os.path.join(folder, '__init__.py')
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(f'"""Módulo de {description}"""\n')
    
    print(f'✓ Criado: {init_path}')

print('\n✅ Todos os arquivos __init__.py foram criados!')