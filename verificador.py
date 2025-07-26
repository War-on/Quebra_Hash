import argparse
import time
import multiprocessing as mp
from hash_detector import detectar_tipo_hash
from paralelismo import executar_paralelismo, verificar_dependencias
from time import sleep

print('''



''')
print('═'*40)
print('Iniciando o verificador de hash...\n')
sleep(3)



def main():
    parser = argparse.ArgumentParser(description='Verificador de hash seguro e realista para wordlist.')
    parser.add_argument('-H', '--hash', required=True, help='Hash alvo')
    parser.add_argument('-W', '--wordlist', required=True, help='Arquivo de wordlist')
    parser.add_argument('-P', '--processos', type=int, default=mp.cpu_count(), help='Número de processos (padrão: número de CPUs)')
    args = parser.parse_args()

    hash_alvo = args.hash
    wordlist = args.wordlist
    num_processos = args.processos

    detector = detectar_tipo_hash(hash_alvo)
    
    # Verifica se o formato do hash é inválido
    if detector == "Formato inválido de hash":
        print("  [\033[31mERRO\033[0m] Formato inválido de hash") 
        exit()
    # Verifica se o hash é desconhecido ou não suportado
    if detector == "Hash desconhecida ou não suportada":
        print("  [\033[31mERRO\033[0m] Hash desconhecida ou não suportada")
        exit()

    print(f'  [\033[32mINFO\033[0m] Tipo de hash detectado: \033[33m{detector}\033[0m')

    print(f'  [\033[32mINFO\033[0m] Hash a ser quebrado: \033[33m{hash_alvo}\033[0m')

    print(f'  [\033[32mINFO\033[0m] Usando \033[33m{num_processos}\033[0m processos')
    print('═'*40)
    sleep(3)
    # Verifica dependências
    try:
        verificar_dependencias(detector)
    except ImportError as e:
        print(f"[\033[31mERRO\033[0m] {e}")
        exit()

    start_time = time.time()
    
    try:
        # Executa o processamento paralelo
        palavra_encontrada, total_testes = executar_paralelismo(hash_alvo, detector, wordlist, num_processos)
        
        tempo = time.time() - start_time
        
        # Exibe resultado
        print('\n' + '╔' + '═'*28 + '╗')
        print(f'║{"RESULTADO":^28}║')
        print('╠' + '═'*28 + '╣')
        if palavra_encontrada:
            print(f'║ Valor encontrado:')
            print(f'║ \033[32m{palavra_encontrada}\033[0m')
        else:
            print(f'║    \033[31mValor NÃO encontrado\033[0m    ║')
        print('╠' + '═'*28 + '╣')
        print(f'║ Total de testes: {total_testes:<8}')
        print(f'║ Tempo: {tempo:.2f} segundos')
        print(f'║ Velocidade: {total_testes/tempo:.0f} hash/s')
        print('╚' + '═'*28 + '╝')
        
    except FileNotFoundError as e:
        print(f"[\033[31mERRO\033[0m] {e}")
    except Exception as e:
        print(f"[\033[31mERRO\033[0m] {e}")

if __name__ == '__main__':
    main()
