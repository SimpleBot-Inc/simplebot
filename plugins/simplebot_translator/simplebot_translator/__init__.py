# -*- coding: utf-8 -*-
import gettext
import os

from simplebot import Plugin
import translators as ts


class Translator(Plugin):

    name = 'Translator'
    version = '0.3.0'

    @classmethod
    def activate(cls, bot):
        super().activate(bot)
        localedir = os.path.join(os.path.dirname(__file__), 'locale')
        lang = gettext.translation('simplebot_translator', localedir=localedir,
                                   languages=[bot.locale], fallback=True)
        lang.install()
        cls.description = _('Translate text. Example: /tr en es hello world')
        cls.commands = [('/tr', ['<lang1>', '<lang2>', '<text>'],
                         _('Translate text from lang1 to lang2'), cls.tr_cmd)]
        cls.bot.add_commands(cls.commands)

    @classmethod
    def tr_cmd(cls, msg, text):
        chat = cls.bot.get_chat(msg)
        if not text:
            chat.send_text(cls.description)
        else:
            text = text.split()
            l1, l2, text = text[0], text[1], ' '.join(text[2:])
            text = ts.google(text=text, from_language=l1,
                             to_language=l2, host='https://translate.google.com')
            chat.send_text(text)