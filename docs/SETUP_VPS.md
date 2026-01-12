# Setup VPS

Guia para configurar o relay server em uma VPS.

## Requisitos

- VPS com Linux (Ubuntu/Debian recomendado)
- Python 3.10+
- Porta 8443 aberta no firewall

## Oracle Cloud Free Tier (Recomendado)

1. Crie uma conta em cloud.oracle.com
2. Crie uma instancia Always Free (VM.Standard.E2.1.Micro)
3. Configure Security List para liberar porta 8443

## Instalacao

```bash
# Instalar Python
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Clonar projeto
git clone https://github.com/seu-usuario/remote-desk.git
cd remote-desk/relay

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Configurar TLS

```bash
# Gerar certificado self-signed (para desenvolvimento)
python ../scripts/generate_cert.py

# Para producao, use Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d meu-relay.duckdns.org
```

## Executar

```bash
# Desenvolvimento
python -m relay.server

# Producao (com systemd)
sudo cp remote-desk.service /etc/systemd/system/
sudo systemctl enable remote-desk
sudo systemctl start remote-desk
```

## DuckDNS (DNS Dinamico Gratuito)

1. Acesse duckdns.org e crie uma conta
2. Crie um subdominio (ex: meu-relay)
3. Configure o IP da VPS

```bash
# Atualizar DNS automaticamente
echo "url='https://www.duckdns.org/update?domains=meu-relay&token=SEU_TOKEN&ip='" | curl -k -o /dev/null -K -
```
