import requests
import json
import re
import time
import pandas as pd
import jieba
import numpy as np
#import jieba.posseg as pseg
import jieba

#无意义字符数组
nosenseWord=['run','to','of','in','it','is','whether','and','the','an','there','have','run','a','this','at']  #全小写字符list
nosenseBigword=[string.capitalize() for string in nosenseWord]

#谷歌翻译语言编码
languageCode:[["auto","检测语言"],["sq","阿尔巴尼亚语"],["ar","阿拉伯语"],["am","阿姆哈拉语"],
       ["as","阿萨姆语"],["az","阿塞拜疆语"],["ee","埃维语"],["ay","艾马拉语"],["ga","爱尔兰语"],
       ["et","爱沙尼亚语"],["or","奥利亚语"],["om","奥罗莫语"],["eu","巴斯克语"],["be","白俄罗斯语"],
       ["bm","班巴拉语"],["bg","保加利亚语"],["is","冰岛语"],["pl","波兰语"],["bs","波斯尼亚语"],
       ["fa","波斯语"],["bho","博杰普尔语"],["af","布尔语(南非荷兰语)"],["tt","鞑靼语"],["da","丹麦语"],
       ["de","德语"],["dv","迪维希语"],["ti","蒂格尼亚语"],["doi","多格来语"],["ru","俄语"],["fr","法语"],
       ["sa","梵语"],["tl","菲律宾语"],["fi","芬兰语"],["fy","弗里西语"],["km","高棉语"],["ka","格鲁吉亚语"],
       ["gom","贡根语"],["gu","古吉拉特语"],["gn","瓜拉尼语"],["kk","哈萨克语"],["ht","海地克里奥尔语"],
       ["ko","韩语"],["ha","豪萨语"],["nl","荷兰语"],["ky","吉尔吉斯语"],["gl","加利西亚语"],["ca","加泰罗尼亚语"],
       ["cs","捷克语"],["kn","卡纳达语"],["co","科西嘉语"],["kri","克里奥尔语"],["hr","克罗地亚语"],["qu","克丘亚语"],
       ["ku","库尔德语（库尔曼吉语）"],["ckb","库尔德语（索拉尼）"],["la","拉丁语"],["lv","拉脱维亚语"],["lo","老挝语"],
       ["lt","立陶宛语"],["ln","林格拉语"],["lg","卢干达语"],["lb","卢森堡语"],["rw","卢旺达语"],["ro","罗马尼亚语"],
       ["mg","马尔加什语"],["mt","马耳他语"],["mr","马拉地语"],["ml","马拉雅拉姆语"],["ms","马来语"],["mk","马其顿语"],
       ["mai","迈蒂利语"],["mi","毛利语"],["mni-Mtei","梅泰语（曼尼普尔语）"],["mn","蒙古语"],["bn","孟加拉语"],
       ["lus","米佐语"],["my","缅甸语"],["hmn","苗语"],["xh","南非科萨语"],["zu","南非祖鲁语"],["ne","尼泊尔语"],
       ["no","挪威语"],["pa","旁遮普语"],["pt","葡萄牙语"],["ps","普什图语"],["ny","齐切瓦语"],["ak","契维语"],
       ["ja","日语"],["sv","瑞典语"],["sm","萨摩亚语"],["sr","塞尔维亚语"],["nso","塞佩蒂语"],["st","塞索托语"],
       ["si","僧伽罗语"],["eo","世界语"],["sk","斯洛伐克语"],["sl","斯洛文尼亚语"],["sw","斯瓦希里语"],["gd","苏格兰盖尔语"],
       ["ceb","宿务语"],["so","索马里语"],["tg","塔吉克语"],["te","泰卢固语"],["ta","泰米尔语"],["th","泰语"],["tr","土耳其语"],
       ["tk","土库曼语"],["cy","威尔士语"],["ug","维吾尔语"],["ur","乌尔都语"],["uk","乌克兰语"],["uz","乌兹别克语"],
       ["es","西班牙语"],["iw","希伯来语"],["el","希腊语"],["haw","夏威夷语"],["sd","信德语"],["hu","匈牙利语"],
       ["sn","修纳语"],["hy","亚美尼亚语"],["ig","伊博语"],["ilo","伊洛卡诺语"],["it","意大利语"],["yi","意第绪语"],
       ["hi","印地语"],["su","印尼巽他语"],["id","印尼语"],["jw","印尼爪哇语"],["en","英语"],["yo","约鲁巴语"],["vi","越南语"],
       ["zh-CN","中文"],["ts","宗加语"]]

#wordflag:[a:形容词,b:区别词,c:连词,d:副词,e:叹词,g:语素字,
#          h:前接成分,i:习用语,j:简称,k:后接成分,m:数词,
#          n:普通名词,nd:方位名词,nh:人名,ni:机构名,
#          nl:处所名词,ns:地名,nt:时间词,nz:其他专名,
#          o:拟声词,p:介词,q:量词r:代词,u:助词,v:动词
#          wp:标点符号,ws:字符串,x:非语素字]





#用于增强歧义纠错能力 的 用户自定义词典
file_userdict_url ="D:/utilfile/userdict.txt"

## 常用词，重复词，特定缩写字典
dictionary = {'统一社会信用代码':'USCC'}
 
# jieba分词（现在没有加语义标注，后期可以尝试添加）
def jiebaDeal(str):
    jieba.load_userdict(file_userdict_url) #导用户自定义词典
    splitlist=list(jieba.cut(str,cut_all=False))
    tagnum=0
    i=0
    while(i<len(splitlist)): #取出括号内的文字
      if splitlist[i] =='(':
          tagnum=1
      elif splitlist[i]==')':
          splitlist.pop(i)
          tagnum=0

      if tagnum==1:
        splitlist.pop(i)
        i=i-1

      
      i+=1
    return splitlist

# 谷歌进行单词分词
# https://blog.csdn.net/qq_36759911/article/details/112058918
def googleTranslate(text):
    
    url = 'https://translate.google.cn/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&f.sid=-2984828793698248690&bl=boq_translate-webserver_20201221.17_p0&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&_reqid=5445720&rt=c'
    headers = {
	    'origin': 'https://translate.google.cn',
	    'referer': 'https://translate.google.cn/',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
	    'x-client-data': 'CIW2yQEIpbbJAQjEtskBCKmdygEIrMfKAQj2x8oBCPfHygEItMvKAQihz8oBCNzVygEIi5nLAQjBnMsB',
	    'Decoded':'message ClientVariations {repeated int32 variation_id = [3300101, 3300133, 3300164, 3313321, 3318700, 3318774, 3318775, 3319220, 3319713, 3320540, 3329163, 3329601];}',
	    'x-same-domain': '1'
	    }  
    data = {
        	'f.req': f'[[["MkEWBc","[[\\"{text}\\",\\"auto\\",\\"en\\",true],[null]]",null,"generic"]]]'
    	}  
    
    res = requests.post(url, headers=headers, data=data).text
    pattern = '\)\]\}\'\s*\d{3,4}\s*\[(.*)\s*' 

    part1 = re.findall(pattern, res)
    part1_list = json.loads('['+part1[0])[0]
    if part1_list[2] is None:  
        return text
    content1 = part1_list[2].replace('\n', '')
    part2_list = json.loads(content1)[1][0][0][5:][0]
    s = ''
    for i in part2_list:  
        s += i[0]
    return s

# 词处理
def enDeal(str):
    name=''
    for sinstr in str.split():
        if sinstr in nosenseWord or sinstr in nosenseBigword:
            continue
        elif name=='':
            name=name+sinstr
        else:
            name=name+'_'+sinstr
               
    return name.lower()

def enchange(str):
    name=''
    if(dictionary.get(str)==None):
        tempstr=googleTranslate(str)
        
        name=enDeal(tempstr)
        dictionary[str]=name
    else:
        name=dictionary.get(str)
    return name

def wordtoname(str):
    tempStr=''

 
    for trans in jiebaDeal(str):
        tempStr=tempStr+' '+enchange(trans)

    return enDeal(tempStr)

def exceltocol(excelList):
    # 分词后返回的二维数组
    namelist=[] 
    for str in excelList:   
        namelist.append(wordtoname(str))
  
    print(namelist)
    return namelist







