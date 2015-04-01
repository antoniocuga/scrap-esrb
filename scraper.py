#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import urllib2
import socks
import socket
from cookielib import CookieJar
import csv


socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, "127.0.0.1", 9050)
socket.socket = socks.socksocket

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

domain = "http://www.esrb.org/ratings/search.jsp"

r1 = opener.open(domain)
rs1 = BeautifulSoup(r1.read(), 'html.parser')


def generateParams():

    values = {
        'offset': '25',
        'scroll': 'prev',
        'javaScript': '0',
        'titleOrPublisher': '',
        'ratingsCriteria': '',
        'fromHome': 'Platforms',
        'searchVersion': 'compact',
        'platformsCriteria': '',
        'searchType': 'title',
        'contentCriteria': '',
        'isIncluding': 'false',
    }

    return values


def getResult():

    filename = "games.csv"
    resultados = open('%s' % filename, 'wb')
    writer = csv.writer(resultados,
                        delimiter=',',
                        quotechar='"',
                        quoting=csv.QUOTE_ALL)

    #Escribimos las cabeceras de nuestro documento
    writer.writerow([
        'Title','Platforms', 'Rating',
        'Content Descriptors', 'Other',
        'Company', 'Rating Summary']
    )

    values = generateParams()

    for i in range(25,26000, 25):

        values['offset'] = i
        data = urllib.urlencode(values)
        html = opener.open(domain, data).read()
        parser = BeautifulSoup(html, 'html.parser')
        tables = parser.findAll('table', {'id': 'mytable'})

        if tables is not None:
            for table in tables:
                rows = table.findAll('tr')
                records = []
                cells = rows[0].findAll('td')
                records.append(cells[0].getText().encode('utf-8'))
                records.append(cells[2].getText().encode('utf-8'))
                records.append((cells[4].find('img')['src']).replace('..','http://www.esrb.org'))
                records.append(cells[6].getText().encode('utf-8'))                        
                records.append(cells[8].getText().encode('utf-8'))
                records.append(cells[10].getText().encode('utf-8'))
                summary = ((rows[1].getText().encode('utf-8')).strip()).replace('Rating Summary: ','')
                records.append(summary)
                writer.writerow(records)                      


if __name__ == '__main__':

    getResult()
