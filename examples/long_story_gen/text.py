import logging
import json

from textpy import code, text

CACHE_DIR = "./cache"

@text(cache=CACHE_DIR)
# 你是一个经验丰富的小说作家，擅长创作长篇小说。你将根据提供的段落、人物、设定和上一段内容，生成完整且连贯的小说内容。
# 你只需要在所给信息的基础上进行扩写，不需要添加新的情节或人物。
# 尽可能多地分段，保证读者阅读时不会感到疲劳。
# 生成400至500字的内容
# 返回一个字符串，包含生成的小说内容。
def writer(*,paragraph:str, caracters:dict, settings:dict,context:str) -> str: ...

@text(cache=CACHE_DIR)
# 你是一个经验丰富的小说作家，擅长对文章进行风格化改写。
# 你将根据提供的段落和风格，将段落改写为指定风格的内容。
# 你只需要在所给信息的基础上进行改写，不需要添加新的情节或人物。
# 段落结构和字数不能有太大变化
# 返回一个字符串，包含改写后的段落内容。
def critical(*,paragraph:str, style:str) -> str: ...