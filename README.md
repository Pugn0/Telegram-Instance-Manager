# 📱 Telegram Instance Manager

Gerenciador completo de múltiplas instâncias do Telegram Desktop para Windows 11.

## 🎯 Funcionalidades

- ✅ **Criar** múltiplas instâncias do Telegram
- ✅ **Listar** todas as instâncias criadas
- ✅ **Renomear** instâncias
- ✅ **Excluir** instâncias (remove pasta e dados)
- ✅ **Iniciar** Telegram de cada instância
- ✅ **Abrir pasta** no Explorer
- ✅ Interface web moderna e responsiva
- ✅ API REST completa
- ✅ Backup automático em JSON

## 📁 Estrutura do Projeto

```
telegram_instance_manager/
│
├── main.py                 # API FastAPI
├── requirements.txt        # Dependências Python
├── README.md              # Esta documentação
│
├── data/
│   └── instances.json     # Banco de dados local (criado automaticamente)
│
└── web/
    └── index.html         # Interface web
```

## 🚀 Instalação

### 1. Clone ou crie a estrutura de pastas

```bash
mkdir telegram_instance_manager
cd telegram_instance_manager
```

### 2. Crie os arquivos

- Copie o conteúdo de `main.py`
- Crie a pasta `web/` e adicione `index.html`
- Crie o arquivo `requirements.txt`

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o servidor

```bash
python main.py
```

## 🌐 Acesso

Após iniciar o servidor, acesse:

- **Interface Web**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

## 📡 API Endpoints

### GET /instances
Lista todas as instâncias criadas.

**Resposta:**
```json
[
  {
    "id": 1,
    "name": "Pugno Coder",
    "folder": "C:\\Users\\pugno\\AppData\\Roaming\\Telegram_Instances\\instance_1",
    "created_at": "2025-11-13T12:00:00"
  }
]
```

### POST /instances
Cria uma nova instância.

**Body:**
```json
{
  "name": "Pugno Coder"
}
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Pugno Coder",
  "folder": "C:\\Users\\pugno\\AppData\\Roaming\\Telegram_Instances\\instance_1",
  "created_at": "2025-11-13T12:00:00"
}
```

### PUT /instances/{id}
Renomeia uma instância.

**Body:**
```json
{
  "name": "Novo Nome"
}
```

### DELETE /instances/{id}
Exclui uma instância e sua pasta.

**Resposta:**
```json
{
  "message": "Instância excluída com sucesso"
}
```

### POST /instances/{id}/start
Inicia o Telegram da instância.

**Resposta:**
```json
{
  "message": "Telegram iniciado: Pugno Coder"
}
```

### POST /instances/{id}/open-folder
Abre a pasta da instância no Explorer.

**Resposta:**
```json
{
  "message": "Pasta aberta no Explorer"
}
```

### GET /health
Verifica o status da API.

**Resposta:**
```json
{
  "status": "ok",
  "telegram_base_exists": true,
  "instances_folder_exists": true
}
```

## 🔧 Configuração

### Caminhos padrão

O sistema usa os seguintes caminhos:

- **Telegram Base**: `C:\Users\pugno\AppData\Roaming\Telegram Desktop`
- **Instâncias**: `C:\Users\pugno\AppData\Roaming\Telegram_Instances`

Se você usar outro usuário do Windows, **modifique estes caminhos** no arquivo `main.py`:

```python
TELEGRAM_BASE = Path(r"C:\Users\SEU_USUARIO\AppData\Roaming\Telegram Desktop")
INSTANCES_BASE = Path(r"C:\Users\SEU_USUARIO\AppData\Roaming\Telegram_Instances")
```

## 💡 Como Usar

### Via Interface Web

1. Acesse http://localhost:8080
2. Digite o nome da instância e clique em "Criar Instância"
3. Aguarde a cópia da pasta (pode demorar alguns segundos)
4. Use os botões para:
   - ▶️ **Iniciar**: Abre o Telegram
   - 📂 **Pasta**: Abre a pasta no Explorer
   - ✏️ **Renomear**: Altera o nome
   - 🗑️ **Excluir**: Remove a instância

### Via API

```bash
# Criar instância
curl -X POST http://localhost:8080/instances \
  -H "Content-Type: application/json" \
  -d '{"name": "Minha Instância"}'

# Listar instâncias
curl http://localhost:8080/instances

# Iniciar instância
curl -X POST http://localhost:8080/instances/1/start

# Renomear instância
curl -X PUT http://localhost:8080/instances/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Novo Nome"}'

# Excluir instância
curl -X DELETE http://localhost:8080/instances/1
```

## ⚠️ Observações Importantes

1. **Backup**: O sistema copia toda a pasta do Telegram. Se você tiver muitos dados (mídia, cache), a cópia pode demorar.

2. **Espaço em disco**: Cada instância ocupa o mesmo espaço que sua pasta original do Telegram.

3. **Dados separados**: Cada instância tem seus próprios dados, configurações e sessões completamente isolados.

4. **Windows 11**: O sistema foi desenvolvido especificamente para Windows 11, mas deve funcionar em Windows 10.

5. **Telegram Base**: É necessário ter o Telegram Desktop instalado e configurado antes de criar instâncias.

## 🐛 Troubleshooting

### "Pasta base do Telegram não encontrada"
- Verifique se o Telegram Desktop está instalado
- Confira se o caminho em `main.py` está correto para seu usuário

### "Erro ao criar instância"
- Verifique se há espaço em disco suficiente
- Certifique-se de que nenhum processo está bloqueando a pasta
- Execute como administrador se necessário

### "Erro ao iniciar Telegram"
- Verifique se o arquivo `Telegram.exe` existe na pasta da instância
- Tente abrir a pasta e executar manualmente para verificar o erro

### Interface não carrega
- Verifique se a pasta `web/` existe
- Confirme se o arquivo `index.html` está presente
- Tente acessar http://localhost:8080/docs para verificar se a API está funcionando

## 📝 Logs

O sistema exibe logs no console:

```
📦 Criando instância 1: Pugno Coder
   Copiando de: C:\Users\pugno\AppData\Roaming\Telegram Desktop
   Para: C:\Users\pugno\AppData\Roaming\Telegram_Instances\instance_1
✅ Instância 1 criada com sucesso!
🚀 Iniciando Telegram da instância 1: Pugno Coder
✅ Telegram iniciado com sucesso!
```

## 🔒 Segurança

- O sistema roda apenas localmente (`localhost`)
- Não há autenticação (use apenas em ambiente local/confiável)
- Cada instância mantém suas próprias sessões do Telegram

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente.

## 🤝 Contribuições

Sinta-se à vontade para melhorar o código, adicionar funcionalidades ou reportar bugs!

---

**Desenvolvido com ❤️ para facilitar o gerenciamento de múltiplas contas do Telegram**
