import itertools
import json
import os
import random
import time

from screenshot import ScreenShot
from button_pos import slot_pos, slot_button_relevant_pos, get_slot_button_pos, recruit_button_pos, get_tags_button_pos
from adb_variable import device_name

adb_devices = os.popen('adb devices').read()
if device_name not in adb_devices:
    print('Trying to connect to %s' % device_name)
    os.popen('adb connect %s' % device_name).read()

manual_tags = ['高级资深干员', '资深干员', '支援机械']

with open('recruit_information.json', 'r', encoding='utf-8') as file:
    op_dict = json.loads(file.read())
tag_dict = {}
reg_dict = {}
for name, info in op_dict.items():
    tag_list = info['tags']
    star = info['星级']
    tag_list.append(info['职业'] + '干员')
    if star == 2:
        tag_list.append('新手')
    elif star == 5:
        tag_list.append('资深干员')
    elif star == 6:
        tag_list.append('高级资深干员')
    for tag in tag_list:
        if tag in tag_dict:
            tag_dict[tag].add(name)
        else:
            tag_dict[tag] = {name}
    reg_dict[info['报到']] = name


def click(button, sleep: float = 1, slot: bool = None):
    if button in slot_button_relevant_pos:
        button_pos = get_slot_button_pos(button, slot)
    elif button in recruit_button_pos:
        button_pos = recruit_button_pos[button]
    else:
        button_pos = button
    click_pos = random_click_pos(button_pos)
    command = 'adb -s %s shell input tap %d %d' % (device_name, click_pos[0], click_pos[1])
    os.system(command)
    time.sleep(sleep)


def random_click_pos(button_pos):
    dx = int((button_pos[2] - button_pos[0]) * 0.1)
    dy = int((button_pos[3] - button_pos[1]) * 0.1)
    x = random.randint(button_pos[0] + dx, button_pos[2] - dx)
    y = random.randint(button_pos[1] + dy, button_pos[3] - dy)
    return x, y


def click_tags(chosen_tags_index):
    for i in chosen_tags_index:
        button = get_tags_button_pos(i)
        click(button)


def get_score(tags):
    if len(tags) == 0:
        return 300 + 5
    possible_result = tag_dict[tags[0]]
    for i in range(1, len(tags)):
        possible_result = possible_result & tag_dict[tags[i]]
    possible_result = set(
        filter(lambda x: 3 <= op_dict[x]['星级'] < (6 if '高级资深干员' not in tag_list else 7), possible_result))
    if possible_result != set():
        star_min = min([op_dict[name]['星级'] for name in possible_result])
        star_max = max([op_dict[name]['星级'] for name in possible_result])
        score = star_min * 100 - 10 * len(tags) + star_max
        return score
    else:
        return 0


def choose_tags():
    recruit_shot = ScreenShot('tag')
    tags = recruit_shot.get_tags()
    for tag in manual_tags:
        if tag in tags:
            exit("出现{tag}，请人工选择".format(tag=tag))
    all_possible_comb = []
    for i in range(4):
        all_possible_comb.extend(list(itertools.combinations(tags, i)))
    all_possible_comb.sort(key=get_score, reverse=True)
    chosen_tags = all_possible_comb[0]
    tag_to_index = dict(zip(tags, range(5)))
    return [tag_to_index[tag] for tag in chosen_tags]


def recruit():
    can_refresh = True
    for slot in slot_pos:
        # 检测槽位状态
        curr_status = ScreenShot('status').recruit_status(slot)
        if curr_status == 'done':
            # 已经完成招募：聘用并开始新招募
            click('聘用候选人', slot=slot)
            click('skip', sleep=3)
            # TODO check recruit result
            click('skip', sleep=3)
        elif curr_status == 'empty':
            # 空闲：开始招募
            pass
        elif curr_status == 'recruiting':
            # 正在招募：不加速
            continue
        click('开始招募干员', slot=slot)
        chosen_tags_index = choose_tags()
        # 如果未选择tags, 刷新tags
        while can_refresh and chosen_tags_index == []:
            can_refresh = ScreenShot('refresh').refresh_status()
            if can_refresh:
                click('刷新标签')
                click('确认', sleep=2)
                chosen_tags_index = choose_tags()
        click_tags(chosen_tags_index)
        # TODO select time function
        click('减少小时')
        click('开始招募')


if __name__ == '__main__':
    recruit()
