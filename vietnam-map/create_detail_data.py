import json
from pathlib import Path

provinces_detail = {
    5: {
        'id': 5,
        'name': 'Tuyên Quang',
        'short': 'Tuyên Quang',
        'slug': 'tuyen-quang',
        'regionId': 'vung-1',
        'regionName': 'Trung Du miền núi Bắc Bộ',
        'silhouette': 'assets/silhouettes/05_tuyen_quang.png',
        'litColor': '#22c55e',
        'quote': 'Thủ đô Khu giải phóng · Cội nguồn cách mạng · Đất đồi nương trù phú',
        'overview': 'Tuyên Quang là một tỉnh miền núi thuộc vùng Đông Bắc Bộ Việt Nam, nổi tiếng với truyền thống lịch sử vẻ vang cùng danh xưng "Thủ đô kháng chiến". Tỉnh sở hữu cảnh quan thiên nhiên tráng lệ từ Cao nguyên đá Đồng Văn, Cột cờ Lũng Cú đến hồ sinh thái Na Hang.',
        'stats': [
            {'label': 'Diện tích', 'value': '13.795,5 km²', 'sub': 'Sau điều chỉnh sáp nhập'},
            {'label': 'Dân số', 'value': '1.865.270', 'sub': 'Giữa năm 2025'},
            {'label': 'Hành chính', 'value': '7 phường, 117 xã', 'sub': 'Trung tâm: P. Minh Xuân'},
            {'label': 'Kinh tế', 'value': 'Dịch vụ 41,8%', 'sub': 'CN-XD 28% · Nông nghiệp 25,8%'}
        ],
        'sections': [
            {
                'title': 'Vị trí địa lý & Điều kiện tự nhiên',
                'icon': 'geo',
                'content': [
                    'Vị trí: Nằm ở trung tâm vùng Đông Bắc Bộ, tiếp giáp với các tỉnh Cao Bằng, Thái Nguyên, Phú Thọ, Lào Cai và có đường biên giới quốc gia.',
                    'Địa hình: Chủ yếu là đồi núi hiểm trở, bị chia cắt mạnh bởi các dãy núi cao cùng hệ thống sông suối lớn như sông Lô và sông Gâm.',
                    'Khí hậu: Nhiệt đới gió mùa vùng núi, mùa đông lạnh mát, mùa hè ôn hòa, tạo điều kiện thuận lợi phát triển lâm nghiệp và cây ăn quả đặc sản.'
                ]
            },
            {
                'title': 'Dân số, Hành chính & Con người',
                'icon': 'users',
                'content': [
                    'Quy mô dân số đạt trên 1,86 triệu người, là nơi hội tụ sinh sống gắn bó của nhiều đồng bào dân tộc anh em như Tày, Dao, Mông, Nùng, Kinh, Sán Dìu...',
                    'Đơn vị hành chính gồm 7 phường và 117 xã. Thủ phủ đặt tại Phường Minh Xuân, trung tâm kinh tế - chính trị - văn hóa của toàn tỉnh.'
                ]
            },
            {
                'title': 'Kinh tế & Định hướng phát triển',
                'icon': 'trend',
                'content': [
                    'Cơ cấu kinh tế: Ngành dịch vụ chiếm tỷ trọng lớn nhất (khoảng 41,79%), tiếp theo là công nghiệp - xây dựng (27,99%) và nông - lâm - thủy sản (25,77%).',
                    'Định hướng: Tỉnh tập trung phát triển du lịch sinh thái - lịch sử, nông nghiệp công nghệ cao và thu hút các ngành công nghiệp chế biến sâu.'
                ]
            }
        ],
        'highlights': [
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
                'title': 'Cam sành Hàm Yên',
                'image': 'assets/images/image3.jpeg',
                'caption': 'Đặc sản Cam sành Hàm Yên vỏ sần vàng mọng nước',
                'desc': 'Cam sành Hàm Yên có quả vỏ sần, tép cam vàng óng mọng nước, vị ngọt thanh pha chút chua dịu, là một trong những loại trái cây đặc sản nổi tiếng nhất miền Bắc.'
            },
            {
                'title': 'Mật ong bạc hà Mèo Vạc',
                'image': 'assets/images/image4.jpeg',
                'caption': 'Mật ong bạc hà hoa tự nhiên sánh vàng quyến rũ',
                'desc': 'Được tạo nên từ nguồn hoa bạc hà tự nhiên mọc trên các vách đá vôi cao nguyên, mật ong có màu vàng chanh óng ánh, vị ngọt thanh mát và hương thơm thảo mộc đặc trưng hiếm có.'
            }
        ],
        'heritage': [
            'Khu di tích quốc gia đặc biệt Tân Trào - Thủ đô kháng chiến',
            'Khu du lịch sinh thái Na Hang - Lâm Bình',
            'Suối khoáng nóng Mỹ Lâm'
        ],
        'links': [
            {'title': 'Cổng thông tin điện tử tỉnh Tuyên Quang', 'url': 'https://www.tuyenquang.gov.vn/'},
            {'title': 'Video tư liệu Tuyên Quang', 'url': 'https://www.tuyenquang.gov.vn/vi/media/video?id=8598&type=TYPE_VIDEO'},
            {'title': 'Bài viết: Cột cờ Lũng Cú biểu tượng thiêng liêng', 'url': 'https://www.tuyenquang.gov.vn/vi/post/cot-co-quoc-gia-lung-cu-bieu-tuong-thieng-lieng-tren-manh-dat-tuyen-quang-moi?id=153402&type=NEWS'}
        ]
    },
    2: {
        'id': 2,
        'name': 'Cao Bằng',
        'short': 'Cao Bằng',
        'slug': 'cao-bang',
        'regionId': 'vung-1',
        'regionName': 'Trung Du miền núi Bắc Bộ',
        'silhouette': 'assets/silhouettes/02_cao_bang.png',
        'litColor': '#06b6d4',
        'quote': 'Công viên địa chất toàn cầu · Đất Pác Bó lịch sử · Thác Bản Giốc hùng vĩ',
        'overview': 'Cao Bằng là một tỉnh miền núi biên giới phía Đông Bắc, nổi bật với cảnh sắc thiên nhiên kỳ vĩ được UNESCO công nhận là Công viên Địa chất Toàn cầu Non Nước Cao Bằng, cùng cội nguồn cách mạng hào hùng tại Pác Bó.',
        'stats': [
            {'label': 'Diện tích', 'value': '6.703 km²', 'sub': '90% diện tích là đồi núi rừng'},
            {'label': 'Dân số', 'value': '~573.000', 'sub': 'Đa số là Tày, Nùng, Mông, Dao'},
            {'label': 'Đường biên giới', 'value': '> 333 km', 'sub': 'Giáp Quảng Tây (Trung Quốc)'},
            {'label': 'Hành chính', 'value': 'TP. Cao Bằng', 'sub': 'Trung tâm hành chính tỉnh'}
        ],
        'sections': [
            {
                'title': 'Vị trí địa lý & Điều kiện tự nhiên',
                'icon': 'geo',
                'content': [
                    'Vị trí: Nằm ở vùng Đông Bắc Việt Nam, có đường biên giới dài hơn 333 km giáp với khu tự trị dân tộc Choang Quảng Tây (Trung Quốc). Giáp với các tỉnh Hà Giang, Tuyên Quang, Bắc Kạn và Lạng Sơn.',
                    'Địa hình: Chủ yếu là đồi núi và rừng chiếm trên 90% diện tích tự nhiên, xen kẽ các thung lũng, hệ thống sông suối uốn lượn và dãy núi đá vôi kỳ vĩ.',
                    'Khí hậu: Nhiệt đới gió mùa vùng cao mát mẻ vào mùa hè, mùa đông lạnh sâu có nơi xuất hiện sương muối và băng tuyết.'
                ]
            },
            {
                'title': 'Kinh tế cửa khẩu & Thương mại biên mậu',
                'icon': 'trend',
                'content': [
                    'Kinh tế chủ yếu dựa vào nông - lâm nghiệp, du lịch sinh thái và kinh tế cửa khẩu biên giới.',
                    'Cửa khẩu quốc tế Trà Lĩnh có lợi thế chiến lược kết nối Cao Bằng với thành phố Bách Sắc (Quảng Tây) và thị trường Tây Nam Trung Quốc.',
                    'Tỉnh đang định hướng tổ chức lại không gian kinh tế, thu hút đầu tư hạ tầng logistics và kho bãi hiện đại.'
                ]
            }
        ],
        'highlights': [
            {
                'title': 'Thác Bản Giốc & Non nước Cao Bằng',
                'image': 'assets/images/image5.jpeg',
                'caption': 'Thác Bản Giốc - Thác nước tự nhiên lớn nhất Đông Nam Á',
                'desc': 'Thác Bản Giốc nằm tại huyện Trùng Khánh, là một trong những thác nước xuyên biên giới đẹp nhất hành tinh, dòng nước tung bọt trắng xóa giữa núi rừng xanh thẳm.'
            },
            {
                'title': 'Cửa khẩu Quốc tế Trà Lĩnh',
                'image': 'assets/images/image6.jpeg',
                'caption': 'Hoạt động giao thương hàng hóa qua Cửa khẩu Trà Lĩnh',
                'desc': 'Cửa ngõ kết nối thương mại quan trọng đưa nông sản và hàng hóa Việt Nam vươn sâu vào thị trường Trung Quốc và quốc tế.'
            },
            {
                'title': 'Làng đá cổ Khuổi Ky hơn 400 năm',
                'image': 'assets/images/image7.jpeg',
                'caption': 'Những ngôi nhà sàn bằng đá tự nhiên độc đáo ở Khuổi Ky',
                'desc': 'Làng đá Khuổi Ky (xã Đàm Thủy) nổi bật với những ngôi nhà sàn xếp bằng đá phiến tự nhiên, mái ngói âm dương cổ kính, lưu giữ nguyên vẹn bản sắc văn hóa Tày, được công nhận Làng văn hóa truyền thống tiêu biểu.'
            }
        ],
        'heritage': [
            'Công viên Địa chất Toàn cầu UNESCO Non Nước Cao Bằng',
            'Khu di tích lịch sử quốc gia đặc biệt Pác Bó',
            'Động Ngườm Ngao & Quần thể hồ Thang Hen'
        ],
        'links': [
            {'title': 'Cổng thông tin điện tử tỉnh Cao Bằng', 'url': 'https://caobang.gov.vn/'},
            {'title': 'Phim tài liệu Làng đá Khuổi Ky 400 năm tuổi', 'url': 'https://nongnghiepmoitruong.vn/video/lang-da-co-hon-400-nam-tuoi-tua-lung-vao-nui-da-o-cao-bang-tv375451.html'}
        ]
    },
    1: {
        'id': 1,
        'name': 'Lạng Sơn',
        'short': 'Lạng Sơn',
        'slug': 'lang-son',
        'regionId': 'vung-1',
        'regionName': 'Trung Du miền núi Bắc Bộ',
        'silhouette': 'assets/silhouettes/01_lang_son.png',
        'litColor': '#3b82f6',
        'quote': 'Cửa ngõ biên cương · Xứ hoa hồi ngát hương · Đỉnh Mẫu Sơn tuyết trắng',
        'overview': 'Lạng Sơn là tỉnh miền núi biên giới chiến lược phía Đông Bắc, được xem là cửa ngõ giao thương đường bộ hàng đầu nối Việt Nam và các nước ASEAN với Trung Quốc, đồng thời nổi danh với cảnh sắc thiên nhiên và di tích lịch sử thiêng liêng.',
        'stats': [
            {'label': 'Diện tích', 'value': '8.310,1 km²', 'sub': 'Cách Hà Nội 154 km'},
            {'label': 'Dân số', 'value': '881.384', 'sub': 'Nùng 43% · Tày 35% · Kinh 15%'},
            {'label': 'Biên giới', 'value': '> 231 km', 'sub': 'Nhiều cửa khẩu quốc tế lớn'},
            {'label': 'Thế mạnh', 'value': 'Kinh tế cửa khẩu', 'sub': 'Dịch vụ logistic & Hoa hồi'}
        ],
        'sections': [
            {
                'title': 'Vị trí địa lý & Dân tộc',
                'icon': 'geo',
                'content': [
                    'Nằm ở phía Đông Bắc Việt Nam, giáp Cao Bằng, Quảng Ninh, Bắc Giang, Thái Nguyên, Bắc Kạn và đường biên giới dài hơn 231 km giáp Trung Quốc.',
                    'Dân tộc phong phú với người Nùng (chiếm ~43%), người Tày (~35%), người Kinh (~15%), người Dao và các dân tộc anh em khác.'
                ]
            },
            {
                'title': 'Tiên phong Cửa khẩu thông minh',
                'icon': 'trend',
                'content': [
                    'Với vị trí địa chiến lược là cửa ngõ quốc tế quan trọng bậc nhất, Lạng Sơn là tỉnh tiên phong triển khai Đề án thí điểm Cửa khẩu thông minh tại Cửa khẩu Quốc tế Hữu Nghị - Hữu Nghị Quan.',
                    'Áp dụng công nghệ tự động hóa, định vị vệ tinh và thủ tục hải quan số, giúp thông quan 24/7 không gián đoạn.'
                ]
            }
        ],
        'highlights': [
            {
                'title': 'Khu du lịch đỉnh Mẫu Sơn',
                'image': 'assets/images/image8.jpeg',
                'caption': 'Mẫu Sơn mùa đông tuyết phủ trắng xóa đỉnh núi',
                'desc': 'Nằm trên độ cao 1.200m - 1.541m so với mặt biển, khí hậu á nhiệt đới mát mẻ mùa hè, mùa đông buốt giá thường xuất hiện băng tuyết. Nơi đây có rừng hoa Đỗ Quyên cổ thụ bạt ngàn và kiến trúc biệt thự Pháp cổ.'
            },
            {
                'title': 'Cửa khẩu Quốc tế Hữu Nghị & Cửa khẩu thông minh',
                'image': 'assets/images/image9.jpeg',
                'caption': 'Trung tâm giao thương sầm uất tại Cửa khẩu Quốc tế Hữu Nghị',
                'desc': 'Đầu mối xuất nhập khẩu hàng triệu tấn nông sản, công nghệ giữa Việt Nam và Trung Quốc với quy mô hiện đại hàng đầu khu vực.'
            },
            {
                'title': 'Đặc sản Hoa Hồi Lạng Sơn',
                'image': 'assets/images/image10.jpeg',
                'caption': 'Hoa hồi xứ Lạng - Tinh hoa nông sản xuất khẩu quốc tế',
                'desc': 'Được mệnh danh là kho báu xứ Lạng, hoa hồi Lạng Sơn có hàm lượng tinh dầu cao bậc nhất, được bảo hộ chỉ dẫn địa lý và xuất khẩu tới hàng chục quốc gia.'
            }
        ],
        'heritage': [
            'Quần thể danh thắng Động Nhị Thanh - Tam Thanh',
            'Núi Tô Thị - Biểu tượng Nàng Vọng Phu thủy chung',
            'Ải Chi Lăng hào hùng & Thành Nhà Mạc'
        ],
        'links': [
            {'title': 'Cổng thông tin điện tử tỉnh Lạng Sơn', 'url': 'https://langson.gov.vn/'},
            {'title': 'Phóng sự Cửa khẩu thông minh Hữu Nghị', 'url': 'https://youtu.be/Kzmb31tonlM?si=O_sJstq94VQITQ-c'}
        ]
    },
    8: {
        'id': 8,
        'name': 'Phú Thọ',
        'short': 'Phú Thọ',
        'slug': 'phu-tho',
        'regionId': 'vung-1',
        'regionName': 'Trung Du miền núi Bắc Bộ',
        'silhouette': 'assets/silhouettes/08_phu_tho.png',
        'litColor': '#f59e0b',
        'quote': 'Đất Tổ Hùng Vương · Cội nguồn dân tộc Việt · Ngã ba sông huyền thoại',
        'overview': 'Phú Thọ là vùng Đất Tổ thiêng liêng, cội nguồn của muôn triệu người con đất Việt. Tỉnh giữ vị trí cửa ngõ phía Tây Bắc Thủ đô Hà Nội, là nơi hội tụ ba dòng sông lớn Hồng, Lô, Đà và hai di sản văn hóa phi vật thể đại diện nhân loại.',
        'stats': [
            {'label': 'Diện tích', 'value': '9.361,4 km²', 'sub': 'Sau sáp nhập mở rộng'},
            {'label': 'Dân số', 'value': '> 4.000.000', 'sub': 'Kinh, Mường, Dao, Sán Chay...'},
            {'label': 'Hành chính', 'value': '15 phường, 133 xã', 'sub': 'Trung tâm: TP. Việt Trì'},
            {'label': 'Di sản UNESCO', 'value': '2 Di sản nhân loại', 'sub': 'Thờ cúng Hùng Vương & Hát Xoan'}
        ],
        'sections': [
            {
                'title': 'Cội nguồn văn hóa & Di sản Thế giới',
                'icon': 'star',
                'content': [
                    'Tín ngưỡng thờ cúng Hùng Vương được UNESCO công nhận là Di sản văn hóa phi vật thể đại diện của nhân loại năm 2012. Ngày Giỗ Tổ 10/3 âm lịch là ngày hội đại đoàn kết toàn dân tộc.',
                    'Hát Xoan Phú Thọ - làn điệu dân ca nghi lễ cổ truyền độc đáo được UNESCO vinh danh di sản nhân loại năm 2017.'
                ]
            },
            {
                'title': 'Kinh tế & Năng lượng trọng điểm',
                'icon': 'trend',
                'content': [
                    'Cơ cấu kinh tế chuyển dịch năng động: Công nghiệp - Xây dựng (>55%), Dịch vụ (>32%), Nông - lâm - thủy sản (~12,5%).',
                    'Sở hữu các công trình năng lượng quốc gia lớn, mạng lưới khu công nghiệp kết nối cao tốc Hà Nội - Lào Cai thông suốt.'
                ]
            }
        ],
        'highlights': [
            {
                'title': 'Khu di tích lịch sử Quốc gia đặc biệt Đền Hùng',
                'image': 'assets/images/image11.jpeg',
                'caption': 'Điện Kính Thiên linh thiêng trên đỉnh núi Nghĩa Lĩnh',
                'desc': 'Nơi thờ tự các Vua Hùng đã có công dựng nước Văn Lang, trung tâm văn hóa tâm linh cội nguồn của toàn thể cộng đồng người Việt Nam trong và ngoài nước.'
            },
            {
                'title': 'Nhà máy Thủy điện Hòa Bình trên dòng sông Đà',
                'image': 'assets/images/image12.jpeg',
                'caption': 'Toàn cảnh Nhà máy Thủy điện Hòa Bình mở rộng 2.400 MW',
                'desc': 'Công trình năng lượng thế kỷ của đất nước, khánh thành mở rộng cuối năm 2025 đạt tổng công suất 2.400 MW, đóng vai trò sống còn trong phát điện, trị thủy sông Đà và tưới tiêu nông nghiệp.'
            },
            {
                'title': 'Thị trấn mờ sương Tam Đảo',
                'image': 'assets/images/image13.jpeg',
                'caption': 'Toàn cảnh khu du lịch Tam Đảo bồng bềnh trong mây',
                'desc': 'Được ví như Đà Lạt của miền Bắc với khí hậu bốn mùa trong một ngày, sương mù bao phủ quanh năm cùng thiên nhiên nguyên sơ tươi đẹp.'
            },
            {
                'title': 'Nhà thờ đá cổ Tam Đảo',
                'image': 'assets/images/image14.jpeg',
                'caption': 'Kiến trúc Gothic cổ kính bằng đá của Nhà thờ Tam Đảo',
                'desc': 'Xây dựng từ thời Pháp thuộc bằng đá xanh, tọa lạc uy nghiêm trên triền núi nhìn xuống toàn cảnh thị trấn thơ mộng.'
            },
            {
                'title': 'Quảng trường Tam Đảo & Vườn quốc gia',
                'image': 'assets/images/image15.jpeg',
                'caption': 'Quảng trường lễ hội rực rỡ sắc màu giữa núi rừng Tam Đảo',
                'desc': 'Không gian sinh hoạt văn hóa, nghệ thuật ngoài trời sôi động cùng thảm thực vật phong phú của Vườn quốc gia Tam Đảo.'
            }
        ],
        'heritage': [
            'Đền Quốc Mẫu Âu Cơ (huyện Hạ Hòa)',
            'Hát Xoan các làng cổ An Thái, Thét, Kim Đới, Phù Đức',
            'Đầm Ao Châu & Vườn quốc gia Xuân Sơn'
        ],
        'links': [
            {'title': 'Cổng thông tin điện tử tỉnh Phú Thọ', 'url': 'https://phutho.gov.vn/'},
            {'title': 'Phim tài liệu Lễ hội Đền Hùng cội nguồn dân tộc', 'url': 'https://youtu.be/Qw3XCMRxMr8?si=b2FoKGitDAD-ugnp'}
        ]
    },
    4: {
        'id': 4,
        'name': 'Thái Nguyên',
        'short': 'Thái Nguyên',
        'slug': 'thai-nguyen',
        'regionId': 'vung-1',
        'regionName': 'Trung Du miền núi Bắc Bộ',
        'silhouette': 'assets/silhouettes/04_thai_nguyen.png',
        'litColor': '#10b981',
        'quote': 'Đệ nhất danh trà · Trung tâm công nghiệp hiện đại · Đất thép miền Gang',
        'overview': 'Thái Nguyên là trung tâm kinh tế, giáo dục và công nghiệp công nghệ cao của vùng Trung du miền núi phía Bắc. Nơi đây vừa là "thủ phủ chè" nổi tiếng với đệ nhất danh trà Tân Cương, vừa là trung tâm sản xuất điện tử hàng đầu quốc gia.',
        'stats': [
            {'label': 'Diện tích', 'value': '8.375,2 km²', 'sub': 'Sau hợp nhất mở rộng'},
            {'label': 'Dân số', 'value': '1.799.489', 'sub': 'Số liệu cuối năm 2024'},
            {'label': 'GRDP bình quân', 'value': '114 triệu đ/năm', 'sub': 'Công nghiệp - XD chiếm 54%'},
            {'label': 'Đặc sản', 'value': 'Chè Tân Cương', 'sub': 'Di sản văn hóa phi vật thể QG'}
        ],
        'sections': [
            {
                'title': 'Thủ phủ chè Việt Nam - Trà Tân Cương',
                'icon': 'leaf',
                'content': [
                    'Thái Nguyên nức tiếng gần xa là "thủ phủ chè" với vùng chè đặc sản Tân Cương. Thổ nhưỡng và nguồn nước sông Công, hồ Núi Cốc tạo nên hương vị tiền chát hậu ngọt, nước chè xanh trong sánh vàng độc nhất vô nhị.',
                    'Văn hóa thưởng trà của Thái Nguyên đã được ghi danh là Di sản văn hóa phi vật thể quốc gia.'
                ]
            },
            {
                'title': 'Cực tăng trưởng công nghiệp công nghệ cao',
                'icon': 'chip',
                'content': [
                    'Là trung tâm luyện kim truyền thống và trung tâm sản xuất điện tử lớn hàng đầu cả nước, nơi đặt các tổ hợp sản xuất quy mô tỷ USD của Samsung Electronics.',
                    'Có trữ lượng khoáng sản lớn, đặc biệt là vonfram và than đá trữ lượng cao.'
                ]
            }
        ],
        'highlights': [
            {
                'title': 'Đồi chè Tân Cương bát ngát',
                'image': 'assets/images/image16.jpeg',
                'caption': 'Vùng chè hữu cơ Tân Cương xanh mướt uốn lượn',
                'desc': 'Những nương chè xanh mơn mởn trải dài tít tắp theo sườn đồi, tạo nên phong cảnh tuyệt đẹp thu hút hàng trăm nghìn lượt khách du lịch trải nghiệm hái chè và sao chè thủ công.'
            },
            {
                'title': 'Tổ hợp Công nghiệp công nghệ cao',
                'image': 'assets/images/image17.jpeg',
                'caption': 'Khu công nghiệp Yên Bình - Tổ hợp sản xuất điện tử hàng đầu',
                'desc': 'Thái Nguyên thu hút các tập đoàn công nghệ toàn cầu, đóng góp tỷ trọng xuất khẩu thiết bị viễn thông và linh kiện điện tử lớn nhất cả nước.'
            },
            {
                'title': 'Dây chuyền sản xuất tự động hóa tiên tiến',
                'image': 'assets/images/image18.jpeg',
                'caption': 'Sản xuất công nghiệp chế biến chế tạo hiện đại',
                'desc': 'Hệ thống nhà xưởng hiện đại, robot và công nghệ thông minh đưa Thái Nguyên vươn lên top đầu tăng trưởng kinh tế miền Bắc.'
            },
            {
                'title': 'Trục du lịch Hồ Núi Cốc – Hồ Ba Bể',
                'image': 'assets/images/image19.jpeg',
                'caption': 'Cảnh sắc thơ mộng trên mặt nước hồ trên núi',
                'desc': 'Hồ Núi Cốc gắn liền với chuyện tình huyền thoại chàng Cốc nàng Công, tạo thành chuỗi du lịch sinh thái hồ trên núi nối liền với danh thắng Hồ Ba Bể hùng vĩ.'
            }
        ],
        'heritage': [
            'Khu di tích lịch sử quốc gia đặc biệt An toàn khu (ATK) Định Hóa',
            'Bảo tàng Văn hóa các Dân tộc Việt Nam tại trung tâm TP Thái Nguyên',
            'Không gian văn hóa Trà Tân Cương'
        ],
        'links': [
            {'title': 'Cổng thông tin điện tử tỉnh Thái Nguyên', 'url': 'https://thainguyen.gov.vn/'},
            {'title': 'VTV V-Việt Nam Chè Tân Cương Thái Nguyên', 'url': 'https://vtv.vn/video/v-viet-nam-che-tan-cuong-thai-nguyen-678829.htm'}
        ]
    },
    6: {
        'id': 6,
        'name': 'Lào Cai',
        'short': 'Lào Cai',
        'slug': 'lao-cai',
        'regionId': 'vung-1',
        'regionName': 'Trung Du miền núi Bắc Bộ',
        'silhouette': 'assets/silhouettes/06_lao_cai.png',
        'litColor': '#eab308',
        'quote': 'Nóc nhà Đông Dương Fansipan · Sa Pa trong sương · Kỳ quan ruộng bậc thang',
        'overview': 'Lào Cai là tỉnh vùng cao biên giới Tây Bắc, sở hữu đỉnh Fansipan 3.143m kiêu hãnh - "Nóc nhà Đông Dương", khu du lịch quốc tế Sa Pa, kỳ quan ruộng bậc thang Mù Cang Chải cùng nguồn tài nguyên Apatit độc nhất vô nhị của quốc gia.',
        'stats': [
            {'label': 'Diện tích', 'value': '13.256,9 km²', 'sub': 'Dãy Hoàng Liên Sơn kỳ vĩ'},
            {'label': 'Dân số', 'value': '1.778.785', 'sub': '27 dân tộc anh em'},
            {'label': 'Đỉnh Fansipan', 'value': '3.143 m', 'sub': 'Nóc nhà Đông Dương'},
            {'label': 'Du lịch', 'value': '> 10,5 triệu', 'sub': 'Lượt du khách mỗi năm'}
        ],
        'sections': [
            {
                'title': 'Đỉnh Fansipan - Nóc nhà Đông Dương',
                'icon': 'mountain',
                'content': [
                    'Sừng sững giữa đại ngàn dãy Hoàng Liên Sơn, đỉnh Fansipan (3.143 m) là biểu tượng tự hào của du lịch Việt Nam.',
                    'Nằm cách Sa Pa 9 km, Fansipan mở ra cảnh sắc thiên nhiên kỳ vĩ với biển mây bồng bềnh cuộn sóng, thảm rừng nguyên sinh đỗ quyên cổ thụ và tuyết trắng phủ ngọn núi vào mùa đông.'
                ]
            },
            {
                'title': 'Tài nguyên Apatit & Kinh tế cửa khẩu',
                'icon': 'gem',
                'content': [
                    'Mỏ Apatit Lào Cai nằm dọc hữu ngạn sông Hồng dài gần 100 km, là mỏ apatit duy nhất của cả nước, nền tảng cho ngành phân bón hóa chất quốc gia.',
                    'Tỉnh có hơn 147.000 ha quế hữu cơ và mạng lưới cửa khẩu quốc tế đường bộ, đường sắt sang tỉnh Vân Nam (Trung Quốc).'
                ]
            }
        ],
        'highlights': [
            {
                'title': 'Tuyệt tác Ruộng bậc thang Mù Cang Chải & Sa Pa',
                'image': 'assets/images/image20.jpeg',
                'caption': 'Mùa vàng trên những triền ruộng bậc thang uốn lượn',
                'desc': 'Di tích quốc gia đặc biệt danh lam thắng cảnh ruộng bậc thang, kiệt tác kiến trúc nông nghiệp do bàn tay tài hoa của đồng bào Mông kiến tạo qua hàng trăm năm, rực rỡ như những nấc thang lên thiên đường khi lúa chín vàng.'
            }
        ],
        'heritage': [
            'Đỉnh Fansipan 3.143m & Vườn quốc gia Hoàng Liên',
            'Thị xã du lịch quốc tế Sa Pa & Đèo Ô Quy Hồ',
            'Chợ phiên Bắc Hà rực rỡ sắc màu thổ cẩm'
        ],
        'links': [
            {'title': 'Cổng thông tin điện tử tỉnh Lào Cai', 'url': 'https://laocai.gov.vn/'},
            {'title': 'Video Chinh phục đỉnh Fansipan 3.143m', 'url': 'https://www.youtube.com/watch?v=9QjsgRa2R7w'},
            {'title': 'VTV Mê mẩn vẻ đẹp ruộng bậc thang Mù Cang Chải', 'url': 'https://vtv.vn/video/me-man-ve-dep-ruong-bac-thang-mu-cang-chai-395183.htm'}
        ]
    },
    11: {
        'id': 11,
        'name': 'Sơn La',
        'short': 'Sơn La',
        'slug': 'son-la',
        'regionId': 'vung-1',
        'regionName': 'Trung Du miền núi Bắc Bộ',
        'silhouette': 'assets/silhouettes/11_son_la.png',
        'litColor': '#f97316',
        'quote': 'Hồ thủy điện lớn nhất Đông Nam Á · Thảo nguyên Mộc Châu · Điệu Xòe Thái di sản',
        'overview': 'Sơn La là tỉnh có diện tích lớn thứ ba cả nước, nằm ở trái tim miền Tây Bắc. Tỉnh nổi danh với công trình Thủy điện Sơn La kỳ vĩ trên sông Đà, cao nguyên xanh Mộc Châu bạt ngàn nương chè hoa mận, cùng di tích Nhà tù Sơn La kiên trung.',
        'stats': [
            {'label': 'Diện tích', 'value': '14.109,8 km²', 'sub': 'Lớn thứ 3 Việt Nam'},
            {'label': 'Dân số', 'value': '~1.400.000', 'sub': '12 dân tộc (Đông nhất: Thái)'},
            {'label': 'Thủy điện Sơn La', 'value': '2.400 MW', 'sub': 'Hồ chứa nhân tạo lớn nhất ĐNA'},
            {'label': 'Di sản UNESCO', 'value': 'Nghệ thuật Xòe Thái', 'sub': 'Di sản văn hóa phi vật thể'}
        ],
        'sections': [
            {
                'title': 'Vị trí địa lý & Dân tộc',
                'icon': 'geo',
                'content': [
                    'Nằm ở trung tâm vùng Tây Bắc, cách Hà Nội khoảng 300 km. Có đường biên giới dài 250 km giáp Lào với các cửa khẩu Chiềng Khương và Lóng Sập.',
                    'Là mái nhà chung của 12 dân tộc anh em, tiêu biểu là người Thái, Mông, Kinh, Mường, Dao, Khơ Mú... với bản sắc văn hóa múa Xòe Thái được UNESCO công nhận là di sản nhân loại.'
                ]
            },
            {
                'title': 'Thủy điện Sơn La & Lòng hồ Sông Đà',
                'icon': 'bolt',
                'content': [
                    'Nhà máy Thủy điện Sơn La trên sông Đà khánh thành năm 2012 với công suất 2.400 MW, từng là công trình thủy điện lớn nhất Đông Nam Á.',
                    'Lòng hồ thủy điện nhân tạo rộng 224 km², dung tích 9,26 tỷ m³ nước, tạo nên kỳ quan hồ sinh thái Mường La hữu tình.'
                ]
            }
        ],
        'highlights': [
            {
                'title': 'Đập & Hồ Thủy điện Sơn La trên sông Đà',
                'image': 'assets/images/image21.jpeg',
                'caption': 'Công trình Thủy điện Sơn La đồ sộ ngăn dòng sông Đà',
                'desc': 'Kỳ tích xây dựng của bàn tay và khối óc Việt Nam, cung cấp nguồn năng lượng khổng lồ cho cả nước, điều hòa lũ cho hạ du đồng bằng Bắc Bộ.'
            },
            {
                'title': 'Cao nguyên Mộc Châu xanh ngát',
                'image': 'assets/images/image22.jpeg',
                'caption': 'Đồi chè trái tim Mộc Châu ngút ngàn xanh biếc',
                'desc': 'Khu du lịch quốc gia Mộc Châu được vinh danh là Điểm đến thiên nhiên khu vực hàng đầu thế giới với khí hậu trong lành, đồi chè ô long, thung lũng mận Nà Ka và trang trại bò sữa.'
            },
            {
                'title': 'Di tích quốc gia đặc biệt Nhà tù Sơn La',
                'image': 'assets/images/image23.jpeg',
                'caption': 'Cây đào Tô Hiệu biểu tượng bất khuất trong Nhà tù Sơn La',
                'desc': 'Được thực dân Pháp xây dựng năm 1908 nhằm đày ải các chiến sĩ cộng sản. Cây đào Tô Hiệu vẫn đơm hoa giữa ngục tù, biểu tượng cho khí tiết kiên trung bất khuất của dân tộc.'
            }
        ],
        'heritage': [
            'Khu du lịch quốc gia Mộc Châu (Đồi chè, Thác Dải Yếm, Rừng thông Bản Áng)',
            'Xã ngọc chiến (Mường La) suối khoáng nóng bản Lướt',
            'Lễ hội Hết Chá và Nghệ thuật Xòe Thái di sản UNESCO'
        ],
        'links': [
            {'title': 'Cổng thông tin điện tử tỉnh Sơn La', 'url': 'https://sonla.gov.vn/'},
            {'title': 'VOV Khám phá Khu du lịch quốc gia Mộc Châu', 'url': 'https://vov.vn/du-lich/khu-du-lich-quoc-gia-moc-chau-truoc-co-hoi-but-pha-post1095930.vov'}
        ]
    },
    10: {
        'id': 10,
        'name': 'Điện Biên',
        'short': 'Điện Biên',
        'slug': 'dien-bien',
        'regionId': 'vung-1',
        'regionName': 'Trung Du miền núi Bắc Bộ',
        'silhouette': 'assets/silhouettes/10_dien_bien.png',
        'litColor': '#a855f7',
        'quote': 'Chiến thắng lừng lẫy năm châu · Điểm cực Tây A Pa Chải · Cánh đồng Mường Thanh',
        'overview': 'Điện Biên là tỉnh biên cương Tây Bắc gắn liền với mốc son chói lọi trong lịch sử dân tộc - Chiến thắng Điện Biên Phủ ngày 07/05/1954. Đây cũng là tỉnh duy nhất của nước ta tiếp giáp với cả hai quốc gia Lào và Trung Quốc.',
        'stats': [
            {'label': 'Diện tích', 'value': '9.541 km²', 'sub': 'Cách Hà Nội 504 km'},
            {'label': 'Dân số', 'value': '~670.000', 'sub': '19 dân tộc: Mông, Thái, Kinh...'},
            {'label': 'Đặc điểm vị trí', 'value': 'Ngã ba biên giới', 'sub': 'Giáp cả Lào và Trung Quốc'},
            {'label': 'Lịch sử', 'value': 'Chiến thắng 1954', 'sub': 'Di tích quốc gia đặc biệt'}
        ],
        'sections': [
            {
                'title': 'Vị trí địa đầu & Điểm cực Tây Tổ quốc',
                'icon': 'compass',
                'content': [
                    'Cách Thủ đô Hà Nội 504 km về phía Tây, phía Đông giáp Sơn La, phía Bắc giáp Lai Châu, Tây Bắc giáp Vân Nam (Trung Quốc), Tây và Nam giáp Lào.',
                    'A Pa Chải (xã Sín Thầu) là điểm cực Tây của dải đất chữ S, nơi cắm cột mốc số 0 tiếp giáp ngã ba biên giới Việt - Lào - Trung.'
                ]
            },
            {
                'title': 'Chiến thắng Điện Biên Phủ lịch sử',
                'icon': 'medal',
                'content': [
                    'Quần thể di tích Chiến trường Điện Biên Phủ là biểu tượng của chủ nghĩa anh hùng cách mạng: Đồi A1, Hầm tướng Đờ Cát, Cầu Mường Thanh, Sở chỉ huy chiến dịch Mường Phăng.',
                    'Tượng đài chiến thắng Điện Biên Phủ sừng sững trên đỉnh đồi D1, là niềm tự hào của muôn thế hệ người Việt.'
                ]
            }
        ],
        'highlights': [
            {
                'title': 'Cột cờ A Pa Chải - Cực Tây Tổ quốc',
                'image': 'assets/images/image24.jpeg',
                'caption': 'Cột cờ A Pa Chải kiêu hãnh nơi cực Tây Tổ quốc',
                'desc': 'Tọa lạc tại đỉnh núi Khoang La San, cao 1.864m so với mực nước biển, điểm cực Tây thiêng liêng nơi một tiếng gà gáy cả ba nước đều nghe.'
            },
            {
                'title': 'Tượng đài Chiến thắng Điện Biên Phủ',
                'image': 'assets/images/image25.jpeg',
                'caption': 'Tượng đài Chiến thắng Điện Biên Phủ uy nghiêm trên đồi D1',
                'desc': 'Cụm tượng đài bằng đồng sừng sững tạc ghi chiến công chấn động địa cầu, thể hiện tinh thần đoàn kết bất diệt của bộ đội và nhân dân các dân tộc.'
            },
            {
                'title': 'Cửa khẩu Quốc tế Tây Trang',
                'image': 'assets/images/image26.jpeg',
                'caption': 'Cửa khẩu quốc tế Tây Trang kết nối trực tiếp với Bắc Lào',
                'desc': 'Cửa ngõ giao thương đường bộ then chốt giữa Việt Nam và Lào, gắn kết tình hữu nghị đặc biệt thủy chung son sắt giữa hai quốc gia anh em.'
            }
        ],
        'heritage': [
            'Cánh đồng lúa Mường Thanh - vựa lúa lớn nhất Tây Bắc',
            'Hồ Pá Khoang & Rừng hoa anh đào Mường Phăng',
            'Đèo Pha Đin hùng vĩ - một trong Tứ đại đỉnh đèo'
        ],
        'links': [
            {'title': 'Cổng thông tin điện tử tỉnh Điện Biên', 'url': 'https://dienbien.gov.vn/'},
            {'title': 'Cổng thông tin Di tích Quốc gia Chiến trường Điện Biên Phủ', 'url': 'https://svhttdl.dienbien.gov.vn/ditich/pages/2025-08-08/Di-tich-Quoc-gia-dac-biet-Chien-truong-Dien-Bien-P1.aspx'}
        ]
    },
    9: {
        'id': 9,
        'name': 'Lai Châu',
        'short': 'Lai Châu',
        'slug': 'lai-chau',
        'regionId': 'vung-1',
        'regionName': 'Trung Du miền núi Bắc Bộ',
        'silhouette': 'assets/silhouettes/09_lai_chau.png',
        'litColor': '#ec4899',
        'quote': 'Đỉnh mây Pu Ta Leng · Thủy điện Lai Châu rực sáng · Vựa lúa Mường Than Séng Cù',
        'overview': 'Lai Châu là tỉnh vùng cao Tây Bắc sở hữu địa hình núi non điệp trùng hiểm trở, những đỉnh núi cao ngất trời như Pu Ta Leng, San Lùng, công trình Thủy điện Lai Châu hùng vĩ trên sông Đà và đặc sản gạo Séng Cù của vựa lúa Mường Than trứ danh.',
        'stats': [
            {'label': 'Diện tích', 'value': '9.068,8 km²', 'sub': 'Đứng thứ 10/63 tỉnh thành'},
            {'label': 'Dân số', 'value': '512.601', 'sub': '20 dân tộc thiểu số'},
            {'label': 'Thủy điện Lai Châu', 'value': '1.200 MW', 'sub': 'Lớn thứ 3 trên sông Đà'},
            {'label': 'Đỉnh Pu Ta Leng', 'value': '3.049 m', 'sub': 'Nóc nhà thứ 2 Đông Dương'}
        ],
        'sections': [
            {
                'title': 'Vị trí địa lý & Địa hình hiểm trở',
                'icon': 'mountain',
                'content': [
                    'Phía Bắc giáp Trung Quốc với đường biên giới 265,165 km và Cửa khẩu quốc tế Ma Lù Thàng; phía Tây và Nam giáp Điện Biên; phía Đông giáp Lào Cai và Yên Bái; phía Nam giáp Sơn La.',
                    'Địa hình chia cắt hiểm trở bậc nhất với những dãy núi cao ngất trời, thung lũng sâu thẳm và hệ thống sông suối dốc đứng.'
                ]
            },
            {
                'title': 'Công nghiệp Thủy điện sông Đà & Cửa khẩu',
                'icon': 'bolt',
                'content': [
                    'Trụ cột kinh tế công nghiệp thủy điện hàng đầu với Nhà máy Thủy điện Lai Châu (1.200 MW) khánh thành năm 2016, sản lượng điện 4,7 tỷ kWh/năm.',
                    'Kinh tế cửa khẩu Ma Lù Thàng và xuất khẩu nông sản chất lượng cao.'
                ]
            }
        ],
        'highlights': [
            {
                'title': 'Nhà máy Thủy điện Lai Châu trên sông Đà',
                'image': 'assets/images/image27.jpeg',
                'caption': 'Công trình Thủy điện Lai Châu nguy nga trên dòng chính sông Đà',
                'desc': 'Công trình thủy điện bậc thang cao nhất trên dòng chính sông Đà, công suất 1.200 MW, góp phần bảo đảm an ninh năng lượng quốc gia và phát triển kinh tế vùng Tây Bắc.'
            },
            {
                'title': 'Gạo Séng Cù & Vựa lúa Mường Than',
                'image': 'assets/images/image28.jpeg',
                'caption': 'Cánh đồng Mường Than thẳng cánh cò bay',
                'desc': 'Vựa lúa lớn thứ ba miền Tây Bắc "Nhất Thanh, nhì Lò, tam Than, tứ Tấc". Đặc sản gạo Séng Cù hạt mẩy, dẻo thơm, giàu dinh dưỡng nức tiếng gần xa.'
            },
            {
                'title': 'Rừng hoa Đỗ Quyên đỉnh Pu Ta Leng',
                'image': 'assets/images/image29.jpeg',
                'caption': 'Sắc màu hoa đỗ quyên rực rỡ trên đỉnh núi cao 3.049m',
                'desc': 'Pu Ta Leng cao 3.049m (xã Hồ Thầu) được xem là nóc nhà thứ 2 của Đông Dương. Cứ mỗi độ xuân về, rừng hoa đỗ quyên cổ thụ lại bung nở rực rỡ muôn sắc đỏ, hồng, tím huyền ảo giữa mây trời.'
            }
        ],
        'heritage': [
            'Đèo Ô Quy Hồ (Cổng trời Lai Châu) - Đèo dài và hiểm trở nhất Việt Nam',
            'Quần thể danh thắng Động Tiên Sơn (huyện Tam Đường)',
            'Bản Sin Suối Hồ - Làng du lịch cộng đồng tiêu biểu ASEAN'
        ],
        'links': [
            {'title': 'Cổng thông tin điện tử tỉnh Lai Châu', 'url': 'https://laichau.gov.vn/'},
            {'title': 'Phim tài liệu Gạo Séng Cù đặc sản Mường Than', 'url': 'https://nongnghiepmoitruong.vn/video/seng-cu--dac-san-cua-vua-lua-muong-than-tv376084.html'},
            {'title': 'Báo Lai Châu: Rực rỡ sắc màu hoa đỗ quyên Pu Ta Leng', 'url': 'https://baolaichau.vn/videos/4874/ruc-ro-sac-mau-hoa-do-quyen-972190'}
        ]
    }
}

p1 = Path(r'd:\WEB 2\testweb\vietnam-map\data')
p2 = Path(r'd:\WEB 2\testweb\vietnam-map\dist\data')
p1.mkdir(parents=True, exist_ok=True)
p2.mkdir(parents=True, exist_ok=True)

content = json.dumps(provinces_detail, ensure_ascii=False, indent=2)
(p1 / 'provinces_detail.json').write_text(content, encoding='utf-8')
(p2 / 'provinces_detail.json').write_text(content, encoding='utf-8')

print('Wrote provinces_detail.json successfully with 9 provinces!')
