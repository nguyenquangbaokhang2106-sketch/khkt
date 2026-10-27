"""Build a dependency-free map from the supplied CSV and SVG geometry."""
from pathlib import Path
import csv, json, html, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / 'data'
NS = {'s': 'http://www.w3.org/2000/svg'}

# Definition of the 5 regions specified by the user
REGIONS_SPEC = [
    {
        'id': 'vung-1',
        'key': 'tdmnbb',
        'name': 'Trung Du miền núi Bắc Bộ',
        'short': 'Trung Du & MN Bắc Bộ',
        'desc': 'Gồm 9 tỉnh: Tuyên Quang, Cao Bằng, Lạng Sơn, Phú Thọ, Thái Nguyên, Lào Cai, Sơn La, Điện Biên, Lai Châu.',
        'theme': '#2d6a4f',
        'accent': '#10b981',
        'province_ids': [5, 2, 1, 8, 4, 6, 11, 10, 9],
        'base_colors': {
            1: '#6b9060',   # Lạng Sơn
            2: '#7fa373',   # Cao Bằng
            4: '#628757',   # Thái Nguyên
            5: '#749868',   # Tuyên Quang
            6: '#587c4d',   # Lào Cai
            8: '#87aa7b',   # Phú Thọ
            9: '#4e7243',   # Lai Châu
            10: '#5e8253',  # Điện Biên
            11: '#6f9364',  # Sơn La
        },
        'lit_colors': {
            1: '#3b82f6',   # Lạng Sơn: Xanh Sapphire rực rỡ
            2: '#06b6d4',   # Cao Bằng: Xanh Ngọc Biển sáng
            4: '#10b981',   # Thái Nguyên: Ngọc Lục Bảo tươi
            5: '#22c55e',   # Tuyên Quang: Xanh Cốm bừng sáng
            6: '#eab308',   # Lào Cai: Vàng Nghệ Hoàng Yến
            8: '#f59e0b',   # Phú Thọ: Cam Hổ Phách rực rỡ
            9: '#ec4899',   # Lai Châu: Hồng Phong Lan kiêu sa
            10: '#a855f7',  # Điện Biên: Tím Thạch Anh tươi sáng
            11: '#f97316',  # Sơn La: Cam Hoàng Hôn rực lửa
        }
    },
    {
        'id': 'vung-2',
        'key': 'dbsh',
        'name': 'Đồng bằng sông Hồng',
        'short': 'Đồng bằng sông Hồng',
        'desc': 'Gồm 6 tỉnh thành: Hà Nội, Hải Phòng, Quảng Ninh, Bắc Ninh, Hưng Yên, Ninh Bình.',
        'theme': '#1d5a84',
        'accent': '#0284c7',
        'province_ids': [3, 34, 30, 7, 33, 32],
        'base_colors': {
            3: '#5b89aa',   # Hà Nội
            7: '#6e9bbd',   # Bắc Ninh
            30: '#4d7b9c',  # Quảng Ninh
            32: '#6491b2',  # Ninh Bình
            33: '#77a4c6',  # Hưng Yên
            34: '#437090',  # Hải Phòng
        },
        'lit_colors': {
            3: '#ef4444',   # Hà Nội: Đỏ Cờ rực sáng hào hoa
            7: '#f59e0b',   # Bắc Ninh: Vàng Tươi Quan Họ
            30: '#06b6d4',  # Quảng Ninh: Xanh Ngọc Biển Vịnh Hạ Long
            32: '#10b981',  # Ninh Bình: Xanh Non Cố Đô Tràng An
            33: '#8b5cf6',  # Hưng Yên: Tím Sen Nhãn Lồng Phố Hiến
            34: '#0284c7',  # Hải Phòng: Xanh Dương Thành Phố Cảng
        }
    },
    {
        'id': 'vung-3',
        'key': 'btb',
        'name': 'Bắc Trung Bộ',
        'short': 'Bắc Trung Bộ',
        'desc': 'Gồm 5 tỉnh thành: Huế, Thanh Hóa, Nghệ An, Hà Tĩnh, Quảng Trị.',
        'theme': '#8c581e',
        'accent': '#f59e0b',
        'province_ids': [16, 12, 13, 14, 15],
        'base_colors': {
            12: '#b88950',  # Thanh Hóa
            13: '#c7975d',  # Nghệ An
            14: '#a97940',  # Hà Tĩnh
            15: '#b88950',  # Quảng Trị
            16: '#9d6d34',  # Huế
        },
        'lit_colors': {
            12: '#f97316',  # Thanh Hóa: Cam Cháy Lam Kinh
            13: '#eab308',  # Nghệ An: Vàng Nắng Chói Lọi Quê Bác
            14: '#06b6d4',  # Hà Tĩnh: Xanh Biển Ngọc Thiên Cầm
            15: '#ef4444',  # Quảng Trị: Đỏ Thắm Thành Cổ Anh Hùng
            16: '#a855f7',  # Huế: Tím Cố Đô Mộng Mơ
        }
    },
    {
        'id': 'vung-4',
        'key': 'dhntbtn',
        'name': 'Duyên hải Nam Trung Bộ và Tây Nguyên',
        'short': 'Nam Trung Bộ & Tây Nguyên',
        'desc': 'Gồm 6 tỉnh thành và 2 quần đảo: Đà Nẵng, Quảng Ngãi, Gia Lai, Đắk Lắk, Khánh Hòa, Lâm Đồng, Hoàng Sa, Trường Sa.',
        'theme': '#943d31',
        'accent': '#f43f5e',
        'province_ids': [17, 28, 27, 25, 26, 29, 35, 36],
        'base_colors': {
            17: '#bc695e',  # Đà Nẵng
            25: '#ae5a50',  # Đắk Lắk
            26: '#c9776c',  # Khánh Hòa
            27: '#a04d43',  # Gia Lai
            28: '#b66358',  # Quảng Ngãi
            29: '#bf6c61',  # Lâm Đồng
            35: '#b57a3e',  # Hoàng Sa: San hô Bãi Cát Vàng
            36: '#3b82c4',  # Trường Sa: Xanh thẳm Biển Đông
        },
        'lit_colors': {
            17: '#0284c7',  # Đà Nẵng: Xanh Biển Mỹ Khê Rực Sáng
            25: '#d97706',  # Đắk Lắk: Nâu Vàng Đất Đỏ Cà Phê
            26: '#14b8a6',  # Khánh Hòa: Xanh Ngọc Biển Trầm Hương
            27: '#16a34a',  # Gia Lai: Xanh Thẫm Rừng Đại Ngàn
            28: '#f43f5e',  # Quảng Ngãi: Đỏ San Hô Đảo Lý Sơn
            29: '#a855f7',  # Lâm Đồng: Tím Ngàn Hoa Xứ Sương Mù
            35: '#f59e0b',  # Hoàng Sa: Vàng Hổ Phách rực rỡ
            36: '#06b6d4',  # Trường Sa: Xanh Ngọc Biển Đảo Trường Sa
        }
    },
    {
        'id': 'vung-5',
        'key': 'dnb',
        'name': 'Đông Nam Bộ',
        'short': 'Đông Nam Bộ & Miền Tây',
        'desc': 'Gồm 8 tỉnh thành: TP.Hồ Chí Minh, Đồng Nai, Tây Ninh, TP.Cần Thơ, An Giang, Vĩnh Long, Cà Mau, Đồng Tháp.',
        'theme': '#60397d',
        'accent': '#8b5cf6',
        'province_ids': [19, 18, 21, 22, 23, 20, 24, 31],
        'base_colors': {
            18: '#8d6ba7',  # Đồng Nai
            19: '#7f5c9a',  # TP.Hồ Chí Minh
            20: '#9977b3',  # Vĩnh Long
            21: '#8462a0',  # Tây Ninh
            22: '#74528f',  # Cần Thơ
            23: '#916fa9',  # An Giang
            24: '#684583',  # Cà Mau
            31: '#9f7db8',  # Đồng Tháp
        },
        'lit_colors': {
            18: '#f59e0b',  # Đồng Nai: Vàng Cam Công Nghiệp Rực Sáng
            19: '#e11d48',  # TP.Hồ Chí Minh: Đỏ Hồng Đô Thị Sôi Động
            20: '#8b5cf6',  # Vĩnh Long: Tím Hoa Lục Bình Phù Sa
            21: '#10b981',  # Tây Ninh: Xanh Non Núi Bà Đen
            22: '#0284c7',  # Cần Thơ: Xanh Dương Sông Nước Tây Đô
            23: '#f97316',  # An Giang: Cam Đất Bảy Núi Thất Sơn
            24: '#0d9488',  # Cà Mau: Xanh Ngập Mặn Rừng Tràm Đất Mũi
            31: '#ec4899',  # Đồng Tháp: Hồng Cánh Sen Tháp Mười
        }
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
    f'<span class="row-dot" style="background:{p["litColor"]}" title="Màu phát sáng: {p["litColor"]}"></span>'
    f'<span class="row-number">{p["id"]:02}</span>'
    f'<span class="row-name">{html.escape(p["short"])}</span>'
    f'<span class="row-region">{html.escape(p["regionShort"])}</span>'
    '<span class="row-arrow" aria-hidden="true">↗</span></button>'
    for p in sorted(provinces, key=lambda p: p['short'].casefold())
)
output = output.replace('<!-- PROVINCE_LIST -->', fallback_rows)

assert all(token not in output for token in ('<!-- PROVINCE_PATHS -->', '/* PROVINCE_DATA */', '/* REGION_DATA */', '<!-- PROVINCE_LIST -->', '<!-- REGION_PILLS -->'))
assert len(provinces) == 36
assert len(regions_data) == 5

(ROOT / 'dist').mkdir(exist_ok=True)
(ROOT / 'dist' / 'index.html').write_text(output, encoding='utf-8')
(ROOT / 'index.html').write_text(output, encoding='utf-8')
print(f'Built {len(provinces)} provinces across {len(regions_data)} regions -> dist/index.html & index.html')
