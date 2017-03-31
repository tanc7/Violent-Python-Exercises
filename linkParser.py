from anonBrowser import *
from BeautifulSoup import BeautifulSoup
import os
import optparse
import re
import urllib2
from urlparse import urlsplit


def printLinks(url):
    ab = anonBrowser()
    ab.anonymize()
    page = ab.open(url)
    html = page.read()
    try:
        print '[+] Printing links from regex.'
        link_finder = re.compile('href="(.*?)"')
        links = link_finder.findall(html)
        for link in links:
            print link
    except:
        pass
    try:
        print '\n[+] Printing links from BeautifulSoup.'
        soup = BeautifulSoup(html)
        links = soup.findall(name='a')
        for link in links:
            if link.has_key('href'):
                print link['href']
    except:
        pass

def main():

    parser = optparse.OptionParser('usage%prog ' + '-u <target url>')
    parser.add_option('-u', dest='tgturl', type='string', help='specify target url')
    (options, args) = parser.parse_args()
    url = options.tgturl
    if url == None:
        print parser.usage
        exit(0)
    else:
        printLinks(url)

if __name__ == "__main__":
    main()
