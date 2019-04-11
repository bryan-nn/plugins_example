# -*- coding: utf-8 -*-

import logging

from django.utils.translation import ugettext_lazy as _

from pipeline.conf import settings
from pipeline.core.flow.activity import Service, StaticIntervalGenerator
from pipeline.component_framework.component import Component

from custom_plugins.components.collections.utils_1 import utils_1_print
from custom_plugins.components.utils_2 import utils_2_print

__group_name__ = _(u"远程自定义原子2(CUS2)")

logger = logging.getLogger('celery')

class Pause2Service(Service):
    __need_schedule__ = False

    def execute(self, data, parent_data):
        logger.info('log from Pause2Service')
        return True
        

    def outputs_format(self):
        return []


class Pause2Component(Component):
    name = _(u'远程测试2')
    code = 'pause2_node'
    bound_service = Pause2Service
    form = settings.STATIC_URL + 'components/atoms/bk/pause.js'
