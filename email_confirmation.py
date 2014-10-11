import requests
import traceback
import urllib2
import time
from main import proxy

class ConfirmEmail:

    def __init__(self):
        self.base_url='https://www.twitter.com/'
    
    def make_request(self,url,request_type='get',headers_addons=None,params=None,cookies=None,data=None):
        headers={}
        headers['Host']='twitter.com'
        headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
        if headers_addons:
            headers.update(headers_addons)
        if request_type=='get':
            response=requests.get(url,params=params,headers=headers,cookies=cookies,verify=False,timeout=60,allow_redirects=False)

        else:
            response=requests.post(url,data=data,headers=headers,cookies=cookies,verify=False,timeout=60,allow_redirects=False)
        return response
        

    def click_on_confirmation_link(self,confirm_link):
        print "%%%%%%%%%%%%%%%%%%%%%% clicking on confirmation link %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        try:
            response=self.make_request(confirm_link,request_type='get')

            if response.status_code==302:
                # print response.content
                # print response.headers
                return response
            else:
                print "clicking on link failed"
                print response.status_code
                print response.content
                return False
        except Exception as e:
            print "Exception in clicking link"
            print traceback.format_exc(e)
            return False

    def click_on_redirect_link(self,redirect_link,cookies,params):
        print "%%%%%%%%%%%%%%%%%%%%%% clicking on redirect link %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        try:
            response=self.make_request(redirect_link,request_type='get',headers_addons=None,params=params,cookies=cookies)
            if response.status_code==200:
                return response
            else:
                print response.status_code
                print response.content
                return False
        except Exception as e:
            print "Exception in clicking on redirect link"
            print traceback.format_exc(e)
            return False

    def login(self,cookies,payload,referer_link):
        print "%%%%%%%%%%%%%%%%%%%%%% Login %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        try:
            headers={}
            headers['Origin']='https://twitter.com'
            headers['Referer']=referer_link
            url=self.base_url+'sessions'
            response=self.make_request(url,request_type='post',headers_addons=headers,cookies=cookies,params=None,data=payload)
            if response.status_code==302:
                return response
            else:
                print response.content
                return False

        except Exception as e:
            print "Exception in login"
            print traceback.format_exc(e)
            return False

    def click_on_link_after_login(self,url,cookies,referer_link):
        print "%%%%%%%%%%%%%%%%%%%%%% clicking on link after login %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        try:
            headers={}
            headers['Referer']=referer_link
            response=self.make_request(url,request_type='get',headers_addons=headers,cookies=cookies)
            if response.status_code==302:
                print response.content
                return response
            else:
                print response.content
                return False

        except Exception as e:
            print "Exception in clicking link after login"
            print traceback.format_exc(e)
            return False

    def click_on_twitter_home(self,url,cookies,referer_link):
        print "%%%%%%%%%%%%%%%%%%%%%% Sending to home page %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        try:
            headers={}
            headers['Referer']=referer_link
            response=self.make_request(url,request_type='get',headers_addons=headers,cookies=cookies)
            if response.status_code==200:
                return response
            else:
                print response.content
                return False
        except Exception as e:
            print "Exception in sending to home page"
            print traceback.format_exc(e)
            return False

    def confirm_email(self,confirm_link,email,password):    
        response=self.click_on_confirmation_link(confirm_link)
        if not response:
            return False
        referer_link=response.headers['location']
        print "referer_link:%s"%referer_link
        cookies={}
        cookies=response.cookies
        
        print "Cookies:%s"%cookies
        redirect_link=urllib2.unquote(referer_link)
        params={}
        key=redirect_link.split('=')[0].split('?')[1]
        value=redirect_link.split('=')[1]
        params[key]=value

        time.sleep(5)
        response=self.click_on_redirect_link(redirect_link,cookies,params)
        if not response:
            return False
        authenticity_token=str(response.content).split('authenticity_token')[1].split('"> </form>')[0].split('value="')[1].split('">')[0]
        print "authenticity_token:%s"%authenticity_token
        cookies={}
        cookies=response.cookies
        print "Cookies:%s"%cookies
        payload={}
        bot_user={}
        bot_user['email']=email
        bot_user['password']=password
        payload['session[username_or_email]']=bot_user['email']
        payload['session[password]']=bot_user['password']
        payload['authenticity_token']=authenticity_token
        payload['scribe_log']=''
        payload['redirect_after_login']=value
        payload['remember_me']=1

        print "Payload:%s"%payload
        time.sleep(5)
        response=self.login(cookies,payload,referer_link)
        if not response:
            return False
        link_after_login=response.headers['location']
        print "Link after login:%s"%link_after_login
        cookies={}
        cookies=response.cookies
        auth_token=cookies['auth_token']
        print "Cookies%s"%cookies
        time.sleep(5)
        response=self.click_on_link_after_login(link_after_login,cookies,referer_link)
        if not response:
            return False
        cookies=response.cookies
        cookies['auth_token']=auth_token
        url=response.headers['location']

        time.sleep(2)
        response=self.click_on_twitter_home(url,cookies,referer_link)
        if not response:
            return False
        else:
            return True


if __name__=='__main__':
    email=ConfirmEmail()
    link='verification link fetched from your email account.'
    email="your email id on twitter"
    password='your password on twitter'
    email.confirm_email(link)
    



