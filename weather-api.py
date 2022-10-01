#by josh chen
from flask import Flask
import requests
import xml.etree.ElementTree as et

app = Flask(__name__)

@app.route('/weather/<city>')

def weather(city):
    Key = "CWB-8AA36519-D072-49C3-9342-3A8B8695419C"
    Data_id = "F-C0032-001"
    
    cities = ["臺北","新北","桃園","臺中","臺南","高雄","基隆","新竹","嘉義"] #市
    counties = ["宜蘭","苗栗","彰化","南投","雲林","屏東","花蓮","臺東","澎湖","金門","連江"] #縣
    showdata = ''
    flagcity = False
    city = city.replace('台','臺')
    if city in cities:
        city += '市'
    elif city in counties:
        city += '縣'
        flagcity = True
    if flagcity:
        url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/%s?Authorization=%s&format=XML" % (Data_id,Key)
        report = requests.get(url).text
        xml_namespace = "{urn:cwb:gov:tw:cwbcommon:0.1}"
        root = et.fromstring(report)
        dataset = root.find(xml_namespace + 'dataset')
        locations_info = dataset.findall(xml_namespace + 'location')
        target_id = -1
        for idx,ele in enumerate(locations_info):
            locationName = ele[0].text
            if locationName == city:
                target_id = idx
                break
        tlist = ['天氣狀況','最高溫','最低溫','舒適度','降雨機率']
        showdata = '{'
        for i in range(len(tlist)):
            element =locations_info[target_id][i+1]
            timeblock = element[1]
            data = timeblock[2][0].text
            showdata = showdata + tlist[i] + ':' + data + '",'
        showdata = showdata[:-2] + "}"
    else:
        showdata = '不存在'
    return showdata

if __name__ == '__main__':
    app.run(host='127.0.0.1',port='8080', debug=False)
