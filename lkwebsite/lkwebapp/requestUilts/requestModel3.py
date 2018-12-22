#coding=utf8
import requests
import json
from requestConfig import *
import re
class requestClass():
    def __init__(self):
        self.header=REQUEST_HEADER
        self.login_agents_data=LOGINAGENTSDATA
        self.login_agent_data=LOGINAGENTDATA
        self.url=URL
        self.isagents=ISAGENTS
    #判断是否存在一个账号管理多个分理商
    def get_request(self,isagents):
        s=requests.session()
        if (isagents):
            s.post(url=self.url+"/bus/login",data=self.login_agents_data)
            login_request_agent=s.post(url=self.url+"/bus/login",data=self.login_agent_data)
           
            #print(login_request_agent.text)
            return login_request_agent
        else:
            login_request_agent=s.post(url=self.url+"/bus/login",data=self.login_agents_data)
        return login_request_agent

    #获取cookies
    def get_cookies(self):
        #进行登陆操作获取authKey
        login_request_agent=self.get_request(self.isagents)
        print(login_request_agent.text)
        UserTenant=re.findall(r'\.(\d+)', login_request_agent.headers['Set-Cookie'])[0]

        self.header['User-Tenant']=UserTenant
        authKey=login_request_agent.cookies.get_dict()['SSO_SERVICE_TOKEN_KEY.{0}'.format(UserTenant)]
        print(authKey)
        #获取cookies
        request_goMenu=requests.get(self.url+'/bus-portal/index/goMenu.do?tenantId={0}&authKey={1}'.format(UserTenant,authKey))
        print(request_goMenu.headers)
        self.header['Cookie']=''.join('name=value;SESSION=')+request_goMenu.cookies.get_dict()['SESSION']+";versionpid=3;SSO_SERVICE_TOKEN_KEY.{0}=".format(UserTenant)+authKey+";SSO_TENANT_ID={0};SYS_I18N=zh-CN; SSO_ACC=13760490584;SSO_CLIENT_TOKEN_KEY.700.{1}=".format(UserTenant,UserTenant)+request_goMenu.cookies.get_dict()['SSO_CLIENT_TOKEN_KEY.700.{0}'.format(UserTenant)]

        return self.header
    def get_rquest_result(self,requestUrl,requesParame):
        header=self.get_cookies()
        #header['Cookie']="name=value; SESSION=050c9559-1dc4-410a-8b4b-8aa74890c84a; SSO_ACC=13760490584; versionpid=3; SSO_SERVICE_TOKEN_KEY.72=TGT-b13ffb28-d363-4c02-85c8-41e079753dc7; SYS_I18N=zh-CN; SSO_TENANT_ID=72; SSO_CLIENT_TOKEN_KEY.700.72=ST-0abafaa4-64b2-47ef-98f2-38afb966c2e3"
        #header['Cookie']="name=value; SESSION=3b469f96-248e-499f-b8e8-8dc4d0f58b8d; SSO_ACC=13760490584; versionpid=3; SSO_SERVICE_TOKEN_KEY.72=TGT-0effb861-35f9-4312-99d5-28232ac74370; SYS_I18N=zh-CN; SSO_TENANT_ID=72; SSO_CLIENT_TOKEN_KEY.700.72=ST-01d2be77-cebc-4c5a-83df-884d8d85649f"
        print(header)
        request=requests.post(url=requestUrl,
                              json=requesParame,
                              headers=header)
        return {'result':json.loads(json.dumps(request.text))}

if __name__ == '__main__':
    q=requestClass()
    data={"orderName":"5","custId":"744","settlementCycle":"3","businessUser":"1153","contactsName":"55","contactsTel":"13526478422","orderDetail":"","signingDate":"2018-12-20","dutyParagraph":"","lineBusinessType":"1","orderTravelInfoReqDtos":[]}
    print(q.get_rquest_result('http://202.105.139.120:8200/bus-portal/opOrder/addOpOrder.json',data))