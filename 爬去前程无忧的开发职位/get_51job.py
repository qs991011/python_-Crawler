#-*- coding:utf-8 -*-

import urllib.request
import  requests
from requests.exceptions import  RequestException
import  re
from bs4  import  BeautifulSoup
import codecs
#爬取51job上的ios职位数
header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
}

DOWN_URL = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=030200%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword=iOS%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88&keywordtype=2&curr_page=1&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&dibiaoid=0&confirmdate=9'
SHENZHEN = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000&keyword=iOS%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9'

def get_one_page(url):
    try:
        response = requests.get(url,headers=header)
        if response.status_code == 200:
            return response.content
        return None
    except RequestException:
        return None

def parse_one_page(html):
    #html = html.decode('GBK').encode('utf-8')

    soup = BeautifulSoup(html,'html.parser')
    joblist = soup.find_all('div',attrs={'class':'el'})

    # print(joblist.count())
    data = []
    for jobdiv in joblist:
         jobCompany = jobdiv.find('span', attrs={'class': 't2'})
         jobsalary = jobdiv.find('span', attrs={'class': 't4'})
         if jobCompany:
             i = {}
             jobname = jobCompany.getText()
             jobsal = jobsalary.getText()
             i['companyName'] = jobname
             i['companySalary'] = jobsal
             #print(jobname)

             data.append(i)
    #获取下一页的链接
    next_pages = soup.find_all('li',attrs={'class','bk'})
    for page in next_pages:
        tag_a = page.find('a')
        if tag_a:
            href = tag_a['href']
            title = tag_a.string
            if title == '下一页':
                return data,href
    return data,None

def processInfo(info):
    try:
        file = open('广州.txt','a')
        for p in info:
            line = str(p['companyName']) + ',' + str(p['companySalary'] + '\n')
            file.write(line)
        file.close()

    except:
        print('Process except')




    # with codecs.open('guang.txt','wb',encoding='utf-8') as fp:
    #     for p in info:
    #         line = str(p['companyName']) + ',' + str(p['companySalary']+'\n')
    #        # print(line)
    #         fp.write(line)


if __name__ == '__main__':
    kdList = [u'iOS']
    citylist = [u'广州',u'深圳']
    index = 1
    url = DOWN_URL
    while url:
        html = get_one_page(url)
        jobs, url = parse_one_page(html)

        processInfo(jobs)



    # html = get_one_page(url)
    #parse_one_page(html)
