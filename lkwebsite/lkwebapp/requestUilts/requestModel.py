#coding=utf8
import requests
import json
from .requestConfig import *
import re
import http.client
class requestClass():
    def __init__(self):
        self.header=REQUEST_HEADER
        self.login_agents_data=LOGINAGENTSDATA
        self.login_agent_data=LOGINAGENTDATA
        self.url=URL
        self.request_url=REQUEST_URL
        self.isagents=ISAGENTS
    #判断是否存在一个账号管理多个分理商
    def get_request(self,isagents):
        s=requests.session()
        if (isagents):
            s.post(url=self.url+"/bus/login",data=self.login_agents_data)
            login_request_agent=s.post(url=self.url+"/bus/login",data=self.login_agent_data)
            return login_request_agent
        else:
            login_request_agent=s.post(url=self.url+"/bus/login",data=self.login_agents_data)
        return login_request_agent

    #获取cookies
    def get_cookies(self):
        #进行登陆操作获取authKey
        login_request_agent=self.get_request(self.isagents)
        UserTenant=re.findall(r'\.(\d+)', login_request_agent.headers['Set-Cookie'])[0]

        self.header['User-Tenant']=UserTenant
        authKey=login_request_agent.cookies.get_dict()['SSO_SERVICE_TOKEN_KEY.{0}'.format(UserTenant)]
        #获取cookies
        request_goMenu=requests.get(self.url+'/bus-portal/index/goMenu.do?tenantId={0}&authKey={1}'.format(UserTenant,authKey))
        self.header['cookie']=''.join('SESSION=')+request_goMenu.cookies.get_dict()['SESSION']+";versionpid=3;SSO_SERVICE_TOKEN_KEY.{0}=".format(UserTenant)+authKey+";SYS_I18N=zh-CN; SSO_ACC=13760490584;SSO_CLIENT_TOKEN_KEY.700.{0}=".format(UserTenant)+request_goMenu.cookies.get_dict()['SSO_CLIENT_TOKEN_KEY.700.{0}'.format(UserTenant)]

        return self.header
    def get_rquest_result(self,requestPath,requesParame):
        conn = http.client.HTTPConnection(self.request_url)
        headers = self.get_cookies()
        print(headers["cookie"])
        conn.request("POST", requestPath, requesParame, headers)
        
        res = conn.getresponse()
        data = res.read()
        
        return {'result':json.loads(json.dumps(data.decode("utf-8")))}

if __name__ == '__main__':
    q=requestClass()
    data="currentPage=1&pageSize=20&custId=&custName=&orderState=&orderStateName=&orderCode=&effDate=2018-12-01&expDate=2018-12-31&orderIds=&tenantIds=72%2C106%2C110%2C111"
    print(q.get_rquest_result('/bus-portal/tenantInfo/getTenantTree.json',data))