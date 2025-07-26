# 🔐 Verificador de Hash Paralelo

Um verificador de hash otimizado com paralelismo para quebra de senhas usando wordlists. Este projeto demonstra técnicas avançadas de processamento paralelo em Python.

## ✨ Características

- 🔥 **Processamento Paralelo**: Utiliza multiprocessing para máxima performance
- 🎯 **Detecção Automática**: Identifica automaticamente o tipo de hash (MD5, SHA1, SHA224, SHA256, SHA384, SHA512, bcrypt, scrypt, Argon2)
- ⚡ **Early Termination**: Para execução quando encontra o resultado
- 📊 **Métricas de Performance**: Mostra velocidade em hash/s e tempo total
- 🔧 **Configurável**: Ajusta número de processos conforme seu hardware
- 🔒 **Hashes Seguros**: Suporte a bcrypt, scrypt e Argon2 para cenários realistas
- 📺 **Progress Visual**: Mostra palavras sendo testadas em tempo real

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/War-on/Quebra_Hash
cd Quebra_Hash

# Instale as dependências básicas
pip install argparse

# Para suporte a hashes seguros (opcional)
pip install bcrypt argon2-cffi scrypt
```

## 📖 Como Usar

### Sintaxe Básica
```bash
python verificador.py -H <hash> -W <wordlist> [-P <processos>]
```

### Parâmetros

| Parâmetro | Descrição | Obrigatório | Padrão |
|-----------|-----------|-------------|--------|
| `-H, --hash` | Hash alvo para quebrar | ✅ | - |
| `-W, --wordlist` | Arquivo de wordlist | ✅ | - |
| `-P, --processos` | Número de processos | ❌ | Número de CPUs |

### Exemplos de Uso

#### 1. Quebra Básica
```bash
# Hash SHA256 de "password"
python verificador.py -H 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 -W Word_list/top10k.txt
```

#### 2. Com Número Específico de Processos
```bash
# Usar 4 processos
python verificador.py -H <hash> -W Word_list/top10k.txt -P 4
```

#### 3. Hash MD5
```bash
# Hash MD5 de "admin"
python verificador.py -H 21232f297a57a5a743894a0e4a801fc3 -W Word_list/santos.txt
```

#### 4. Hash SHA1
```bash
# Hash SHA1 de "123456"
python verificador.py -H 7c4a8d09ca3762af61e59520943dc26494f8941b -W Word_list/Top100000.txt
```

#### 5. Hash Bcrypt (Seguro)
```bash
# Hash bcrypt de "password"
python verificador.py -H '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4tbQJh/6m' -W Word_list/top10k.txt
```

#### 6. Hash Argon2 (Muito Seguro)
```bash
# Hash Argon2 de "admin"
python verificador.py -H '$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG' -W Word_list/santos.txt
```

## 📊 Formatos de Hash Suportados

O verificador detecta automaticamente os seguintes tipos de hash:

### Hashes Clássicos (Rápidos)
| Tipo | Comprimento | Exemplo |
|------|-------------|---------|
| MD5 | 32 caracteres | `5d41402abc4b2a76b9719d911017c592` |
| SHA1 | 40 caracteres | `aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d` |
| SHA256 | 64 caracteres | `5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8` |
| SHA512 | 128 caracteres | `ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff` |

### Hashes Seguros (Lentos - Cenários Reais)
| Tipo | Prefixo | Exemplo |
|------|---------|---------|
| bcrypt | `$2a$`, `$2b$`, `$2y$` | `$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4tbQJh/6m` |
| scrypt | `$scrypt$` | `$scrypt$ln=16384,r=8,p=1$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG` |
| Argon2 | `$argon2i$`, `$argon2d$`, `$argon2id$` | `$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG` |

## ⚡ Otimizações de Performance

### Paralelismo com Multiprocessing
- Divide a wordlist em chunks
- Processa cada chunk em um processo separado
- Utiliza todos os cores da CPU

### Configurações Recomendadas

| Hardware | Processos Recomendados | Performance Esperada |
|----------|----------------------|---------------------|
| 2 Cores | 2 | 2-3x mais rápido |
| 4 Cores | 4 | 3-4x mais rápido |
| 8 Cores | 8 | 4-6x mais rápido |
| 16 Cores | 8-12 | 6-8x mais rápido |

## 📁 Estrutura do Projeto

```
Quebra_Hash/
├── verificador.py          # Script principal
├── hash_detector.py        # Detector de tipo de hash
├── Word_list/              # Wordlists
│   ├── top10k.txt         # Top 10k senhas
│   ├── Top100000.txt      # Top 100k senhas
│   └── santos.txt         # Lista personalizada
└── README.md              # Este arquivo
```

## 🎯 Exemplos Práticos

### Teste com Senha Conhecida
```bash
# 1. Gerar hash de uma senha
echo -n "minhasenha" | sha256sum
# Saída: 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918

# 2. Quebrar o hash
python verificador.py -H 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918 -W Word_list/top10k.txt
```

## 📈 Interpretando os Resultados

### Progresso Visual
Durante a execução, você verá:
```
Testando: password123
Testando: admin
Testando: 123456
```

### Output de Sucesso
```
╔════════════════════════════╗
║        RESULTADO           ║
╠════════════════════════════╣
║ Valor encontrado:          
║ password                   
╠════════════════════════════╣
║ Total de testes: 5000      
║ Tempo: 2.34 segundos       
║ Velocidade: 2136 hash/s    
╚════════════════════════════╝
```

### Output de Falha
```
╔════════════════════════════╗
║        RESULTADO           ║
╠════════════════════════════╣
║    Valor NÃO encontrado    ║
╠════════════════════════════╣
║ Total de testes: 10000     
║ Tempo: 4.67 segundos       
║ Velocidade: 2141 hash/s    
╚════════════════════════════╝
```

## 🔧 Troubleshooting

### Erro: "Arquivo não encontrado"
```bash
# Verifique se o caminho da wordlist está correto
ls -la Word_list/
python verificador.py -H <hash> -W ./Word_list/top10k.txt
```

### Erro: "Import could not be resolved"
```bash
# Para bcrypt
pip install bcrypt

# Para argon2
pip install argon2-cffi

# Para scrypt (pode precisar de Visual C++ Build Tools no Windows)
pip install scrypt
```

### Performance Ruim
```bash
# Reduza o número de processos
python verificador.py -H <hash> -W <wordlist> -P 2

# Use wordlists menores para teste
python verificador.py -H <hash> -W Word_list/santos.txt
```

### Erro de Memória
```bash
# Use menos processos
python verificador.py -H <hash> -W <wordlist> -P 1

# Divida wordlists grandes
split -l 10000 Word_list/Top100000.txt Word_list/chunk_
```

## 📚 Dependências

### Básicas (Incluídas)
- **Python 3.6+**
- **argparse** (incluído na biblioteca padrão)
- **hashlib** (incluído na biblioteca padrão)
- **multiprocessing** (incluído na biblioteca padrão)

### Para Hashes Seguros (Opcionais)
- **bcrypt**: `pip install bcrypt`
- **argon2-cffi**: `pip install argon2-cffi`
- **scrypt**: `pip install scrypt`

> **Nota**: Se as bibliotecas de hashes seguros não estiverem instaladas, o verificador funcionará apenas com hashes clássicos (MD5, SHA1, SHA256, etc.).

## 🔒 Considerações de Segurança

⚠️ **AVISO IMPORTANTE**: Este software é destinado para teste de segurança legítimos.

### Uso Ético
- ✅ Teste apenas senhas de sistemas que você possui
- ✅ Use para auditorias de segurança autorizadas
- ✅ Aprenda sobre criptografia e segurança

### Uso Proibido
- ❌ Não use para acessar sistemas sem autorização
- ❌ Não use para atividades maliciosas
- ❌ Não viole leis locais sobre segurança computacional

## 🤝 Contribuindo

Contribuições são bem-vindas! Algumas ideias:

1. **Novos algoritmos de hash** (PBKDF2, bcrypt com salt customizado, etc.)
2. **Otimizações de performance** para hashes seguros
3. **Interface gráfica** com progresso visual
4. **Suporte a wordlists em banco de dados**
5. **Métricas avançadas de performance** por tipo de hash
6. **Configuração de parâmetros** para bcrypt, scrypt e Argon2

## 🆘 Suporte

Se encontrar problemas:

1. Verifique se todas as dependências estão instaladas
2. Confirme que os caminhos dos arquivos estão corretos
3. Teste com wordlists menores primeiro
4. Verifique se o hash está no formato correto
