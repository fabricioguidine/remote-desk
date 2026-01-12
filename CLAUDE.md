# RemoteDesk - Instrucoes de Desenvolvimento

## Contexto do Projeto

Ferramenta de acesso remoto desktop (similar ao TeamViewer/AnyDesk), open source, para controlar PCs Windows em casa a partir de um notebook Windows externo.

**Requisitos:**
- Funcionar sem privilegios de administrador
- Executavel portatil (sem instalacao)
- Ver tela e controlar mouse/teclado remotamente
- Funcionar atraves da internet (NAT traversal)

---

## Arquiteturas Disponiveis (escolha uma)

### Opcao 1: Relay Server (RECOMENDADA)

Servidor intermediario em VPS que roteia o trafego.

```
[Notebook fora]  <--->  [VPS Relay]  <--->  [PCs em casa]
   (Client)              (Relay)             (Server)
```

**Pros:** Sempre funciona, confiavel, sem configuracao de roteador
**Contras:** Precisa de VPS (Oracle Free Tier e gratis)

---

### Opcao 2: Tunel Reverso com Servico Gratuito

Usa servicos como ngrok, Cloudflare Tunnel, ou bore.pub.

```
[PC em casa]  --tunel-->  [Servico externo]  <--conexao--  [Notebook fora]
  (Server)                 (ngrok/cloudflare)               (Client)
```

**Pros:** Sem precisar de VPS proprio, setup rapido
**Contras:** Dependencia de servico terceiro, URL muda a cada reinicio (ngrok free)

---

### Opcao 3: Hole Punching P2P (sem servidor)

Conexao direta entre Client e Server usando STUN/TURN.

**Bibliotecas:** `aiortc`, `aioice`

**Pros:** Sem intermediario, menor latencia
**Contras:** Funciona so em ~70-80% dos casos (alguns NAT bloqueiam)

---

### Opcao 4: VPN Mesh (Tailscale/ZeroTier como fallback)

Se nenhuma opcao funcionar, orienta o usuario a instalar Tailscale.

**Nota:** Requer instalacao com admin, mas e fallback se nada mais funcionar.

---

## Arquitetura Tecnica Detalhada

### Fluxo de Dados

```
                         RELAY SERVER
  +------------+    +------------+    +------------+
  |   Auth     |    |   Router   |    |   Session  |
  |   Manager  |--->|   Handler  |--->|   Manager  |
  +------------+    +------------+    +------------+
        ^                 ^                 |
        |                 |                 v
   [Valida Token]   [Roteia Msgs]   [Pareia Client/Server]

          ^                                 |
          |              WebSocket          |
          |                                 v
+---------------------+         +---------------------+
|       SERVER        |         |       CLIENT        |
|  +---------------+  |         |  +---------------+  |
|  | Screen Capture|  | Frames  |  |    Viewer     |  |
|  |    (mss)      |--+-------->|  |   (pygame)    |  |
|  +---------------+  |         |  +---------------+  |
|  +---------------+  |         |  +---------------+  |
|  | Input Handler |  | Commands|  | Input Capture |  |
|  |   (pynput)    |<-+---------+--|   (pynput)    |  |
|  +---------------+  |         |  +---------------+  |
|  +---------------+  |         |  +---------------+  |
|  |  Compression  |  |         |  | Decompression |  |
|  |    (lz4)      |  |         |  |    (lz4)      |  |
|  +---------------+  |         |  +---------------+  |
+---------------------+         +---------------------+
```

---

## Stack Tecnologica

### Relay (Python - Linux VPS)
```
websockets>=12.0      # Servidor WebSocket async
asyncio               # Built-in async
ssl                   # Built-in TLS
```

### Desktop (Python - Windows)
```
websockets>=12.0      # Conexao WebSocket
mss>=9.0              # Captura de tela (rapido, sem admin)
Pillow>=10.0          # Encoding JPEG
pynput>=1.7           # Mouse/teclado (sem admin)
lz4>=4.3              # Compressao rapida
pygame>=2.5           # Exibicao no client
pystray>=0.19         # System tray (server)
pyinstaller>=6.0      # Gerar .exe
```

---

## Protocolo de Mensagens

### Formato Base
```python
# Mensagens de controle: JSON
{
    "type": "message_type",
    "payload": { ... }
}

# Mensagens de frame: Binario
[1 byte: tipo] [4 bytes: timestamp] [N bytes: dados comprimidos]
```

### Tipos de Mensagem

| Type | Direcao | Payload |
|------|---------|---------|
| `register` | Client/Server -> Relay | `{role, id?, token}` |
| `registered` | Relay -> Client/Server | `{success, error?}` |
| `list_servers` | Client -> Relay | `{}` |
| `server_list` | Relay -> Client | `{servers: [{id, connected}]}` |
| `connect_to` | Client -> Relay | `{target_id}` |
| `client_connected` | Relay -> Server | `{client_id}` |
| `connected` | Relay -> Client | `{target_id, width, height}` |
| `disconnect` | Any -> Relay | `{}` |
| `frame` | Server -> Client | Binario |
| `mouse_move` | Client -> Server | `{x, y}` |
| `mouse_click` | Client -> Server | `{x, y, button, action}` |
| `mouse_scroll` | Client -> Server | `{x, y, dx, dy}` |
| `key` | Client -> Server | `{key, action}` |
| `ping` | Any -> Any | `{timestamp}` |
| `pong` | Any -> Any | `{timestamp, latency}` |

---

## Configuracao (config.json)

```json
{
    "connection": {
        "mode": "relay",
        "relay_url": "wss://meu-relay.duckdns.org:8443",
        "token": "minha-senha-secreta-456",
        "reconnect_interval": 5,
        "timeout": 30
    },
    "server": {
        "id": "PC-ESCRITORIO",
        "capture_fps": 30,
        "quality": 70,
        "scale": 1.0,
        "monitor": 0
    },
    "client": {
        "show_fps": true,
        "show_latency": true,
        "fullscreen_key": "F11",
        "disconnect_key": "Escape"
    },
    "alternatives": {
        "ngrok_enabled": false,
        "ngrok_authtoken": "",
        "bore_enabled": false,
        "bore_server": "bore.pub"
    }
}
```

---

## Fases de Desenvolvimento

### Fase 1: Estrutura e MVP Local
- [ ] Criar estrutura de pastas conforme especificado
- [ ] Inicializar git
- [ ] Implementar `relay/server.py` basico (aceita conexoes, loga)
- [ ] Implementar `desktop/common/protocol.py` (classes de mensagem)
- [ ] Implementar `desktop/server/screen.py` (captura tela)
- [ ] Implementar `desktop/client/viewer.py` (exibe imagem)
- [ ] Testar localmente sem rede (mock)

### Fase 2: Comunicacao Basica
- [ ] Implementar WebSocket no relay
- [ ] Implementar conexao Server -> Relay
- [ ] Implementar conexao Client -> Relay
- [ ] Implementar roteamento de mensagens
- [ ] Testar streaming de tela via localhost

### Fase 3: Controles de Input
- [ ] Implementar `desktop/server/input.py` (executa mouse/teclado)
- [ ] Implementar `desktop/client/input.py` (captura mouse/teclado)
- [ ] Mapear coordenadas (resolucao client != server)
- [ ] Testar controle remoto local

### Fase 4: Autenticacao e Seguranca
- [ ] Implementar `relay/auth.py` (validacao de token)
- [ ] Adicionar TLS no relay
- [ ] Gerar certificados (self-signed para dev, Let's Encrypt para prod)
- [ ] Rate limiting basico

### Fase 5: Robustez
- [ ] Reconexao automatica com backoff
- [ ] Heartbeat/ping-pong
- [ ] Graceful shutdown
- [ ] Tratamento de erros

### Fase 6: Interface
- [ ] GUI no client (lista PCs, config, status)
- [ ] System tray no server
- [ ] Indicadores de FPS/latencia
- [ ] Hotkeys (fullscreen, disconnect)

### Fase 7: Alternativas
- [ ] Implementar modo tunel (ngrok/bore)
- [ ] Fallback automatico se relay falhar
- [ ] Documentar setup de cada alternativa

### Fase 8: Distribuicao
- [ ] Scripts PyInstaller
- [ ] Gerar `server.exe` e `client.exe`
- [ ] Testar executaveis em Windows limpo
- [ ] Documentacao completa

---

## Comandos de Desenvolvimento

```powershell
# Entrar na pasta do projeto
cd C:\Users\fabri\Documents\repos\remote-desk

# Criar ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r desktop/requirements.txt

# Rodar relay (em outro terminal ou VPS)
python -m relay.server

# Rodar server
python -m desktop.server.main

# Rodar client
python -m desktop.client.main

# Build executaveis
python scripts/build_server.py
python scripts/build_client.py
```

---

## Notas Importantes

1. **Sem admin:** `mss` e `pynput` funcionam sem elevacao
2. **Antivirus:** Pode alertar sobre pynput (e normal, adicionar excecao)
3. **Firewall:** Na primeira execucao, Windows pede permissao de rede
4. **Encoding:** Usar JPEG (rapido), nao PNG (lento demais)
5. **Binario vs JSON:** Frames em binario, controle em JSON
6. **Monitor multiplo:** mss suporta, configuravel via `monitor` no config
