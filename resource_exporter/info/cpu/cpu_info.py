import abc
from typing import Any

import requests
from bs4 import BeautifulSoup


class CPUInfo(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def get(self):
        pass

    @classmethod
    def _get_cpu_benchmark_net_data(cls, cpu_name):

        def remove_space(value):
            new_value = value.replace('  ', ' ')
            old_value = value
            while old_value != new_value:
                old_value = new_value
                new_value = new_value.replace('  ', ' ')
            return new_value

        cpu_name = cpu_name.strip().replace(' ', '+')
        url = 'https://www.cpubenchmark.net/cpu.php?cpu=' + cpu_name
        res = requests.get(url, timeout=1)
        if res.status_code != 200:
            return {}
        text = res.text
        bs = BeautifulSoup(text, "html5lib")
        div = bs.find('div', class_='desc-body')
        p_list = div.find_all('p')
        info: dict[str | Any, int | dict[Any, Any] | Any] = {}
        for p_tag in p_list:
            items = p_tag.text.split(":")
            if len(items) == 2:
                info[items[0].strip()] = remove_space(items[1].strip())
            if "No of Cores" in info:
                raw = info["No of Cores"].strip()
                raw = raw.replace("No of Cores", "")
                raw = raw.replace("logical core per physical", "")
                raw = raw.replace("(", "")
                raw = raw.replace(")", "")
                items = raw.split(' ')
                info['Cores'] = int(items[0])
                if len(items) == 1:
                    continue

                if items[1] == 'in':
                    info['Threads'] = info['Cores']
                else:
                    info['Threads'] = int(items[1]) * info['Cores']

        strong_list = bs.find('div', class_='right-desc').find_all('strong')
        info['Score_Detail'] = {}
        for strong in strong_list:
            info['Score_Detail'][strong.text.replace(": ", "").strip()] = str(strong.next_sibling)
        if 'Margin for error' in info['Score_Detail']:
            info['Score_Detail'].pop('Margin for error')

        info['Score'] = bs.find('div', class_='right-desc').find_all('span')[1].text

        val = info.get('CPU First Seen on Charts', "")
        if val != "":
            info['CPU First Seen on Charts'] = val.split(' ')[1] + " " + val.split(' ')[0]
        else:
            info['CPU First Seen on Charts'] = "unknown"

        val = info.get('Typical TDP', "")
        if val != "":
            info['Typical TDP'] = val.split(' ')[0]
        else:
            info['Typical TDP'] = "unknown"
        return info
