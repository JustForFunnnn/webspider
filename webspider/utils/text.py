# coding=utf-8
import re


def to_plaintext(content, pattern=r'<br/?>|\n', strip=True):
    """
    根据 pattern 过滤文本
    :param content: 需要过滤的文本
    :param pattern: 需要过滤内容的正则表达式
    :param strip: 是否去掉首尾空格
    :return:
    """
    plaintext = re.sub(pattern=pattern, repl='', string=content)
    if strip:
        plaintext = plaintext.strip()
    return plaintext


def replace_text_inside_space(content, fill_str=''):
    """
    替换 content 内多余空格
    :param content: 需要被替代的文本
    :param fill_str: 填补的字符串， 默认为''
    :return:
    """
    plaintext = re.sub(pattern='\s+', repl=fill_str, string=content)
    return plaintext
