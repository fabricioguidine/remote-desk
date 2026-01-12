# Arquitetura do RemoteDesk

## Visao Geral

```
[Client]  <--WebSocket-->  [Relay]  <--WebSocket-->  [Server]
```

### Componentes

1. **Relay Server**: Intermediario que roteia mensagens
2. **Desktop Server**: Captura e transmite a tela
3. **Desktop Client**: Recebe e exibe a tela, captura inputs

---

## Fluxo de Dados

### Conexao

1. Server conecta ao Relay e se registra
2. Client conecta ao Relay e solicita lista de servers
3. Client seleciona server para conectar
4. Relay pareia Client e Server

### Streaming

1. Server captura tela (mss)
2. Server comprime frame (JPEG + LZ4)
3. Server envia frame via Relay
4. Client recebe e descomprime
5. Client renderiza frame (pygame)

### Input

1. Client captura evento de mouse/teclado
2. Client envia comando via Relay
3. Server recebe e executa (pynput)

---

## Protocolo

### Mensagens de Controle (JSON)

```json
{
    "type": "message_type",
    "payload": { ... }
}
```

### Mensagens de Frame (Binario)

```
[1 byte: tipo] [4 bytes: timestamp] [N bytes: dados]
```

---

## Seguranca

### Autenticacao

- Token compartilhado entre todos os participantes
- Validado no Relay antes de permitir registro

### Criptografia

- TLS obrigatorio em producao
- Certificados Let's Encrypt recomendados

### Rate Limiting

- Limite de conexoes por IP
- Limite de mensagens por segundo

---

## Performance

### Otimizacoes

- JPEG para encoding (rapido, boa compressao)
- LZ4 para compressao adicional
- Envio apenas de frames alterados (futuro)
- Escala de resolucao configuravel

### Metricas Alvo

- 30 FPS em rede local
- 15-20 FPS via internet
- Latencia < 100ms em rede local

---

## Dependencias

### Relay
- websockets: Servidor WebSocket async

### Desktop
- websockets: Cliente WebSocket
- mss: Captura de tela (rapido, sem admin)
- Pillow: Encoding JPEG
- pynput: Controle mouse/teclado
- lz4: Compressao
- pygame: Renderizacao
- pystray: System tray
