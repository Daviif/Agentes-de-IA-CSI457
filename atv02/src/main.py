from files import NOME_ARQUIVO_LABIRINTO
from buscas import LabirintoBusca
from exibir import imprimir_labirinto, imprimir_metricas

# Carregar labirinto
lab = LabirintoBusca(NOME_ARQUIVO_LABIRINTO)

print('Labirinto carregado:')
imprimir_labirinto(lab, resultado=None, mostrar_explorados=False)

# Escolher algoritmo
print('\nEscolha o algoritmo de busca:')
print('1 - Busca em Largura (BFS)')
print('2 - Busca em Profundidade (DFS)')
print('3 - Busca de Custo Uniforme (UCS)')
print('4 - Greedy Best-First Search')
print('5 - Weighted A*')
print('6 - IDA*')

opcao = input('Digite a opção desejada [1-6]: ').strip()

# Executar busca
if opcao == '1':
    resultado = lab.busca_largura()
elif opcao == '2':
    resultado = lab.busca_profundidade()
elif opcao == '3':
    resultado = lab.busca_custo_uniforme()
elif opcao == '4':
    resultado = lab.busca_gulosa()
elif opcao == '5':
    peso = float(input('Informe o peso w da Weighted A*; exemplo: 2.0: ').strip())
    resultado = lab.busca_weighted_astar(peso=peso)
elif opcao == '6':
    resultado = lab.busca_idastar()
else:
    raise ValueError('Opção inválida. Execute novamente e escolha um valor de 1 a 6.')

# Exibir resultados
print('\nSolução encontrada no labirinto:')
imprimir_labirinto(lab, resultado=resultado, mostrar_explorados=True)

imprimir_metricas(resultado)