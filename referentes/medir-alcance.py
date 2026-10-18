"""Consulta puntual de canales públicos enlazados desde los sitios institucionales."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlsplit, urlunsplit
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from datetime import datetime, timezone
import json, re

ROOT = Path(__file__).parent

def read(site):
    try:
        data = json.loads(site.read_text())
        links = [x['href'] for x in data.get('links', []) if 'youtube.com/' in x['href'] and not any(t in x['href'] for t in ['/watch', '/embed', '/playlist'])]
        if data['id'] == 'missio':
            links = [u for u in links if 'iglesiacristianamissiocord873' in u]
        if not links:
            return {'id': data['id'], 'verified': False, 'reason': 'No se identificó un canal en la portada consultada.'}
        parts = urlsplit(links[0])
        url = urlunsplit((parts.scheme, parts.netloc, parts.path, '', ''))
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
        match = re.search(r'(?:var ytInitialData = |ytInitialData\s*=\s*)', html)
        if not match:
            return {'id': data['id'], 'url': url, 'verified': False, 'reason': 'La respuesta no expuso los datos públicos del canal.'}
        obj = json.JSONDecoder().raw_decode(html[match.end():])[0]
        title = obj.get('metadata', {}).get('channelMetadataRenderer', {}).get('title', '')
        values = []
        def walk(value):
            if isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, str) and re.search(r'\b(subscribers|suscriptores)\b', v, re.I):
                        values.append(v)
                    elif isinstance(v, (dict, list)):
                        walk(v)
            elif isinstance(value, list):
                for v in value: walk(v)
        walk(obj.get('header', {}))
        counts = [v for v in values if len(v) < 130 and re.search(r'\d', v)]
        return {'id': data['id'], 'url': url, 'title': title, 'verified': bool(title and counts), 'subscriberLabel': counts[0] if counts else None, 'observedAt': datetime.now(timezone.utc).isoformat(), 'scope': 'Canal institucional enlazado desde la portada; no agrega música ni sedes.'}
    except Exception as exc:
        return {'id': site.stem, 'verified': False, 'reason': str(exc)}

if __name__ == '__main__':
    sites = [p for p in (ROOT/'datos').glob('*.json') if p.stem in ['life','elevation','saddleback','hillsong','bethel','passion','ieb-cordoba','rey-jesus','adoracion','centro-adoracion','rincon','missio']]
    records = list(ThreadPoolExecutor(max_workers=6).map(read, sites))
    (ROOT/'datos'/'alcance.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
    for item in records:
        print(json.dumps(item, ensure_ascii=False))
