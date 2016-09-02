import urllib
import urllib2
import cookielib

# create opener
cookie = cookielib.CookieJar()
httphandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie), httphandler, httpsHandler)

# request info
postdata = urllib.urlencode(
	{
		'username':'adamwu',
		'password':'123456'
	}
	)
headers = {
	'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
req = urllib2.Request(url='http://www.baidu.com/', headers=headers)

try:
	response = opener.open(req)
	print response.read()
except urllib2.HTTPError, e:
	print "error code:", e.code
except urllib2.URLError, e:
	print "reason:", e.reason