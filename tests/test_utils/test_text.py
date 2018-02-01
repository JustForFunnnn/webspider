# coding=utf-8
from unittest import TestCase

from webspider.utils.text import to_plaintext


class TestUtilText(TestCase):
    def test_to_plaintext(self):
        init_text = '<br/>abcd \n '
        self.assertEqual(to_plaintext(content=init_text, strip=False), 'abcd  ')

        init_text = '<br/>abcd  \n  '
        self.assertEqual(to_plaintext(content=init_text, strip=True), 'abcd')

        init_text = '<br/>abcd  \n  '
        self.assertEqual(to_plaintext(content=init_text, pattern=u'a|b', strip=False), '<r/>cd  \n  ')
