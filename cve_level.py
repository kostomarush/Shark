import os
import json

def get_cvss_score(cve_id, nvd_json_path):
    year = cve_id.split('-')[1]  # Извлекаем год из названия CVE
    json_file = os.path.join(nvd_json_path, f"nvdcve-1.1-{year}.json")

    if not os.path.isfile(json_file):
        print(f"Файл с данными CVE {cve_id} для года {year} не найден.")
        return None

    with open(json_file, 'r') as file:
        nvd_data = json.load(file)
    
    for item in nvd_data['CVE_Items']:
        if item['cve']['CVE_data_meta']['ID'] == cve_id:
            cvss_score = None
            if 'baseMetricV3' in item['impact']:
                cvss = item['impact']['baseMetricV3']['cvssV3']
                cvss_score = cvss['baseScore']
            elif 'baseMetricV2' in item['impact']:
                cvss = item['impact']['baseMetricV2']['cvssV2']
                cvss_score = cvss['baseScore']

            if cvss_score is not None:
                return cvss_score
    
    print(f"Информация о CVE {cve_id} не найдена для года {year}.")
    return None

def get_criticality(cve_id, nvd_json_path):
    cvss_score = get_cvss_score(cve_id, nvd_json_path)
    if cvss_score is not None:
        if cvss_score >= 9.0:
            return "Критично"
        elif cvss_score >= 7.0:
            return "Высокая"
        elif cvss_score >= 4.0:
            return "Средняя"
        else:
            return "Низкая"
    return f"Информация о CVE {cve_id} не найдена для года."

if __name__ == "__main__":
    nvd_json_path = "/home/user/Desktop/clone/Dipl/cvss"  # Укажите путь к папке с данными CVE
    cve_id = 'CVE-2007-4654'
    criticality = get_criticality(cve_id, nvd_json_path)
    print(f"Критичность {cve_id}: {criticality}")
