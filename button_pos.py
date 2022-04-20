import itertools

slot_size = (615, 248)
slot_pos = ((17, 182), (650, 182), (17, 459), (650, 459))
slot_button_relevant_pos = {
    '开始招募干员': (220, 140, 390, 181),
    '聘用候选人': (220, 170, 390, 228),
    '立即招募': (390, 170, 520, 228),
}
recruit_button_pos = {
    '增加小时': (380, 127, 520, 173),
    '减少小时': (380, 274, 520, 320),
    '增加分钟': (545, 127, 690, 173),
    '减少分钟': (545, 274, 690, 320),
    '刷新标签': (910, 450, 1032, 473),
    'tags': ((376, 360), (543, 360), (710, 360), (376, 432), (543, 432)),
    'tag_size': (142, 45),
    '开始招募': (887, 556, 1070, 606),
    'skip': (1174, 10, 1268, 78),
    '确认': (873, 474, 1050, 540)
}


def get_slot_button_pos(button: str, slot: (int, int)) -> list:
    pos = slot_button_relevant_pos[button]
    return list(map(sum, zip(pos, itertools.cycle(slot))))


def get_tags_button_pos(index):
    tag_pos = recruit_button_pos['tags'][index]
    tag_size = recruit_button_pos['tag_size']
    return tag_pos[0], tag_pos[1], tag_pos[0] + tag_size[0], tag_pos[1] + tag_size[1]
