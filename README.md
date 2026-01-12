# RemoteDesk

Ferramenta de acesso remoto desktop open source para Windows, similar ao TeamViewer/AnyDesk.

## Funcionalidades

- Ver tela e controlar mouse/teclado remotamente
- Funciona sem privilegios de administrador
- Executavel portatil (sem instalacao)
- Funciona atraves da internet (NAT traversal via relay server)

## Arquitetura

```
[Notebook fora]  <--->  [VPS Relay]  <--->  [PCs em casa]
   (Client)              (Relay)             (Server)
```

## Requisitos

- Python 3.10+
- Windows 10/11 (client e server)
- Linux VPS (relay)

## Instalacao

```powershell
# Clonar repositorio
git clone https://github.com/seu-usuario/remote-desk.git
cd remote-desk

# Criar ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r desktop/requirements.txt
```

## Uso

### Rodar Relay (na VPS)
```bash
python -m relay.server
```

### Rodar Server (no PC a ser controlado)
```bash
python -m desktop.server.main
```

### Rodar Client (no PC que vai controlar)
```bash
python -m desktop.client.main
```

## Build Executaveis

```powershell
python scripts/build_server.py
python scripts/build_client.py
```

## Documentacao

- [Setup VPS](docs/SETUP_VPS.md)
- [Alternativas de conexao](docs/SETUP_ALTERNATIVES.md)
- [Uso detalhado](docs/USAGE.md)
- [Arquitetura](docs/ARCHITECTURE.md)

## Licenca

MIT License - veja [LICENSE](LICENSE)
