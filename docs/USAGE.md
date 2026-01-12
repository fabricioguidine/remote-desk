# Uso do RemoteDesk

## Primeiro Uso

### 1. Configurar

Copie `config.example.json` para `config.json` e edite:

```powershell
copy desktop\config.example.json config.json
notepad config.json
```

Configure:
- `relay_url`: URL do seu relay server
- `token`: Senha compartilhada entre server e client
- `server.id`: Nome identificador do PC

### 2. Iniciar Server (no PC a ser controlado)

```powershell
python -m desktop.server.main
```

O server ira:
- Conectar ao relay
- Mostrar icone na bandeja do sistema
- Aguardar conexoes

### 3. Iniciar Client (no PC que vai controlar)

```powershell
python -m desktop.client.main
```

O client ira:
- Conectar ao relay
- Mostrar lista de servers disponiveis
- Permitir selecionar e conectar

---

## Controles

### Client

| Tecla | Acao |
|-------|------|
| F11 | Alternar tela cheia |
| Escape | Desconectar |
| Ctrl+Alt | Liberar mouse (quando em tela cheia) |

### Server

O server roda minimizado na bandeja do sistema. Clique com botao direito para:
- Ver status
- Pausar/Retomar compartilhamento
- Sair

---

## Executaveis Portateis

Para usar sem Python instalado:

```powershell
# Gerar server.exe
python scripts/build_server.py

# Gerar client.exe
python scripts/build_client.py
```

Os executaveis estarao em `dist/`.

---

## Resolucao de Problemas

### "Conexao recusada"

- Verifique se o relay esta rodando
- Verifique a URL no config.json
- Verifique se a porta esta aberta no firewall

### "Token invalido"

- O token deve ser igual no server e client
- Verifique espacos em branco extras

### "Tela preta"

- Verifique se o monitor correto esta selecionado
- Tente mudar `monitor` no config.json

### "Mouse nao funciona"

- Alguns apps de tela cheia capturam o mouse
- Tente minimizar o app problemático
