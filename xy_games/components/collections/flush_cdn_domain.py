# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from pipeline.conf import settings
from pipeline.core.flow.activity import Service, StaticIntervalGenerator
from pipeline.component_framework.component import Component
import datetime,re,json,requests
import base64,hmac

__group_name__ = _(u"轩辕游戏(XY_GAMES)")


class OpenApiDemo:
    def getDate(self):
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        date_gmt = datetime.datetime.utcnow().strftime(GMT_FORMAT)
        return date_gmt

    def getAuth(self, userName, apikey, date):
        signed_apikey = hmac.new(apikey.encode('utf-8'), date.encode('utf-8'), sha256).digest()
        signed_apikey = base64.b64encode(signed_apikey)
        signed_apikey = userName + ":" + signed_apikey.decode()
        signed_apikey = base64.b64encode(signed_apikey.encode('utf-8'))
        return signed_apikey

    def createHeader(self, accept, authStr, date):
        headers = {
            'Date': date,
            'Accept': accept,
            'Content-type': accept,
            'Authorization': 'Basic ' + authStr.decode()
        }
        return headers

    def sendRequest(self, httpUrl, method, httpBodyParams, headers):
        if method.upper() == 'POST':
            resp = requests.post(httpUrl, data=httpBodyParams, headers=headers)
        elif method.upper() == 'GET':
            resp = requests.get(httpUrl, headers=headers)
        #self.printResp(resp)
        r = {'text':resp.text,'code':resp.status_code}
        return r


class FlushCdnService(Service):
    __need_schedule__ = False

    def get_domain_name(openApiDemo , userName , apikey , regular):
        # 获取指定域名信息
        # 返回指定格式
        # <dir>https://downtm.f8rjk34s.cn/</dir><dir>https://downtm.foshandai.cn/</dir>
        str_msg = ''
        str_res = ''
        method = 'GET'
        accept = 'application/json'
        api_url = "https://open.chinanetcenter.com/api/domain"
        httpBodyParamsXML = ''

        date = openApiDemo.getDate()
        authStr = openApiDemo.getAuth(userName , apikey , date)
        headers = openApiDemo.createHeader(accept , authStr , date)
        res = openApiDemo.sendRequest(api_url , method , httpBodyParamsXML , headers)

        for i in json.loads(res['text']):
            if re.match(regular,i['domain-name']):
                str_msg = str_msg + i['domain-name'] + '\n'
                str_res = str_res + '<dir>https://' + i['domain-name'] + '/</dir>'
        dict = {'str_msg':str_msg,'str_res':str_res}
        return dict

    def flush_purge(openApiDemo,userName,apikey , dir_str):
        method = 'POST'
        accept = 'application/xml'
        api_url = "https://open.chinanetcenter.com/ccm/purge/ItemIdReceiver"
        httpBodyParamsXML = r'''<?xml version="1.0" encoding="utf-8"?>
                                <purge>
                                    <dirs>
                                        ''' + dir_str['dir'] + '''
                                    </dirs>
                                    <dir-action>expire</dir-action>
                                </purge>
                             '''
        date = openApiDemo.getDate()
        authStr = openApiDemo.getAuth(userName , apikey , date)
        headers = openApiDemo.createHeader(accept , authStr , date)
        res = openApiDemo.sendRequest(api_url , method , httpBodyParamsXML , headers)
        print(res['text'])
        if re.search(r'<code>1</code>' , res['text']):
            print('Sync domain name success!')


    def execute(self, data, parent_data):
        accesskey = data.get_one_of_inputs('accesskey')
        regular_expression = data.get_one_of_inputs('regular_expression')

        try:
            openApiDemo = OpenApiDemo()
            result = self.get_domain_name(openApiDemo , accesskey.split(',')[0] , accesskey.split(',')[1] , regular_expression)
            self.flush_purge(openApiDemo ,  accesskey.split(',')[0] , accesskey.split(',')[1] , result['str_res'])

            data.set_outputs('data',result)
            return True
        except:
            data.set_outputs('data' , {'str_msg':'failed!'})
            return False



    def outputs_format(self):
        return [
            self.OutputItem(name=u'刷新信息',key='str_msg',type='str')
        ]


class FlushCdnComponent(Component):
    name = _(u'推送网宿CDN(模糊匹配)')
    code = 'flush_cdn'
    embedded_form = True
    bound_service = FlushCdnService
    form = """
    (function(){
        $.atoms.flush_cdn = [
            {
                tag_code: "accesskey",
                type: "radio",
                attrs: {
                    name: gettext("网宿账号选择"),
                    items: [
                        {value: "yinchi,yinchi123.", name: gettext("银驰")},
                        {value: "axjs,axjs..123", name: gettext("安迅")},
                        {value: "njks,njks..123", name: gettext("凯硕")}
                    ],
                    default: "银驰",
                    hookable: true,
                    validation: [
                        {
                            type: "required"
                        }
                    ]
                }
            },
            {
                tag_code: "regular_expression",
                type: "textarea",
                attrs: {
                    name: gettext("正则"),
                    placeholder: gettext("正则表达式"),
                    hookable: true,
                    validation: [
                        {
                            type: "required"
                        }
                    ]
                }
            }
        ]
    })();"""

