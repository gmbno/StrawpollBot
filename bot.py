import sys
import time
import urllib
import urllib2
import bs4


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

def init(id, file):
    try:
        f = open(file, 'r')
    except Exception:
        print '\033[92m[OK]\033[0m file not found.',
    req = urllib2.Request('http://www.strawpoll.me/%s' % id, headers=headers)
    content = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(content, 'html5lib')
    sectoken = soup.find('input', id='field-security-token')['value']
    authtoken = soup.find('input', id='field-authenticity-token')['name']
    opts = soup.find('div', id='field-options').find_all('div')
    optz = []
    for i in range(len(opts)):
        opt = opts[i]
        name = opt.find('label').get_text()
        value = opt.find('input')['value']
        optz.append({'name': name, 'value': value})
        print '%d:' % (i+1), name, '(%s)' % value
    opt = optz[int(raw_input('Choice: ')) - 1]
    form_vals={'security-token':sectoken, authtoken:'', 'options':opt['value']}
    form_vals = urllib.urlencode(form_vals)
    for ip in f:
	print 'trying proxy ip: %s' % ip,
	proxy = urllib2.ProxyHandler({'http': ip})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	try:
            req = urllib2.Request('http://www.strawpoll.me/%s' % id, data=form_vals, headers=headers)
	    urllib2.urlopen(req, timeout=10)
            print '\033[92m[OK]\033[0m vote done...\n'
        except Exception as e:
            print '\033[91m[KO]\033[0m %s, keep going...\n' % e

if __name__ == '__main__':
    if len(sys.argv[1:]):
        init(sys.argv[1], sys.argv[2])
    else:
        print 'Usage: python %s [strawpoll_id] [proxy_list_file]' % sys.argv[0]

