"""Build a dependency-free map from the supplied CSV and SVG geometry."""
from pathlib import Path
import csv, json, html, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / 'data'
NS = {'s': 'http://www.w3.org/2000/svg'}

# Definition of the 6 regions specified by user map
REGIONS_SPEC = [
    {
        'id': 'vung-1',
        'key': 'tdmnbb',
        'name': 'Trung Du miền núi Bắc Bộ',
        'short': 'Trung Du & MN Bắc Bộ',
        'desc': 'Gồm 9 tỉnh: Tuyên Quang, Cao Bằng, Lạng Sơn, Phú Thọ, Thái Nguyên, Lào Cai, Sơn La, Điện Biên, Lai Châu.',
        'theme': '#1a5d33',
        'accent': '#22773d',
        'province_ids': [5, 2, 1, 8, 4, 6, 11, 10, 9],
        'base_colors': {pid: '#1f753c' for pid in [5, 2, 1, 8, 4, 6, 11, 10, 9]},
        'lit_colors': {pid: '#34d399' for pid in [5, 2, 1, 8, 4, 6, 11, 10, 9]}
    },
    {
        'id': 'vung-2',
        'key': 'dbsh',
        'name': 'Đồng bằng sông Hồng',
        'short': 'Đồng bằng sông Hồng',
        'desc': 'Gồm 6 tỉnh thành: Hà Nội, Hải Phòng, Quảng Ninh, Bắc Ninh, Hưng Yên, Ninh Bình.',
        'theme': '#bf3717',
        'accent': '#ec5028',
        'province_ids': [3, 34, 30, 7, 33, 32],
        'base_colors': {pid: '#ea4d25' for pid in [3, 34, 30, 7, 33, 32]},
        'lit_colors': {pid: '#fb7185' for pid in [3, 34, 30, 7, 33, 32]}
    },
    {
        'id': 'vung-3',
        'key': 'btb',
        'name': 'Bắc Trung Bộ',
        'short': 'Bắc Trung Bộ',
        'desc': 'Gồm 5 tỉnh thành: Huế, Thanh Hóa, Nghệ An, Hà Tĩnh, Quảng Trị.',
        'theme': '#a26d17',
        'accent': '#d0942d',
        'province_ids': [16, 12, 13, 14, 15],
        'base_colors': {pid: '#d49832' for pid in [16, 12, 13, 14, 15]},
        'lit_colors': {pid: '#f59e0b' for pid in [16, 12, 13, 14, 15]}
    },
    {
        'id': 'vung-4',
        'key': 'dhntbtn',
        'name': 'Duyên hải Nam Trung Bộ và Tây Nguyên',
        'short': 'Nam Trung Bộ & Tây Nguyên',
        'desc': 'Gồm 6 tỉnh thành và 2 quần đảo: Đà Nẵng, Quảng Ngãi, Gia Lai, Đắk Lắk, Khánh Hòa, Lâm Đồng, Hoàng Sa, Trường Sa.',
        'theme': '#0b75a6',
        'accent': '#0ca0e5',
        'province_ids': [17, 28, 27, 25, 26, 29, 35, 36],
        'base_colors': {pid: '#109ddc' for pid in [17, 28, 27, 25, 26, 29, 35, 36]},
        'lit_colors': {pid: '#38bdf8' for pid in [17, 28, 27, 25, 26, 29, 35, 36]}
    },
    {
        'id': 'vung-5',
        'key': 'dnb',
        'name': 'Đông Nam Bộ',
        'short': 'Đông Nam Bộ',
        'desc': 'Gồm 3 tỉnh thành: TP.Hồ Chí Minh, Đồng Nai, Tây Ninh.',
        'theme': '#6d226a',
        'accent': '#92368c',
        'province_ids': [19, 18, 21],
        'base_colors': {pid: '#963b90' for pid in [19, 18, 21]},
        'lit_colors': {pid: '#d946ef' for pid in [19, 18, 21]}
    },
    {
        'id': 'vung-6',
        'key': 'dbscl',
        'name': 'Đồng bằng sông Cửu Long',
        'short': 'Đồng bằng sông Cửu Long',
        'desc': 'Gồm 5 tỉnh thành: TP.Cần Thơ, An Giang, Đồng Tháp, Vĩnh Long, Cà Mau.',
        'theme': '#6f8f20',
        'accent': '#9eca3f',
        'province_ids': [22, 23, 31, 20, 24],
        'base_colors': {pid: '#9eca3f' for pid in [22, 23, 31, 20, 24]},
        'lit_colors': {pid: '#bef264' for pid in [22, 23, 31, 20, 24]}
    }
]

# Map each province ID to its region dict
province_region_map = {}
for r in REGIONS_SPEC:
    for pid in r['province_ids']:
        province_region_map[pid] = r

rows = list(csv.DictReader((DATA / 'Danh_sach_34_tinh_thanh.csv').open(encoding='utf-8-sig')))
provinces, groups = [], []
for row in rows:
    svg = ET.parse(DATA / row['tep_svg']).getroot()
    paths = list(svg.findall('.//s:path', NS))
    # Source brown paths are decorative markers, not province boundaries.
    paths = [p for p in paths if p.get('fill') != '#491b02']
    assert paths, row['tep_svg']
    name = row['tinh_thanh']
    short = name.replace('Thành phố ', '')
    idx = int(row['stt'])
    geometry = ''.join(f'<path d="{p.get("d")}" fill-rule="evenodd"/>' for p in paths)
    texts = list(svg.findall('.//s:text', NS))
    x = sum(float(t.get('x', 0)) for t in texts)/len(texts) + 65 if texts else 0
    y = sum(float(t.get('y', 0)) for t in texts)/len(texts) if texts else 0

    reg = province_region_map[idx]
    base_color = reg['base_colors'][idx]
    lit_color = reg['lit_colors'][idx]

    groups.append(f'''<g class="province" id="province-{idx}" data-id="{idx}" data-region="{reg['id']}" role="button" tabindex="0" aria-label="{html.escape(name)}" aria-pressed="false" style="--base-shade:{base_color}; --lit-shade:{lit_color}; --region-theme:{reg['theme']}; --shade:{base_color}">
    <title>{html.escape(name)} ({html.escape(reg['name'])})</title><g class="hit-area">{geometry}</g>
    <g class="province-face"><g class="land">{geometry}</g><text class="province-label" x="{x:.1f}" y="{y:.1f}">{html.escape(short)}</text></g></g>''')

    provinces.append({
        'id': idx,
        'name': name,
        'short': short,
        'file': row['tep_svg'],
        'viewBox': svg.get('viewBox'),
        'regionId': reg['id'],
        'regionName': reg['name'],
        'regionShort': reg['short'],
        'baseColor': base_color,
        'litColor': lit_color,
        'themeColor': reg['theme']
    })

regions_data = [
    {
        'id': r['id'],
        'key': r['key'],
        'name': r['name'],
        'short': r['short'],
        'desc': r['desc'],
        'theme': r['theme'],
        'accent': r['accent'],
        'count': len(r['province_ids']),
        'provinces': r['province_ids']
    }
    for r in REGIONS_SPEC
]

template = (ROOT / 'template.html.in').read_text(encoding='utf-8')
for marker in ('<!-- PROVINCE_PATHS -->', '/* PROVINCE_DATA */', '/* REGION_DATA */', '<!-- PROVINCE_LIST -->', '<!-- REGION_PILLS -->'):
    assert template.count(marker) == 1, f'Missing or duplicate template marker: {marker}'

region_pills_html = [
    '<button type="button" class="region-pill is-active" data-region="all" role="tab" aria-selected="true" title="Xem tất cả 34 tỉnh thành và 2 quần đảo">'
    '<span class="pill-dot" style="background:#4b6b55"></span>'
    '<span class="pill-title">Tất cả vùng</span>'
    '<span class="pill-badge">36</span>'
    '</button>'
]
for r in REGIONS_SPEC:
    region_pills_html.append(
        f'<button type="button" class="region-pill" data-region="{r["id"]}" role="tab" aria-selected="false" title="{html.escape(r["name"])}">'
        f'<span class="pill-dot" style="background:{r["accent"]}"></span>'
        f'<span class="pill-title">{html.escape(r["short"])}</span>'
        f'<span class="pill-badge">{len(r["province_ids"])}</span>'
        '</button>'
    )

output = (template
    .replace('<!-- PROVINCE_PATHS -->', '\n'.join(groups))
    .replace('/* PROVINCE_DATA */', json.dumps(provinces, ensure_ascii=False))
    .replace('/* REGION_DATA */', json.dumps(regions_data, ensure_ascii=False))
    .replace('<!-- REGION_PILLS -->', '\n'.join(region_pills_html)))

fallback_rows = ''.join(
    f'<button type="button" class="province-row" data-id="{p["id"]}" data-region="{p["regionId"]}" aria-pressed="false">'
    f'<span class="row-dot" style="background:{p["baseColor"]}" title="Màu vùng: {p["baseColor"]}"></span>'
    f'<span class="row-number">{p["id"]:02}</span>'
    f'<span class="row-name">{html.escape(p["short"])}</span>'
    f'<span class="row-region">{html.escape(p["regionShort"])}</span>'
    '<span class="row-arrow" aria-hidden="true">↗</span></button>'
    for p in sorted(provinces, key=lambda p: p['short'].casefold())
)
output = output.replace('<!-- PROVINCE_LIST -->', fallback_rows)

assert all(token not in output for token in ('<!-- PROVINCE_PATHS -->', '/* PROVINCE_DATA */', '/* REGION_DATA */', '<!-- PROVINCE_LIST -->', '<!-- REGION_PILLS -->'))
assert len(provinces) == 36
assert len(regions_data) == 6

(ROOT / 'dist').mkdir(exist_ok=True)
(ROOT / 'dist' / 'index.html').write_text(output, encoding='utf-8')
(ROOT / 'index.html').write_text(output, encoding='utf-8')
(ROOT.parent / 'index.html').write_text(output, encoding='utf-8')
print(f'Built {len(provinces)} provinces across {len(regions_data)} regions -> dist/index.html & index.html')
