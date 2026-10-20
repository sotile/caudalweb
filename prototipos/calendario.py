"""Próximas actividades desde un Google Calendar público.

La dirección iCal se lee de calendario.config.json y no se versiona:
puede ser el enlace secreto del calendario. Sin ese archivo, los
prototipos siguen con la agenda de muestra.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).parent
CONFIG = ROOT / 'calendario.config.json'
CACHE = ROOT / 'datos' / 'eventos.json'
ZONA = ZoneInfo('America/Argentina/Buenos_Aires')
DIAS = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}
SEMANA = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
SEMANA_CORTA = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom']
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
MESES_CORTOS = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
WHATSAPP = '541138230456'


def cargar_config():
    if not CONFIG.exists():
        return None
    data = json.loads(CONFIG.read_text())
    url = (data.get('ics_url') or '').strip()
    if not url:
        return None
    if not url.startswith('https://'):
        raise ValueError('La dirección del calendario tiene que empezar con https://')
    data['ics_url'] = url
    data.setdefault('zona', 'America/Argentina/Buenos_Aires')
    data.setdefault('dias', 90)
    data.setdefault('maximo', 3)
    return data


def unfold(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return re.sub(r'\n[ \t]', '', text)


def unescape(value):
    return (value.replace('\\n', '\n').replace('\\N', '\n')
            .replace('\\,', ',').replace('\\;', ';').replace('\\\\', '\\'))


def split_prop(line):
    if ':' not in line:
        return None
    head, value = line.split(':', 1)
    parts = head.split(';')
    params = {}
    for part in parts[1:]:
        if '=' in part:
            key, raw = part.split('=', 1)
            params[key.upper()] = raw.strip('"')
    return parts[0].upper(), params, value


def parse_dt(value, params, zona):
    value = value.strip()
    tzname = params.get('TZID')
    try:
        tz = ZoneInfo(tzname) if tzname else zona
    except Exception:
        tz = zona
    all_day = params.get('VALUE', '').upper() == 'DATE' or 'T' not in value
    if all_day:
        day = datetime.strptime(value[:8], '%Y%m%d').replace(tzinfo=tz)
        return day, True
    stamp = datetime.strptime(value[:15], '%Y%m%dT%H%M%S')
    if value.endswith('Z'):
        return stamp.replace(tzinfo=timezone.utc).astimezone(zona), False
    return stamp.replace(tzinfo=tz).astimezone(zona), False


def parse_byday(raw):
    items = []
    for piece in raw.split(','):
        piece = piece.strip()
        if len(piece) < 2:
            continue
        day = piece[-2:].upper()
        if day not in DIAS:
            continue
        ordinal = int(piece[:-2]) if piece[:-2] else None
        items.append((ordinal, DIAS[day]))
    return items


def nth_weekday(year, month, ordinal, weekday):
    if ordinal > 0:
        cursor = datetime(year, month, 1)
        shift = (weekday - cursor.weekday()) % 7
        cursor += timedelta(days=shift + (ordinal - 1) * 7)
        return cursor if cursor.month == month else None
    if month == 12:
        cursor = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        cursor = datetime(year, month + 1, 1) - timedelta(days=1)
    shift = (cursor.weekday() - weekday) % 7
    cursor -= timedelta(days=shift + (-ordinal - 1) * 7)
    return cursor if cursor.month == month else None


def parse_blocks(text):
    events = []
    for block in re.findall(r'BEGIN:VEVENT\n(.*?)\nEND:VEVENT', unfold(text), re.S):
        item = {'exdates': [], 'params': {}}
        for line in block.split('\n'):
            parsed = split_prop(line)
            if not parsed:
                continue
            name, params, value = parsed
            if name == 'EXDATE':
                for piece in value.split(','):
                    moment, _ = parse_dt(piece, params, ZONA)
                    item['exdates'].append(moment)
            elif name in ('DTSTART', 'DTEND', 'RECURRENCE-ID'):
                item[name.lower().replace('-', '_')] = parse_dt(value, params, ZONA)
                item['params'][name] = params
            else:
                item[name.lower()] = unescape(value).strip()
        if 'dtstart' in item:
            events.append(item)
    return events


def same_moment(left, right):
    if left.tzinfo and right.tzinfo:
        return left.astimezone(timezone.utc).replace(second=0, microsecond=0) == right.astimezone(timezone.utc).replace(second=0, microsecond=0)
    return left.replace(second=0, microsecond=0) == right.replace(second=0, microsecond=0)


def skipped(moment, exdates):
    return any(same_moment(moment, item) for item in exdates)


def occurrences(event, window_start, window_end):
    start, all_day = event['dtstart']
    end = event['dtend'][0] if 'dtend' in event else start + (timedelta(days=1) if all_day else timedelta(hours=1))
    duration = end - start
    rule = event.get('rrule')
    if not rule:
        yield start, start + duration, all_day
        return
    parts = {}
    for piece in rule.split(';'):
        if '=' in piece:
            key, value = piece.split('=', 1)
            parts[key.upper()] = value
    freq = parts.get('FREQ', 'DAILY')
    interval = max(1, int(parts.get('INTERVAL', '1') or 1))
    count = int(parts['COUNT']) if parts.get('COUNT') else None
    until = None
    if parts.get('UNTIL'):
        until, _ = parse_dt(parts['UNTIL'], {}, start.tzinfo or ZONA)
    byday = parse_byday(parts['BYDAY']) if parts.get('BYDAY') else []
    produced = 0
    cursor = start
    guard = 0
    while guard < 800 and cursor <= window_end and (until is None or cursor <= until):
        guard += 1
        batch = []
        if freq == 'WEEKLY' and byday:
            week = cursor - timedelta(days=cursor.weekday())
            for _, weekday in byday:
                day = week + timedelta(days=weekday)
                candidate = day.replace(hour=start.hour, minute=start.minute, second=0, microsecond=0, tzinfo=start.tzinfo)
                if candidate >= start:
                    batch.append(candidate)
            cursor = week + timedelta(days=7 * interval)
        elif freq == 'MONTHLY' and byday and byday[0][0]:
            ordinal, weekday = byday[0]
            found = nth_weekday(cursor.year, cursor.month, ordinal, weekday)
            if found and found.date() >= start.date():
                batch.append(found.replace(hour=start.hour, minute=start.minute, tzinfo=start.tzinfo))
            month = cursor.month + interval
            year = cursor.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            cursor = cursor.replace(year=year, month=month, day=1)
        elif freq == 'MONTHLY':
            batch.append(cursor)
            month = cursor.month + interval
            year = cursor.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            day = min(start.day, 28)
            cursor = cursor.replace(year=year, month=month, day=day)
        elif freq == 'WEEKLY':
            batch.append(cursor)
            cursor += timedelta(days=7 * interval)
        else:
            batch.append(cursor)
            cursor += timedelta(days=interval)
        for candidate in batch:
            if count is not None and produced >= count:
                return
            if until and candidate > until:
                return
            if candidate < start or skipped(candidate, event['exdates']):
                produced += 1
                continue
            produced += 1
            finish = candidate + duration
            if finish > window_start and candidate <= window_end:
                yield candidate, finish, all_day


def proximas(text, ahora=None, dias=90, maximo=3, zona=ZONA):
    ahora = ahora or datetime.now(zona)
    if ahora.tzinfo is None:
        ahora = ahora.replace(tzinfo=zona)
    ventana = ahora + timedelta(days=dias)
    masters = []
    overrides = []
    for event in parse_blocks(text):
        if event.get('class', '').upper() in ('PRIVATE', 'CONFIDENTIAL'):
            continue
        if 'recurrence_id' in event:
            overrides.append(event)
        else:
            masters.append(event)
    found = []
    for event in masters:
        if event.get('status', '').upper() == 'CANCELLED':
            continue
        for start, end, all_day in occurrences(event, ahora, ventana):
            found.append({'uid': event.get('uid', ''), 'start': start, 'end': end, 'all_day': all_day, 'title': event.get('summary') or 'Actividad', 'where': event.get('location', ''), 'text': event.get('description', ''), 'url': event.get('url', ''), 'status': event.get('status', '')})
    for event in overrides:
        stamp, _ = event['recurrence_id']
        match = next((item for item in found if item['uid'] == event.get('uid') and same_moment(item['start'], stamp)), None)
        if event.get('status', '').upper() == 'CANCELLED':
            if match:
                found.remove(match)
            continue
        start, all_day = event['dtstart']
        end = event['dtend'][0] if 'dtend' in event else start + timedelta(hours=1)
        replacement = {'uid': event.get('uid', ''), 'start': start, 'end': end, 'all_day': all_day, 'title': event.get('summary') or (match['title'] if match else 'Actividad'), 'where': event.get('location', match['where'] if match else ''), 'text': event.get('description', match['text'] if match else ''), 'url': event.get('url', match['url'] if match else ''), 'status': 'CONFIRMED'}
        if match:
            found.remove(match)
        if end > ahora and start <= ventana:
            found.append(replacement)
    found = [item for item in found if item['end'] > ahora and item['status'].upper() != 'CANCELLED']
    found.sort(key=lambda item: item['start'])
    unique = []
    seen = set()
    for item in found:
        key = (item['uid'], item['start'].isoformat())
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique[:maximo]


def limpiar(text, limite=140):
    text = re.sub(r'<[^>]+>', ' ', text or '')
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= limite:
        return text
    return text[:limite].rsplit(' ', 1)[0] + '…'


def etiqueta(item):
    start = item['start'].astimezone(ZONA)
    when = f'{SEMANA[start.weekday()]} {start.day} de {MESES[start.month - 1]}'
    if item['all_day']:
        return when[:1].upper() + when[1:]
    return f'{when[:1].upper() + when[1:]} · {start.strftime("%H:%M")}'


def enlace(item):
    url = item.get('url') or ''
    if url.startswith('https://') or url.startswith('http://'):
        return url, 'Quiero participar'
    mensaje = urllib.parse.quote(f'Hola, quisiera información sobre {item["title"]}')
    return f'https://wa.me/{WHATSAPP}?text={mensaje}', 'Consultá esta actividad'


def tarjeta(item):
    start = item['start'].astimezone(ZONA)
    href, accion = enlace(item)
    detalle = limpiar(item.get('text', ''))
    if detalle.lower() == item['title'].lower():
        detalle = ''
    lugar = limpiar(item.get('where', ''), 80)
    extra = f' <p>{escape(lugar)}</p>' if lugar else ''
    texto = f'<p>{escape(detalle)}</p>' if detalle else ''
    return (
        f'<a class="event-card event-card-live" href="{escape(href, quote=True)}">'
        f'<div class="event-date"><span>{SEMANA_CORTA[start.weekday()]}</span>'
        f'<strong>{start.day}</strong><small>{MESES_CORTOS[start.month - 1]}</small></div>'
        f'<div><p class="eyebrow">{escape(etiqueta(item))}</p><h3>{escape(item["title"])}</h3>'
        f'{texto}{extra}<span class="text-link">{accion} ↗</span></div></a>'
    )


def seccion(items, origen):
    if items:
        grilla = ''.join(tarjeta(item) for item in items)
        nota = 'Próximas actividades del calendario.'
    else:
        ahora = datetime.now(ZONA)
        salto = (5 - ahora.weekday()) % 7
        sabado = ahora + timedelta(days=salto)
        grilla = (
            f'<a class="event-card event-card-live" href="#visitanos"><div class="event-date"><span>{SEMANA_CORTA[sabado.weekday()]}</span><strong>{sabado.day}</strong><small>{MESES_CORTOS[sabado.month - 1]}</small></div>'
            '<div><p class="eyebrow">Cuando no hay una actividad especial</p><h3>Nos encontramos en casa.</h3>'
            '<p>El calendario no tiene otra convocatoria en los próximos días. La reunión de fin de semana sigue en pie.</p>'
            '<span class="text-link">Prepará tu visita ↗</span></div></a>'
        )
        nota = 'Calendario conectado, sin otra actividad cargada.'
    return (
        f'<section class="events section wrap" id="eventos"><div class="section-heading"><div>'
        f'<p class="eyebrow">La vida de Caudal</p><h2>Hay mucho para <em>compartir.</em></h2></div>'
        f'<p>{nota}<br>Los horarios salen de Google Calendar.</p></div>'
        f'<div class="event-grid">{grilla}</div>'
        f'<p class="event-source">Fuente: {escape(origen)}</p></section>'
    )


def descargar(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'CaudalAgenda/1.0'})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode('utf-8', 'replace')


def guardar(items):
    CACHE.parent.mkdir(exist_ok=True)
    payload = []
    for item in items:
        copy = dict(item)
        copy['start'] = item['start'].isoformat()
        copy['end'] = item['end'].isoformat()
        payload.append(copy)
    CACHE.write_text(json.dumps({'guardado': datetime.now(ZONA).isoformat(), 'eventos': payload}, ensure_ascii=False, indent=2))


def leer_cache():
    if not CACHE.exists():
        return None
    data = json.loads(CACHE.read_text())
    items = []
    for item in data.get('eventos', []):
        item['start'] = datetime.fromisoformat(item['start'])
        item['end'] = datetime.fromisoformat(item['end'])
        items.append(item)
    return items


def actividades(config=None, texto=None):
    config = config if config is not None else cargar_config()
    if not config and texto is None:
        return None
    zona = ZoneInfo(config.get('zona', 'America/Argentina/Buenos_Aires')) if config else ZONA
    if texto is None:
        try:
            texto = descargar(config['ics_url'])
        except Exception as exc:
            cached = leer_cache()
            print(f'Agenda: no se pudo leer el calendario ({exc}).', file=sys.stderr)
            if cached is None:
                return None
            print('Agenda: se usa la última lectura guardada.', file=sys.stderr)
            return cached
    items = proximas(texto, dias=int(config.get('dias', 90)) if config else 90, maximo=int(config.get('maximo', 3)) if config else 3, zona=zona)
    if config and config.get('ics_url'):
        guardar(items)
    return items


def html_eventos(root=None):
    config = cargar_config()
    if not config:
        return None
    items = actividades(config)
    if items is None:
        return None
    return seccion(items, 'Google Calendar')


def probar():
    zona = ZONA
    ahora = datetime(2026, 10, 19, 12, tzinfo=zona)
    muestra = """BEGIN:VCALENDAR
BEGIN:VEVENT
UID:pasado@caudal
DTSTART;TZID=America/Argentina/Buenos_Aires:20261001T190000
DTEND;TZID=America/Argentina/Buenos_Aires:20261001T210000
SUMMARY:Retiro vencido
END:VEVENT
BEGIN:VEVENT
UID:unico@caudal
DTSTART;TZID=America/Argentina/Buenos_Aires:20261025T190000
DTEND;TZID=America/Argentina/Buenos_Aires:20261025T210000
SUMMARY:Integrar
LOCATION:España 1626
DESCRIPTION:Encuentro para conocer Caudal.
END:VEVENT
BEGIN:VEVENT
UID:cancelado@caudal
DTSTART;TZID=America/Argentina/Buenos_Aires:20261026T190000
SUMMARY:No sale
STATUS:CANCELLED
END:VEVENT
BEGIN:VEVENT
UID:domingo@caudal
DTSTART;TZID=America/Argentina/Buenos_Aires:20261004T100000
DTEND;TZID=America/Argentina/Buenos_Aires:20261004T120000
RRULE:FREQ=WEEKLY;BYDAY=SU
EXDATE;TZID=America/Argentina/Buenos_Aires:20261025T100000
SUMMARY:Reunión del domingo
END:VEVENT
BEGIN:VEVENT
UID:domingo@caudal
RECURRENCE-ID;TZID=America/Argentina/Buenos_Aires:20261101T100000
DTSTART;TZID=America/Argentina/Buenos_Aires:20261101T100000
SUMMARY:Reunión del domingo
STATUS:CANCELLED
END:VEVENT
BEGIN:VEVENT
UID:jornada@caudal
DTSTART;VALUE=DATE:20261112
DTEND;VALUE=DATE:20261113
SUMMARY:Jornada de misiones
END:VEVENT
END:VCALENDAR
"""
    items = proximas(muestra, ahora=ahora, dias=40, maximo=6)
    titles = [(item['title'], item['start'].strftime('%Y-%m-%d %H:%M')) for item in items]
    assert ('Retiro vencido', '2026-10-01 19:00') not in titles, titles
    assert ('No sale', '2026-10-26 19:00') not in titles, titles
    assert ('Integrar', '2026-10-25 19:00') in titles, titles
    assert ('Reunión del domingo', '2026-10-25 10:00') not in titles, titles
    assert ('Reunión del domingo', '2026-11-01 10:00') not in titles, titles
    assert ('Reunión del domingo', '2026-11-08 10:00') in titles, titles
    assert ('Jornada de misiones', '2026-11-12 00:00') in titles, titles
    integrar = next(item for item in items if item['title'] == 'Integrar')
    assert integrar['start'].hour == 19, integrar['start']
    assert 'España 1626' in integrar['where']
    print('Agenda: pruebas ok')
    for title, when in titles:
        print(f'  {when}  {title}')


if __name__ == '__main__':
    if '--probar' in sys.argv:
        probar()
    else:
        config = cargar_config()
        if not config:
            print('No hay calendario.config.json con ics_url. Los prototipos siguen con la agenda de muestra.')
            sys.exit(0)
        items = actividades(config)
        if not items:
            print('Calendario conectado. No hay actividades en la ventana.')
        for item in items or []:
            print(f"{etiqueta(item)}  {item['title']}")
