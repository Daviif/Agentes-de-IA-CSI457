from pathlib import Path


print('Informe manualmente o caminho do arquivo .txt do labirinto.')
NOME_ARQUIVO_LABIRINTO = input('Caminho do arquivo: ').strip()
# Expandir ~ para o diretório home
NOME_ARQUIVO_LABIRINTO = str(Path(NOME_ARQUIVO_LABIRINTO).expanduser())

if not Path(NOME_ARQUIVO_LABIRINTO).exists():
    raise FileNotFoundError(f'Arquivo não encontrado: {NOME_ARQUIVO_LABIRINTO}')

print(f'Arquivo carregado: {NOME_ARQUIVO_LABIRINTO}')
