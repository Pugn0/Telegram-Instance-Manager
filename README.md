# 📱 Telegram Instance Manager

> Gerencie múltiplas instâncias do Telegram Desktop de forma simples e eficiente

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Sobre o Projeto

O **Telegram Instance Manager** é uma ferramenta completa para gerenciar múltiplas instâncias do Telegram Desktop no Windows. Ideal para quem precisa usar várias contas simultaneamente sem complicações.

### ✨ Funcionalidades

- ✅ **Criar instâncias** - Clone sua instalação do Telegram Desktop
- ▶️ **Iniciar/Parar** - Controle cada instância individualmente
- 🔄 **Status em tempo real** - Veja quais instâncias estão ativas
- 🕒 **Histórico de uso** - Acompanhe "visto por último" de cada instância
- ✏️ **Renomear** - Organize suas instâncias com nomes personalizados
- 📂 **Acesso rápido** - Abra a pasta de cada instância diretamente
- 🗑️ **Exclusão segura** - Remova instâncias que não precisa mais
- 🌐 **Interface web** - Moderna, responsiva e intuitiva

## 🚀 Como Usar

### Pré-requisitos

- Windows 10/11
- Python 3.7 ou superior
- Telegram Desktop instalado

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/Pugn0/Telegram-Instance-Manager.git
cd Telegram-Instance-Manager
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute o programa**
```bash
python main.py
```

ou simplesmente clique duas vezes em:
```
telegram.bat
```

4. **Acesse a interface**
- O navegador abrirá automaticamente
- Ou acesse manualmente: `http://localhost:8080`

## 📖 Guia Rápido

### Criar uma Nova Instância

1. Digite um nome no campo "Nome da instância"
2. Clique em **Criar Instância**
3. Aguarde a cópia dos arquivos
4. Pronto! Sua instância está criada

### Iniciar uma Instância

1. Clique no botão **▶️ Iniciar**
2. O Telegram abrirá automaticamente
3. O status mudará para **🟢 Ativo agora**

### Parar uma Instância

1. Clique no botão **⏹️ Parar**
2. O Telegram será fechado
3. O status mostrará **🕒 Visto por último**

## 🛠️ Estrutura do Projeto

```
Telegram-Instance-Manager/
│
├── main.py                 # Backend FastAPI
├── telegram.bat            # Script de inicialização Windows
├── requirements.txt        # Dependências Python
│
├── web/
│   └── index.html         # Interface web
│
└── data/
    └── instances.json     # Banco de dados das instâncias
```

## 🔧 Configuração

### Caminhos Padrão

O programa busca o Telegram Desktop em:
```
C:\Users\[SEU_USUARIO]\AppData\Roaming\Telegram Desktop
```

As instâncias são salvas em:
```
C:\Users\[SEU_USUARIO]\AppData\Roaming\Telegram_Instances
```

Para alterar esses caminhos, edite as variáveis em `main.py`:
```python
TELEGRAM_BASE = Path(r"C:\Seu\Caminho\Telegram Desktop")
INSTANCES_BASE = Path(r"C:\Seu\Caminho\Telegram_Instances")
```

## 🎨 Recursos da Interface

- **Dashboard intuitivo** - Veja todas as instâncias de uma vez
- **Atualização automática** - Status atualiza a cada 3 segundos
- **Notificações toast** - Feedback visual de todas as ações
- **Design responsivo** - Funciona em qualquer tamanho de tela
- **Animações suaves** - Transições e efeitos modernos

## 📊 API REST

O projeto expõe uma API REST completa:

### Endpoints Principais

```
GET    /instances              # Lista todas as instâncias
POST   /instances              # Cria nova instância
PUT    /instances/{id}         # Renomeia instância
DELETE /instances/{id}         # Exclui instância
POST   /instances/{id}/start   # Inicia Telegram
POST   /instances/{id}/stop    # Para Telegram
POST   /instances/{id}/open-folder  # Abre pasta
```

Acesse a documentação completa em:
```
http://localhost:8080/docs
```

## 🐛 Solução de Problemas

### O programa não inicia

- Verifique se o Python está instalado: `python --version`
- Instale as dependências: `pip install -r requirements.txt`

### "Pasta base do Telegram não encontrada"

- Verifique se o Telegram Desktop está instalado
- Confira o caminho em `main.py` (variável `TELEGRAM_BASE`)

### Instância não inicia

- Verifique se o arquivo `Telegram.exe` existe na pasta da instância
- Tente excluir e criar a instância novamente

### Porta já em uso

- O programa encontra automaticamente uma porta livre (8080-8180)
- Ou altere manualmente em `main.py` (variável `start_port`)

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Minha nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## 📝 Changelog

### v1.0.0 (2026-01-16)

- ✅ Sistema de criação de instâncias
- ✅ Interface web completa
- ✅ Iniciar/Parar instâncias
- ✅ Status em tempo real
- ✅ Histórico de última sessão
- ✅ Renomear e excluir instâncias
- ✅ Detecção automática de porta

## ⚠️ Avisos Importantes

- Esta ferramenta cria cópias completas do Telegram Desktop
- Cada instância ocupa ~200-300MB de espaço
- Use apenas para fins legítimos e pessoais
- Respeite os termos de serviço do Telegram

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Desenvolvedor

**Pugno**

- Telegram: [@pugno_dev](https://t.me/pugno_dev)
- GitHub: [@Pugn0](https://github.com/Pugn0)

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!

**Feito com ❤️ por Pugno**