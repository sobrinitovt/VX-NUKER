<p align="center">
  <img src="https://files.catbox.moe/wgke8n.png" width="200"/>
</p>

<h1 align="center">VX-NUKER</h1>

<p align="center">
  <strong>v1.0.0</strong> &mdash; Herramienta avanzada de administracion y testing de servidores Discord
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white"/>
  <img src="https://img.shields.io/badge/aiohttp-3.9+-2C5BB4?style=for-the-badge&logo=aiohttp&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyArmor-Obfuscated-FF4500?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyInstaller-Compiled-00C853?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/UAC-Admin%20Required-FFD600?style=for-the-badge&logo=windows&logoColor=black"/>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-0078D6?style=for-the-badge&logo=windows&logoColor=white"/>
</p>

<p align="center">
  <a href="https://discord.gg/QAkKn3a8ya"><img src="https://img.shields.io/badge/Discord-Server-5865F2?style=for-the-badge&logo=discord&logoColor=white"/></a>
  <a href="https://guns.lol/vxsociety"><img src="https://img.shields.io/badge/GitHub-VX--Project-181717?style=for-the-badge&logo=github&logoColor=white"/></a>
  <a href="https://guns.lol/vxsociety"><img src="https://img.shields.io/badge/Guns.lol-vxsociety-FF4500?style=for-the-badge&logo=target&logoColor=white"/></a>
</p>

---

## Tabla de Contenidos

- [Descripcion General](#descripcion-general)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Requisitos Previos](#requisitos-previos)
- [Instalacion](#instalacion)
- [Tutorial: Crear el Bot en Discord](#tutorial-crear-el-bot-en-discord)
- [Como Usar la Herramienta](#como-usar-la-herramienta)
- [Lista Completa de Funciones](#lista-completa-de-funciones)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Solucion de Errores Comunes](#solucion-de-errores-comunes)
- [Creditos](#creditos)

---

## Descripcion General

**VX-NUKER** es una herramienta de linea de comandos que permite realizar operaciones masivas sobre servidores de Discord a traves de un bot. La herramienta cuenta con una interfaz TUI (Text User Interface) con animaciones, efectos visuales tipo matrix y un sistema de menus paginados con mas de 40 funciones disponibles.

La herramienta opera mediante un bot de Discord con permisos de administrador y ejecuta todas las acciones de forma asincrona utilizando `asyncio`, lo que garantiza velocidad maxima en cada operacion.

---

## Tecnologias Utilizadas

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" height="40"/>
  <img src="https://img.shields.io/badge/discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white" height="40"/>
  <img src="https://img.shields.io/badge/aiohttp-2C5BB4?style=for-the-badge&logo=aiohttp&logoColor=white" height="40"/>
  <img src="https://img.shields.io/badge/asyncio-FFD43B?style=for-the-badge&logo=python&logoColor=black" height="40"/>
  <img src="https://img.shields.io/badge/colorama-44CC11?style=for-the-badge&logo=python&logoColor=white" height="40"/>
</p>

| Tecnologia | Version Minima | Uso |
|---|---|---|
| Python | 3.10+ | Lenguaje principal |
| discord.py | 2.3.0+ | Comunicacion con la API de Discord |
| aiohttp | 3.9.0+ | Peticiones HTTP asincronas y webhooks |
| colorama | 0.4.6+ | Colores en terminal multiplataforma |
| asyncio | stdlib | Concurrencia y ejecucion paralela |
| PyArmor | 8.0+ | Ofuscacion y proteccion del codigo fuente |
| PyInstaller | 6.0+ | Compilacion a ejecutable standalone |

---

## Requisitos Previos

- **Python 3.10** o superior instalado y agregado al PATH del sistema
- **pip** (gestor de paquetes de Python)
- **Conexion a internet** estable
- **Un bot de Discord** con los permisos e intents necesarios (ver tutorial abajo)
- **El ID del servidor** donde el bot sera utilizado

---

## Instalacion

### Windows

```
1. Descargar o clonar el repositorio
2. Ejecutar install.bat (doble clic) — solicita permisos de Administrador
3. Esperar a que se instalen las dependencias + herramientas de build
4. Ejecutar build.bat para compilar el ejecutable ofuscado
5. Ejecutar start.bat para iniciar — solicita permisos de Administrador
```

### Linux

```bash
git clone https://guns.lol/vxsociety
cd VX-NUKER
chmod +x install.sh start.sh
./install.sh      # Solicita permisos de root
./start.sh        # Solicita permisos de root
```

### Compilacion (Build)

El sistema de compilacion utiliza **PyArmor** para ofuscar el codigo fuente y **PyInstaller** para generar un ejecutable standalone:

```
build.bat         # Windows — genera dist/VX-NUKER.exe
```

El ejecutable resultante:
- **Requiere permisos de Administrador** (UAC manifest integrado)
- Codigo fuente completamente ofuscado (PyArmor)
- Empaquetado con todas las dependencias (no requiere Python instalado)
- Icono personalizado (`icon.ico`)

### Instalacion Manual

```bash
pip install -r requirements.txt
python main.py
```

### Dependencias

El archivo `requirements.txt` contiene:

```
discord.py>=2.3.0
aiohttp>=3.9.0
colorama>=0.4.6
pyarmor>=8.0.0
pyinstaller>=6.0.0
```

---

## Tutorial: Crear el Bot en Discord

Este tutorial detalla paso a paso como crear correctamente el bot para que VX-NUKER funcione sin errores.

### Paso 1 - Acceder al Portal de Desarrolladores

1. Ir a https://discord.com/developers/applications
2. Iniciar sesion con tu cuenta de Discord
3. Hacer clic en el boton **"New Application"** (esquina superior derecha)
4. Escribir un nombre para la aplicacion (por ejemplo: `VX-NUKER`)
5. Aceptar los terminos y hacer clic en **"Create"**

### Paso 2 - Crear el Bot

1. En el menu lateral izquierdo, hacer clic en **"Bot"**
2. Si no se ha creado automaticamente, hacer clic en **"Add Bot"** y confirmar
3. En la seccion del bot, hacer clic en **"Reset Token"** para generar el token
4. **Copiar el token** y guardarlo en un lugar seguro (solo se muestra una vez)

### Paso 3 - Configurar los Intents (MUY IMPORTANTE)

Sin los intents correctos, el bot dara errores de permisos o no funcionara.

1. En la misma pagina del Bot, bajar hasta la seccion **"Privileged Gateway Intents"**
2. Activar **TODOS** los siguientes intents:
   - **PRESENCE INTENT** - Activar
   - **SERVER MEMBERS INTENT** - Activar
   - **MESSAGE CONTENT INTENT** - Activar
3. Hacer clic en **"Save Changes"**

### Paso 4 - Configurar los Permisos del Bot

1. En el menu lateral, ir a **"OAuth2"** > **"URL Generator"**
2. En la seccion **"SCOPES"**, marcar:
   - `bot`
   - `applications.commands`
3. En la seccion **"BOT PERMISSIONS"**, marcar:
   - **Administrator** (esto otorga todos los permisos necesarios)
4. Copiar la URL generada abajo

### Paso 5 - Invitar el Bot al Servidor

1. Pegar la URL copiada en el navegador
2. Seleccionar el servidor donde quieres agregar el bot
3. Hacer clic en **"Autorizar"**
4. Completar el captcha si aparece

### Paso 6 - Asegurar que el Rol del Bot este Arriba

1. Ir a **Configuracion del Servidor** > **Roles**
2. Arrastrar el rol del bot (VX-NUKER o el nombre que le hayas dado) lo mas **arriba posible** en la lista de roles
3. El bot solo puede actuar sobre usuarios cuyo rol mas alto este **por debajo** del suyo

### Paso 7 - Obtener el ID del Servidor

1. En Discord, ir a **Configuracion de Usuario** > **Avanzado** > activar **Modo Desarrollador**
2. Hacer clic derecho sobre el nombre del servidor en la barra lateral
3. Seleccionar **"Copiar ID del servidor"**
4. Guardar este ID, lo necesitaras al iniciar VX-NUKER

---

## Como Usar la Herramienta

### Primer Inicio

Al ejecutar `start.bat` (Windows) o `./start.sh` (Linux):

1. Se solicitan **permisos de Administrador** (UAC en Windows, sudo en Linux)
2. Se muestra una animacion de inicio tipo matrix
3. El programa solicita:
   - **Token del bot** - El token que copiaste en el Paso 2
   - **Server ID** - El ID del servidor que copiaste en el Paso 7
4. La sesion se guarda automaticamente en `.vx_session.json` para futuros inicios

> **Nota**: Si existe `dist/VX-NUKER.exe`, el lanzador ejecutara la version compilada. De lo contrario, ejecuta `main.py` directamente.

### Sesiones Guardadas

En inicios posteriores, VX-NUKER detectara la sesion anterior y preguntara si deseas reutilizarla. Escribe `yes` para cargar automaticamente el token y server ID guardados.

### Navegacion del Menu

Una vez conectado, se muestra un menu interactivo paginado con las funciones disponibles:

- Escribir el **numero** de la funcion (01-40) y presionar Enter para ejecutarla
- Escribir `n` para ir a la **siguiente pagina**
- Escribir `b` para ir a la **pagina anterior**
- Escribir `q` para **salir** de la herramienta

### Ejecucion de Funciones

Cada funcion solicita los parametros necesarios de forma interactiva:

- Los campos marcados como `[enter = pub]` usan un valor por defecto si se presiona Enter sin escribir nada
- Las confirmaciones requieren escribir `yes` exactamente para proceder
- Al finalizar cada operacion, se muestra un resumen con acciones exitosas, errores y tiempo total

---

## Lista Completa de Funciones

### Pagina 1 - Funciones Principales

| N | Funcion | Descripcion |
|---|---|---|
| 01 | **Nuke** | Destruccion total: elimina canales, roles, crea nuevos y spamea con webhooks |
| 02 | **Auto Raid** | Raid automatizado: limpia, crea 50 canales y los inunda con mensajes |
| 03 | **Ban All** | Banea a todos los miembros del servidor |
| 04 | **Kick All** | Expulsa a todos los miembros del servidor |
| 05 | **Mute All** | Silencia a todos los miembros por un tiempo determinado |
| 06 | **Unban All** | Desbanea a todos los usuarios baneados |
| 07 | **Del Channels** | Elimina todos los canales del servidor |
| 08 | **Del Emojis** | Elimina todos los emojis personalizados |
| 09 | **Del Stickers** | Elimina todos los stickers personalizados |
| 10 | **Create Channels** | Crea multiples canales (texto o voz) |
| 11 | **Create Roles** | Crea multiples roles con colores aleatorios |
| 12 | **Create Cats** | Crea multiples categorias |
| 13 | **Rename Channels** | Renombra todos los canales |
| 14 | **Rename Roles** | Renombra todos los roles |
| 15 | **Edit Server** | Cambia nombre, icono y descripcion del servidor |
| 16 | **Rename Members** | Cambia el apodo de todos los miembros |
| 17 | **Fix Nicks** | Elimina caracteres especiales al inicio de los apodos |
| 18 | **Get Admin** | Crea un rol con permisos de administrador y lo asigna |
| 19 | **Impersonate** | Envia mensajes haciendose pasar por otro usuario via webhooks |
| 20 | **Ghost Ping** | Menciona y elimina mensajes para generar pings fantasma |

### Pagina 2 - Funciones Avanzadas

| N | Funcion | Descripcion |
|---|---|---|
| 21 | **Remov Roles** | Elimina todos los roles asignados a los miembros |
| 22 | **Message All** | Envia un DM a todos los miembros |
| 23 | **DM Spam User** | Spam de mensajes directos a un usuario especifico |
| 24 | **Webhook Spam** | Crea webhooks en cada canal y spamea a traves de ellos |
| 25 | **Server Info** | Muestra informacion detallada del servidor |
| 26 | **Clone Server** | Exporta la estructura del servidor a un archivo JSON |
| 27 | **Webhook Logs** | Activa un logger que envia toda la actividad a un webhook externo |
| 28 | **Lockdown** | Bloquea el envio de mensajes en todos los canales |
| 29 | **Sourdine VC** | Ensordece a todos los usuarios en canales de voz |
| 30 | **Kick VC All** | Desconecta a todos los usuarios de los canales de voz |
| 31 | **Move All VC** | Mueve a todos los usuarios de voz a un canal especifico |
| 32 | **Invite Spam** | Genera multiples invitaciones del servidor |
| 33 | **Spam** | Envia mensajes masivos en todos los canales de texto |
| 34 | **Thread Spam** | Crea hilos masivos en todos los canales |
| 35 | **Reaction Spam** | Agrega reacciones masivas a mensajes existentes |
| 36 | **Voice Spam** | Conexion y desconexion rapida en canales de voz |
| 37 | **Spoiler Spam** | Envia mensajes con spoilers masivos |
| 38 | **Poll Spam** | Crea encuestas masivas en los canales |
| 39 | **Event Spam** | Crea eventos programados masivos |
| 40 | **Quit** | Cierra la herramienta |

### Pagina 3 - Funciones Extra

| N | Funcion | Descripcion |
|---|---|---|
| 41 | **Purge Msgs** | Elimina mensajes masivos de uno o todos los canales (hasta 1000 por canal) |
| 42 | **Export Logs** | Exporta el historial de logs de la sesion actual a un archivo .txt |
| 43 | **Slowmode All** | Aplica slowmode (0-21600 segundos) en todos los canales de texto |
| 44 | **Webhook Nuke** | Elimina todos los webhooks existentes en el servidor |
| 45 | **Role All** | Asigna un rol a todos los miembros o crea uno nuevo con permisos de admin |
| 46 | **Topic Spam** | Cambia el topic/descripcion de todos los canales de texto |
| 47 | **Perm Override** | Aplica overrides de permisos en todos los canales (deny_send, deny_view, deny_all, allow_all) |
| 48 | **Steal Emojis** | Copia todos los emojis de otro servidor donde el bot este presente |
| 49 | **Prune Members** | Expulsa miembros inactivos (sin rol, 1-30 dias de inactividad) |
| 50 | **Change Server** | Cambia el servidor objetivo sin reiniciar la herramienta |
| 51-60 | **Star-unlock** | Funciones adicionales que requieren dar estrella al repositorio |

---

## Arquitectura del Proyecto

```
VX-NUKER/
|-- main.py              # Script principal con toda la logica
|-- config.json          # Configuracion externa editable
|-- requirements.txt     # Dependencias de Python
|-- install.bat          # Instalador para Windows (requiere Admin)
|-- install.sh           # Instalador para Linux (requiere root)
|-- build.bat            # Script de compilacion (PyArmor + PyInstaller)
|-- start.bat            # Lanzador para Windows (requiere Admin)
|-- start.sh             # Lanzador para Linux (requiere root)
|-- icon.ico             # Icono del ejecutable
|-- app.manifest         # Manifiesto UAC (solicitud de Administrador)
|-- dist/VX-NUKER.exe    # Ejecutable compilado (generado por build.bat)
|-- .vx_session.json     # Sesion guardada (token + server ID)
|-- .vx_first            # Flag de primer inicio
|-- logs_*.txt           # Archivos de log exportados (generados)
```

### Flujo de Ejecucion

```
Inicio (requiere Administrador / root)
  |
  v
Verificacion de privilegios elevados (UAC / sudo)
  |
  v
Animacion Matrix (boot)
  |
  v
Cargar sesion anterior o pedir token + server ID
  |
  v
Conectar bot a Discord (discord.py)
  |
  v
Mostrar banner + info del servidor
  |
  v
Menu interactivo paginado (loop)
  |
  v
Ejecutar funcion seleccionada (asincrona)
  |
  v
Mostrar resumen de resultados
  |
  v
Volver al menu
```

### Flujo de Compilacion

```
build.bat
  |
  v
PyArmor: Ofuscacion del codigo fuente (main.py -> obfuscated/main.py)
  |
  v
PyInstaller: Empaquetado con hidden-imports + icon.ico + UAC manifest
  |
  v
Output: dist/VX-NUKER.exe (standalone, requiere Admin)
```

### Configuracion Externa (config.json)

El archivo `config.json` permite modificar el comportamiento de la herramienta sin tocar el codigo fuente:

```json
{
    "tool_name": "VX-NUKER",
    "discord_url": "https://discord.gg/QAkKn3a8ya",
    "github_url": "https://guns.lol/vxsociety",
    "raid_name": "raid-by-vx",
    "gif_banner": "URL del GIF banner",
    "no_ban_kick_ids": [123456789, 987654321],
    "auto_raid": {
        "num_channels": 50,
        "num_messages": 10
    },
    "server": {
        "new_name": "RAIDED BY VX-NUKER",
        "new_icon": "",
        "new_description": "discord.gg/QAkKn3a8ya"
    },
    "bot_presence": {
        "type": "playing",
        "text": "discord.gg/QAkKn3a8ya"
    }
}
```

- **no_ban_kick_ids**: Lista de IDs de usuario que seran protegidos contra ban, kick y mute
- **auto_raid.num_channels**: Cantidad de canales que se crean en el auto raid
- **auto_raid.num_messages**: Mensajes por canal durante el flood
- **bot_presence.type**: Tipo de actividad (playing, watching, listening, streaming)
- Si el archivo no existe o tiene errores, la herramienta usa valores por defecto

### Caracteristicas Tecnicas

- **Ejecucion asincrona**: Todas las operaciones se ejecutan con `asyncio.gather()` para maxima velocidad
- **Manejo de errores**: Cada operacion captura `discord.Forbidden` y `discord.HTTPException` individualmente
- **Lista de proteccion**: La variable `NO_BAN_KICK_ID` permite proteger IDs de usuarios contra ban/kick
- **Efectos visuales**: Animaciones glitch, barras de carga y efecto matrix en el boot
- **Guardado de sesion**: El token y server ID se almacenan localmente para reconexion rapida
- **Sistema de logs**: Registro con timestamps y categorias (OK, ERROR, WARN, INFO)
- **Ofuscacion de codigo**: PyArmor protege el codigo fuente contra ingenieria inversa
- **Compilacion standalone**: PyInstaller empaqueta todo en un unico ejecutable portable
- **Privilegios elevados**: El ejecutable requiere permisos de Administrador (Windows UAC / Linux sudo)

---

## Solucion de Errores Comunes

### "Privileged Intents Required"

```
discord.errors.PrivilegedIntentsRequired
```

**Causa**: Los intents privilegiados no estan activados en el portal de desarrolladores.

**Solucion**: Ir al portal de desarrolladores > Bot > Activar los tres Privileged Gateway Intents (ver Paso 3 del tutorial).

---

### "Improper Token"

```
discord.errors.LoginFailure: Improper token has been passed
```

**Causa**: El token ingresado es incorrecto o ha sido regenerado.

**Solucion**:
1. Ir al portal de desarrolladores > Bot > Reset Token
2. Copiar el nuevo token completo (sin espacios)
3. Eliminar `.vx_session.json` para que solicite el token nuevamente

---

### "Missing Permissions" / "Forbidden"

```
discord.errors.Forbidden: 403 Forbidden
```

**Causa**: El rol del bot no tiene permisos suficientes o esta por debajo de otros roles.

**Solucion**:
1. Verificar que el bot tiene permiso de **Administrador**
2. Mover el rol del bot al **tope** de la lista de roles del servidor
3. El bot no puede actuar sobre el propietario del servidor ni sobre roles superiores al suyo

---

### "Guild not found"

**Causa**: El Server ID ingresado es incorrecto o el bot no esta en ese servidor.

**Solucion**:
1. Verificar que el bot fue invitado correctamente al servidor
2. Confirmar que el ID es correcto (Modo Desarrollador > clic derecho > Copiar ID)

---

### "Rate Limited"

**Causa**: Discord aplica limites de velocidad cuando se hacen demasiadas peticiones.

**Solucion**: Esto es normal en operaciones masivas. La herramienta maneja esto internamente, pero en operaciones muy grandes algunas acciones pueden fallar. Los contadores de error del resumen final reflejan estas fallas.

---

### Error al Instalar Dependencias

**Windows**: Asegurarse de que Python esta en el PATH. Ejecutar `python --version` en CMD para verificar.

**Linux**: Instalar pip si no esta disponible:
```bash
sudo apt install python3-pip
```

---

## Creditos

<p align="center">
  <strong>VX SOCIETY Dev</strong>
</p>

<p align="center">
  <a href="https://discord.gg/QAkKn3a8ya">Discord</a> &mdash;
  <a href="https://guns.lol/vxsociety">GitHub</a>
</p>
(Inspired in VOID-NUKE)

---

<p align="center">
  <img src="https://img.shields.io/badge/VX--NUKER-v1.0.0-DC143C?style=for-the-badge"/>
</p>
