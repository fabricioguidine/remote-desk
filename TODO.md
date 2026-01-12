# RemoteDesk - Lista de Tarefas

## Fase 1: Estrutura e MVP Local
- [x] Criar estrutura de pastas conforme especificado
- [x] Inicializar git
- [ ] Implementar `relay/server.py` basico (aceita conexoes, loga)
- [ ] Implementar `desktop/common/protocol.py` (classes de mensagem)
- [ ] Implementar `desktop/server/screen.py` (captura tela)
- [ ] Implementar `desktop/client/viewer.py` (exibe imagem)
- [ ] Testar localmente sem rede (mock)

## Fase 2: Comunicacao Basica
- [ ] Implementar WebSocket no relay
- [ ] Implementar conexao Server -> Relay
- [ ] Implementar conexao Client -> Relay
- [ ] Implementar roteamento de mensagens
- [ ] Testar streaming de tela via localhost

## Fase 3: Controles de Input
- [ ] Implementar `desktop/server/input.py` (executa mouse/teclado)
- [ ] Implementar `desktop/client/input.py` (captura mouse/teclado)
- [ ] Mapear coordenadas (resolucao client != server)
- [ ] Testar controle remoto local

## Fase 4: Autenticacao e Seguranca
- [ ] Implementar `relay/auth.py` (validacao de token)
- [ ] Adicionar TLS no relay
- [ ] Gerar certificados (self-signed para dev, Let's Encrypt para prod)
- [ ] Rate limiting basico

## Fase 5: Robustez
- [ ] Reconexao automatica com backoff
- [ ] Heartbeat/ping-pong
- [ ] Graceful shutdown
- [ ] Tratamento de erros

## Fase 6: Interface
- [ ] GUI no client (lista PCs, config, status)
- [ ] System tray no server
- [ ] Indicadores de FPS/latencia
- [ ] Hotkeys (fullscreen, disconnect)

## Fase 7: Alternativas
- [ ] Implementar modo tunel (ngrok/bore)
- [ ] Fallback automatico se relay falhar
- [ ] Documentar setup de cada alternativa

## Fase 8: Distribuicao
- [ ] Scripts PyInstaller
- [ ] Gerar `server.exe` e `client.exe`
- [ ] Testar executaveis em Windows limpo
- [ ] Documentacao completa
