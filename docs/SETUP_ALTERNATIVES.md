# Alternativas de Conexao

Se voce nao quiser ou nao puder usar um relay server proprio, existem alternativas.

## Opcao 1: ngrok

Servico de tunel gratuito (com limitacoes).

### Instalacao

```bash
# Windows
winget install ngrok

# Ou baixe de ngrok.com
```

### Configuracao

1. Crie conta em ngrok.com
2. Copie seu authtoken
3. Configure no config.json:

```json
{
    "alternatives": {
        "ngrok_enabled": true,
        "ngrok_authtoken": "seu-authtoken"
    }
}
```

### Limitacoes

- URL muda a cada reinicio (versao free)
- Limite de conexoes simultaneas
- Latencia adicional

---

## Opcao 2: bore.pub

Tunel TCP gratuito e open source.

### Instalacao

```bash
# Windows (via cargo)
cargo install bore-cli

# Ou baixe binario de github.com/ekzhang/bore
```

### Uso

```bash
bore local 5900 --to bore.pub
```

### Configuracao

```json
{
    "alternatives": {
        "bore_enabled": true,
        "bore_server": "bore.pub"
    }
}
```

---

## Opcao 3: Cloudflare Tunnel

Tunel gratuito da Cloudflare (requer dominio).

### Instalacao

```bash
winget install cloudflare.cloudflared
```

### Configuracao

1. Crie conta na Cloudflare
2. Adicione seu dominio
3. Configure tunnel via dashboard

---

## Opcao 4: Tailscale (Fallback)

VPN mesh gratuita. Requer instalacao com admin.

### Quando usar

- Quando nenhuma outra opcao funcionar
- Para uso permanente em maquinas proprias

### Instalacao

1. Baixe de tailscale.com
2. Instale (requer admin)
3. Conecte ambas maquinas na mesma rede Tailscale

### Vantagem

- Conexao direta, sem intermediario
- Menor latencia possivel
