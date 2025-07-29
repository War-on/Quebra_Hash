import hashlib
import multiprocessing as mp
import chardet
import os

# Novas libs para hashes seguros
try:
    import bcrypt
except ImportError:
    bcrypt = None
try:
    from argon2 import PasswordHasher
except ImportError:
    PasswordHasher = None
try:
    import scrypt
except ImportError:
    scrypt = None

def detectar_codificacao(arquivo_path):
    """Detecta a codificação do arquivo automaticamente"""
    try:
        # Lê uma amostra do arquivo para detectar a codificação
        with open(arquivo_path, 'rb') as file:
            amostra = file.read(10000)  # Lê os primeiros 10KB
            resultado = chardet.detect(amostra)
            return resultado['encoding'] or 'utf-8'
    except Exception:
        return 'utf-8'

def dividir_wordlist(wordlist_path, num_processos):
    """Divide a wordlist em chunks para processamento paralelo com suporte a arquivos grandes"""
    try:
        # Detecta a codificação do arquivo
        codificacao = detectar_codificacao(wordlist_path)
        print(f"Detectada codificação: {codificacao}")
        
        # Para arquivos muito grandes, processa em chunks menores
        tamanho_arquivo = os.path.getsize(wordlist_path)
        tamanho_maximo_memoria = 100 * 1024 * 1024  # 100MB
        
        if tamanho_arquivo > tamanho_maximo_memoria:
            print(f"Arquivo muito grande ({tamanho_arquivo / (1024*1024):.1f}MB). Processando em chunks...")
            return dividir_wordlist_grande(wordlist_path, num_processos, codificacao)
        else:
            # Para arquivos menores, carrega tudo na memória
            return dividir_wordlist_pequeno(wordlist_path, num_processos, codificacao)
            
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        # Fallback para UTF-8
        return dividir_wordlist_pequeno(wordlist_path, num_processos, 'utf-8')

def dividir_wordlist_pequeno(wordlist_path, num_processos, codificacao):
    """Processa arquivos pequenos carregando tudo na memória"""
    try:
        with open(wordlist_path, 'r', encoding=codificacao, errors='ignore') as file:
            linhas = file.readlines()
    except UnicodeDecodeError:
        # Se falhar, tenta com UTF-8
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            linhas = file.readlines()
    
    # Remove linhas vazias e espaços em branco
    linhas = [linha.strip() for linha in linhas if linha.strip()]
    
    tamanho_chunk = max(1, len(linhas) // num_processos)
    chunks = []
    for i in range(num_processos):
        inicio = i * tamanho_chunk
        fim = inicio + tamanho_chunk if i < num_processos - 1 else len(linhas)
        chunks.append(linhas[inicio:fim])
    return chunks

def dividir_wordlist_grande(wordlist_path, num_processos, codificacao):
    """Processa arquivos grandes dividindo em chunks menores"""
    chunks = [[] for _ in range(num_processos)]
    chunk_atual = 0
    
    try:
        with open(wordlist_path, 'r', encoding=codificacao, errors='ignore') as file:
            for linha in file:
                palavra = linha.strip()
                if palavra:  # Ignora linhas vazias
                    chunks[chunk_atual].append(palavra)
                    chunk_atual = (chunk_atual + 1) % num_processos
    except UnicodeDecodeError:
        # Se falhar, tenta com UTF-8
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for linha in file:
                palavra = linha.strip()
                if palavra:  # Ignora linhas vazias
                    chunks[chunk_atual].append(palavra)
                    chunk_atual = (chunk_atual + 1) % num_processos
    
    return chunks

def processar_chunk(chunk_data):
    """Processa um chunk de palavras em paralelo"""
    hash_alvo, detector, chunk = chunk_data
    total_testes = 0
    for palavra in chunk:
        palavra = palavra.strip()
        total_testes += 1
        # Mostra a palavra testada apenas a cada 5000 testes para não sobrecarregar
        if total_testes % 5000 == 0:
            print(f'\rTestando: \033[33m{palavra}\033[0m', end='', flush=True)
        
        if detector == "BCRYPT":
            if not bcrypt:
                continue
            try:
                if bcrypt.checkpw(palavra.encode(), hash_alvo.encode()):
                    return (True, palavra, total_testes)
            except Exception:
                continue
        elif detector == "SCRYPT":
            if not scrypt:
                continue
            try:
                # scrypt.hash retorna bytes, então comparar com hash alvo em bytes
                hash_bytes = scrypt.hash(palavra, salt=b"salt", N=16384, r=8, p=1)
                if hash_bytes.hex() == hash_alvo:
                    return (True, palavra, total_testes)
            except Exception:
                continue
        elif detector == "ARGON2":
            if not PasswordHasher:
                continue
            ph = PasswordHasher()
            try:
                ph.verify(hash_alvo, palavra)
                return (True, palavra, total_testes)
            except Exception:
                continue
        else:
            # Hashes clássicos
            try:
                hash_func = getattr(hashlib, detector.lower())
                hash_digest = hash_func(palavra.encode()).hexdigest()
                if hash_digest == hash_alvo:
                    return (True, palavra, total_testes)
            except Exception:
                continue
    return (False, None, total_testes)

def executar_paralelismo(hash_alvo, detector, wordlist, num_processos):
    """Executa o processamento paralelo e retorna os resultados"""
    try:
        chunks = dividir_wordlist(wordlist, num_processos)
        dados_processos = [(hash_alvo, detector, chunk) for chunk in chunks]
        
        with mp.Pool(processes=num_processos) as pool:
            resultados = pool.map(processar_chunk, dados_processos)
        
        total_testes = 0
        palavra_encontrada = None
        
        for sucesso, palavra, testes in resultados:
            total_testes += testes
            if sucesso:
                palavra_encontrada = palavra
                break
        
        return palavra_encontrada, total_testes
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{wordlist}' não encontrado.")
    except Exception as e:
        raise Exception(f"Erro durante processamento paralelo: {e}")

def verificar_dependencias(detector):
    """Verifica se as dependências necessárias estão instaladas"""
    try:
        import chardet
    except ImportError:
        raise ImportError("Instale a biblioteca 'chardet' para detecção de codificação: pip install chardet")
    
    if detector == "BCRYPT" and not bcrypt:
        raise ImportError("Instale a biblioteca 'bcrypt' para suporte a bcrypt: pip install bcrypt")
    if detector == "ARGON2" and not PasswordHasher:
        raise ImportError("Instale a biblioteca 'argon2-cffi' para suporte a Argon2: pip install argon2-cffi")
    if detector == "SCRYPT" and not scrypt:
        raise ImportError("Instale a biblioteca 'scrypt' para suporte a scrypt: pip install scrypt")
