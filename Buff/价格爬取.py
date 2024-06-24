import csv
import time
import requests
import json

def get_json(url, timeout=3):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41'
        }
        r = requests.post(url, timeout=timeout, headers=headers)
        r.raise_for_status()
        if r.text.strip():  # 检查返回的内容是否为空
            return r.json()
    except Exception as error:
        print(error)

def save_csv(item, path):
    with open(path, 'a+', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(item)

def parse(json_data):
    out_list = []
    for row in json_data['data']:
        row_list = [
            row[0],    # id
            row[1],    # price
            row[2],    # price1
            row[3],    # shou
            row[4],    # kui
            row[5],    # kui1
            row[6],    # kui2
            row[7],    # high
            row[8]     # qiu
        ]
        out_list.append(row_list)
    return out_list

def main():
    url = 'https://www.csgoob.com/api/v1/goods/chart'

    while True:
        json_data = get_json(url)
        print(json_data)
        if json_data is not None and 'data' in json_data:
            result = parse(json_data)
            if len(result) > 0:
                for row in result:
                    print(row)

                    save_csv(row, 'data.csv')
        time.sleep(3)
if __name__ == '__main__':
    main()