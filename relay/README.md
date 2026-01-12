# Relay Server

Servidor intermediario WebSocket que roteia conexoes entre clients e servers.

## Requisitos

- Python 3.10+
- Linux (recomendado para VPS)

## Instalacao

```bash
pip install -r requirements.txt
```

## Uso

```bash
python -m relay.server
```

## Configuracao

Edite `config.py` para ajustar:
- Porta do servidor
- Certificados TLS
- Token de autenticacao

## Deploy em VPS

Veja [docs/SETUP_VPS.md](../docs/SETUP_VPS.md) para instrucoes detalhadas.
