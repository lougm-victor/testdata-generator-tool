import random
import json
import os
import sys
from datetime import datetime

if getattr(sys, 'frozen', None):
    base_dir = os.path.join(sys._MEIPASS, 'asserts')
else:
    base_dir = os.path.join(os.path.abspath("."), 'asserts')

class LottoGenerator:
    def __init__(self, file_path='/lotto.json'):
        self.file_path = file_path
        self.lotto = self.load_lotto_data()

    def random_lotto(self):
        today = datetime.now().date()

        # 检查是否已经生成过今天的数据
        if self.lotto and self.lotto.get('date') == str(today):
            # print("已生成今日的数据:", self.lotto['numbers'])
            return self.lotto['numbers']

        # 生成新的数据
        red_balls = random.sample(range(1, 34), 6)
        red_balls.sort()

        blue_ball = random.choice(range(1, 17))

        red_balls_str = ' '.join(map(str, red_balls))
        blue_ball_str = str(blue_ball)

        # 保存到实例变量中
        self.lotto = {
            'date': str(today),
            'numbers': f'今日双色球百万大奖: {red_balls_str} {blue_ball_str}'
        }

        # 保存数据到文件
        self.save_lotto_data()

        # print("生成新的今日数据:", self.lotto['numbers'])
        return self.lotto['numbers']

    def save_lotto_data(self):
        with open(base_dir + self.file_path, 'w') as f:
            json.dump(self.lotto, f)

    def load_lotto_data(self):
        if os.path.exists(base_dir + self.file_path):
            with open(base_dir + self.file_path, 'r') as f:
                return json.load(f)
        return None
