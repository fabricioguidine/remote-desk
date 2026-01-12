# RemoteDesk - Changelog

## 2026-01-12 - Sessao 1: Criacao do Projeto

### Adicionado
- Estrutura completa de pastas do projeto
- Arquivos de configuracao raiz:
  - `CLAUDE.md` - instrucoes de desenvolvimento
  - `README.md` - documentacao do projeto
  - `.gitignore` - arquivos ignorados
  - `LICENSE` - MIT License
  - `STATUS.md` - estado atual do projeto
  - `TODO.md` - checklist de tarefas
  - `CHANGELOG.md` - historico de mudancas

- Modulo `relay/`:
  - `__init__.py`, `server.py`, `handler.py`, `auth.py`, `config.py`
  - `requirements.txt`, `README.md`

- Modulo `desktop/common/`:
  - `__init__.py`, `protocol.py`, `compression.py`, `config.py`, `connection.py`

- Modulo `desktop/server/`:
  - `__init__.py`, `main.py`, `app.py`, `screen.py`, `input.py`, `tray.py`, `gui.py`

- Modulo `desktop/client/`:
  - `__init__.py`, `main.py`, `app.py`, `viewer.py`, `input.py`, `gui.py`

- Arquivos `desktop/`:
  - `requirements.txt`, `config.example.json`

- Pasta `scripts/`:
  - `build_server.py`, `build_client.py`, `build_relay.py`, `generate_cert.py`

- Pasta `docs/`:
  - `SETUP_VPS.md`, `SETUP_ALTERNATIVES.md`, `USAGE.md`, `ARCHITECTURE.md`

- Pasta `tests/`:
  - `test_protocol.py`, `test_compression.py`, `test_connection.py`

### Git
- Repositorio inicializado
- Commit inicial: "Initial commit: project structure"
- Commit de limpeza: "Remove temp file and update gitignore"

### Notas
- Todos os arquivos .py estao como esqueletos (apenas comentarios)
- Proxima sessao: implementar relay/server.py basico
