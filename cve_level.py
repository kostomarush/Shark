import os
import xml.etree.ElementTree as ET
from cvss import CVSS3

def get_cvss_score(cve_id, nvd_data_path):
    xml_file = os.path.join(nvd_data_path, "nvdcve-{}trans.xml".format(cve_id.split("-")[1]))

    if not os.path.isfile(xml_file):
        print(f"Файл с данными CVE {cve_id} не найден.")
        return None

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for entry in root.findall(".//{http://cve.mitre.org/cve/data_interchange/4}entry"):
        cve_id_element = entry.find(".//{http://cve.mitre.org/cve/data_interchange/4}cve-id")
        if cve_id_element is not None and cve_id_element.text == cve_id:
            cvssv3 = entry.find(".//{http://cve.mitre.org/cve/data_interchange/4}cvssv3")
            if cvssv3 is not None:
                cvss_vector = cvssv3.find(".//{http://www.w3.org/2001/XMLSchema-instance}value").text
                cvss_score = CVSS3(cvss_vector).base_score
                return cvss_score

    return None

def get_criticality(cve_id, nvd_data_path):
    cvss_score = get_cvss_score(cve_id, nvd_data_path)
    if cvss_score is not None:
        if cvss_score >= 9.0:
            return "Критично"
        elif cvss_score >= 7.0:
            return "Высокая"
        elif cvss_score >= 4.0:
            return "Средняя"
        else:
            return "Низкая"
    else:
        return "Информация о CVE не найдена."

if __name__ == "__main__":
    nvd_data_path = "/home/user/Dipl/cvss"  # Укажите путь к папке с данными NVD
    cve_id = input("Введите CVE ID (например, CVE-2019-12345): ")
    criticality = get_criticality(cve_id, nvd_data_path)
    print(f"Критичность CVE {cve_id}: {criticality}")
