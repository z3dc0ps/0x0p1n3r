#!/usr/bin/env python3
# takeover - subdomain takeover finder
# coded by M'hamed (@m4ll0k) Outaadi 

import os 
import json
import requests 
import urllib.parse
import concurrent.futures as thread
import urllib3
import getopt
import sys
import re


r ='\033[1;31m'
g ='\033[1;32m'
y ='\033[1;33m'
b ='\033[1;34m'
r_='\033[0;31m'
g_='\033[0;32m'
y_='\033[0;33m'
b_='\033[0;34m'
e ='\033[0m'

global _output
_output = []
global k_
k_ = {
    'domain'     : None,
    'threads'    : 1,
    'd_list'     : None,
    'proxy'      : None,
    'output'     : None,
    'timeout'    : None,
    'process'    : False,
    'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.36 Safari/537.36',
    'verbose'    : False,
    'dict_len'   : 0 
}

# index/lenght * 100
PERCENT = lambda x,y: float(x)/float(y) * 100

services = {
        'AWS/S3'          : {'error':r'The specified bucket does not exist'},
        'BitBucket'       : {'error':r'Repository not found'},
        'Github'          : {'error':r'There isn\\\'t a Github Pages site here\.'},
        'Shopify'         : {'error':r'Sorry\, this shop is currently unavailable\.'},
        'Fastly'          : {'error':r'Fastly error\: unknown domain\:'},

        'Ghost'           : {'error':r'The thing you were looking for is no longer here\, or never was'},
        'Heroku'          : {'error':r'no-such-app.html|<title>no such app</title>|herokucdn.com/error-pages/no-such-app.html'},
        'Pantheon'        : {'error':r'The gods are wise, but do not know of the site which you seek.'},
        'Tumbler'         : {'error':r'Whatever you were looking for doesn\\\'t currently exist at this address.'},
        'Wordpress'       : {'error':r'Do you want to register'},

        'TeamWork'        : {'error':r'Oops - We didn\'t find your site.'},
        'Helpjuice'       : {'error':r'We could not find what you\'re looking for.'},
        'Helpscout'       : {'error':r'No settings were found for this company:'},
        'Cargo'           : {'error':r'<title>404 &mdash; File not found</title>'},
        'Uservoice'       : {'error':r'This UserVoice subdomain is currently available!'},
        'Surge'           : {'error':r'project not found'},
        'Intercom'        : {'error':r'This page is reserved for artistic dogs\.|Uh oh\. That page doesn\'t exist</h1>'},

        'Webflow'         : {'error':r'<p class=\"description\">The page you are looking for doesn\'t exist or has been moved.</p>'},
        'Kajabi'          : {'error':r'<h1>The page you were looking for doesn\'t exist.</h1>'},
        'Thinkific'       : {'error':r'You may have mistyped the address or the page may have moved.'},
        'Tave'            : {'error':r'<h1>Error 404: Page Not Found</h1>'},

        'Wishpond'        : {'error':r'<h1>https://www.wishpond.com/404?campaign=true'},
        'Aftership'       : {'error':r'Oops.</h2><p class=\"text-muted text-tight\">The page you\'re looking for doesn\'t exist.'},
        'Aha'             : {'error':r'There is no portal here \.\.\. sending you back to Aha!'},
        'Tictail'         : {'error':r'to target URL: <a href=\"https://tictail.com|Start selling on Tictail.'},
        'Brightcove'      : {'error':r'<p class=\"bc-gallery-error-code\">Error Code: 404</p>'},
        'Bigcartel'       : {'error':r'<h1>Oops! We couldn&#8217;t find that page.</h1>'},
        'ActiveCampaign'  : {'error':r'alt=\"LIGHTTPD - fly light.\"'},

        'Campaignmonitor' : {'error':r'Double check the URL or <a href=\"mailto:help@createsend.com'},
        'Acquia'          : {'error':r'The site you are looking for could not be found.|If you are an Acquia Cloud customer and expect to see your site at this address'},
        'Proposify'       : {'error':r'If you need immediate assistance, please contact <a href=\"mailto:support@proposify.biz'},
        'Simplebooklet'   : {'error':r'We can\'t find this <a href=\"https://simplebooklet.com'},
        'GetResponse'     : {'error':r'With GetResponse Landing Pages, lead generation has never been easier'},
        'Vend'            : {'error':r'Looks like you\'ve traveled too far into cyberspace.'},
        'Jetbrains'       : {'error':r'is not a registered InCloud YouTrack.'},

        'Smartling'       : {'error':r'Domain is not configured'},
        'Pingdom'         : {'error':r'pingdom'},
        'Tilda'           : {'error':r'Domain has been assigned'},
        'Surveygizmo'     : {'error':r'data-html-name'},
        'Mashery'         : {'error':r'Unrecognized domain <strong>'},
        'Divio'           : {'error':r'Application not responding'},
        'feedpress'       : {'error':r'The feed has not been found.'},
        'readme'          : {'error':r'Project doesnt exist... yet!'},   
        'statuspage'      : {'error':r'You are being <a href=\'https>'},
        'zendesk'         : {'error':r'Help Center Closed'},
        'worksites.net'   : {'error':r'Hello! Sorry, but the webs>'}
}
def plus(string):
    print('{0}[ + ]{1} {2}'.format(g,e,string))

def warn(string,exit=not 1):
    print('{0}[ ! ]{1} {2}'.format(r,e,string))
    if exit:
        sys.exit()

def info(string):
    print('{0}[ i ]{1} {2}'.format(y,e,string))

def _info():
    return '{0}[ i ]{1} '.format(y,e)

def err(string):
    print(r'  |= [REGEX]: {0}{1}{2}'.format(y_,string,e))


def request(domain,proxy,timeout,user_agent):
        url = checkurl(domain)
        timeout = timeout
        proxies = {
        'http'  : proxy,
        'https' : proxy
        }
        redirect = True
        headers = {
            'User-Agent': user_agent
        }
        try:
                req = requests.packages.urllib3.disable_warnings(
            urllib3.exceptions.InsecureRequestWarning
            )
                req = requests.get(
                url = url,
                headers = headers,
                verify = False,
                allow_redirects = redirect,
                timeout = int(timeout) if timeout != None else None,
                proxies = proxies
                )
                return req.status_code,req.content
        except Exception as err:
            pass;

def find(status,content,ok):
        for service in services:
                for values in services[service].items():
                        if re.findall(str(values[1]),str(content),re.I) and int(status) in range(201 if ok is False else 200,599):
                                return str(service),str(values[1])

def banner():
        print("\n   /~\\")
        print("  C oo   ---------------")
        print(" _( ^)  |T|A|K|E|O|V|E|R|")
        print("/   ~\\  ----------------")
        print("#> by M'hamed (@m4ll0k) Outaadi")
        print("#> http://github.com/m4ll0k")
        print("-"*40)

def help(_exit_=False):
        
        print("Usage: %s [OPTION]\n"%sys.argv[0])
        print("\t-d\tSet domain URL (e.g: www.test.com)")
        print("\t-t\tSet threads, default 1")
        print("\t-l\tScan multiple targets in a text file")
        print("\t-p\tUse a proxy to connect the target URL")
        print("\t-o\tUse this settings for save a file, args=json or text")
        print("\t-T\tSet a request timeout,default value is 20 seconds")
        print("\t-k\tProcess 200 http code, cause more false positive")
        print("\t-u\tSet custom user agent (e.g: takeover-bot)")
        print("\t-v\tVerbose, print more info\n")
        if _exit_:
                sys.exit()

def checkpath(path):
        if os.path.exists(path):
                return path
        elif os.path.isdir(path):
                warn('"%s" is directory!',1)
        elif os.path.exists(path) is False:
                warn('"%s" not exists!'%path,1)
        else:
                warn('Error in: "%s"'%path,1)

def readfile(path):
        return [x.strip() for x in open(checkpath(path),'r')]

def checkurl(url):
        o = urllib.parse.urlsplit(url)
        if o.scheme  not  in ['http','https','']:
                warn('Scheme "%s" not supported!'%o.scheme,1)
        if o.netloc == '':
                return 'http://' + o.path
        elif o.netloc:
                return o.scheme + '://' + o.netloc 
        else:
                return 'http://' + o.netloc 

def print_(string):
    sys.stdout.write('\033[1K')
    sys.stdout.write('\033[0G')
    sys.stdout.write(string)
    sys.stdout.flush()

def runner(k):
        threadpool = thread.ThreadPoolExecutor(max_workers=k.get('threads'))
        if k.get('verbose'):
            info('Set %s threads..'%k.get('threads'))
        futures = (threadpool.submit(requester,domain,k.get("proxy"),k.get("timeout"), k.get("user_agent"),
                k.get("output"),k.get('process'),k.get('verbose')) for domain in k.get("domains"))
        for i,results in enumerate(thread.as_completed(futures)):
            pass

def requester(domain,proxy,timeout,user_agent,output,ok,v):
        code,html = request(domain,proxy,timeout,user_agent)
        service,error = find(code,html,ok)
        if service and error:
                if output:
                    _output.append((domain,service,error))
                    if v and not k_.get('d_list'):
                        plus('%s service found! Potential domain takeover found! - %s'%(service,domain))
                    elif v and k_.get('d_list'):
                        print("")
                        plus('%s service found! Potential domain takeover found! - %s'%(service,domain))
                else:
                    if k_.get('d_list'):
                        print("")
                        plus('%s service found! Potential domain takeover found! - %s'%(service,domain))
                    elif not k_.get('d_list'):
                        plus('%s service found! Potential domain takeover found! - %s'%(service,domain))
                    if v:
                        err(error)

def savejson(path,content,v):
    if v and not k_.get('d_list'):
        info('Writing file..')
    elif v and k_.get('d_list'):
        print("")
        info("Writing file..")
    a = {}
    b = {"domains":{}}
    for i in content:
        a.update({i[0]:{'service':i[1],'error':i[2]}})
    b['domains'] = a
    with open(path,'w+') as outjsonfile:
        json.dump(b,outjsonfile,indent=4)
        outjsonfile.close()
    info('Saved at '+path+'..')

def savetxt(path,content,v):
    if v and not k_.get('d_list'):
        info('Writing file..')
    elif v and k_.get('d_list'):
        print("")
        info("Writing file..")
    br = '-'*40
    bf = '='*40
    out = ''+br+'\n'
    for i in content:
        out += 'Domain\t: %s\n'%i[0]
        out += 'Service\t: %s\n'%i[1]
        out += 'Error\t: %s\n'%i[2]
        out += ''+bf+'\n'
    out += ''+br+'\n'
    with open(path,'w+') as outtxtfile:
        outtxtfile.write(out)
        outtxtfile.close()
    info('Saved at '+path+'..')

def main(): 
        # -- 
        if len(sys.argv) < 2:
                help(1)
        try:
                opts,args = getopt.getopt(sys.argv[1:],
                        'd:l:p:o:t:T::u:kv',
                        ['d=','l=','p=','v','o=','t=','T=','u=','k'])
        except Exception as e:
                warn(e,1)
        for o,a in opts:
                if o == '-d': k_['domain'] = a 
                if o == '-t': k_['threads'] = int(a)
                if o == '-l': k_['d_list'] = a  
                if o == '-p': k_['proxy'] = a 
                if o == '-o': k_['output'] = a 
                if o == '-T': k_['timeout'] = int(a)
                if o == '-k': k_['process'] = True
                if o == '-u': k_['user_agent'] = a
                if o == '-v': k_['verbose'] = True

        if k_.get("domain") or k_.get("d_list"):
            
            domains = []
            if k_.get('verbose'):
                info('Starting..')
            
            if k_.get("d_list"):
                domains.extend(readfile(k_.get("d_list")))
            else: 
                domains.append(k_.get("domain"))
            k_['domains'] = domains
            k_['dict_len'] = len(domains)
            runner(k_)
            if k_.get("output"):
                if '.txt' in k_.get('output'):
                    savetxt(k_.get('output'),_output,k_.get('verbose'))
                elif '.json' in k_.get('output'):
                    savejson(k_.get('output'),_output,k_.get('verbose'))
                else:
                    warn('Output Error: %s extension not supported, only .txt or .json'%k_.get('output').split('.')[1],1)
        elif k_.get('domain') is None and k_.get('d_list') is None:
                help(1)
        
if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt) as e:
        sys.exit(0)
