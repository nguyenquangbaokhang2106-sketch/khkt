# -*- coding: utf-8 -*-
"""Generate comprehensive dataset for all 34 provinces + 2 archipelagos (Hoàng Sa, Trường Sa) from user JSON files."""
import json, re, html, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / 'data'

# Read text files
tong_hop_text = (DATA / '_MConverter.eu_Tong_hop_34_tinh_thanh_Viet_Nam_2025.json').read_text(encoding='utf-8')
lien_ket_text = (DATA / '_MConverter.eu_Lien_ket_hinh_anh_34_tinh_thanh.json').read_text(encoding='utf-8')
hoang_truong_sa_file = DATA / '_MConverter.eu_Tong_hop_Hoang_Sa_Truong_Sa_chi_tiet_2026.json'
hoang_truong_sa_text = hoang_truong_sa_file.read_text(encoding='utf-8') if hoang_truong_sa_file.exists() else ""

# Read existing 9 provinces detail to keep Tuyen Quang & TDMNBB photos
from create_detail_data import provinces_detail as existing_detail

# CSV mapping
import csv
csv_rows = list(csv.DictReader((DATA / 'Danh_sach_34_tinh_thanh.csv').open(encoding='utf-8-sig')))
stt_to_meta = {}
name_to_stt = {}
for r in csv_rows:
    idx = int(r['stt'])
    name = r['tinh_thanh']
    stt_to_meta[idx] = r
    short = name.replace('Thành phố ', '').replace('Quần đảo ', '').replace('Đặc khu ', '').replace('Huyện ', '')
    name_to_stt[name.lower()] = idx
    name_to_stt[short.lower()] = idx

# 5 Regions definition
REGIONS_MAP = {
    # Vung 1: Trung Du mien nui Bac Bo
    1: 'vung-1', 2: 'vung-1', 4: 'vung-1', 5: 'vung-1', 6: 'vung-1', 8: 'vung-1', 9: 'vung-1', 10: 'vung-1', 11: 'vung-1',
    # Vung 2: Dong bang song Hong
    3: 'vung-2', 7: 'vung-2', 30: 'vung-2', 32: 'vung-2', 33: 'vung-2', 34: 'vung-2',
    # Vung 3: Bac Trung Bo
    12: 'vung-3', 13: 'vung-3', 14: 'vung-3', 15: 'vung-3', 16: 'vung-3',
    # Vung 4: Duyen hai Nam Trung Bo va Tay Nguyen (+ Hoang Sa & Truong Sa)
    17: 'vung-4', 25: 'vung-4', 26: 'vung-4', 27: 'vung-4', 28: 'vung-4', 29: 'vung-4', 35: 'vung-4', 36: 'vung-4',
    # Vung 5: Dong Nam Bo
    18: 'vung-5', 19: 'vung-5', 20: 'vung-5', 21: 'vung-5', 22: 'vung-5', 23: 'vung-5', 24: 'vung-5', 31: 'vung-5'
}

REGION_NAMES = {
    'vung-1': 'Trung Du miền núi Bắc Bộ',
    'vung-2': 'Đồng bằng sông Hồng',
    'vung-3': 'Bắc Trung Bộ',
    'vung-4': 'Duyên hải Nam Trung Bộ và Tây Nguyên',
    'vung-5': 'Đông Nam Bộ'
}

PROVINCE_COLORS = {
    1: '#3b82f6', 2: '#06b6d4', 3: '#ef4444', 4: '#10b981', 5: '#22c55e',
    6: '#eab308', 7: '#f59e0b', 8: '#f59e0b', 9: '#ec4899', 10: '#a855f7',
    11: '#f97316', 12: '#f97316', 13: '#eab308', 14: '#06b6d4', 15: '#ef4444',
    16: '#a855f7', 17: '#0284c7', 18: '#f59e0b', 19: '#e11d48', 20: '#8b5cf6',
    21: '#10b981', 22: '#0284c7', 23: '#f97316', 24: '#0d9488', 25: '#d97706',
    26: '#14b8a6', 27: '#16a34a', 28: '#f43f5e', 29: '#a855f7', 30: '#06b6d4',
    31: '#ec4899', 32: '#10b981', 33: '#8b5cf6', 34: '#0284c7',
    35: '#f59e0b', # Hoàng Sa: Vàng Hổ Phách Bãi Cát Vàng
    36: '#06b6d4'  # Trường Sa: Xanh Ngọc Biển Sáng
}

# Parse Tong hop sections
raw_blocks = re.split(r'={20,}\s*\n', tong_hop_text)
parsed_tong_hop = {}

for i in range(1, len(raw_blocks), 2):
    header = raw_blocks[i].strip()
    body = raw_blocks[i+1].strip() if i+1 < len(raw_blocks) else ''
    m = re.match(r'^(\d{2})\.\s*([^\n]+)', header)
    if not m:
        continue
    num = int(m.group(1))
    raw_name = m.group(2).strip()
    
    # Extract fields from body
    def find_field(pattern, text, default=''):
        fm = re.search(pattern, text, re.MULTILINE)
        return fm.group(1).strip() if fm else default
    
    p_name = find_field(r'^Tên:\s*([^\n]+)', body, raw_name.title())
    p_type = find_field(r'^Loại hình:\s*([^\n]+)', body, 'Tỉnh')
    p_formed = find_field(r'^Địa giới hình thành từ:\s*([^\n]+)', body, '')
    p_coords = find_field(r'^Tọa độ tham khảo:\s*([^\n]+)', body, '')
    p_pop = find_field(r'^Dân số tham chiếu:\s*([^\n]+)', body, '')
    p_area = find_field(r'^Diện tích tự nhiên:\s*([^\n]+)', body, '')
    p_admin = find_field(r'^Số phường, xã, đặc khu:\s*([^\n]+)', body, '')
    
    # Economy block
    eco_m = re.search(r'Cơ cấu kinh tế \(các ngành nổi bật\):\s*\n(.*?)(?=\n\n|\nDu lịch|$)', body, re.DOTALL)
    p_economy = eco_m.group(1).strip() if eco_m else ''
    
    # Tourism block
    tour_m = re.search(r'Du lịch – đặc điểm địa phương:\s*\n(.*?)(?=\n\n|\nDanh lam|$)', body, re.DOTALL)
    p_tourism = tour_m.group(1).strip() if tour_m else ''
    
    # Landmarks block
    land_m = re.search(r'Danh lam thắng cảnh / di tích tiêu biểu:\s*\n(.*?)(?=\n\nMột vài fact|\nHình ảnh|$)', body, re.DOTALL)
    landmarks_text = land_m.group(1).strip() if land_m else ''
    landmarks = []
    for item in re.split(r'\n-\s*', '\n' + landmarks_text):
        item = item.strip()
        if not item: continue
        parts = item.split(':', 1)
        if len(parts) == 2:
            landmarks.append({'title': parts[0].strip(), 'desc': parts[1].strip()})
        else:
            landmarks.append({'title': item[:40], 'desc': item})

    # Facts block
    fact_m = re.search(r'Một vài fact địa phương:\s*\n(.*?)(?=\nHình ảnh|$)', body, re.DOTALL)
    p_facts = fact_m.group(1).strip() if fact_m else ''
    
    # Search links
    g_img = find_field(r'Google Images:\s*([^\n]+)', body, '')
    wm_img = find_field(r'Wikimedia Commons:\s*([^\n]+)', body, '')
    
    parsed_tong_hop[p_name.lower()] = {
        'num': num,
        'name': p_name,
        'type': p_type,
        'formed': p_formed,
        'coords': p_coords,
        'population': p_pop,
        'area': p_area,
        'admin': p_admin,
        'economy': p_economy,
        'tourism': p_tourism,
        'landmarks': landmarks,
        'facts': p_facts,
        'google_img': g_img,
        'wikimedia_img': wm_img
    }

# Read Bac Trung Bo docx structure to associate btb images
btb_landmarks = {
    16: [ # Hue
        {'title': 'Quần thể di tích Cố đô Huế', 'image': 'assets/images/btb_image1.jpeg', 'desc': 'Quần thể kiến trúc Cố đô Huế do triều Nguyễn xây dựng, Di sản Văn hoá Thế giới UNESCO công nhận năm 1993, di tích quốc gia đặc biệt quan trọng.'},
        {'title': 'Hệ đầm phá Tam Giang – Cầu Hai', 'image': 'assets/images/btb_image2.jpeg', 'desc': 'Hệ đầm phá nước lợ ven biển tiêu biểu trải dài 68 km, hệ sinh thái phong phú bậc nhất Đông Nam Á.'},
        {'title': 'Hoàng hôn trên phá Tam Giang', 'image': 'assets/images/btb_image3.jpeg', 'desc': 'Cảnh sắc mây nước thơ mộng, không gian sinh kế nuôi trồng thủy sản và du lịch cộng đồng độc đáo.'},
        {'title': 'Cảng Chân Mây & Vịnh Lăng Cô', 'image': 'assets/images/btb_image4.jpeg', 'desc': 'Cảng biển nước sâu chiến lược miền Trung trong Khu kinh tế Chân Mây – Lăng Cô, đón tàu du lịch quốc tế.'}
    ],
    12: [ # Thanh Hoa
        {'title': 'Di sản Thế giới Thành nhà Hồ', 'image': 'assets/images/btb_image6.png', 'desc': 'Kinh đô Đại Ngu thời nhà Hồ (năm 1397) xây bằng các phiến đá xanh nguyên khối khổng lồ, Di sản Văn hóa Thế giới UNESCO.'},
        {'title': 'Kiến trúc vòm đá cổ Thành nhà Hồ', 'image': 'assets/images/btb_image7.jpeg', 'desc': 'Kiến trúc vòm đá cuốn độc nhất vô nhị tồn tại bền vững hơn 600 năm lịch sử.'},
        {'title': 'Bãi biển Sầm Sơn', 'image': 'assets/images/btb_image8.jpeg', 'desc': 'Bãi cát thoai thoải trải dài 6 km với sóng mạnh trong xanh, trung tâm nghỉ mát nổi tiếng từ năm 1906.'},
        {'title': 'Tổ hợp Lọc hóa dầu Nghi Sơn', 'image': 'assets/images/btb_image9.jpeg', 'desc': 'Công trình năng lượng trọng điểm quốc gia, công suất 10 triệu tấn dầu thô/năm tại Khu kinh tế Nghi Sơn.'}
    ],
    13: [ # Nghe An
        {'title': 'Khu di tích Quốc gia đặc biệt Kim Liên', 'image': 'assets/images/btb_image12.jpeg', 'desc': 'Quê nội Làng Sen và quê ngoại Hoàng Trù của Chủ tịch Hồ Chí Minh, nơi lưu giữ kỷ niệm tuổi thơ Người.'},
        {'title': 'Nhà tranh quê Bác tại Làng Sen', 'image': 'assets/images/btb_image13.jpeg', 'desc': 'Ngôi nhà lá đơn sơ dưới rặng cau, điểm về nguồn thiêng liêng của hàng triệu trái tim người Việt.'},
        {'title': 'Khu kinh tế Đông Nam Nghệ An', 'image': 'assets/images/btb_image14.jpeg', 'desc': 'Động lực phát triển công nghiệp đa ngành, logistics, cảng biển nước sâu quy mô hơn 100.000 ha.'},
        {'title': 'Bãi biển Cửa Lò', 'image': 'assets/images/btb_image15.jpeg', 'desc': 'Bãi biển cát trắng mịn dài 12 km, điểm nghỉ dưỡng hấp dẫn nhìn ra đảo Ngư và đảo Lan Châu.'}
    ],
    14: [ # Ha Tinh
        {'title': 'Di tích quốc gia đặc biệt Ngã ba Đồng Lộc', 'image': 'assets/images/btb_image16.jpeg', 'desc': 'Nơi 10 nữ thanh niên xung phong anh dũng hy sinh ngày 24/7/1968, biểu tượng bất tử của lòng quả cảm.'},
        {'title': 'Tượng đài và mộ 10 nữ liệt sĩ Đồng Lộc', 'image': 'assets/images/btb_image17.jpeg', 'desc': 'Khu tưởng niệm trang nghiêm giữa thung lũng Trường Sơn, ngọn lửa tri ân muôn đời.'},
        {'title': 'Khu kinh tế và Cảng nước sâu Vũng Áng', 'image': 'assets/images/btb_image18.jpeg', 'desc': 'Cảng biển quốc tế có khả năng tiếp nhận tàu trọng tải đến 100.000 DWT, trung tâm công nghiệp luyện kim và điện năng.'},
        {'title': 'Vườn Quốc gia Vũ Quang – Vườn Di sản ASEAN', 'image': 'assets/images/btb_image19.jpeg', 'desc': 'Kho báu xanh giữa đại ngàn Trường Sơn với nhiều loài động thực vật quý hiếm như Sao La, Mang Lớn.'}
    ],
    15: [ # Quang Tri
        {'title': 'Di tích quốc gia đặc biệt Thành cổ Quảng Trị', 'image': 'assets/images/btb_image21.jpeg', 'desc': 'Chứng tích 81 ngày đêm rực lửa mùa hè năm 1972, đài tưởng niệm tri ân những người con anh dũng vì độc lập.'},
        {'title': 'Địa đạo Vịnh Mốc trong lòng đất lửa', 'image': 'assets/images/btb_image22.jpeg', 'desc': 'Kỳ tích làng hầm quân dân sự sâu trong lòng đất bờ bắc sông Bến Hải, tồn tại kiên cường suốt 1965-1972.'},
        {'title': 'Cánh đồng Điện gió miền Tây Quảng Trị', 'image': 'assets/images/btb_image23.jpeg', 'desc': 'Tiềm năng năng lượng tái tạo sạch vươn tầm, biến gió ngàn thành nguồn năng lượng phát triển kinh tế.'},
        {'title': 'Vườn quốc gia Phong Nha – Kẻ Bàng', 'image': 'assets/images/btb_image26.jpeg', 'desc': 'Di sản Thiên nhiên Thế giới UNESCO với vương quốc hang động kỳ vĩ Sơn Đoòng, Phong Nha, Thiên Đường.'}
    ]
}

# Famous landmarks keywords for other regions to build beautiful cards
REGION_LANDMARK_CARDS = {
    # Dong bang song Hong
    3: [ # Ha Noi
        {'title': 'Hoàng thành Thăng Long', 'desc': 'Di sản văn hóa thế giới UNESCO, trung tâm quyền lực chính trị qua 13 thế kỷ liên tục từ thời Lý, Trần, Lê đến thời đại Hồ Chí Minh.'},
        {'title': 'Văn Miếu – Quốc Tử Giám', 'desc': 'Trường đại học đầu tiên của Việt Nam, biểu tượng truyền thống hiếu học và trọng dụng nhân tài của dân tộc.'},
        {'title': 'Khu phố cổ Hà Nội & Hồ Hoàn Kiếm', 'desc': 'Trái tim ngàn năm văn hiến với Tháp Rùa cổ kính, cầu Thê Húc, đền Ngọc Sơn và 36 phố phường rêu phong nhộn nhịp.'}
    ],
    34: [ # Hai Phong
        {'title': 'Quần đảo Cát Bà & Vịnh Lan Hạ', 'desc': 'Khu dự trữ sinh quyển thế giới và Di sản Thiên nhiên Thế giới UNESCO, vịnh biển thơ mộng với hàng trăm hòn đảo đá vôi kỳ thú.'},
        {'title': 'Thành phố Cảng & Hoa phượng đỏ', 'desc': 'Cửa chính ra biển của miền Bắc, trung tâm logistics cảng nước sâu quốc tế Lạch Huyện hiện đại.'}
    ],
    30: [ # Quang Ninh
        {'title': 'Vịnh Hạ Long – Kỳ quan thiên nhiên thế giới', 'desc': 'Di sản Thiên nhiên Thế giới UNESCO với hàng nghìn đảo đá vôi nhô lên từ làn nước màu ngọc bích tuyệt mỹ.'},
        {'title': 'Non thiêng Yên Tử', 'desc': 'Cội nguồn Thiền phái Trúc Lâm do Phật hoàng Trần Nhân Tông sáng lập, trung tâm Phật giáo danh tiếng.'},
        {'title': 'Đảo ngọc Cô Tô & Trà Cổ', 'desc': 'Bãi cát trắng mịn nguyên sơ, mũi Sa Vĩ nơi nét vẽ đầu tiên của bản đồ Tổ quốc.'}
    ],
    7: [ # Bac Ninh
        {'title': 'Dân ca Quan họ Bắc Ninh', 'desc': 'Di sản văn hóa phi vật thể đại diện của nhân loại được UNESCO vinh danh năm 2009, nét tinh hoa văn hóa Kinh Bắc.'},
        {'title': 'Chùa Bút Tháp & Chùa Dâu', 'desc': 'Các ngôi chùa cổ linh thiêng bậc nhất, nơi lưu giữ bảo vật quốc gia tượng Phật Bà Quan Âm nghìn mắt nghìn tay.'}
    ],
    33: [ # Hung Yen
        {'title': 'Quần thể di tích Phố Hiến', 'desc': 'Thương cảng quốc tế hưng thịnh thế kỷ 16-17 với câu ca dao lưu truyền: "Thứ nhất Kinh Kỳ, thứ nhì Phố Hiến".'},
        {'title': 'Đặc sản Nhãn lồng & Chùa Chuông', 'desc': 'Sản vật tiến vua trứ danh cùng các di tích cổ kính đậm đặc dấu ấn châu thổ sông Hồng.'}
    ],
    32: [ # Ninh Binh
        {'title': 'Quần thể danh thắng Tràng An', 'desc': 'Di sản Thế giới kép (văn hóa và thiên nhiên) duy nhất tại Đông Nam Á, cảnh quan karst nhiệt đới ngập nước kỳ vĩ.'},
        {'title': 'Cố đô Hoa Lư & Tam Cốc Bích Động', 'desc': 'Kinh đô đầu tiên của nhà nước phong kiến trung ương tập quyền Việt Nam dưới thời Đinh, Tiền Lê.'}
    ],
    # Nam Trung Bo & Tay Nguyen
    17: [ # Da Nang
        {'title': 'Bà Nà Hills & Cầu Vàng', 'desc': 'Biểu tượng du lịch hiện đại nổi tiếng toàn cầu, đỉnh núi Chúa mát mẻ quanh năm cùng làng Pháp mộng mơ.'},
        {'title': 'Bán đảo Sơn Trà & Biển Mỹ Khê', 'desc': 'Bãi biển nằm trong top quyến rũ nhất hành tinh, rừng nguyên sinh Sơn Trà là ngôi nhà của Voọc chà vá chân nâu.'},
        {'title': 'Cầu Rồng & Sông Hàn lung linh', 'desc': 'Thành phố đáng sống với những cây cầu độc đáo, các lễ hội pháo hoa quốc tế rực rỡ.'}
    ],
    28: [ # Quang Ngai
        {'title': 'Đảo thiên đường Lý Sơn', 'desc': 'Bảo tàng sống về địa chất núi lửa biển với cổng Tò Vò, miệng núi lửa Thới Lới và di tích Đội Hoàng Sa kiêm quản Bắc Hải.'},
        {'title': 'Khu kinh tế Dung Quất', 'desc': 'Nhà máy lọc dầu đầu tiên của Việt Nam, trung tâm công nghiệp nặng ven biển năng động.'}
    ],
    27: [ # Gia Lai
        {'title': 'Biển Hồ Pleiku (Hồ T\'Nưng)', 'desc': 'Được mệnh danh là "Mắt ngọc Pleiku", dấu tích miệng núi lửa cổ đại ngút ngàn nước xanh trong biếc.'},
        {'title': 'Không gian Văn hóa Cồng chiêng', 'desc': 'Kiệt tác truyền khẩu và Di sản văn hóa phi vật thể nhân loại của UNESCO giữa đại ngàn Tây Nguyên.'}
    ],
    25: [ # Dak Lak
        {'title': 'Thủ phủ Cà phê Buôn Ma Thuột', 'desc': 'Thủ phủ cà phê Việt Nam với thương hiệu cà phê Robusta nổi danh thế giới, bảo tàng thế giới cà phê.'},
        {'title': 'Hồ Lắk & Thác Dray Nur', 'desc': 'Hồ nước ngọt tự nhiên lớn nhất Tây Nguyên, thác nước Dray Nur - Dray Sáp hùng vĩ gắn với sử thi hào hùng.'}
    ],
    26: [ # Khanh Hoa
        {'title': 'Vịnh Nha Trang & Tháp Bà Ponagar', 'desc': 'Một trong những vịnh biển đẹp nhất thế giới, quần thể đền tháp Chăm Pa cổ kính trên đồi Cù Lao.'},
        {'title': 'Đảo Yến & Bán đảo Cam Ranh', 'desc': 'Xứ sở Trầm hương và Yến sào trứ danh, vịnh biển nước sâu tự nhiên hàng đầu thế giới.'}
    ],
    29: [ # Lam Dong
        {'title': 'Thành phố Festival Hoa Đà Lạt', 'desc': 'Thành phố sương mù ngàn hoa, thung lũng Tình Yêu, hồ Xuân Hương và khí hậu ôn đới quanh năm.'},
        {'title': 'Đỉnh Langbiang huyền thoại', 'desc': 'Nóc nhà Đà Lạt với chuyện tình chàng K\'lang và nàng H\'biang, rừng thông đại ngàn bát ngát.'}
    ],
    # Dong Nam Bo
    19: [ # TP. Ho Chi Minh
        {'title': 'Dinh Độc Lập & Bưu điện Trung tâm', 'desc': 'Chứng tích lịch sử thống nhất đất nước, công trình kiến trúc Pháp cổ kính biểu tượng giữa trung tâm hoa lệ.'},
        {'title': 'Địa đạo Củ Chi – Đất thép thành đồng', 'desc': 'Mê cung hầm ngầm kỳ vĩ dưới lòng đất dài hơn 250 km, minh chứng tinh thần bất khuất trong kháng chiến.'},
        {'title': 'Đô thị sông Sài Gòn & Trung tâm kinh tế', 'desc': 'Đầu tàu kinh tế, tài chính, đổi mới sáng tạo và giao thương quốc tế lớn nhất cả nước.'}
    ],
    18: [ # Dong Nai
        {'title': 'Vườn quốc gia Cát Tiên', 'desc': 'Khu Dự trữ Sinh quyển Thế giới UNESCO, rừng mưa nhiệt đới nguyên sinh với hệ động thực vật vô cùng phong phú.'},
        {'title': 'Thủ phủ công nghiệp & Sân bay Long Thành', 'desc': 'Trung tâm công nghiệp chế biến, siêu dự án Cảng hàng không quốc tế Long Thành cửa ngõ bầu trời.'}
    ],
    21: [ # Tay Ninh
        {'title': 'Quần thể núi Bà Đen – Nóc nhà Nam Bộ', 'desc': 'Ngọn núi cao nhất miền Nam (986 m), trung tâm hành hương tâm linh với tượng Phật Bà bằng đồng cao nhất châu Á.'},
        {'title': 'Tòa thánh Tây Ninh', 'desc': 'Tổ đình đạo Cao Đài với kiến trúc độc đáo kết hợp tinh hoa tôn giáo phương Đông và phương Tây.'}
    ],
    22: [ # Can Tho
        {'title': 'Chợ nổi Cái Răng', 'desc': 'Di sản văn hóa phi vật thể quốc gia, nét sinh hoạt thương hồ độc đáo bậc nhất đồng bằng sông Cửu Long.'},
        {'title': 'Bến Ninh Kiều & Đô thị Tây Đô', 'desc': 'Trung tâm kinh tế, giáo dục, văn hóa của miền Tây Nam Bộ bên dòng sông Hậu hiền hòa.'}
    ],
    23: [ # An Giang
        {'title': 'Miếu Bà Chúa Xứ Núi Sam & Vùng Bảy Núi', 'desc': 'Lễ hội Vía Bà Chúa Xứ Núi Sam di sản văn hóa phi vật thể nhân loại, địa hình Thất Sơn huyền bí.'},
        {'title': 'Rừng tràm Trà Sư', 'desc': 'Hệ sinh thái ngập nước tiêu biểu mùa nước nổi, thảm bèo xanh mướt chim muông ríu rít.'}
    ],
    20: [ # Vinh Long
        {'title': 'Cầu Mỹ Thuận & Đất cù lao miệt vườn', 'desc': 'Cây cầu dây văng lịch sử bắc qua sông Tiền, các cù lao trĩu quả chôm chôm, sầu riêng, bưởi Năm Roi.'},
        {'title': 'Làng gốm đỏ Mang Thít', 'desc': 'Vương quốc gốm đỏ hơn 100 năm tuổi với hàng nghìn lò gạch nung rực rỡ bên dòng sông Cổ Chiên.'}
    ],
    24: [ # Ca Mau
        {'title': 'Vườn quốc gia Mũi Cà Mau & Cột mốc tọa độ', 'desc': 'Điểm cực Nam Tổ quốc nơi mũi đất vươn ra biển, biểu tượng con tàu hướng ra đại dương.'},
        {'title': 'Rừng ngập mặn U Minh Hạ', 'desc': 'Khu Dự trữ Sinh quyển Thế giới, cánh rừng tràm bạt ngàn với nghề gác kèo ong lấy mật độc đáo.'}
    ],
    31: [ # Dong Thap
        {'title': 'Vườn quốc gia Tràm Chim', 'desc': 'Khu Ramsar thế giới, xứ sở của loài Sếu đầu đỏ quý hiếm và bạt ngàn sen hồng ngát hương.'},
        {'title': 'Làng hoa kiểng Sa Đéc', 'desc': 'Thủ phủ hoa kiểng trăm năm tuổi miền Tây, cung cấp hoa xuân rực rỡ muôn màu cho cả nước.'}
    ]
}

# Load authentic landmark images extracted from ds.docx / vertopal.com_ds (1)
landmark_img_file = DATA / 'landmark_mapping.json'
landmark_img_map = json.loads(landmark_img_file.read_text(encoding='utf-8')) if landmark_img_file.exists() else {}

def normalize_key(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

norm_landmark_map = {normalize_key(k): v for k, v in landmark_img_map.items()}

def get_landmark_image(title, fallback):
    nt = normalize_key(title)
    if nt in norm_landmark_map:
        return norm_landmark_map[nt]
    for k, v in norm_landmark_map.items():
        if nt in k or k in nt:
            return v
    words = [w for w in nt.split() if len(w) > 3]
    for k, v in norm_landmark_map.items():
        if sum(1 for w in words if w in k) >= 2:
            return v
    return fallback

# Now, compile all 34 provinces + 2 island territories
final_dataset = {}

for row in csv_rows:
    idx = int(row['stt'])
    name = row['tinh_thanh']
    short = name.replace('Thành phố ', '').replace('Quần đảo ', '')
    slug = re.sub(r'[^a-z0-9]+', '-', row['tep_svg'].replace('.svg', '').replace('tinh_', ''))
    reg_id = REGIONS_MAP[idx]
    reg_name = REGION_NAMES[reg_id]
    lit_color = PROVINCE_COLORS[idx]

    # SPECIAL HANDLING FOR HOANG SA (ID 35)
    if idx == 35:
        final_dataset[35] = {
            'id': 35,
            'name': 'Đặc khu Hoàng Sa (Quần đảo Hoàng Sa)',
            'short': 'Hoàng Sa',
            'slug': 'hoang-sa',
            'regionId': 'vung-4',
            'regionName': 'Duyên hải Nam Trung Bộ và Tây Nguyên',
            'silhouette': 'assets/silhouettes/35_hoang_sa.png',
            'litColor': '#f59e0b',
            'quote': 'Chủ quyền thiêng liêng nơi đầu sóng · Hào khí Hùng binh Hoàng Sa · Cương vực ngàn đời của Tổ quốc',
            'overview': 'Quần đảo Hoàng Sa (Paracel Islands, trong thư tịch cổ còn gọi là Bãi Cát Vàng) là một quần đảo san hô gồm khoảng 37 đảo, đá, cồn cát, bãi cạn và rạn san hô trên vùng biển rộng khoảng 30.000 km² ở phía đông miền Trung Việt Nam. Theo tổ chức hành chính Việt Nam sau sắp xếp năm 2025 (Nghị quyết 1659/NQ-UBTVQH15), đây là Đặc khu Hoàng Sa trực thuộc thành phố Đà Nẵng. Việt Nam khẳng định có đầy đủ cơ sở lịch sử và pháp lý vững chắc khẳng định chủ quyền không thể chối cãi đối với quần đảo Hoàng Sa theo luật pháp quốc tế.',
            'stats': [
                {'label': 'Vùng biển', 'value': '~30.000 km²', 'sub': 'Phần nổi ~10 km² (37 đảo, đá, rạn)'},
                {'label': 'Hành chính', 'value': '01 Đặc khu', 'sub': 'Đặc khu Hoàng Sa, TP. Đà Nẵng'},
                {'label': 'Dân số', 'value': 'Lực lượng nhiệm vụ', 'sub': 'Ngư dân bám biển & nhân sự công tác'},
                {'label': 'Tọa độ cực', 'value': '15°44′B – 17°06′B', 'sub': 'Kinh độ: 111°11′Đ – 112°53′Đ'}
            ],
            'sections': [
                {
                    'title': 'Vị trí địa lý, Tên gọi & Cấu trúc địa hình',
                    'icon': 'geo',
                    'content': [
                        'Tên gọi: Quần đảo Hoàng Sa (tên quốc tế: Paracel Islands, sử liệu cổ Việt Nam ghi chép là "Bãi Cát Vàng"). Vị trí nằm ở phía đông đất liền miền Trung Việt Nam, thuộc Biển Đông, án ngữ các trục đường hàng hải quốc tế huyết mạch.',
                        'Tọa độ các điểm cực: Cực Bắc (đảo Đá Bắc: 17°06′00″B, 111°30′08″Đ); Cực Nam (bãi ngầm Ốc Tai Voi: 15°44′02″B, 112°14′01″Đ); Cực Đông (bãi cạn Gò Nổi: 16°49′07″B, 112°53′04″Đ); Cực Tây (đảo Tri Tôn: 15°47′02″B, 111°11′08″Đ).',
                        'Cấu trúc: Quần đảo gồm khoảng 37 đảo, đá, bãi cạn, bãi ngầm chia làm hai nhóm chính: Cụm Lưỡi Liềm (Trăng Khuyết) ở phía tây (Hoàng Sa, Hữu Nhật, Quang Ảnh, Quang Hòa, Duy Mộng, Tri Tôn...) và Cụm An Vĩnh ở phía đông bắc (Phú Lâm, đảo Cây, Linh Côn, bãi Bông Bay...).'
                    ]
                },
                {
                    'title': 'Chủ quyền lịch sử & Căn cứ pháp lý vững chắc',
                    'icon': 'flag',
                    'content': [
                        'Lập trường Việt Nam: Việt Nam có đầy đủ cơ sở lịch sử và pháp lý vững chắc khẳng định chủ quyền đối với quần đảo Hoàng Sa. Thư tịch cổ, bản đồ cổ, Châu bản triều Nguyễn ghi chép hoạt động kiểm soát, tuần tra, khai thác liên tục của Hải đội Hoàng Sa và Đội Bắc Hải từ nhiều thế kỷ.',
                        'Pháp lý quốc tế: Nhà nước Việt Nam qua các thời kỳ lịch sử đã xác lập và thực thi chủ quyền một cách hòa bình, thực chất, liên tục và phù hợp với luật pháp quốc tế, bao gồm Công ước Liên Hợp Quốc về Luật Biển 1982 (UNCLOS).',
                        'Tình trạng thực tế: Trung Quốc dùng vũ lực chiếm đóng trái phép toàn bộ quần đảo Hoàng Sa từ năm 1974 sau cuộc xung đột quân sự với lực lượng quân đội Việt Nam Cộng hòa. Việt Nam liên tục lên tiếng phản đối và kiên quyết khẳng định chủ quyền không thể chối cãi.'
                    ]
                },
                {
                    'title': 'An ninh – Quốc phòng & Diễn biến Biển Đông (Cập nhật 2026)',
                    'icon': 'shield',
                    'content': [
                        'Ý nghĩa phòng thủ: Hoàng Sa giữ vai trò tiền tiêu đặc biệt trọng yếu đối với việc kiểm soát, quan sát, bảo đảm thông tin liên lạc, an toàn hàng hải và an ninh vùng biển phía bắc Biển Đông.',
                        'Diễn biến đáng chú ý năm 2026: Việt Nam liên tục theo dõi sát sao và lên tiếng kiên quyết phản đối các hoạt động cải tạo, xây dựng trái phép của Trung Quốc tại các thực thể như rạn Hải Sâm (Antelope Reef) và đảo Ba Ba (Yagong).',
                        'Ngày 28/08/2026, Người phát ngôn Bộ Ngoại giao Việt Nam chính thức tuyên bố phản đối mọi hoạt động xâm phạm chủ quyền, yêu cầu tôn trọng luật pháp quốc tế, DOC và không làm phức tạp thêm tình hình trên Biển Đông.'
                    ]
                },
                {
                    'title': 'Vị trí chiến lược & Giá trị kinh tế biển',
                    'icon': 'trend',
                    'content': [
                        'Tuyến hàng hải huyết mạch: Nằm gần tuyến hàng hải quốc tế kết nối Đông Bắc Á với Đông Nam Á, Ấn Độ Dương và châu Âu, vận chuyển hàng tỷ thùng dầu và nguồn năng lượng LNG trọng yếu mỗi năm.',
                        'Khai thác hải sản: Vùng biển Hoàng Sa là ngư trường truyền thống của ngư dân Đà Nẵng, Quảng Ngãi, Quảng Nam với nguồn lợi hải sản phong phú ngàn đời.',
                        'Tiềm năng nghiên cứu & khoáng sản: Tiềm năng năng lượng thềm lục địa, nguồn tài nguyên khoáng sản biển sâu và giá trị vô giá cho nghiên cứu hải dương học, hệ sinh thái rạn san hô nhiệt đới.'
                    ]
                }
            ],
            'highlights': [
                {
                    'title': 'Đảo Hoàng Sa (Pattle Island) & Cụm Lưỡi Liềm',
                    'image': 'assets/images/hoang_sa_island.jpg',
                    'caption': 'Vẻ đẹp kỳ vĩ của đảo Hoàng Sa giữa biển trời xanh biếc',
                    'desc': 'Đảo san hô hình vòng cung nổi tiếng nằm ở phía tây quần đảo. Thảm thực vật xanh tươi, bãi cát trắng mịn bao quanh bởi làn nước màu ngọc bích tuyệt mỹ, là biểu tượng thiêng liêng của quần đảo Hoàng Sa.'
                },
                {
                    'title': 'Đảo Phú Lâm & Nhóm An Vĩnh',
                    'image': 'assets/images/ds_image6.jpeg',
                    'caption': 'Đảo Phú Lâm - thực thể có diện tích đất nổi lớn nhất quần đảo',
                    'desc': 'Nằm trong cụm An Vĩnh phía đông bắc, là thực thể đảo san hô có diện tích nổi tự nhiên lớn nhất (khoảng 2,1 km²), giữ vị trí quan sát chiến lược bao quát vùng biển phía bắc.'
                },
                {
                    'title': 'Đảo Tri Tôn & Ngư trường Hoàng Sa',
                    'image': 'assets/images/ds_image25.webp',
                    'caption': 'Vùng biển Lý Sơn - cửa ngõ vươn khơi hướng về Hoàng Sa',
                    'desc': 'Đảo Tri Tôn nằm ở cực tây nam của quần đảo Hoàng Sa, là ngư trường truyền thống của ngư dân các tỉnh miền Trung Việt Nam suốt nhiều thế kỷ.'
                },
                {
                    'title': 'Nhà trưng bày Hoàng Sa bên bờ biển Đà Nẵng',
                    'image': 'assets/images/ds_image16.jpeg',
                    'caption': 'Nhà trưng bày Hoàng Sa tại đường Hoàng Sa, TP. Đà Nẵng',
                    'desc': 'Công trình kiến trúc hình Con dấu chủ quyền của các vua triều Nguyễn, nơi lưu giữ hàng trăm tấm bản đồ cổ, Châu bản triều Nguyễn và hiện vật lịch sử khẳng định chủ quyền bất khả xâm phạm của Việt Nam.'
                }
            ],
            'heritage': [
                'Lễ khao lề thế lính Hoàng Sa (Di sản phi vật thể quốc gia)',
                'Di tích Đội Hoàng Sa kiêm quản Bắc Hải (Đảo Lý Sơn)',
                'Hệ thống Châu bản triều Nguyễn về chủ quyền Hoàng Sa',
                'Nhà trưng bày Hoàng Sa (Đường Hoàng Sa, TP. Đà Nẵng)'
            ],
            'links': [
                {'title': 'Cổng thông tin điện tử UBND TP. Đà Nẵng (Đặc khu Hoàng Sa)', 'url': 'https://danang.gov.vn/'},
                {'title': 'Tra cứu tư liệu Quần đảo Hoàng Sa trên Google Images', 'url': 'https://www.google.com/search?tbm=isch&q=Qu%E1%BA%A7n+%C4%91%E1%BA%A3o+Ho%C3%A0ng+Sa+Vi%E1%BB%87t+Nam'},
                {'title': 'Hình ảnh tư liệu Hoàng Sa (Paracel Islands) - Wikimedia Commons', 'url': 'https://commons.wikimedia.org/w/index.php?search=Paracel+Islands&title=Special:MediaSearch&type=image'}
            ]
        }
        continue

    # SPECIAL HANDLING FOR TRUONG SA (ID 36)
    if idx == 36:
        final_dataset[36] = {
            'id': 36,
            'name': 'Huyện Trường Sa (Quần đảo Trường Sa)',
            'short': 'Trường Sa',
            'slug': 'truong-sa',
            'regionId': 'vung-4',
            'regionName': 'Duyên hải Nam Trung Bộ và Tây Nguyên',
            'silhouette': 'assets/silhouettes/36_truong_sa.png',
            'litColor': '#06b6d4',
            'quote': 'Trường Sa vì cả nước, cả nước vì Trường Sa · Lá chắn tiền tiêu hiên ngang giữa biển trời Tổ quốc',
            'overview': 'Quần đảo Trường Sa (Spratly Islands) nằm ở phía nam Biển Đông, gồm hơn 100 đảo nổi, đảo chìm, bãi đá ngầm và rạn san hô trải rộng trên vùng biển chiến lược từ 160.000 đến 410.000 km². Theo tổ chức hành chính Việt Nam, quần đảo là huyện Trường Sa thuộc tỉnh Khánh Hòa, gồm 1 thị trấn (Trường Sa) và 2 xã đảo (Song Tử Tây, Sinh Tồn). Nơi đây giữ vị trí yết hầu về quốc phòng - an ninh trên biển, nằm sát ngã tư các tuyến hàng hải quốc tế nhộn nhịp bậc nhất thế giới. Quân và dân Trường Sa ngày đêm vững vàng nơi đầu sóng ngọn gió, bảo vệ trọn vẹn chủ quyền biển đảo thiêng liêng.',
            'stats': [
                {'label': 'Vùng biển', 'value': '160.000 – 410.000 km²', 'sub': 'Phần nổi tự nhiên ~2 - 11 km² (>100 đảo, đá, rạn)'},
                {'label': 'Hành chính', 'value': '1 thị trấn, 2 xã', 'sub': 'TT. Trường Sa, xã Song Tử Tây, xã Sinh Tồn'},
                {'label': 'Dân số', 'value': 'Quân & dân huyện đảo', 'sub': 'Cộng đồng cư dân, trường học, trạm xá, âu tàu'},
                {'label': 'Tọa độ cực', 'value': '06°30′B – 12°00′B', 'sub': 'Kinh độ: 111°30′Đ – 117°20′Đ'}
            ],
            'sections': [
                {
                    'title': 'Vị trí địa lý, Tên gọi & Hệ thống các cụm đảo',
                    'icon': 'geo',
                    'content': [
                        'Tên gọi: Quần đảo Trường Sa (tên quốc tế: Spratly Islands). Nằm ở khu vực phía nam Biển Đông, án ngữ cửa ngõ hàng hải giao thương quốc tế nối Ấn Độ Dương với Thái Bình Dương.',
                        'Hệ thống thực thể đảo: Gồm hơn 100 đảo, đá, rạn san hô, bãi cạn và bãi ngầm phân bố thành nhiều cụm: Cụm Song Tử (Song Tử Tây, Song Tử Đông), Cụm Loại Ta, Cụm Nam Yết (Nam Yết, Sơn Ca), Cụm Sinh Tồn, Cụm Trường Sa Lớn, Cụm An Bang, Cụm Tiên Nữ.',
                        'Đặc điểm tự nhiên: Khí hậu nhiệt đới gió mùa biển, nhiều nắng và gió bão khắc nghiệt. Đất đảo cát san hô cằn cỗi nhưng dưới bàn tay quân và dân ta nay đã xanh tươi bóng cây bàng vuông, mù u, tra biển.'
                    ]
                },
                {
                    'title': 'Chủ quyền thiêng liêng & Quản lý thực tế',
                    'icon': 'flag',
                    'content': [
                        'Căn cứ lịch sử và pháp lý: Việt Nam khẳng định có đầy đủ cơ sở lịch sử và chứng cứ pháp lý xác lập chủ quyền đối với quần đảo Trường Sa qua nhiều thế kỷ, thực thi quyền chủ quyền liên tục và hòa bình.',
                        'Quản lý thực tế: Hiện nay, Việt Nam đang quản lý thực tế 21 thực thể đảo, đá, rạn san hô trong quần đảo Trường Sa cùng hệ thống các Trạm Dịch vụ Kinh tế - Khoa học kỹ thuật (nhà giàn DK1) trên thềm lục địa phía Nam.',
                        'Tuân thủ pháp luật quốc tế: Việt Nam kiên quyết bảo vệ chủ quyền bằng biện pháp hòa bình, trên cơ sở luật pháp quốc tế, đặc biệt là UNCLOS 1982 và nỗ lực cùng ASEAN hoàn thiện Bộ Quy tắc Ứng xử Biển Đông (COC).'
                    ]
                },
                {
                    'title': 'Đời sống quân dân, Giáo dục & Y tế hải đảo',
                    'icon': 'users',
                    'content': [
                        'Hạ tầng dân sinh khang trang: Đảo Trường Sa Lớn, Song Tử Tây, Sinh Tồn có trường tiểu học kiên cố, các lớp học rộn rã tiếng giảng bài của thầy cô và tiếng cười trẻ thơ.',
                        'Y tế biển đảo: Bệnh xá quân dân y trên các đảo được trang bị máy móc hiện đại, hệ thống Telemedicine kết nối trực tiếp với các bệnh viện đầu ngành trong đất liền, kịp thời cấp cứu chiến sĩ và ngư dân.',
                        'Năng lượng xanh & phủ sóng 4G: Hệ thống pin năng lượng mặt trời, tua-bin gió và mạng viễn thông Viettel phủ sóng toàn huyện đảo, kết nối Trường Sa gần hơn với đất liền.'
                    ]
                },
                {
                    'title': 'Hậu cần nghề cá & Ngã tư hàng hải quốc tế',
                    'icon': 'trend',
                    'content': [
                        'Điểm tựa của ngư dân: Các âu tàu tại Trường Sa Lớn, Song Tử Tây, Sinh Tồn, Đá Tây có khả năng tiếp nhận hàng trăm tàu cá vào tránh trú bão, được cung cấp miễn phí nước ngọt, khám bệnh và hỗ trợ sửa chữa máy móc.',
                        'Hệ thống Hải đăng quốc gia: Những ngọn hải đăng sừng sững (Trường Sa Lớn, Song Tử Tây, Đá Lát, An Bang...) là "mắt thần" thắp sáng dẫn đường an toàn cho tàu thuyền quốc tế qua lại.',
                        'Tuyến vận tải huyết mạch: Nằm gần ngã tư đường hàng hải quốc tế nhộn nhịp nhất thế giới qua Biển Đông, có ý nghĩa chiến lược sống còn đối với an ninh giao thương toàn cầu.'
                    ]
                }
            ],
            'highlights': [
                {
                    'title': 'Đảo Trường Sa Lớn & Cột mốc chủ quyền',
                    'image': 'assets/images/truong_sa_island.jpg',
                    'caption': 'Cột mốc chủ quyền và quốc kỳ thiêng liêng trên đảo Trường Sa Lớn',
                    'desc': 'Trái tim của quần đảo, trung tâm hành chính huyện đảo Trường Sa với đường băng, chùa Trường Sa trang nghiêm, bờ kè đá vững chãi và cột mốc chủ quyền thiêng liêng sừng sững giữa biển khơi.'
                },
                {
                    'title': 'Hệ thống Hải đăng Trường Sa & Song Tử Tây',
                    'image': 'assets/images/ds_image21.jpeg',
                    'caption': 'Hải đăng kiên cường thắp sáng thâu đêm giữa đại dương',
                    'desc': 'Những "mắt thần" biển đảo dẫn đường cho các đoàn tàu hàng hải quốc tế và tàu cá ngư dân qua lại an toàn giữa đại dương.'
                },
                {
                    'title': 'Cây bàng vuông & Cây phong ba kiên cường',
                    'image': 'assets/images/ds_image22.jpeg',
                    'caption': 'Sức sống kiên cường nơi đầu sóng ngọn gió',
                    'desc': 'Loài cây biểu tượng cho ý chí sắt đá, bất khuất của cán bộ chiến sĩ và nhân dân bám trụ nơi tiền tiêu Tổ quốc.'
                },
                {
                    'title': 'Âu tàu và điểm tựa cứu hộ ngư dân',
                    'image': 'assets/images/ds_image25.webp',
                    'caption': 'Âu tàu tiếp tế nước ngọt và nơi tránh trú bão an toàn',
                    'desc': 'Điểm tựa vững chắc giữa trùng khơi, cung cấp nước ngọt, y tế, sửa chữa tàu thuyền miễn phí cho bà con ngư dân đánh bắt xa bờ.'
                }
            ],
            'heritage': [
                'Cột mốc chủ quyền Quốc gia Quần đảo Trường Sa',
                'Quần thể chùa Trường Sa (Trường Sa Lớn, Song Tử Tây, Sinh Tồn)',
                'Khu tưởng niệm Chiến sĩ Gạc Ma (Bán đảo Cam Ranh, Khánh Hòa)',
                'Hệ thống Nhà giàn DK1 trên thềm lục địa phía Nam Tổ quốc'
            ],
            'links': [
                {'title': 'Cổng thông tin điện tử tỉnh Khánh Hòa (Huyện Trường Sa)', 'url': 'https://khanhhoa.gov.vn/'},
                {'title': 'Tra cứu tư liệu Quần đảo Trường Sa trên Google Images', 'url': 'https://www.google.com/search?tbm=isch&q=Qu%E1%BA%A7n+%C4%91%E1%BA%A3o+Tr%C6%B0%E1%BB%9Dng+Sa+Vi%E1%BB%87t+Nam'},
                {'title': 'Hình ảnh tư liệu Trường Sa (Spratly Islands) - Wikimedia Commons', 'url': 'https://commons.wikimedia.org/w/index.php?search=Spratly+Islands&title=Special:MediaSearch&type=image'}
            ]
        }
        continue

    # Check if we have Tong hop data
    th_key = name.lower()
    if th_key not in parsed_tong_hop:
        th_key = short.lower()
    
    th_info = parsed_tong_hop.get(th_key, {})
    if not th_info:
        for k, v in parsed_tong_hop.items():
            if short.lower() in k or k in short.lower():
                th_info = v
                break
                
    # If it is one of the 9 provinces in Trung Du Bac Bo, use existing details and fix Tuyen Quang
    if idx in existing_detail:
        p_obj = dict(existing_detail[idx])
        p_obj['regionId'] = reg_id
        p_obj['regionName'] = reg_name
        p_obj['litColor'] = lit_color
        
        # FIX TUYEN QUANG IMAGES IF IDX == 5
        if idx == 5:
            p_obj['highlights'] = [
                {
                    'title': 'Cột cờ Quốc gia Lũng Cú & Cao nguyên đá',
                    'image': 'assets/images/image1.jpeg',
                    'caption': 'Cột cờ Quốc gia Lũng Cú kiêu hãnh trên đỉnh núi Rồng',
                    'desc': 'Cột cờ Quốc gia Lũng Cú là biểu tượng thiêng liêng nơi địa đầu Tổ quốc, nằm giữa cảnh quan hùng vĩ của Cao nguyên đá Đồng Văn. Nổi bật trên đỉnh núi Rồng, lá cờ đỏ sao vàng 54m² tung bay giữa núi đá trùng điệp, bản làng vùng cao và những thửa ruộng uốn lượn, khẳng định chủ quyền quốc gia vững chắc.'
                },
                {
                    'title': 'Kỳ quan Cao nguyên đá Đồng Văn',
                    'image': 'assets/images/image2.jpeg',
                    'caption': 'Cảnh sắc kỳ vĩ của Công viên Địa chất Cao nguyên đá',
                    'desc': 'Những vạt núi đá vôi xám tai mèo trải dài bất tận hòa cùng cuộc sống kiên cường của đồng bào vùng cao tạo nên một bức tranh thiên nhiên và nhân văn vô cùng độc đáo.'
                },
                {
                    'title': 'Mật ong bạc hà Mèo Vạc',
                    'image': 'assets/images/image3.jpeg',
                    'caption': 'Mật ong hoa bạc hà tự nhiên sánh vàng quyến rũ trên cao nguyên đá',
                    'desc': 'Được tạo nên từ nguồn hoa bạc hà tự nhiên mọc trên các vách đá vôi cao nguyên, mật ong có màu vàng chanh óng ánh, vị ngọt thanh mát và hương thơm thảo mộc đặc trưng hiếm có.'
                },
                {
                    'title': 'Cam sành Hàm Yên',
                    'image': 'assets/images/image4.jpeg',
                    'caption': 'Thu hoạch cam sành Hàm Yên quả vỏ sần tép vàng mọng nước',
                    'desc': 'Cam sành Hàm Yên có quả vỏ sần, tép cam vàng óng mọng nước, vị ngọt thanh pha chút chua dịu, là một trong những loại trái cây đặc sản nức tiếng cả nước.'
                }
            ]
        final_dataset[idx] = p_obj
        continue

    # Otherwise build from Tong hop & Docx & Landmarks
    p_area = th_info.get('area', '')
    p_pop = th_info.get('population', '')
    p_admin = th_info.get('admin', '')
    p_eco = th_info.get('economy', '')
    p_tour = th_info.get('tourism', '')
    p_facts = th_info.get('facts', '')
    
    # Check if BTB has images
    btb_pics = btb_landmarks.get(idx, [])
    hl_list = []
    if btb_pics:
        for pic in btb_pics:
            hl_list.append({
                'title': pic['title'],
                'image': pic['image'],
                'caption': pic['title'],
                'desc': pic['desc']
            })
    else:
        # Use regional landmark cards with authentic photos from ds.docx / vertopal.com_ds (1)
        reg_cards = REGION_LANDMARK_CARDS.get(idx, [])
        for c in reg_cards:
            fallback_sil = f'assets/silhouettes/{row["tep_png"]}'
            real_img = get_landmark_image(c['title'], fallback_sil)
            hl_list.append({
                'title': c['title'],
                'image': real_img,
                'caption': f'Địa danh tiêu biểu: {c["title"]}',
                'desc': c['desc']
            })

    # Stats list
    stats = [
        {'label': 'Diện tích', 'value': p_area or 'N/A', 'sub': 'Sau sắp xếp 2025'},
        {'label': 'Dân số', 'value': p_pop.replace(' người', '') or 'N/A', 'sub': 'Dân số tham chiếu'},
        {'label': 'Hành chính', 'value': p_admin.split(';')[0] if ';' in p_admin else p_admin, 'sub': th_info.get('type', 'Tỉnh')},
        {'label': 'Tọa độ', 'value': th_info.get('coords', '').split('(')[0].strip() or 'Việt Nam', 'sub': 'Điểm tham chiếu'}
    ]
    
    # Sections list
    sections = [
        {
            'title': 'Vị trí địa lý & Địa giới hành chính',
            'icon': 'geo',
            'content': [
                f'Địa giới hành chính: {th_info.get("formed", name)}.',
                f'Đơn vị hành chính cấp xã: {p_admin}.',
                f'Tọa độ tham khảo: {th_info.get("coords", "")}.'
            ]
        },
        {
            'title': 'Cơ cấu kinh tế nổi bật',
            'icon': 'trend',
            'content': [
                p_eco or 'Phát triển thương mại, dịch vụ, công nghiệp và nông - lâm - thủy sản thế mạnh vùng.'
            ]
        },
        {
            'title': 'Du lịch & Đặc điểm địa phương',
            'icon': 'mountain',
            'content': [
                p_tour or 'Thế mạnh du lịch cảnh quan thiên nhiên, biển đảo, di tích lịch sử và văn hóa bản địa.',
                p_facts or ''
            ]
        }
    ]
    
    # Heritage list
    her_list = []
    for lm in th_info.get('landmarks', [])[:4]:
        her_list.append(lm['title'])
    if not her_list:
        her_list = ['Di tích lịch sử - văn hóa địa phương', 'Thắng cảnh thiên nhiên tiêu biểu']
        
    # Links list
    links = []
    if th_info.get('google_img'):
        links.append({'title': f'Tra cứu ảnh {short} trên Google Images', 'url': th_info['google_img']})
    if th_info.get('wikimedia_img'):
        links.append({'title': f'Hình ảnh tư liệu Wikimedia Commons ({short})', 'url': th_info['wikimedia_img']})
        
    final_dataset[idx] = {
        'id': idx,
        'name': name,
        'short': short,
        'slug': slug,
        'regionId': reg_id,
        'regionName': reg_name,
        'silhouette': f'assets/silhouettes/{row["tep_png"]}',
        'litColor': lit_color,
        'quote': f'Vùng đất {reg_name} · Tinh hoa văn hóa & Tiềm năng phát triển bền vững',
        'overview': f'{name} là một trong những trung tâm trọng điểm thuộc {reg_name}. {p_tour} {p_facts}',
        'stats': stats,
        'sections': sections,
        'highlights': hl_list,
        'heritage': her_list,
        'links': links
    }

print('Compiled full dataset for', len(final_dataset), 'provinces & island territories!')

# Save to data/provinces_detail.json and dist/data/provinces_detail.json
out_data = ROOT / 'data' / 'provinces_detail.json'
out_dist = ROOT / 'dist' / 'data' / 'provinces_detail.json'
out_data.parent.mkdir(parents=True, exist_ok=True)
out_dist.parent.mkdir(parents=True, exist_ok=True)

content = json.dumps(final_dataset, ensure_ascii=False, indent=2)
out_data.write_text(content, encoding='utf-8')
out_dist.write_text(content, encoding='utf-8')
print('Wrote provinces_detail.json successfully with all 36 entities!')
