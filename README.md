# ShockwaveTR

ShockwaveTR es una herramienta **OSINT de terminal** escrita en Python con 5 módulos independientes: rastreo de IPs, análisis de números de teléfono, búsqueda de usuarios en redes sociales, lookup de dominios y visualización completa de tu red local. Todo desde la línea de comandos, con historial automático y soporte para daltonismo.

---

## Módulos

### 1. IP Tracker
Geolocaliza cualquier IP pública y extrae toda la información disponible:

- País, ciudad, región y código postal
- Coordenadas + enlace directo a Google Maps
- ISP, ASN y organización
- Timezone, hora local en tiempo real y offset UTC
- Código de llamada, capital, bandera emoji y países fronterizos

---

### 2. Show Your IP
Muestra tu IP pública y el detalle completo de tu red local:

- IP pública via `ipify.org`
- IP local, máscara de subred, CIDR y dirección de broadcast
- Rango de hosts usables y total disponible
- Gateway por defecto
- Subredes `/24` si la red es más grande

---

### 3. Phone Number Tracker
Analiza un número de teléfono con formato internacional:

- Localización y código de región
- Operadora (carrier)
- Timezone del número
- Formatos: internacional, E.164, marcación móvil
- Validez real del número (no solo formato)
- Tipo: Móvil, Fijo, VoIP, Gratuito, Tarificación especial

---

### 4. Username Tracker
Busca un username en **22 plataformas en paralelo**:

| Plataforma | Plataforma | Plataforma |
|---|---|---|
| GitHub | Instagram | TikTok |
| YouTube | Twitch | SoundCloud |
| Pinterest | Tumblr | Reddit |
| Twitter / X | LinkedIn | Behance |
| Medium | Flickr | Dribbble |
| DeviantArt | Steam | Spotify |
| Product Hunt | Quora | Telegram |
| Snapchat | | |

Soporta búsqueda de **1 usuario o varios a la vez** (separados por comas).
Guarda historial con los resultados de cada búsqueda.

---

### 5. Domain Lookup
Obtiene información completa de un dominio:

- Resolución DNS → IP
- País, ciudad e ISP del servidor
- Registrador y fecha de creación (via whoisxmlapi)
- Registros DNS con `nslookup`

---

## Extras

- **Historial automático** → cada búsqueda se guarda en `results/history_<tipo>_<fecha>.json`
- **Soporte daltonismo** → 4 modos de color: normal, protanopia, deuteranopia, tritanopia
- **Ejecución paralela** → el username tracker usa `ThreadPoolExecutor` para escanear las 22 plataformas a la vez
- **Banner ASCII** de Shockwave en el menú principal

---

## Instalación

**Requisitos:**
- Python 3.9+ (Python 3.8 funciona con `pytz` instalado)

**Dependencias:**
```bash
pip install requests phonenumbers
```

**Opcional** (mejor detección de interfaces de red):
```bash
pip install netifaces pytz
```

---

## Uso

```bash
python ShockwaveTR.py
```

**Menú principal:**
```
[ 1 ] IP Tracker
[ 2 ] Show Your IP
[ 3 ] Phone Number Tracker
[ 4 ] Username Tracker
[ 5 ] Domain Lookup
[ 6 ] Color Config
[ 0 ] Exit
```

**Ejemplo — IP Tracker:**
```
Enter IP target : 8.8.8.8

IP target        : 8.8.8.8
Country          : United States
City             : Mountain View
ISP              : Google LLC
Maps             : https://www.google.com/maps/@37.386,-122.0838,8z
Current Time     : 2025-04-17 10:32:15 PDT
```

**Ejemplo — Username Tracker:**
```
Username : patpuralu

Escaneando 22 plataformas...

[✓] GitHub               (1/22)
[✗] Instagram            (2/22)
[✓] YouTube              (3/22)
...

[+] Encontrado en 3 plataformas

  [✓] GitHub     https://www.github.com/patpuralu
  [✓] YouTube    https://www.youtube.com/@patpuralu
  [✓] Reddit     https://www.reddit.com/user/patpuralu
```

---

## Archivos generados

```
results/
 └─ history_tracklu_2025-04-17.json    ← búsquedas de username
 └─ history_ip_2025-04-17.json         ← búsquedas de IP
 └─ history_domain_2025-04-17.json     ← búsquedas de dominio
```

---

## Aviso ético

ShockwaveTR está diseñado para:

- Auditar tu propia red e infraestructura
- Investigación y aprendizaje en ciberseguridad
- Localizar tus propios perfiles en redes sociales

**No usar en redes, dispositivos o cuentas ajenas sin permiso explícito.**
