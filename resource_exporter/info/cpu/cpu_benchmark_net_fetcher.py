import requests
from bs4 import BeautifulSoup


class CpuBenchmarkNetFetcher:
    @staticmethod
    def remove_space(value):
        while '  ' in value:
            value = value.replace('  ', ' ')
        return value

    @staticmethod
    def parse_info_from_paragraphs(p_list):
        info = {}
        for p_tag in p_list:
            items = p_tag.text.split(":")
            if len(items) == 2:
                info[items[0].strip()] = CpuBenchmarkNetFetcher.remove_space(items[1].strip())
        return info

    @staticmethod
    def parse_cores_and_threads(info):
        if "No of Cores" in info:
            raw = (info["No of Cores"].replace("No of Cores", "").replace("logical core per physical", "")
            .replace("(",")", ""))
            items = raw.split()
            info['Cores'] = int(items[0])
            if len(items) > 1 and items[1] != 'in':
                info['Threads'] = int(items[1]) * info['Cores']
            else:
                info['Threads'] = info['Cores']

    @staticmethod
    def parse_score_details(strong_list):
        score_detail = {}
        for strong in strong_list:
            score_detail[strong.text.replace(": ", "").strip()] = str(strong.next_sibling)
        score_detail.pop('Margin for error', None)  # Remove if exists
        return score_detail

    @staticmethod
    def fetch_cpu_info(cpu_name):
        cpu_name = cpu_name.strip().replace(' ', '+')
        url = f'https://www.cpubenchmark.net/cpu.php?cpu={cpu_name}'
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return {}

        soup = BeautifulSoup(res.text, "html5lib")
        div = soup.find('div', class_='desc-body')
        p_list = div.find_all('p') if div else []

        info = CpuBenchmarkNetFetcher.parse_info_from_paragraphs(p_list)
        CpuBenchmarkNetFetcher.parse_cores_and_threads(info)

        right_desc_div = soup.find('div', class_='right-desc')
        strong_list = right_desc_div.find_all('strong') if right_desc_div else []
        info['Score_Detail'] = CpuBenchmarkNetFetcher.parse_score_details(strong_list)
        info['Score'] = right_desc_div.find_all('span')[1].text if right_desc_div else "unknown"

        # Date and TDP processing
        for key in ['CPU First Seen on Charts', 'Typical TDP']:
            val = info.get(key, "")
            if val:
                info[key] = ' '.join(val.split()[:2]) if key == 'CPU First Seen on Charts' else val.split(' ')[0]
            else:
                info[key] = "unknown"

        return info
