# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from pipeline.conf import settings
from pipeline.core.flow.activity import Service, StaticIntervalGenerator
from pipeline.component_framework.component import Component
import telebot

__group_name__ = _(u"轩辕游戏(XY_GAMES)")


class SendTelegramService(Service):
    __need_schedule__ = False

    def execute(self, data, parent_data):
        receiver = data.get_one_of_inputs('receiver_input')
        content = data.get_one_of_inputs('text_input')

        try:
            bot = telebot.TeleBot('1085188337:AAHTAOgwfVmERK5CLuLDirpCz9xcLAeSw-U')
            bot.send_message(chat_id=receiver,text=content)
            return True
        except:
            return False



    def outputs_format(self):
        return []


class SendTelegramComponent(Component):
    name = _(u'发送纸飞机')
    code = 'telegram_custom'
    bound_service = SendTelegramService
    form = settings.STATIC_URL + 'components/static/xy_games/send_telegram.js'

