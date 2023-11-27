import prot_pb2
import prot_pb2_grpc
from server.models import ScanInfo, DataServer, ClientBD, SegmentScan, SegmentResult, IPAddress, ResultPorts, CveInformation, ResultPortsAim, CveInformationAim, LevelCveAim, LevelCve
import threading
import time
import json
import re
import os




class RPCServicer(prot_pb2_grpc.RPCServicer):

    def __init__(self):
        self.last_ping_times = {}

    def get_cvss_score(self, cve_id, nvd_json_path):
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

    def get_criticality(self, cve_id, nvd_json_path):
        cvss_score = self.get_cvss_score(cve_id, nvd_json_path)
        if cvss_score is not None:
            if cvss_score >= 9.0:
                return "Критичная"
            elif cvss_score >= 7.0:
                return "Высокая"
            elif cvss_score >= 4.0:
                return "Средняя"
            else:
                return "Низкая"
        return f"Информация неизвестна"
    
    def segment_scan(self, request, context):
        data_segment = IPAddress.objects.in_bulk()
        response = prot_pb2.DataSegment()
        for i in data_segment:
                if data_segment[i].tag == 'Proc' and data_segment[i].client.ip_client == request.name_cl:
                    if request.message:
                        save_data_seg = IPAddress.objects.get(id=i)
                        save_data_seg.tag = 'Done'
                        save_data_seg.save()
                        return response
                    elif request.data:
                        result = IPAddress.objects.get(id=data_segment[i].id)
                        alls_info = request.data
                        all_info = eval(alls_info)
                        for host, info in all_info.items():
                            if info['tag'] == 'OS':
                                for os, os_data in info.items():
                                    if os != 'host' and os != 'state' and os != 'tag':
                                        vendor = os_data['vendor']
                                        osfamily = os_data['osfamily']
                                        osgen = os_data['osgen']
                                        accuracy = os_data['accuracy']
                                        save_data_in_segment = SegmentResult(
                                        host=info['host'], state_scan=info['state'],full_name = os, vendor=vendor, osfamily=osfamily, osgen=osgen, accuracy=accuracy, result=result)
                                        save_data_in_segment.save()
                                    else:
                                        pass
                                        
                            else:
                                save_data_in_segment = SegmentResult(
                                    host=info['host'], state_ports = info['state_ports'], state_scan=info['state'], result=result)
                                save_data_in_segment.save()

                                for port_info in info['open_ports']:
                                    port = port_info['port']
                                    state = port_info['state']
                                    reason = port_info['reason']
                                    service = port_info['service']
                                    cve = port_info['cve']

                                    # Используем регулярное выражение для поиска всех [CVE ...]
                                    cve_matches = re.findall(r'\[CVE-\d{4}-\d+\]', cve)
                            
                                    # Выводим результат
                                    nvd_json_path = "/usr/share/nmap/scripts/vulscan/cvss"
                                    all_cve=''
                                    for cve_match in cve_matches:
                                        stripped_cve = cve_match.strip("[]")
                                        year = cve_match.split("-")[1]
                                        criticality = self.get_criticality(stripped_cve, nvd_json_path)
                                        all_cve += f'[{stripped_cve}] - {criticality}'+ '\n'
                                        save_cve_level = LevelCve(port = port, cve=stripped_cve, level=criticality, year = year, result = save_data_in_segment)
                                        save_cve_level.save()                                  
                                        
                                    save_data_in_segment_ports = ResultPorts(
                                        port=port, state=state, reason=reason, service=service, one_cve=all_cve, all_info=save_data_in_segment)
                                    save_data_in_segment_ports.save()
                                    save_cve = CveInformation(cve_information = cve, result_ports = save_data_in_segment_ports)
                                    save_cve.save()
                    
                        save_data_in_segment.mark_execution_complete()                
                                    
                        return response
                    
        for i in data_segment:
            if data_segment[i].tag == 'False':
                client = ClientBD.objects.get(ip_client=request.name_cl)
                save_seg_ip = IPAddress.objects.get(id=i)
                save_seg_ip.client = client
                save_seg_ip.tag = 'Proc'
                save_seg_ip.save()
                ip_address = data_segment[i].address
                mode = data_segment[i].seg_scan.mode
                cve_report = f'{data_segment[i].seg_scan.cve_report}'
                full_scan = f'{data_segment[i].seg_scan.full_scan}'
                response_start = prot_pb2.DataSegment(
                    ip_address=ip_address, mode=mode, cve_report=cve_report, full_scan=full_scan)
                return response_start
    
    
    def scan(self, request, context):
        data_server = DataServer.objects.in_bulk()
        response = prot_pb2.DataServer()
        for data_id in data_server:
            
            if data_server[data_id].tag == 'Proc' and f'{data_server[data_id].client.ip_client}' == request.name_cl:
                if request.message:
                    save_data = DataServer.objects.get(id=data_id)
                    save_data.tag = 'Done'
                    save_data.save()
                    return response
                elif request.data:
                    result = DataServer.objects.get(id=data_server[data_id].id)
                    alls_info = request.data
                    all_info = eval(alls_info)
                    
                    if all_info['tag'] == 'OS':
                        for os, os_data in all_info.items():
                            if os != 'host' and os != 'state' and os != 'tag':
                                vendor = os_data['vendor']
                                osfamily = os_data['osfamily']
                                osgen = os_data['osgen']
                                accuracy = os_data['accuracy']
                                save_scan_info_os = ScanInfo(
                                host=all_info['host'], state_scan=all_info['state'],full_name = os, vendor=vendor, osfamily=osfamily, osgen=osgen, accuracy=accuracy, result=result)
                                save_scan_info_os.save()
                            else:
                                pass
                                    
                    else:
                        save_data = ScanInfo(
                            host=all_info['host'], state_ports = all_info['state_ports'], state_scan=all_info['state'], result=result)
                        save_data.save()
                        for port_info in all_info['ports']:
                            port = port_info['port']
                            state = port_info['state']
                            reason = port_info['reason']
                            service = port_info['service']
                            cve = port_info['cve']
                            # Используем регулярное выражение для поиска всех [CVE ...]
                            cve_matches = re.findall(r'\[CVE-\d{4}-\d+\]', cve)
                            
                            # Выводим результат
                            nvd_json_path = "/usr/share/nmap/scripts/vulscan/cvss"
                            all_cve=''
                            for cve_match in cve_matches:
                                stripped_cve = cve_match.strip("[]")
                                year = cve_match.split("-")[1]
                                criticality = self.get_criticality(stripped_cve, nvd_json_path)
                                all_cve += f'[{stripped_cve}] - {criticality}'+ '\n'
                                save_cve_level = LevelCveAim(port = port, cve=stripped_cve, level=criticality, result = save_data)
                                save_cve_level.save()                                  
                                
                            save_data_in_aim_ports = ResultPortsAim(
                                port=port, state=state, reason=reason, service=service, one_cve=all_cve, all_info=save_data)
                            save_data_in_aim_ports.save()
                            save_cve = CveInformationAim(cve_information = cve, result_ports = save_data_in_aim_ports)
                            save_cve.save()
                    return response
                                
            elif data_server[data_id].tag == 'False':
                client = ClientBD.objects.get(ip_client=request.name_cl)
                save_tab = DataServer.objects.get(id=data_id)
                save_tab.client = client
                save_tab.tag = 'Proc'
                save_tab.save()
                ip = data_server[data_id].ip
                port = data_server[data_id].port
                mode = data_server[data_id].mode
                cve_report = f'{data_server[data_id].cve_report}'
                response_aim = prot_pb2.DataServer(
                    ip_address=ip, port=port, mode=mode, cve_report=cve_report)
                return response_aim
                

    def SayHello(self, request, context):
        if request.message == "Ping":
            # Обработка сообщения PING
            self.last_ping_times[request.name] = time.time()
            return prot_pb2.HelloReply(message="Received PING")
        else:
            pass


def check_ping_thread(my_service):
    while True:
        current_time = time.time()
        if not my_service.last_ping_times:
            pass
        else:
            keys_to_remove = []
            for client_name, last_ping_time in my_service.last_ping_times.items():
                if current_time - last_ping_time > 30:
                    print(
                        f"Клиент {client_name} не отправлял PING в течение 1 минуты")
                    keys_to_remove.append(client_name)
                    elements_on_delete = IPAddress.objects.in_bulk()
                    for i in elements_on_delete:
                        try:
                            if elements_on_delete[i].client.ip_client == client_name and elements_on_delete[i].tag == 'Proc':
                                del_ip = IPAddress.objects.get(id=i)
                                del_ip.client.ip_client='None' 
                                del_ip.tag='False'
                                del_ip.save()
                                print(
                                    f'Клиент {client_name} удален!')
                        except:
                            pass
            # Удаляем элементы из словаря
            for client_name in keys_to_remove:
                del my_service.last_ping_times[client_name]

        time.sleep(1)


def grpc_hook(server):
    try:
        my_service = RPCServicer()

        prot_pb2_grpc.add_RPCServicer_to_server(my_service, server)

        # Создаем и запускаем поток для проверки PING
        ping_check_thread = threading.Thread(
            target=check_ping_thread, args=(my_service,))
        ping_check_thread.daemon = True
        ping_check_thread.start()

    except KeyboardInterrupt:
        import sys
        sys.exit()
