import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
import json  # json import하기
import urllib.request
import warnings
import signaturehelper
import pyperclip
print("""\


          _____                    _____                    _____                    _____
         /\    \                  /\    \                  /\    \                  /\    \
        /::\    \                /::\    \                /::\    \                /::\____\
        \:::\    \              /::::\    \              /::::\    \              /:::/    /
         \:::\    \            /::::::\    \            /::::::\    \            /:::/    /
          \:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/    /
           \:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/____/
           /::::\    \      /::::\   \:::\    \      /::::\   \:::\    \      /::::\    \
  _____   /::::::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \    /::::::\____\________
 /\    \ /:::/\:::\    \  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\____\  /:::/\:::::::::::\    \
/::\    /:::/  \:::\____\/:::/  \:::\   \:::\____\/:::/  \:::\   \:::|    |/:::/  |:::::::::::\____/
\:::\  /:::/    \::/    /\::/    \:::\  /:::/    /\::/   |::::\  /:::|____|\::/   |::|~~~|~~~~~
 \:::\/:::/    / \/____/  \/____/ \:::\/:::/    /  \/____|:::::\/:::/    /  \/____|::|   |
  \::::::/    /                    \::::::/    /         |:::::::::/    /         |::|   |
   \::::/    /                      \::::/    /          |::|\::::/    /          |::|   |
    \::/    /                       /:::/    /           |::| \::/____/           |::|   |
     \/____/                       /:::/    /            |::|  ~|                 |::|   |
                                  /:::/    /             |::|   |                 |::|   |
                                 /:::/    /              \::|   |                 \::|   |
                                 \::/    /                \:|   |                  \:|   |
                                  \/____/                  \|___|                   \|___|


""")


def shop_finder(search):

    keyword = search.split(',')

    conclusion = False
    for al in keyword:
        pagenum = 1
        conclusion = False
        while True:

            r = requests.get('https://search.shopping.naver.com/search/all?bt=0&frm=NVSCPRO&origQuery='+str(al) +
                             '&pagingIndex='+str(pagenum)+'&pagingSize=40&productSet=total&query='+str(al)+'&sort=rel&timestamp=&viewType=list')

            r = r.text

            r = r.split('"item":')

            r = r[1:]
            num = 1

            for li in r:
                if '래빈' in li and 'adId' in li:
                    print(str(al)+' '+str(pagenum)+'페이지 광고'+str(num)+'번 입니다')
                    conclusion = True
                    break
                if '래빈' in li:
                    print(str(al)+' '+str(pagenum)+'페이지'+str(num)+'번 입니다')
                    conclusion = True
                    break
                num = num + 1
            if conclusion == True:
                break
            pagenum = pagenum + 1
            time.sleep(0.8)

            if pagenum == 10:

                break


def keyword_finder(search):
    print()
    keyword = {'keyword': search}
    Url = 'https://api.itemscout.io/api/keyword'
    res = requests.post(Url, data=keyword)
    key_id = json.loads(res.text)
    key_id = key_id['data']

    Url = 'https://api.itemscout.io/api/keyword/'+str(key_id)+'/data'
    res = requests.get(Url)

    key_id = json.loads(res.text)

    key_id = key_id['data']
    print('키워드-'+key_id['keyword'], end='  ')
    key_monthly = key_id['monthly']
    print('검색량-'+str(key_monthly['total']), end='  ')
    print('삼품량-'+str(key_id['prdCnt']), end='  ')
    print('경쟁량-'+str(round(key_id['prdCnt'] /
                           key_monthly['total'], 2)), end='  ')
    key_bid = key_id['bid']
    print('pc광고비-'+str(key_bid['pc_bid']), end='  ')
    print('mo광고비-'+str(key_bid['mobile_bid']))
    key_rel = key_id['relKeywords']
    print()
    print(key_rel)


def keyword_finder_wm():
    txt = pyperclip.paste()
    array_law = txt.split('\n')
    rel_keyword = []
    array = []
    for li in array_law:

        if li == '\r':
            continue
        li = li.replace('\r', '')
        li = li.replace(' ', '')
        rel_keyword.append(li)

    name_array = []
    pc_bid_array = []
    mobile_bid_array = []
    prdCnt_array = []
    total_array = []
    average_array = []
    i = 0
    while True:

        if len(rel_keyword) > 100:
            len1 = rel_keyword[:100]
            del rel_keyword[:100]
            print(len(rel_keyword))
            array.append(len1)
        print(1)
        i = i + 1
        if len(rel_keyword) <= 100:
            array.append(rel_keyword)
            break

    for i in array:

        keyword = {'keywords': i}

        # print(array[0])
        Url = 'https://api.itemscout.io/api/keyword/data/list'
        r = requests.post(Url, data=keyword)
        json_val = json.loads(r.text)
        array = json_val['data']
        i = 1

        for li in array:
            try:

                name = li['keyword']
                bid = li['bid']
                pc_bid = bid['pc_bid']
                mobile_bid = bid['mobile_bid']
                prdCnt = li['prdCnt']
                monthly = li['monthly']
                total = monthly['total']
                average = prdCnt/total
                name_array.append(name)
                pc_bid_array.append(pc_bid)
                mobile_bid_array.append(mobile_bid)
                total_array.append(total)
                average_array.append(average)
                prdCnt_array.append(prdCnt)

            # print(li['prdCnt'])
            # print(clicka['total'])
            # print(li['bid'])
            except:
                continue
        time.sleep(0.5)
        print(len(name_array))
        print(len(prdCnt_array))
        print(len(total_array))
        print(len(average_array))
        print(len(pc_bid_array))
        print(len(mobile_bid_array))

    data = pd.DataFrame({
        '이름': name_array,
        '상품량': prdCnt_array,
        '검색량': total_array,
        '경쟁량': average_array,
        'pc단가': pc_bid_array,
        '모바일단가': mobile_bid_array
    })
    data.to_csv('ex 키워드.csv', mode='w', encoding='utf-8-sig')


def tag_finder(search):
    num = 1
    # print(search)
    request_headers = {
        # 'Accept': 'text/plain, */*; q=0.01',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '23',
        # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '__gads=ID=d6f8b65d221e914d:T=1589607954:S=ALNI_MapXb5s2XoCIopSXIUvwITSv9oxiw; _ga=GA1.2.92760573.1589607951; _gid=GA1.2.156504514.1590543922',
        # 'Host': 'whereispost.com',
        # 'Origin': 'http: // whereispost.com',
        'Referer': 'http: // naver.com /',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

    num = 1
    que = 0
    Url = 'https://search.shopping.naver.com/search/all.nhn?origQuery='+str(search)+'&pagingIndex=' + \
        str(num)+'&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query='+str(search)+''
    key_append = []
    req = requests.get(Url)
    soup = BeautifulSoup(req.text, 'html.parser')
    soup = str(soup)
    soup = soup.split('{"props":{"initialProps"')
    soup = soup[1]
    soup = soup.split('</script>')
    soup = soup[0].split(',')
    for li in soup:
        if 'mallProductUrl' in li:
            li = li.replace('"mallProductUrl":"', '')
            li = li.replace('"', '')
            key_append.append(li)

    for li in key_append:
        print(num)

        if li == '':
            continue
        if li == '쇼핑몰별 최저가':
            continue
        if li == '인터파크 쎈딜':
            continue
        if li == '럭키투데이':
            continue

        if 'smartstore.naver.com/' in li:
            # goods_url = li.select_one('.thumbnail_thumb__3Agq6')
            # goods_name = li.select_one('.basicList_link__1MaTN')
            # # print(goods_name.text)

            req = requests.get(li, headers=request_headers)

            soup = BeautifulSoup(req.text, 'html.parser')
            # f = open("./text.txt", 'w', -1, "utf-8")

            # f.write(str(soup))
            # f.close()
            list_data2 = soup.select('.goods_tag > ul > li')

            # print(list_data2.get('href'))
            # break
            for tag in list_data2:
                print(tag.text)

            num = num + 1

            if num == 5:

                break

        time.sleep(1)


def category_finder(search):
    num = 1
    # print(search)
    request_headers = {
        # 'Accept': 'text/plain, */*; q=0.01',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '23',
        # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '__gads=ID=d6f8b65d221e914d:T=1589607954:S=ALNI_MapXb5s2XoCIopSXIUvwITSv9oxiw; _ga=GA1.2.92760573.1589607951; _gid=GA1.2.156504514.1590543922',
        # 'Host': 'whereispost.com',
        # 'Origin': 'http: // whereispost.com',
        'Referer': 'http: // naver.com /',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

    num = 1
    que = 0
    Url = 'https://search.shopping.naver.com/search/all.nhn?origQuery='+str(search)+'&pagingIndex=' + \
        str(num)+'&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query='+str(search)+''
    req = requests.get(Url)
    soup = BeautifulSoup(req.text, 'html.parser')
    titles = soup.select('.basicList_item__2XT81')

    name = titles[0].select('.basicList_category__wVevj')
    for li in name:
        if li is name[-1]:
            print(li.text)
            break

        print(li.text, end='>')
    name = titles[1].select('.basicList_category__wVevj')
    for li in name:
        if li is name[-1]:
            print(li.text)
            break

        print(li.text, end='>')
    name = titles[2].select('.basicList_category__wVevj')
    for li in name:
        if li is name[-1]:
            print(li.text)
            break

        print(li.text, end='>')


def rel_finder(search):
    num = 1
    # print(search)
    request_headers = {
        # 'Accept': 'text/plain, */*; q=0.01',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '23',
        # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '__gads=ID=d6f8b65d221e914d:T=1589607954:S=ALNI_MapXb5s2XoCIopSXIUvwITSv9oxiw; _ga=GA1.2.92760573.1589607951; _gid=GA1.2.156504514.1590543922',
        # 'Host': 'whereispost.com',
        # 'Origin': 'http: // whereispost.com',
        'Referer': 'http: // naver.com /',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }
    num = 1

    Url = 'https://search.shopping.naver.com/search/all.nhn?origQuery='+str(search)+'&pagingIndex=' + \
        str(num)+'&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query='+str(search)+''
    req = requests.get(Url)
    soup = BeautifulSoup(req.text, 'html.parser')
    titles = soup.select('.relatedTags_relation_srh__1CleC > ul')

    for li in titles:
        if li is titles[-1]:
            print(li.text)
            break

        print(li.text, end='>')


def option_finder(url_input):
    warnings.filterwarnings("ignore")
    s = requests.Session()

    headers = {'Host': 'domeme.domeggook.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',

               }

    user = 'didutc'
    pw = '$$PP4663676'
    sess = requests.session()
    login = {'mode': "mongoLogin", 'back': "aHR0cHM6Ly9kb21lbWVkYi5kb21lZ2dvb2suY29tL2luZGV4",
             'extCookie': '', 'id': user, 'pass': pw}
    url = 'https://domeggook.com/main/member/mem_ing.php'
    res = s.post(url, data=login, verify=False)

    redirect_cookie = res.headers['Set-Cookie']
    headers = {'Host': 'domeme.domeggook.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
               'Cookie': redirect_cookie
               }

    res = s.get(url_input, data=login, )
    res.encoding = 'euc-kr'

    soup = BeautifulSoup(res.text, 'html.parser')
    # titles = soup.select_one('.pSelectUIMenu')
    print('')

    html_parse = soup.select('#lInfoViewItemContents')  # url 뽑기
    html_parse_price = soup.select_one('.lItemPrice ')
    html_parse_store = soup.select_one('#lBtnShowSellerInfo > b ')
    html_parse_prd = soup.select_one('#lInfoItemTitle')

    print('제품명')
    print(html_parse_prd.text)
    print('')
    print('상점 이름')
    print(html_parse_store.text)
    print('')
    print('가격')
    try:
        print(html_parse_price.text)
    except:
        pass
    print('')
    html_parse_logi = soup.select_one('.lDeliMethod  ')
    print('택배비')
    logi_string = html_parse_logi.text
    print(logi_string.lstrip())
    print()

    html_parse = str(html_parse)
    html_parse = html_parse.split('\n')

    toto = []
    for li in html_parse:
        if '<img src=' in li:
            toto.append(li)

    if len(toto) == 0:
        for li in html_parse:
            if 'img src=' in li:
                toto.append(li)
    print(toto)

    print('')
    print('제품 정보')
    maker_info = soup.select_one('.lTblWrap')  # 원산지 뽑기

    maker_info = maker_info.text

    maker_info = maker_info.split('\n')

    maker_info = list(filter(None, maker_info))
    print(maker_info)

    soup = str(soup)
    f = open("./text.txt", 'w', -1, "utf-8")

    f.write(str(soup))
    f.close()
    soup = soup.split('\n')
    print('')
    print('옵션명')
    print('')
    for li in soup:
        if 'data		: {"type' in li:
            goods_data = li
            goods_data = goods_data[16:]
            goods_data = goods_data[:-2]
            json_data = json.loads(goods_data)

            js_nu = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                     '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

            js_n = 0
            json_array = json_data['data']

            for cu in json_array:
                joson_data_dict = json_data['data'][js_nu[js_n]]
                last_data = joson_data_dict['name']
                last_data_hid = joson_data_dict['hid']
                if last_data_hid == 1:
                    js_n = js_n + 1
                    continue
                if js_n + 1 is len(json_array):
                    print(last_data)
                    break
                print(last_data, end=',')
                js_n = js_n + 1
    print('')
    print('세부옵션')
    print('')
    for li in soup:
        if 'data		: {"type' in li:
            goods_data = li
            goods_data = goods_data[16:]
            goods_data = goods_data[:-2]
            json_data = json.loads(goods_data)

            js_nu = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                     '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

            js_n = 0
            json_array = json_data['data']

            for cu in json_array:
                joson_data_dict = json_data['data'][js_nu[js_n]]
                last_data_name = joson_data_dict['name']
                last_data_suprice = joson_data_dict['supPrice']
                last_data_qty = joson_data_dict['qty']
                last_data_hid = joson_data_dict['hid']

                # if js_n + 1 is len(json_array):
                #     print(last_data)
                print('이름'+last_data_name+'', end='=')
                print('추가금'+str(last_data_suprice)+'', end='=')

                if last_data_hid == 1:
                    js_n = js_n + 1
                    print('품절')
                    continue
                print('수량'+str(last_data_qty)+'')
                js_n = js_n + 1


BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000621aae65a5a7d651ffcb463d89f74a27d08e61f26fa4514be999d771a0cdfb99'
SECRET_KEY = 'AQAAAABiGq5lpafWUf/LRj2J90onCrj+bzbfcT48VD4z9PX9JA=='
CUSTOMER_ID = '1538797'


def item_scout(category):
    name_array = []
    pc_bid_array = []
    mobile_bid_array = []
    prdCnt_array = []
    total_array = []
    average_array = []

    df = pd.read_csv('./category.csv')
    df = df.values.tolist()
    for li in df:

        if category == li[0]:
            category = li[1]

    conclusion = []
    duration_dict = {
        "duration": '30d',
        "genders": "f,m",
        "ages": "10,20,30,40"
    }
    json_trans = json.dumps(duration_dict)
    r = requests.post('https://api.itemscout.io/api/category/'+str(category)+'/data',
                      data=duration_dict)

    key_id = json.loads(r.text)
    # print(res.text)
    # print(key_id)
    array = key_id['data']['data']
    i = 1
    json_key = []
    for li in array:
        json_key.append(li)
    # key_id = json.dumps(array)
    # print(key_id[0])

    for al in json_key:
        li = array[al]
        try:

            name = li['keyword']
            bid = li['bid']
            pc_bid = bid['pc_bid']
            mobile_bid = bid['mobile_bid']
            prdCnt = li['prdCnt']
            monthly = li['monthly']
            total = monthly['total']
            average = prdCnt/total
            name_array.append(name)
            pc_bid_array.append(pc_bid)
            mobile_bid_array.append(mobile_bid)
            total_array.append(total)
            average = round(average, 2)
            average_array.append(average)
            prdCnt_array.append(prdCnt)

        # print(li['prdCnt'])
        # print(clicka['total'])
        # print(li['bid'])
        except:
            continue
    time.sleep(0.5)

    data = pd.DataFrame({
        '이름': name_array,
        '상품량': prdCnt_array,
        '검색량': total_array,
        '경쟁량': average_array,
        'pc단가': pc_bid_array,
        '모바일단가': mobile_bid_array
    })
    data.to_csv("아이템스카우트.csv", mode='w', encoding='utf-8-sig')


def item_detail(detail_input):
    name_array = []
    pc_bid_array = []
    mobile_bid_array = []
    prdCnt_array = []
    total_array = []
    average_array = []
    # 연관검색어

    uri = '/keywordstool'
    method = 'GET'
    r = requests.get(BASE_URL + uri, params={'hintKeywords': detail_input},
                     headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    json_data = json.loads(r.text)

    json_data = json_data['keywordList']
    rel_keyword = []
    for i in json_data:
        rel_keyword.append(i['relKeyword'])

        if i == 1:
            break
    # print(type(rel_keyword))
    array = []

    i = 0
    while True:

        if len(rel_keyword) > 100:
            len1 = rel_keyword[:100]
            del rel_keyword[:100]
            print(len(rel_keyword))
            array.append(len1)
        print(1)
        i = i + 1
        if len(rel_keyword) <= 100:
            array.append(rel_keyword)
            break

    for i in array:
        keyword = {'keywords': i}

        # print(array[0])
        Url = 'https://api.itemscout.io/api/keyword/data/list'
        res = requests.post(Url, data=keyword)
        json_val = json.loads(res.text)
        array = json_val['data']
        i = 1

        for li in array:
            try:

                name = li['keyword']
                bid = li['bid']
                pc_bid = bid['pc_bid']
                mobile_bid = bid['mobile_bid']
                prdCnt = li['prdCnt']
                monthly = li['monthly']
                total = monthly['total']
                average = prdCnt/total
                name_array.append(name)
                pc_bid_array.append(pc_bid)
                mobile_bid_array.append(mobile_bid)
                total_array.append(total)
                average_array.append(average)
                prdCnt_array.append(prdCnt)

            # print(li['prdCnt'])
            # print(clicka['total'])
            # print(li['bid'])
            except:
                continue
        time.sleep(0.5)
        print(len(name_array))
        print(len(prdCnt_array))
        print(len(total_array))
        print(len(average_array))
        print(len(pc_bid_array))
        print(len(mobile_bid_array))

    data = pd.DataFrame({
        '이름': name_array,
        '상품량': prdCnt_array,
        '검색량': total_array,
        '경쟁량': average_array,
        'pc단가': pc_bid_array,
        '모바일단가': mobile_bid_array
    })
    data.to_csv("rel_key.csv", mode='w', encoding='utf-8-sig')


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(
        timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


def get_exhange(money):

    print()
    print()
    Url = 'https://m.search.naver.com/p/csearch/content/qapirender.nhn?_callback=a&pkid=141&key=exchangeApiNationOnly&where=nexearch&q=%EC%A4%91%EA%B5%AD+%ED%99%98%EC%9C%A8&u6=standardUnit&u7=0&u3=CNY&u4=KRW&u2=' + \
        str(money)+'&u1=keb&u8=down&u5=info&_=1592612372619'
    req = requests.get(Url)  # custom_header를 사용하지 않으면 접근 불가
    exchange_price = req.text
    exchange_price = exchange_price[2:]
    exchange_price = exchange_price[:-2]
    # print(exchange_price) 문제가 생겼을 경우 이것을 봐라

    json_data = json.loads(exchange_price)
    print(json_data['itemList']["from"]["subPrice"])
    print(json_data['itemList']["to"]["subPrice"])


client_id = "j6V6dD6f1YCjncBEOBas"
client_secret = "9E9BIJvIQ5"


def ex_ch():
    print('타겟 -> ch')
    while True:
        srcText = input()
        if srcText == 'out':
            break
        encText = urllib.parse.quote(srcText)
        data = "source=ko&target=zh-CN&text=" + encText

        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(
            request, data=data.encode("utf-8"))
        rescode = response.getcode()
        response_body = response.read()
        # print(response_body.decode('utf-8'))

        # json 형 변환
        res = json.loads(response_body.decode('utf-8'))
        from pprint import pprint
        res = res['message']
        res = res['result']
        res = res['translatedText']
        print(res)
        if clip == 1:
            pyperclip.copy(res)
        print()


def ex_ko():
    print('타겟 -> ch')
    while True:
        srcText = input()
        if srcText == 'out':
            break
        encText = urllib.parse.quote(srcText)
        data = "source=zh-CN&target=ko&text=" + encText

        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(
            request, data=data.encode("utf-8"))
        rescode = response.getcode()
        response_body = response.read()
        # print(response_body.decode('utf-8'))

        # json 형 변환
        res = json.loads(response_body.decode('utf-8'))
        from pprint import pprint
        res = res['message']
        res = res['result']
        res = res['translatedText']
        print(res)
        if clip == 1:
            pyperclip.copy(res)
        print()


def split():
    html_file = open('text.txt', 'r', -1, "utf-8")

    html_file = html_file.read()
    html_file = html_file.split('\n')
    list_a = []
    while True:
        for li in html_file:
            html_file = html_file[1:]
            list_a.append(li)
            if len(list_a) == 100:
                break

        for li in list_a:
            print(li)
        input()
        list_a = []
        if len(html_file) == 0:
            break


while True:
    print('1:내 상품 검색기 2:키워드 검색기 3:태그 검색기 4:카테고리 검색기 5:연관검색어 6:도매매 옵션파인더 7:세부 키워드 분석 8:계산기 9:환율 10:파파고번역기 11: 아이템 스카우트 랭킹 12: 스플릿')
    human_input = input()
    if human_input == 'out':
        break

    if human_input == str(1):
        while True:
            print('키워드를 입력하세요')
            shop_input = input()
            if shop_input == 'out':
                break
            shop_finder(shop_input)
    if human_input == str(3):
        while True:

            print('키워드를 입력하세요')
            tag_input = input()
            if tag_input == 'out':
                break
            tag_finder(tag_input)
    if human_input == str(4):
        while True:

            print('키워드를 입력하세요')
            category_input = input()
            if category_input == 'out':
                break
            category_finder(category_input)
    if human_input == str(5):
        while True:

            print('키워드를 입력하세요')
            rel_input = input()
            if rel_input == 'out':
                break
            rel_finder(rel_input)

    if human_input == str(6):
        while True:

            print('URL을 입력하세요')
            option_input = input()
            if option_input == 'out':
                break
            option_finder(option_input)
    if human_input == str(7):
        while True:

            print('키워드를 입력하세요')
            detail_input = input()
            if detail_input == 'out':
                break
            item_detail(detail_input)
    if human_input == str(8):
        print('계산기')
        while True:

            try:
                cal = input('입력:')
                if cal == 'out':
                    break
                t = eval(cal)

                print(t)
                print()
            except:
                continue
    if human_input == str(9):
        while True:
            print('중국 -> 한국 환율')
            print('금액을 입력하세요')
            money = input()

            if money == 'out':
                break
            get_exhange(money)

    if human_input == str(10):
        clip = 0

        while True:
            print('모드를 말해주세요')
            mode = input()
            if mode == 'ch':
                ex_ch()

            if mode == 'ko':
                ex_ko()
            if mode == 'ex':
                print('클립보드모드 ON')
                clip = 1
            if mode == 'out':
                break
    if human_input == str(11):
        while True:

            print('카테고리를 입력하세요')
            detail_input = input()
            if detail_input == 'out':
                break
            item_scout(detail_input)
    if human_input == str(12):
        while True:

            print('키워드 나누기')
            detail_input = input()
            if detail_input == 'out':
                break
            split()
    else:
        while True:
            print()
            print('키워드를 입력하세요(ex는 단체키워드 모드)')
            print()
            keyword_input = input()
            if keyword_input == 'out':
                break
            if keyword_input == 'ex':
                while True:
                    print('ex키워드는 클립보드에 저장되어있는 형식으로 되었습니다. 준비가 되었다면 엔터를 누르세요')
                    keyword_input = input()
                    if keyword_input == 'out':
                        break
                    keyword_finder_wm()

            if keyword_input == 'out':
                break
            keyword_finder(keyword_input)

    #  1. 카워드 검색기
