import pyperclip as cp
import random
import tkinter as tk
import os
import sys

from datetime import datetime, timedelta
from tkinter.messagebox import *
from tkinter import IntVar
from tkinter import ttk

if getattr(sys, 'frozen', None):
    base_dir = os.path.join(sys._MEIPASS, 'asserts')
else:
    base_dir = os.path.join(os.path.abspath("."), 'asserts')

def set_entry_value(entry, value):
    entry.delete(0, tk.END)
    entry.insert(0, value)

def read_file(file_path):
    with open(base_dir + file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def generate_random_date(start_year=1960, end_year=2020):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    
    return random_date.strftime("%Y%m%d")

def calculate_checksum(id_number):
    factorArr = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
    parityBit = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
    
    intweightSum = sum(int(id_number[i]) * factorArr[i] for i in range(17))
    intCheckDigit = parityBit[intweightSum % 11]

    return intCheckDigit

# 定义校验码计算函数
def calculate_check_digit(code):
    # 权重系数
    ws = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
    # 字符映射
    str_chars = "0123456789ABCDEFGHJKLMNPQRTUWXY"
    
    # 验证代码长度
    if len(code) != 17:
        raise ValueError("Input code must be 17 characters long")
    
    # 确保所有字符在映射表中
    for char in code:
        if char not in str_chars:
            raise ValueError(f"Character '{char}' not found in mapping table")

    # 计算加权和
    sum_val = sum(str_chars.index(char) * ws[i] for i, char in enumerate(code))

    # 计算校验码
    check_digit_num = 31 - (sum_val % 31)
    if check_digit_num > 30:
        check_digit = '0'
    else:
        check_digit = str_chars[check_digit_num]
    
    return check_digit

def calculate_org_code_check_digit(org_code):
    # 权重系数
    ws = [3, 7, 9, 10, 5, 8, 4, 2]
    # 字符映射
    str_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # 计算加权和
    sum_val = sum(str_chars.index(char) * ws[i] for i, char in enumerate(org_code[:8]))
    
    # 计算校验码
    check_digit_num = 11 - (sum_val % 11)
    if check_digit_num == 11:
        check_digit = '0'
    elif check_digit_num == 10:
        check_digit = 'X'
    else:
        check_digit = str(check_digit_num)
    
    return check_digit
    
def generate_org_code():
    chars = "0123456789ABCDEFGHJKLMNPQRTUWXY"
    org_code = ''.join(random.choice(chars) for _ in range(8))
    check_digit = calculate_org_code_check_digit(org_code)

    return org_code + '-' + check_digit

def generate_bank_card(bank_type):
    # 中国银行
    boc_prefix_list = [
        "621660", "621661", "621663", "621667", 
        "621668", "621666", "621256", "621212", 
        "621283", "621725"
    ]

    # 建设银行
    ccb_prefix_list = [
        "621700", "436742", "436745", "622280"
    ]

    # 农业银行
    abc_prefix_list = ['622848']

    # 工商银行
    icbc_prefix_list = [
        '620200', '620302', '622200', '955880'
    ]
    
    # 邮储银行
    psbc_prefix_list = [
        '622150', '622151', '622181', '622188'
    ]

    if bank_type == 'BOC':
        prefix_list = boc_prefix_list
    elif bank_type == 'CCB':
        prefix_list = ccb_prefix_list
    elif bank_type == 'ABC':
        prefix_list = abc_prefix_list
    elif bank_type == 'ICBC':
        prefix_list = icbc_prefix_list
    elif bank_type == 'PSBC':
        prefix_list = psbc_prefix_list
    else:
        prefix_list = ['666666']
    
    prefix = random.choice(prefix_list)
    suffix = ''.join(random.choices("0123456789", k=13))
    
    # 拼接为19位银行卡号
    bank_card_number = prefix + suffix
    
    return bank_card_number

# 根据性别随机生成三位顺序码
def generate_sequence_code(gender):
    while True:
        sequence_code = random.randint(100, 999)
        
        if gender == 1:
            if sequence_code % 2 != 0:
                break
        else:
            if sequence_code % 2 == 0:
                break
    
    return str(sequence_code)

# 验证输入的日期字符串格式是否正确
def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y%m%d")
        return True
    except ValueError:
        return False

class numberGen:
    def show_ui(self, root):
        self.root = root

        root.title(u'号码生成工具')
        root.geometry('700x600')

        link = tk.Label(root, text='所有数据均为测试数据, 使用时请遵守法律法规！', cursor='hand2', foreground="#FF0000")
        link.grid(row=0, column=0, sticky='W', padx=3, pady=3, columnspan=3)

        lotto = tk.Label(root, text=self.lotto, fg="red")
        lotto.grid(row=0, column=2, sticky='W', padx=3, pady=3, columnspan=3)

        self.entries = []

        self.gender = IntVar()        
        tk.Label(root, text="性别：").grid(row=1, column=0, sticky='W', padx=3, pady=3)
        tk.Radiobutton(root, text="男", variable=self.gender, value=1).grid(row=1, column=1, padx=3, pady=3)
        tk.Radiobutton(root, text="女", variable=self.gender, value=0).grid(row=1, column=2, padx=3, pady=3)

        tk.Label(root, text="出生日期：").grid(row=2, column=0, sticky='W', padx=3, pady=3)
        self.birth_date_var = tk.StringVar()
        self.birth_date_entry = tk.Entry(root, width=20)
        self.birth_date_entry.grid(row=2, column=1, padx=3, pady=3)
        self.entries.append(self.birth_date_entry)

        # 创建标签和输入框
        labels = ['姓名:', '手机号:', '身份证号:', '公司名称:', '统一社会信用代码:', '组织机构代码:', '中征码:', '中国银行卡号: ', '建设银行卡号: ', '农业银行卡号: ', '工商银行卡号: ', '邮储银行卡号: ']
        entries_names = ['ename', 'ephone', 'eidn', 'ecompanyname', 'ecreditcode', 'eorgancode', 'epbccode', 'boccode', 'ccbcode', 'abccode', 'icbccode', 'psbccode']

        for i, (label_text, entry_name) in enumerate(zip(labels, entries_names)):
            tk.Label(root, text=label_text).grid(row=i + 3, column=0, padx=3, pady=3, sticky='W')
            entry = tk.Entry(root, width=20)
            entry.grid(row=i + 3, column=1, padx=3, pady=3)
            setattr(self, entry_name, entry)
            self.entries.append(entry)

        # 创建生成和复制按钮
        buttons = [
            (self.random_name, 'ename'),
            (self.random_phone_number, 'ephone'),
            (self.random_id_card, 'eidn'),
            (self.random_company_name, 'ecompanyname'),
            (self.random_credit_code, 'ecreditcode'),
            (self.random_organ_code, 'eorgancode'),
            (self.random_pbc_code, 'epbccode'),
            (self.random_boc_code, 'boccode'),
            (self.random_ccb_code, 'ccbcode'),
            (self.random_abc_code, 'abccode'),
            (self.random_icbc_code, 'icbccode'),
            (self.random_psbc_code, 'psbccode'),
        ]

        for i, (gen_command, entry_name) in enumerate(buttons):
            self.create_buttons(root, i + 3, gen_command, getattr(self, entry_name))

        ttk.Button(root, text=u'生成', width=15, command=self.generatorAll).grid(row=20, column=0, padx=3, pady=3)
        ttk.Button(root, text=u'重置', width=15, command=self.resetAll).grid(row=20, column=1, padx=3, pady=3)

    def create_buttons(self, root, row, gen_command, entry):
        ttk.Button(root, text='生成', command=gen_command).grid(row=row, column=2, padx=3, pady=3)
        ttk.Button(root, text='复制', command=lambda: self.copy_to_clipboard(entry.get())).grid(row=row, column=3, padx=3, pady=3)

    # 姓名
    def random_name(self):
        # 1 姓氏
        name_xing_all = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
                        '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
                        '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
                        '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
                        '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
                        '姚', '邵', '湛', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
                        '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '杜', '阮', '蓝', '闵', '席', '季', '麻', '强', '贾', '路', '娄', '危',
                        '江', '童', '颜', '郭', '梅', '盛', '林', '刁', '锺', '徐', '丘', '骆', '高', '夏', '蔡', '田', '樊', '胡', '凌', '霍',
                        '虞', '万', '支', '柯', '昝', '管', '卢', '莫', '经', '房', '裘', '缪', '干', '解', '应', '宗', '丁', '宣', '贲', '邓',
                        '郁', '单', '杭', '洪', '包', '诸', '左', '石', '崔', '吉', '钮', '龚', '程', '嵇', '邢', '滑', '裴', '陆', '荣', '翁',
                        '荀', '羊', '於', '惠', '甄', '麹', '家', '封', '芮', '羿', '储', '靳', '汲', '邴', '糜', '松', '井', '段', '富', '巫',
                        '乌', '焦', '巴', '弓', '牧', '隗', '山', '谷', '车', '侯', '宓', '蓬', '全', '郗', '班', '仰', '秋', '仲', '伊', '宫',
                        '甯', '仇', '栾', '暴', '甘', '钭', '厉', '戎', '祖', '武', '符', '刘', '景', '詹', '束', '龙', '叶', '幸', '司', '韶',
                        '郜', '黎', '蓟', '薄', '印', '宿', '白', '怀', '蒲', '邰', '从', '鄂', '索', '咸', '籍', '赖', '卓', '蔺', '屠', '蒙',
                        '池', '乔', '阴', '鬱', '胥', '能', '苍', '双', '闻', '莘', '党', '翟', '谭', '贡', '劳', '逄', '姬', '申', '扶', '堵',
                        '冉', '宰', '郦', '雍', '郤', '璩', '桑', '桂', '濮', '牛', '寿', '通', '边', '扈', '燕', '冀', '郏', '浦', '尚', '农',
                        '温', '别', '庄', '晏', '柴', '瞿', '阎', '充', '慕', '连', '茹', '习', '宦', '艾', '鱼', '容', '向', '古', '易', '慎',
                        '戈', '廖', '庾', '终', '暨', '居', '衡', '步', '都', '耿', '满', '弘', '匡', '国', '文', '寇', '广', '禄', '阙', '东',
                        '欧', '殳', '沃', '利', '蔚', '越', '夔', '隆', '师', '巩', '厍', '聂', '晁', '勾', '敖', '融', '冷', '訾', '辛', '阚',
                        '那', '简', '饶', '空', '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰', '巢', '关', '蒯', '相', '查', '后', '荆', '红',
                        '游', '竺', '权', '逯', '盖', '益', '桓', '公', '万俟', '司马', '上官', '欧阳', '夏侯', '诸葛', '闻人', '东方', '赫连', '皇甫',
                        '尉迟', '公羊', '澹台', '公冶', '宗政', '濮阳', '淳于', '单于', '太叔', '申屠', '公孙', '仲孙', '轩辕', '令狐', '锺离', '宇文',
                        '长孙', '慕容', '鲜于', '闾丘', '司徒', '司空', '亓官', '司寇', '仉', '督', '子车', '颛孙', '端木', '巫马', '公西', '漆雕', '乐正',
                        '壤驷', '公良', '拓跋', '夹谷', '宰父', '穀梁', '晋', '楚', '闫', '法', '汝', '鄢', '涂', '钦', '段干', '百里', '东郭', '南门',
                        '呼延', '归海', '羊舌', '微生', '岳', '帅', '缑', '亢', '况', '後', '有', '琴', '梁丘', '左丘', '东门', '西门', '商', '牟',
                        '佘', '佴', '伯', '赏', '南宫', '墨', '哈', '谯', '笪', '年', '爱', '阳', '佟', '第五', '言', '福']
        # 2.1 男孩名字
        name_body_ming = ['壮', '昱杰', '开虎', '凯信', '永斌', '方洲', '长发', '可人', '天弘', '炫锐', '富明', '俊枫']
        # 男孩名字
        name_body_ming2 = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘'
        for everyChar in name_body_ming2:
            name_body_ming.append(everyChar)

        # 2.2 女孩名字
        name_girl_ming = ['小玉', '蓝', '琬郡', '琛青', '予舴', '妙妙', '梓茵', '海蓉', '语娜', '馨琦', '晓馥', '佳翊']
        # 女孩名字
        name_girl_ming2 = '秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽'
        for everyChar in name_girl_ming2:
            name_girl_ming.append(everyChar)

        # 随机生成姓氏
        name_xing = random.choice(name_xing_all)
        # 随机生成性别
        sex = self.gender.get() if self.gender.get() in [0, 1] else random.choice([0, 1])

        if sex == 0:
            # 女性
            name_ming = random.choice(name_girl_ming)
        else:
            # 男性
            name_ming = random.choice(name_body_ming)

        set_entry_value(self.ename, name_xing + name_ming)

    # 手机号
    def random_phone_number(self):
        prefixes = ["13", "15", "16", "17", "18", "19"]
        prefix = random.choice(prefixes)
        remaining_digits = ''.join(random.choices("0123456789", k=9))
        phone_number = prefix + remaining_digits
        
        set_entry_value(self.ephone, phone_number)

    # 身份证号码
    def random_id_card(self):
        # 随机选择一个省级地区码
        lines = read_file("/areaCode.txt")
        region_code = random.choice(lines)
        
        # 随机生成一个有效的出生日期
        if (validate_date(self.birth_date_entry.get())):
            birth_date = self.birth_date_entry.get()
        else:
            birth_date = generate_random_date()
        
        # 随机生成后三位顺序码
        sequence_code = generate_sequence_code(self.gender.get())
        
        # 拼接前17位
        id_number_17 = region_code + birth_date + sequence_code
        
        # 计算校验码
        checksum = calculate_checksum(id_number_17)
        
        # 生成完整的身份证号
        id_number = id_number_17 + checksum
        
        set_entry_value(self.eidn, id_number)

    # 公司名称
    def random_company_name(self):
        characters = [
            '华', '瑞', '恒', '新', '盛', '丰', '达', '信', '优', '凯', '安', '宝', '泰', '利', '佳', '美',
            '捷', '锐', '博', '宏', '鑫', '科', '创', '智', '冠', '顺', '捷', '通', '光', '天', '龙', '航',
            '联', '迅', '智', '捷', '航', '腾', '飞', '盛', '达', '诚', '益', '达', '和', '合', '伟', '欣',
            '豪', '峰', '华', '裕', '荣', '嘉', '业', '业', '隆', '顺', '益', '盛', '捷', '顺', '福', '安',
            '富', '高', '新', '新', '优', '胜', '亿', '阳', '隆', '鑫', '利', '佳', '益', '和', '美', '世',
            '弘', '万', '龙', '正', '浩', '荣', '庆', '达', '恒', '耀', '悦', '优', '邦', '源', '泰', '金',
            '万', '宝', '恒', '安', '康', '达', '广', '合', '通', '捷', '航', '顺', '瑞', '荣', '欣', '佳'
        ]
        company_name = ''.join(random.choice(characters) for _ in range(6)) + '公司'
        
        set_entry_value(self.ecompanyname, company_name)

    # 统一社会信用代码
    def random_credit_code(self):
        # 随机选择登记管理部门代码
        management_code = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'N', 'Y'])
        
        # 随机选择机构类别代码
        department_code = {
            '1': '1',
            '2': random.choice(['1', '9']),
            '3': random.choice(['1', '2', '3', '4', '5', '9']),
            '4': random.choice(['1', '9']),
            '5': random.choice(['1', '2', '3', '9']),
            '6': random.choice(['1', '2', '9']),
            '7': random.choice(['1', '2', '9']),
            '8': random.choice(['1', '9']),
            '9': random.choice(['1', '2', '3']),
            'A': random.choice(['1', '9']),
            'N': random.choice(['1', '2', '3', '9']),
            'Y': '1'
        }
        institution_code = department_code[management_code]
        
        # 读取行政区划码，这里假设我们已经有了行政区划码列表
        lines = read_file("/areaCode.txt")
        administrative_code = random.choice(lines)
        
        # 生成组织机构代码
        self.organization_code = generate_org_code()
        
        # 生成校验码
        usc_code = management_code + institution_code + administrative_code + self.organization_code.replace("-", "")

        check_digit = calculate_check_digit(usc_code)
        
        # 返回完整的统一社会信用代码
        set_entry_value(self.ecreditcode, usc_code + check_digit)

    # 组织机构代码
    def random_organ_code(self):

        set_entry_value(self.eorgancode, self.organization_code)

    # 中征码
    def random_pbc_code(self):
        # 加权因子
        weight_factor = [1, 3, 5, 7, 11, 2, 13, 1, 1, 17, 19, 97, 23, 29]
        # 生成前14位的随机字符（包括数字和大写字母）
        chars = '0123456789'
        id_code = ''.join(random.choices(chars, k=14))

        # 计算校验位
        num = 0
        for i in range(14):
            if 'A' <= id_code[i] <= 'Z':
                temp = ord(id_code[i]) - 55  # 字母转数字
            else:
                temp = ord(id_code[i]) - 48  # 数字直接转
            num += temp * weight_factor[i]

        # 取余+1
        residue = num % 97 + 1

        # 将校验位拼接到前14位生成完整的中征码
        code = f"{residue:02d}"  # 校验位确保两位
        
        set_entry_value(self.epbccode, id_code + code)

    # 随机一组双色球号码(6个红球 1个蓝球)
    def random_lotto(self):
        red_balls = random.sample(range(1, 34), 6)
        red_balls.sort()
        
        blue_ball = random.choice(range(1, 17))
        
        red_balls_str = ' '.join(map(str, red_balls))
        blue_ball_str = str(blue_ball)

        self.lotto = '今日双色球百万大奖: ' + red_balls_str + ' ' + blue_ball_str

    def random_boc_code(self): 
        bank_card_no = generate_bank_card('BOC')

        set_entry_value(self.boccode, bank_card_no)

    def random_ccb_code(self): 
        bank_card_no = generate_bank_card('CCB')

        set_entry_value(self.ccbcode, bank_card_no)

    def random_abc_code(self): 
        bank_card_no = generate_bank_card('ABC')

        set_entry_value(self.abccode, bank_card_no)
    
    def random_icbc_code(self): 
        bank_card_no = generate_bank_card('ICBC')

        set_entry_value(self.icbccode, bank_card_no)

    def random_psbc_code(self):
        bank_card_no = generate_bank_card('PSBC')

        set_entry_value(self.psbccode, bank_card_no)

    def generatorAll(self):
        self.random_name()
        self.random_phone_number()
        self.random_id_card()
        self.random_company_name()
        self.random_credit_code()
        self.random_organ_code()
        self.random_pbc_code()
        self.random_boc_code()
        self.random_ccb_code()
        self.random_abc_code()
        self.random_icbc_code()
        self.random_psbc_code()

    def resetAll(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def copy_to_clipboard(self, text):
        cp.copy(text)
        showinfo('成功', '复制成功')

    def run(self):
        root = tk.Tk()
        self.random_lotto()
        self.show_ui(root)
        root.protocol('WM_DELETE_WINDOW', lambda: sys.exit(0))
        root.mainloop()

# if __name__ == "__main__":
#     number_gen = numberGen()
#     number_gen.run()
