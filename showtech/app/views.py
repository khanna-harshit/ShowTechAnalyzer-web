from django.shortcuts import render, redirect
from django.contrib import messages
from pymongo import MongoClient
import gzip
import re
import tarfile
import datetime
import gridfs
import os
from .models import Document
import shutil
from netmiko import ConnectHandler

def download(request):
    return render(request, 'app/ShowTechReport.html')

def result(request):
    text = extract_upload()
    location = 'app/templates/app/ShowTechReport.html'
    Func = open(location, "w")
    download_text = '''<!DOCTYPE html>
    <html lang="en" xmlns="http://www.w3.org/1999/html">
    <head>
        <meta charset="UTF-8">
        <title>Report..</title>
        <style>
        body{
            font-family: monospace;
            margin:50px 50px;
            font-size:15px;
        }
        </style>
    </head>
    <body>
    <h1 style="font-size:40px; margin-bottom:40px"> Results .. </h1>


     ''' + text + '''


    </body>
    </html>'''
    # Adding input data to the HTML file
    Func.write(download_text)

    # Saving the data into the HTML file
    Func.close()
    try:
        shutil.rmtree('/sonic')
    except:
        messages.error(request, 'ShowTechFile is not deleted from directory')
        pass
    try:
        client = MongoClient()
        # Connect with the port number and host

        client = MongoClient("mongodb://localhost:27017/")
        # client = MongoClient(
        #     "mongodb+srv://harshit064:<password>@cluster1.p6axqua.mongodb.net/?retryWrites=true&w=majority")
        db = client["ShowTechAnalyser"]
        db.collection1.remove()
        db.collection2.remove()
        db.collection3.remove()
    except:
        messages.error(request, 'Data not deleted from database')
        pass
    return render(request, 'app/result.html', {'text': text, 'download': 'app/ShowTechReport.html'})

def snapshot(request):
    if request.method == 'POST':
        button = request.POST['button']
        if button == 'Analyze':

            username = request.POST['username']
            password = request.POST['password']
            ip_address = request.POST['ip_address']
            command_name = request.POST['dropdown']
            try:
                linux = {
                    'device_type': 'linux',
                    'ip': ip_address,
                    'username': username,
                    'password': password,
                }
                connection = ConnectHandler(**linux)

                if command_name == 'show ip interface':
                    output_of_command = connection.send_command('show ip interface')
                    print(output_of_command)
                    print("karan")
                    output = show_ip_interface(output_of_command)
                    text = output[0]
                if command_name == 'show ip route':
                    output_of_command = connection.send_command('show ip route')
                    print(output_of_command)
                    output = show_ip_route(output_of_command)
                    text = output[0]
                if command_name == 'show interface status':
                    output_of_command = connection.send_command('show interface status')
                    output = show_interface_status(output_of_command)
                    text = output[0]
                if command_name == 'show version':
                    output_of_command = connection.send_command('show version')
                    output = show_version(output_of_command, None)
                    text = output[0]
                location = 'app/templates/app/ShowTechReport.html'
                Func = open(location, "w")
                download_text = '''<!DOCTYPE html>
                    <html lang="en" xmlns="http://www.w3.org/1999/html">
                    <head>
                        <meta charset="UTF-8">
                        <title>Report..</title>
                        <style>
                        body{
                            font-family: monospace;
                            margin:50px 50px;
                            font-size:15px;
                        }
                        </style>
                    </head>
                    <body>
                    <h1 style="font-size:40px; margin-bottom:40px"> Results .. </h1>
    
    
                     ''' + text + '''
    
    
                    </body>
                    </html>'''
                # Adding input data to the HTML file
                Func.write(download_text)

                # Saving the data into the HTML file
                Func.close()
                return render(request, 'app/result.html', {'text': text, 'download': 'app/ShowTechReport.html'})

            except:
                messages.error(request, 'Please enter correct IP address or username or password :(')
                return redirect('/')
        else:
            pass
    return render(request, 'app/firstInterface.html')



def textarea(request):
    if request.method == 'POST':
        button = request.POST['button']
        if button == 'Analyze':
            answer = ''
            output_of_command = request.POST['textarea']
            command_name = request.POST['dropdown']
            if command_name == 'show ip interface':
                output = show_ip_interface(output_of_command)
                if output[1]:
                    answer = output[0]
            if command_name == 'show ip route':
                output = show_ip_route(output_of_command)
                if  output[1]:
                    answer = output[0]
            if command_name == 'show interface status':
                output = show_interface_status(output_of_command)
                if  output[2]:
                    answer = output[0]
            if command_name == 'show top':
                output = show_top(output_of_command)
                if  output[1]:
                    answer = output[0]
            if command_name == 'show version':
                output = show_version(output_of_command, None)
                if  output[1]:
                    answer = output[0]
            if command_name == 'show broadcom knet link':
                output = show_broadcom_knet_link(output_of_command)
                if  output[2]:
                    answer = output[0]
            if command_name == 'show broadcom ps':
                output = show_broadcom_ps(output_of_command)
                if  output[1]:
                    answer = output[0]
            if command_name == 'show frr interfaces':
                output = show_frr_interfaces(output_of_command)
                if  output[1]:
                    answer = output[0]
            if command_name == 'show lldp control':
                output = show_lldpctl(output_of_command)
                if  output[1]:
                    answer = output[0]
            if command_name == 'show port summary':
                output = show_port_summary(output_of_command)
                if  output[1]:
                    answer = output[0]
            if command_name == 'show bridge fdb':
                output = show_bridge_fdb(output_of_command)
                if output[1]:
                    answer = output[0]
            if len(answer) != 0:
                location = 'app/templates/app/ShowTechReport.html'
                Func = open(location, "w")
                download_text = '''<!DOCTYPE html>
                    <html lang="en" xmlns="http://www.w3.org/1999/html">
                    <head>
                        <meta charset="UTF-8">
                        <title>Report..</title>
                        <style>
                        body{
                            font-family: monospace;
                            margin:50px 50px;
                            font-size:15px;
                        }
                        </style>
                    </head>
                    <body>
                    <h1 style="font-size:40px; margin-bottom:40px"> Results .. </h1>
    
    
                     ''' + answer + '''
    
    
                    </body>
                    </html>'''
                # Adding input data to the HTML file
                Func.write(download_text)

                # Saving the data into the HTML file
                Func.close()
                return render(request, 'app/result.html', {'text': answer, 'download': 'app/ShowTechReport.html'})
            else:
                messages.error(request, 'Please enter the correct output :(')
                return redirect('/')
        else:
            pass
    return render(request, 'app/firstInterface.html')

def file(request):
    if request.method == 'POST':
        button = request.POST['button']
        if button == 'Analyze':
            try:

                newdoc = Document(docfile=request.FILES['filename'])
                newdoc.save()

                global path
                path = newdoc.docfile.path

                try:
                    file = tarfile.open(path)
                except:
                    messages.error(request, 'Please Upload show-tech file')
                    return redirect('/')

                file_name = file.getnames()
                dump_files = []
                proc_files = []
                log_files = []
                for i in range(1, len(file_name) - 1):
                    file_name_split = file_name[i].split('/')
                    if file_name_split[1] == 'dump':
                        dump_files.append(file_name[i])
                    if file_name_split[1] == 'proc':
                        proc_files.append(file_name[i])
                    if file_name_split[1] == 'log':
                        log_files.append(file_name[i])
                if len(dump_files) != 0:
                    return render(request, 'app/analyze.html')
                else:
                    newdoc.delete()
                    messages.error(request, 'Please Upload correct show-tech file')
                    return redirect('/')
            except:

                messages.error(request, 'Please Upload a file')
                return redirect('/')
        else:
            pass

    return render(request, 'app/firstInterface.html')

def main(request):
    return render(request, 'app/firstInterface.html')


def extract_upload():
    file = tarfile.open(path)
    file_name = file.getnames()
    dump_files = []
    proc_files = []
    log_files = []
    for i in range(1, len(file_name) - 1):
        file_name_split = file_name[i].split('/')
        if file_name_split[1] == 'dump':
            dump_files.append(file_name[i])
        if file_name_split[1] == 'proc':
            proc_files.append(file_name[i])
        if file_name_split[1] == 'log':
            log_files.append(file_name[i])
    if len(dump_files) != 0:
        file.extractall('/sonic')
        now = datetime.datetime.now()
        file.close()
        insert_dump = []
        insert_proc = []
        insert_log = []
        for i in dump_files:
            try:
                f = open("/sonic" + '/' + i, 'r')

                text = f.read()
                path_list = i.split('/')
                file_name = ''
                temp_name = path_list[-1]
                temp_name_list = temp_name.split('.')
                for j in range(0, len(temp_name_list)):
                    if j == len(temp_name_list) - 1:
                        file_name = file_name + temp_name_list[j]
                    else:
                        file_name = file_name + temp_name_list[j] + " "
                insert_dump.append(
                    {'path': 'sonic' + '/' + i, 'name': "show " + file_name, 'contents': text, 'time': now})
            except:
                messages.error(request, 'file not open the dump folder')
                pass

        for i in proc_files:
            try:
                path_list = i.split('/')
                file_name = path_list[-1]
                if file_name == 'arp':
                    f = open("/sonic" + '/' + i, 'r')
                    text = f.read()
                    insert_proc.append(
                        {'path': 'sonic' + '/' + i, 'name': "show " + file_name, 'contents': text,
                         'time': now})
                elif file_name == 'meminfo':
                    f = open("/sonic" + '/' + i, 'r')
                    text = f.read()
                    insert_proc.append(
                        {'path': 'sonic' + '/' + i, 'name': "show " + file_name, 'contents': text,
                         'time': now})
                elif file_name == 'config':
                    if path_list[-2] == 'vlan':
                        f = open("/sonic" + '/' + i, 'r')
                        text = f.read()
                        insert_proc.append(
                            {'path': 'sonic' + '/' + i, 'name': "show " + file_name, 'contents': text,
                             'time': now})
            except:
                messages.error(request, 'file not open the proc folder')
                pass
        for i in log_files:
            try:
                path_list = i.split('/')
                file_name = ''
                temp_name = path_list[-1]
                temp_name_list = temp_name.split('.')
                for j in range(0, len(temp_name_list)):
                    if j == len(temp_name_list) - 1:
                        file_name = file_name + temp_name_list[j]
                    else:
                        file_name = file_name + temp_name_list[j] + " "
                insert_log.append(
                    {'path': 'sonic' + '/' + i, 'name': "show " + file_name, 'contents': text, 'time': now})

            except:
                messages.error(request, 'file not open the log folder')
                pass
        # connect with database
        client = MongoClient()
        # Connect with the port number and host
        client = MongoClient("mongodb://localhost:27017/")
        db = client["ShowTechAnalyser"]
        collection1 = db["Dump_Data"]
        collection2 = db["Proc_Data"]
        collection3 = db["Log_Data"]
        # Get the list of all files and directories
        x = db.collection1.insert_many(insert_dump)
        y = db.collection2.insert_many(insert_proc)
        z = db.collection3.insert_many(insert_log)

        # result shown in "Results" Screen with the data fetch from database with the help of id
        dump_data_temp = []
        proc_data_temp = []
        dump_data = []
        proc_data = []
        log_data_temp = []
        log_data = []
        collection1_inserted_ids = x.inserted_ids
        collection2_inserted_ids = y.inserted_ids
        collection3_inserted_ids = z.inserted_ids
        for items in collection1_inserted_ids:
            dump_data_temp.append(list(db.collection1.find({'_id': items})))
        for items in collection2_inserted_ids:
            proc_data_temp.append(list(db.collection2.find({'_id': items})))
        for items in collection3_inserted_ids:
            log_data_temp.append(list(db.collection3.find({'_id': items})))
        for items in proc_data_temp:
            proc_data.append(items[0])
        for items in dump_data_temp:
            dump_data.append(items[0])
        for items in log_data_temp:
            log_data.append(items[0])

        # used to store the result of the analyzed commands so that they can be displayed with priority
        analyzed_commands = dict()
        cli_asic = dict()
        cli_asic['show interface status'] = ['show broadcom knet link']
        for i in dump_data:
            if i['name'] == 'show bridge vlan':
                # calls show_bridge_vlan() function
                analyzed_commands['show bridge vlan'] = show_bridge_vlan(i)
        for i in log_data:
            if i['name'] == 'show syslog gz':
                # calls show_syslog_gz() function
                analyzed_commands['show syslog gz'] = show_syslog_gz(i)
            if i['name'] == 'show syslog 1 gz':
                # calls show_syslog_1_gz() function
                analyzed_commands['show syslog 1 gz'] = show_syslog_1_gz(i)

        for i in proc_data:
            if i['name'] == 'show arp':
                # calls show_arp() function
                analyzed_commands['show arp'] = show_arp(i)
            if i['name'] == 'show config':
                # calls show_config() function
                analyzed_commands['show config'] = show_config(i)
            if i['name'] == 'show meminfo':
                # calls show_meminfo() function
                analyzed_commands['show meminfo'] = show_meminfo(i)
        for i in dump_data:
            if i['name'] == 'show interface status':
                # calls show_interface_status() function
                output = show_interface_status(i)
                analyzed_commands['show interface status'] = output
            elif i['name'] == 'show ip interface':
                # calls show_ip_interface() function
                output = show_ip_interface(i)
                analyzed_commands['show ip interface'] = output[0]
            elif i['name'] == 'show vlan summary':
                # calls show_vlan_summary() function
                if 'show bridge vlan' in analyzed_commands:
                    analyzed_commands['show vlan summary'] = show_vlan_summary(i, analyzed_commands[
                        'show bridge vlan'][1])
                else:
                    analyzed_commands['show vlan summary'] = show_vlan_summary(i, [])
            elif i['name'] == 'show bridge fdb':
                # calls show_bridge_fdb() function
                analyzed_commands['show bridge fdb'] = show_bridge_fdb(i)
            elif i['name'] == 'show ip route':
                # calls show_ip_route() function
                analyzed_commands['show ip route'] = show_ip_route(i)
            elif i['name'] == 'show bgp summary':
                # calls show_bgp_summary() function
                analyzed_commands['show bgp summary'] = show_bgp_summary(i)
            elif i['name'] == 'show ip neigh':
                # calls show_ip_neigh() function
                analyzed_commands['show ip neigh'] = show_ip_neigh(i)
            elif i['name'] == 'show platform summary':
                # calls show_platform_summary() function
                analyzed_commands['show platform summary'] = show_platform_summary(i)
            elif i['name'] == 'show mirror summary':
                # calls show_mirror_summary function
                analyzed_commands['show mirror summary'] = show_mirror_summary(i)
            elif i['name'] == 'show port summary':
                # calls show_port_summary() function
                analyzed_commands['show port summary'] = show_port_summary(i)
            elif i['name'] == 'show lldpctl':
                # calls show_lldpctl() function
                analyzed_commands['show lldpctl'] = show_lldpctl(i)
            elif i['name'] == 'show top':
                # calls show_top() function
                analyzed_commands['show top'] = show_top(i)
            elif i['name'] == 'show version':
                # calls show_version() function
                if 'show meminfo' in analyzed_commands:
                    meminfo_result = analyzed_commands['show meminfo']
                    analyzed_commands['show version'] = show_version(i, meminfo_result)
                else:
                    analyzed_commands['show version'] = show_version(i, None)

            elif i['name'] == 'show broadcom knet link':
                # calls show_broadcom_knet_link() function
                analyzed_commands['show broadcom knet link'] = show_broadcom_knet_link(i)
            # elif i['name'] == 'show fp summary':
            #     # calls show_fp_summary() function
            #     analyzed_commands['show fp summary'] = show_fp_summary(i)
            elif i['name'] == 'show frr interfaces':
                # calls show_frr_interfaces() function
                analyzed_commands['show frr interfaces'] = show_frr_interfaces(i)
            elif i['name'] == 'show broadcom ps':
                # calls show_broadcom_ps() function
                analyzed_commands['show broadcom ps'] = show_broadcom_ps(i)
            elif i['name'] == 'show reboot cause':
                # calls show_reboot_cause() function
                analyzed_commands['show reboot cause'] = show_reboot_cause(i)

            elif i['name'] == 'show docker stats':
                # calls show_docker_stats() function
                analyzed_commands['show docker stats'] = show_docker_stats(i)
            elif i['name'] == 'show docker ps':
                # calls show_docker_ps() function
                analyzed_commands['show docker ps'] = show_docker_ps(i)

        # arranging the commands according to priority
        str = ''
        if 'show platform summary' in analyzed_commands:
            str += analyzed_commands['show platform summary']
            del analyzed_commands['show platform summary']

        str += '<p style="color:#000000; font-size:25px;"> <b>' + 'CLI command         :'.replace(' ',
                                                                                                  '&nbsp;')
        str += 'ASIC command</b></p>' + '\n\n'
        str += '<p style="color:#DE0D82;"> <b>'
        for key, value in cli_asic.items():
            new_key = key
            for space in range(len(key), 35):
                new_key = new_key + ' '
            str += new_key.replace(' ', '&nbsp;') + ':'
            for entry in range(0, len(value)):
                if entry != len(value) - 1:
                    new_entry = value[entry]
                    for space in range(len(entry), 28):
                        new_entry = new_entry + ' '
                    str += new_entry.replace(' ', '&nbsp;') + ': '
                else:
                    str += value[entry]
        str += '</b></p>\n\n'

        if 'show version' in analyzed_commands:
            str += analyzed_commands['show version'][0]
            if 'show meminfo' in analyzed_commands:

                del analyzed_commands['show meminfo']
            del analyzed_commands['show version']

        if 'show ip neigh' in analyzed_commands:
            str += analyzed_commands['show ip neigh']
            del analyzed_commands['show ip neigh']

        if 'show arp' in analyzed_commands:
            str += analyzed_commands['show arp']
            del analyzed_commands['show arp']

        if 'show reboot cause' in analyzed_commands:
            str += analyzed_commands['show reboot cause']
            del analyzed_commands['show reboot cause']

        # if 'show broadcom knet link' in analyzed_commands and 'show interface status' in analyzed_commands:
        #     if analyzed_commands['show broadcom knet link'][1][0] == \
        #             analyzed_commands['show interface status'][1][
        #                 0] and analyzed_commands['show broadcom knet link'][1][1] == \
        #             analyzed_commands['show interface status'][1][1] and \
        #             analyzed_commands['show broadcom knet link'][1][2] == \
        #             analyzed_commands['show interface status'][1][2]:
        #         str += '<p style="color:#000000; font-size:20px;"> <b>' + 'NOTE: show interface status and show broadcom knet link commands are matching\n\n' + '</b></p>'
        #     else:
        #         str += '<p style="color:#000000; font-size:20px;"> <b>' + 'NOTE: show interface status and show broadcom knet link commands are not matching\n\n' + '</b></p>'

        if 'show interface status' in analyzed_commands:
            str += analyzed_commands['show interface status'][0]


        if 'show broadcom knet link' in analyzed_commands:
            str += analyzed_commands['show broadcom knet link'][0]


        if 'show broadcom knet link' in analyzed_commands and 'show interface status' in analyzed_commands:
            if analyzed_commands['show broadcom knet link'][1][0] == \
                    analyzed_commands['show interface status'][1][
                        0] and analyzed_commands['show broadcom knet link'][1][1] == \
                    analyzed_commands['show interface status'][1][1] and \
                    analyzed_commands['show broadcom knet link'][1][2] == \
                    analyzed_commands['show interface status'][1][2]:
                str += '<p style="color:#000000; font-size:20px;"> <b>' + 'NOTE: show interface status and show broadcom knet link commands are matching\n\n' + '</b></p>'
            else:
                str += '<p style="color:#000000; font-size:20px;"> <b>' + 'NOTE: show interface status and show broadcom knet link commands are not matching\n\n' + '</b></p>'

        if 'show interface status' in analyzed_commands:
            del analyzed_commands['show interface status']

        if 'show broadcom knet link' in analyzed_commands:
            del analyzed_commands['show broadcom knet link']

        if 'show broadcom ps' in analyzed_commands:
            str += analyzed_commands['show broadcom ps'][0]
            del analyzed_commands['show broadcom ps']

        if 'show bridge vlan' in analyzed_commands:
            str += analyzed_commands['show bridge vlan'][0]
            del analyzed_commands['show bridge vlan']

        if 'show vlan summary' in analyzed_commands:
            str += analyzed_commands['show vlan summary']
            del analyzed_commands['show vlan summary']

        if 'show config' in analyzed_commands:
            str += analyzed_commands['show config']
            del analyzed_commands['show config']

        if 'show docker stats' in analyzed_commands:
            str += analyzed_commands['show docker stats']
            del analyzed_commands['show docker stats']

        if 'show docker ps' in analyzed_commands:
            str += analyzed_commands['show docker ps']
            del analyzed_commands['show docker ps']

        if 'show frr interfaces' in analyzed_commands:
            str += analyzed_commands['show frr interfaces'][0]
            del analyzed_commands['show frr interfaces']

        if 'show fp summary' in analyzed_commands:
            str += analyzed_commands['show fp summary']
            del analyzed_commands['show fp summary']

        if 'show top' in analyzed_commands:
            str += analyzed_commands['show top'][0]
            del analyzed_commands['show top']

        if 'show lldpctl' in analyzed_commands:
            str += analyzed_commands['show lldpctl'][0]
            del analyzed_commands['show lldpctl']

        if 'show bgp summary' in analyzed_commands:
            str += analyzed_commands['show bgp summary']
            del analyzed_commands['show bgp summary']

        if 'show mirror summary' in analyzed_commands:
            str += analyzed_commands['show mirror summary']
            del analyzed_commands['show mirror summary']

        if 'show port summary' in analyzed_commands:
            str += analyzed_commands['show port summary'][0]
            del analyzed_commands['show port summary']

        if 'show ip route' in analyzed_commands:
            str += analyzed_commands['show ip route'][0]
            del analyzed_commands['show ip route']

        if 'show bridge fdb' in analyzed_commands:
            str += analyzed_commands['show bridge fdb'][0]
            del analyzed_commands['show bridge fdb']



        for ii, jj in analyzed_commands.items():
            if ii != 'show syslog gz' and ii != 'show syslog 1 gz':
                str += jj
        if 'show syslog gz' in analyzed_commands:
            str += analyzed_commands['show syslog gz']
            del analyzed_commands['show syslog gz']

        if 'show syslog 1 gz' in analyzed_commands:
            str += analyzed_commands['show syslog 1 gz']
            del analyzed_commands['show syslog 1 gz']

        text = "<p>" + str.replace("\n", "<br>") + "</p>"
        return text


# this function is used to show syslog
def show_syslog_gz(i):
    # These all statements are used for formatting the results to show in result screen.
    with gzip.open("/" + i['path'], mode="rt") as f:
        file_content = f.read()
        lst = file_content.split('\n')
        error = ''
        critical = ''
        for x in lst:
            y = re.search('ERROR', x)
            z = re.search('CRITICAL', x)

            if y is not None:
                error += x.replace(' ', '&nbsp;') + '\n\n'
            if z is not None:
                critical += x.replace(' ', '&nbsp;') + '\n\n'
    if error == '':
        error = 'There is no error log present'
    if critical == '':
        critical = 'There is no critical log present'
    string = '<div style="color:#0000FF; font-size:30px;"> <b>show syslog </b></div>'
    string += '\n\n'
    string += '<div style="color:#000000; font-size:20px;"> <b>Error..</b> </div>'
    string += '\n\n'
    string += '<div style="color:#FF0000;"><b>' + error + '</b></div>'
    string += '\n\n'
    string += '<div style="color:#000000; font-size:20px;"> <b>Critical..</b> </div>'
    string += '\n\n'
    string += '<div style="color:#FF0000;"><b>' + critical + '</b></div>'
    string += '\n\n\n'
    return string


# this function is used to show syslog 1
def show_syslog_1_gz(i):
    # These all statements are used for formatting the results to show in result screen.
    with gzip.open("/" + i['path'], mode="rt") as f:
        file_content = f.read()
        lst = file_content.split('\n')
        error = ''
        critical = ''
        for x in lst:
            y = re.search('ERROR', x)
            z = re.search('CRITICAL', x)

            if y is not None:
                error += x.replace(' ', '&nbsp;') + '\n\n'
            if z is not None:
                critical += x.replace(' ', '&nbsp;') + '\n\n'
    if error == '':
        error = 'There is no error log present'
    if critical == '':
        critical = 'There is no critical log present'
    string = '<div style="color:#0000FF; font-size:30px;"> <b>show syslog 1 </b></div>'
    string += '\n\n'
    string += '<div style="color:#000000; font-size:20px;"> <b>Error..</b> </div>'
    string += '\n\n'
    string += '<div style="color:#FF0000;"><b>' + error + '</b></div>'
    string += '\n\n'
    string += '<div style="color:#000000; font-size:20px;"> <b>Critical..</b> </div>'
    string += '\n\n'
    string += '<div style="color:#FF0000;"><b>' + critical + '</b></div>'
    string += '\n\n\n'
    return string


# this function is used to show the docker ps
def show_docker_ps(i):
    content = i['contents']
    list = content.split('\n')
    up = 0
    down = 0
    result = ''
    up_entries = ''
    down_entries = ''
    for item in list:
        # regex for searching the statement which contains UP
        x = re.search('Up ', item)
        y = re.search('STATUS', item)
        if len(item) != 0:
            if y is not None:
                result += '<p style="color:#000000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            elif x is None:
                result += '<p style="color:#DE0D82; "> <b>' + item.replace(' ', '&nbsp;') + '</b></p>' + ''
                down_entries += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>' + ''
                down = down + 1
            else:
                result += '<p style="color:#DE0D82;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>' + ''
                up_entries += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>' + ''
                up = up + 1

    # These all statements are used for formatting the results to show in result screen.
    string = '<p style="color:#0000FF; font-size:30px;"> <b>show docker ps </b></p>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '\n\n'
    string += '<p style="color:#09075d;"><b> Number of entries with UP status    : '
    string += str(up) + '</b></p> \n\n'
    string += up_entries
    string += '\n\n'
    string += '<p style="color:#09075d;"><b> Number of entries with DOWN status    : '
    string += str(down) + '</b></p> \n\n'
    string += down_entries
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '\n\n'
    string += result
    string += '\n\n\n'
    return string


# this function is used to show the docker statistics
def show_docker_stats(i):
    # These all statements are used for formatting the results to show in result screen.
    string = '<p style="color:#0000FF; font-size:30px;"> <b>show docker stats </b></p>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b></p>'
    string += '\n\n'
    string += '<p style="color:#DE0D82;"> <b>' + i['contents'].replace(' ', '&nbsp;') + '</b></p>'
    string += '\n\n\n'
    return string


# this function is used to the reboot cause
def show_reboot_cause(i):
    # These all statements are used for formatting the results to show in result screen.
    string = '<p style="color:#0000FF; font-size:30px;"> <b>show reboot cause </b></p>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b></p>'
    string += '\n\n'
    string += '<p style="color:#DE0D82;"> <b>' + i['contents'].replace(' ', '&nbsp;') + '</b></p>'
    string += '\n\n\n'
    return string


# this function is used to show the arp
def show_arp(i):
    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show arp (linux) </b></div>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b></p>'
    string += '\n\n'
    string += '<p style="color:#DE0D82;"> <b>' + i['contents'].replace(' ', '&nbsp;') + '</b></p>'
    string += '\n\n\n'
    return string


# this function is used to show the configuration
def show_config(i):
    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show vlan (linux) </b></div>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b></p>'
    string += '\n\n'
    string += '<p style="color:#DE0D82;"> <b>' + i['contents'].replace(' ', '&nbsp;') + '</b></p>'
    string += '\n\n\n'
    return string


# this function is used to show memory information
def show_meminfo(i):
    # These all statements are used for formatting the results to show in result screen.
    content = i['contents']
    items = content.split('\n')
    string = ''
    for i in range(0, 3):
        string += items[i].replace(' ', '&nbsp;') + '\n\n'
    return string


# this function is used to show broadcom ps
def show_broadcom_ps(i):
    try:
        content = i['contents']
        items = content.split('\n')
    except:
        items= i.splitlines()
    up = 0
    down = 0
    result = ''
    correct_or_not = False
    for item in items:
        # regex
        x = re.search('up ', item)
        y = re.search('down ', item)
        z = re.search('!ena ', item)
        if x is not None:
            up = up + 1
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        elif y is not None or z is not None:
            down = down + 1
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'

        else:
            result += '<p style="color:#DE0D82;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
    if up+down >1:
        correct_or_not = True
    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show broadcom ps </b></div>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '<br>'
    string += '<p style="color:#09075d;"> <b>' + 'number of total links     :'.replace(' ', '&nbsp;') + str(
        up + down) + '</b></p>'
    string += '<p style="color:#014421;"> <b>' + 'number of up links        :'.replace(' ', '&nbsp;') + str(
        up) + '</b></p>'
    string += '<p style="color:#FF0000;"> <b>' + 'number of down links      :'.replace(' ', '&nbsp;') + str(
        down) + '</b></p>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '<br>'
    string += result
    string += '<br><br>'
    return [string, correct_or_not]


# this function is used to show frr interfaces
def show_frr_interfaces(i):
    try:
        content = i['contents']
        items = content.split('\n')
    except:
        items = i.splitlines()
    count = 0
    result = ''
    correct_or_not = False
    for item in items:
        # regex
        x = re.search('Interface', item)
        y = re.search('line protocol', item)
        if x is not None and y is not None:
            count = count + 1
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        else:
            result += '<p style="color:#DE0D82;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
    if count >1 :
        correct_or_not = True
    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show frr interfaces </b></div>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '<br>'
    string += '<p style="color:#09075d;"> <b>number of total interfaces      :' + str(count) + '</b></p>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '<br>'
    string += result
    string += '<br><br>'
    return [string, correct_or_not]


# this function is used to sho the fp summary
def show_fp_summary(i):
    content = i['contents']
    items = content.split('\n')
    count = 0
    result = ''
    for item in items:
        # regex
        x = re.search('EID', item)
        if x is not None:
            count = count + 1
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        else:
            result += item.replace(' ', '&nbsp;') + '\n'

    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show fp summary </b></div>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '\n\n'
    string += '<p style="color:#09075d;"> <b>number of total EID \'s      :' + str(count) + '</b></p>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '\n\n'
    string += result
    string += '\n\n\n'
    return string


# this function is used to show broadcom knet link
def show_broadcom_knet_link(i):
    try:
        content = i['contents']
        items = content.split('\n')
    except:
        items = i.splitlines()
    correct_or_not = False
    down = 0
    up = 0
    result = ''
    for item in items:
        # regex
        x = re.search('down', item)
        y = re.search('up', item)
        if x is not None:
            down = down + 1
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        elif y is not None:
            up = up + 1
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        else:
            result += '<p style="color:#DE0D82;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
    # These all statements are used for formatting the results to show in result screen.
    if up+down > 1:
        correct_or_not = True
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show broadcom knet link </b></div>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '<br>'
    string += '<p style="color:#09075d;"> <b>number of total interfaces      :' + str(up + down) + '</b></p>'
    string += '<p style="color:#FF0000;"> <b>number of total DOWN interfaces :' + str(down) + '</b></p>'
    string += '<p style="color:#014421;"> <b>number of total UP interfaces   :' + str(up) + '</b></p>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '<br>'
    string += result
    string += '<br><br>'
    return [string, [up + down, up, down], correct_or_not]


# this function is used to show the bridge vlan
def show_bridge_vlan(i):
    content = i['contents']
    items = content.split('\n')
    result = ''
    lst = []
    flag = False
    for item in items:
        # regex
        x = re.search('Bridge', item)
        lst1 = item.split()
        if x is not None:
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            values = item.split()
            lst.append(values[1])
            flag = True
        elif flag == True and len(lst1) == 1:
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            lst.append(lst1[0])
        else:
            flag = False
            result += '<p style="color:#DE0D82;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'

    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show bridge vlan </b></div>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '\n\n'
    string += '<p style="color:#014421;"> <b>' + 'number of bridges: ' + str(len(lst)) + '\n' + '</b></p>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '\n\n'
    string += result
    string += '\n\n\n'
    return [string, lst]


# this function is used to show version
def show_version(i, meminfo_result):
    try:
        content = i['contents']
        contents = i['contents']
        items = content.split('\n')
    except:
        contents = i.replace('\n', '<br>')

        items = i.splitlines()
    result = ''
    correct_or_not = False
    for item in items:
        # regex
        x = re.search('SONiC Software Version:', item)
        y = re.search('HwSKU:', item)
        z = re.search('ASIC:', item)
        if x is not None:
            lst = item.split(':')
            correct_or_not = True
            result += '<p style="color:#014421;"> <b>' + 'SONiC Software Version : '.replace(' ', '&nbsp;') + lst[
                1] + '</b></p>'
        if y is not None:
            lst = item.split(':')
            result += '<p style="color:#014421;"> <b>' + 'Platform               : '.replace(' ', '&nbsp;') + lst[
                1] + '</b></p>'
        if z is not None:
            lst = item.split(':')
            result += '<p style="color:#014421;"> <b>' + 'ASIC                   : '.replace(' ', '&nbsp;') + lst[
                1] + '</b></p>'
    if meminfo_result is not None:
        result += '<p style="color:#000000; font-size:20px;"> <b>memory information (linux)</b> </p>\n\n'
        result += '<p style="color:#014421;"> <b>' + meminfo_result.replace(' ', '&nbsp;') + '</b></p>'

    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show version </b></div>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '<br>'
    string += result
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '<br>'
    string += '<p style="color:#DE0D82;"> <b>' + contents.replace(' ', '&nbsp;') + '</b></p>'
    string += '<br><br>'
    return [string, correct_or_not]

# this function is used to show top
def show_top(i):
    try:
        content = i['contents']
        items = content.split('\n')
    except:
        items = i.splitlines()
    result = ''
    data = ''
    correct_or_not = False
    for item in items:
        # regex to find the CPU percentage
        x = re.search('Cpu', item)
        if x is not None:
            lst = item.split()
            correct_or_not = True
            result += '<p style="color:#014421;"> <b>' + 'Percentage CPU sys ' + lst[3] + '</b></p>'
        data += '<p style="color:#DE0D82;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'

    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show top </b></div>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '<br>'
    string += result
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '<br>'
    string += data
    string += '<br><br>'
    return [string, correct_or_not]


# This function is used to show lldp control data
def show_lldpctl(i):
    try:
        content = i['contents']
        contents = i['contents']
        items = content.split('\n')
    except:
        items = i.splitlines()
        contents = i.replace('\n', '<br>')
    result = ''
    count = 0
    correct_or_not = False
    for item in items:
        # regex to find Interface ChassisId Management id
        x = re.match('Interface:', item)
        y = re.search('ChassisID:', item)
        z = re.search('MgmtIP:', item)
        if x is not None:
            count = count + 1
            result += '\n<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        elif y is not None:
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        elif z is not None:
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
    if count>0:
        correct_or_not = True
    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show lldp control </b></div>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '<br>'
    string += '<p style="color:#09075d;"> <b>Total number of interfaces: ' + str(count) + '</b></p>' + '\n'
    result += '<p style="color:#014421;"> <b>' + result + '</b></p>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '<br>'
    string += '<p style="color:#DE0D82;"> <b>' + contents.replace(' ', '&nbsp;') + '</b></p>'
    string += '<br><br>'
    return [string, correct_or_not]


# this function is used to show the port summary
def show_port_summary(i):
    try:
        content = i['contents']
        items = content.split('\n')
    except:
        items= i.splitlines()
    result = ''
    disable = 0
    enable = 0
    correct_or_not = False
    for item in items:
        # regex to find Disabled entries
        x = re.search('Disabled', item)
        # regex to find the Enabled entries
        y = re.search('Enabled', item)
        if x is None and y is None:
            result += '<p style="color:#DE0D82;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        elif x is not None:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            disable = disable + 1
        elif y is not None:
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            enable = enable + 1
    if enable> 0  or disable> 0:
        correct_or_not = True
    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show port summary </b></div>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '<br>'
    string += '<p style="color:#014421;"> <b>' + 'Number of entries which are enabled        :'.replace(' ', '&nbsp')
    string += str(enable) + '</b></p>'
    string += '<p style="color:#FF0000;"> <b>' + 'Number of entries which are disabled       :'.replace(' ', '&nbsp')
    string += str(disable) + '</b></p>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '<br>'
    string += result
    string += '<br><br>'
    return [string, correct_or_not]


# this function is used to show mirror summary
def show_mirror_summary(i):
    # These all statements are used for formatting the results to show in result screen.
    content = i['contents']
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show mirror summary </b></div>'
    string += '\n\n'
    string += '<p style="color:#DE0D82;"> <b>' + i['contents'].replace(' ', '&nbsp;') + '</b></p>'
    string += '\n\n\n'
    return string


# this function is used to show platform summary
def show_platform_summary(i):
    result = ''
    content = i['contents']
    items = content.split('\n')
    proper_spacing = dict()
    left_max_length = 0
    right_max_length = 0
    # used to show data into formatted form
    for item in items:
        lst = item.split(':')
        if len(lst) == 2:
            if left_max_length < len(lst[0]):
                left_max_length = len(lst[0])
            if right_max_length < len(lst[1]):
                right_max_length = len(lst[1])
            proper_spacing[lst[0]] = lst[1]
    left_max_length += 2
    right_max_length += 2
    for ii, jj in proper_spacing.items():
        left = ii
        right = jj
        for spaces in range(len(ii), left_max_length + 1):
            left += ' '
        for spaces in range(len(jj), right_max_length + 1):
            right += ' '
        result += '<p style="color:#014421;"> <b>' + left.upper().replace(' ', '&nbsp') + ':' + right.replace(' ',
                                                                                                              '&nbsp') + '</b></p>'
    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px"> <b> show platform summary </b></div>'
    string += '\n\n'
    string += result
    string += '\n\n\n'
    return string


# this function is used to show ip neighbour
def show_ip_neigh(i):
    result = ''
    content = i['contents']
    items = content.split('\n')
    permanent = 0
    noarp = 0
    reachable = 0
    stale = 0
    none = 0
    incomplete = 0
    delay = 0
    probe = 0
    failed = 0
    # used to count the status
    for item in items:
        a = re.search('PERMANENT', item)
        b = re.search('NOARP', item)
        c = re.search('REACHABLE', item)
        d = re.search('STALE', item)
        e = re.search('NONE', item)
        f = re.search('INCOMPLETE', item)
        g = re.search('DELAY', item)
        h = re.search('PROBE', item)
        ii = re.search('FAILED', item)
        if a is not None:
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            permanent = permanent + 1
        elif b is not None:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            noarp = noarp + 1
        elif c is not None:
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            reachable = reachable + 1
        elif d is not None:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            stale = stale + 1
        elif e is not None:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            none = none + 1
        elif f is not None:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            incomplete = incomplete + 1
        elif g is not None:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            delay = delay + 1
        elif h is not None:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            probe = probe + 1
        elif ii is not None:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            failed = failed + 1

    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show ip neighbour </b></div>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '\n\n'
    string += '<p style="color:#09075d;"><b>' + 'Number of entries                         : '.replace(' ', '&nbsp;')
    string += str(
        permanent + noarp + reachable + stale + none + incomplete + delay + probe + failed) + '</b></p>'
    string += '<p style="color:#014421;"><b>' + 'Number of entries with status PERMANENT   : '.replace(' ', '&nbsp;')
    string += str(permanent) + '</b></p>'
    string += '<p style="color:#FF0000;"><b>' + 'Number of entries with status NO ARP      : '.replace(' ', '&nbsp;')
    string += str(noarp) + '</b></p>'
    string += '<p style="color:#014421;"><b>' + 'Number of entries with status REACHABLE   : '.replace(' ', '&nbsp;')
    string += str(reachable) + '</b></p>'
    string += '<p style="color:#FF0000;"><b>' + 'Number of entries with status STALE       : '.replace(' ', '&nbsp;')
    string += str(stale) + '</b></p>'
    string += '<p style="color:#FF0000;"><b>' + 'Number of entries with status NONE        : '.replace(' ', '&nbsp;')
    string += str(none) + '</b></p>'
    string += '<p style="color:#FF0000;"><b>' + 'Number of entries with status INCOMPLETE  : '.replace(' ', '&nbsp;')
    string += str(incomplete) + '</b></p>'
    string += '<p style="color:#FF0000;"><b>' + 'Number of entries with status DELAY       : '.replace(' ', '&nbsp;')
    string += str(delay) + '</b></p>'
    string += '<p style="color:#FF0000;"><b>' + 'Number of entries with status PROBE       : '.replace(' ', '&nbsp;')
    string += str(probe) + '</b></p>'
    string += '<p style="color:#FF0000;"><b>' + 'Number of entries with status FAILED      : '.replace(' ', '&nbsp;')
    string += str(failed) + '</b></p>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '\n\n'
    string += result
    string += '\n\n\n'
    return string


# this function used to show the bgp summary
def show_bgp_summary(i):
    content = i['contents']
    result = ''
    ans = ''
    AS = dict()
    items = content.split('\n')
    for item in items:
        # regex to find the ip address without subnet
        x = re.match('([01]?\d\d?|2[0-4]\d|25[0-5])(\.[01]?\d\d?|\.2[0-4]\d|\.25[0-5]){3}', item)
        y = re.match('Neighbor', item)
        z = re.match('Total number of neighbors', item)
        establish = re.search('Established', item)
        if x is not None:
            lst = item.split()
            AS[lst[2]] = AS.get(lst[2], 0) + 1
            if establish is not None:
                result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            else:
                result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        elif y is not None:
            result += '<p style="color:#000000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        elif z is not None:
            ans += '<p style="color:#09075d;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show bgp summary </b></div>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '\n\n'
    string += ans
    string += '<p style="color:#014421;"> <b>' + 'Total number of AS ' + str(len(AS)) + '</b></p>'
    for i, j in AS.items():
        string += '<p style="color:#014421;"> <b>' + 'number of entries with AS ' + i + ' ' + str(j) + '\n' + '</b></p>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '\n\n'
    string += result
    string += '\n\n\n'
    return string


# This function match the statement which starts from IP address e.g, 10.0.0.1/32
def show_ip_route(i):
    try:
        content = i['contents']
        list = content.split('\n')
    except:
        list = i.splitlines()
    count = 0
    result = ''
    linkdown = 0
    correct_or_not = False
    for item in list:
        # regex match the statement starts with an IP address
        x = re.match('([1-9]|[1-9][0-9]{1,3})\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/?[0-9]?[0-9]?(/[0-9]{1,2}|/2[0-4][0-9]|/25[0-5])', item)
        if x is None:
            result += '<p style="color:#DE0D82;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        else:
            # regex search the statement which contains linkdown
            y = re.search('linkdown', item)
            if y is not None:
                result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
                linkdown = linkdown + 1
            else:
                result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            count = count + 1
    if count > 0:
        correct_or_not = True
    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show ip route </b></div><br>'
    string += ''
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p><br>'
    string += ''
    string += '<p style="color:#09075d;"> <b>' +'Number of entries                  : '.replace(' ', '&nbsp;')
    string += str(count) + '</b></p><br>'
    string += ''
    string += '<p style="color:#FF0000;"> <b>' + 'Number of entries with linkdown    : '.replace(' ', '&nbsp;')
    string += str(linkdown) + '</b></p><br>'
    string += ''
    string += '<p style="color:#014421;"> <b>' + 'Number of entries without linkdown : '.replace(' ', '&nbsp;')
    string += str(count - linkdown) + '</b></p><br>'
    string += ''
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p><br>'
    string += ''
    string += result
    string += '<br><br>'
    return [string, correct_or_not]


# This function match the statement which starts from mac-address e.g, 01:01:01:01:01:01
def show_bridge_fdb(i):
    try:
        content = i['contents']
        list = content.split('\n')
    except:
        list = i.splitlines()

    interface = dict()

    count = 0
    result = ''
    correct_or_not = False
    for item in list:
        # regex match the statement starts with a mac-address
        result += '<p style="color:#DE0D82;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        value = item.split()
        x = re.match('(?:[0-9a-fA-F]:?){12}', item)
        if x is None:
            continue
        else:
            interface[value[2]] = interface.get(value[2], 0) + 1
            count = count + 1
    if count>0 :
        correct_or_not = True
    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show bridge fdb </b></div>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '<br>'
    string += '<p style="color:#09075d;"><b>' + 'Number of entries                              : '.replace(' ','&nbsp;')
    string += str(count) + '</b></p>'
    for key, value in interface.items():
        ans = key
        for space in range(len(key), 15):
            ans += ' '
        string += '<p style="color:#014421;"> <b>' +'Number of entries in interface ' + ans.replace(' ',
                                                                                                '&nbsp;') + ' : ' + str(
            value) + ' </b></p>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '<br>'
    string += result
    string += '<br><br>'
    return [string, correct_or_not]


# This function searches for number of UP and DOWN Interfaces on teh basis of oper.
def show_interface_status(i):
    try:
        content = i['contents']
        list = content.split('\n')
    except:
        list = i.splitlines()
    result = ''
    up=0
    down=0
    correct_or_not = False
    for item in list:
        # regex for searching the statement which contains UP
        x = re.search('up', item)
        # regex for searching the statement which contains DOWN
        y = re.search('down', item)
        if x is None and y is None:
            result += '<p style="color:#000000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        elif x is None:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            down = down + 1
        elif y is None:
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            up = up + 1
        elif x.span()[1] < y.span()[1]:
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            up = up + 1
        else:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            down = down + 1
    if up+down >0 :
        correct_or_not = True
    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show interface status </b></div><br>'
    string += ''
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p><br>'
    string += ''
    string += '<p style="color:#09075d;"><b>' + 'Total number of Interfaces      : '.replace(' ', '&nbsp;')
    string += str(up + down) + '</b></p>'
    string += '<p style="color:#014421;"><b>' + 'Total number of UP Interfaces   : '.replace(' ', '&nbsp;')
    string += str(up) + '</b></p>'
    string += '<p style="color:#FF0000;"><b>' + 'Total number of DOWN Interfaces : '.replace(' ', '&nbsp;')
    string += str(down) + '</b></p><br>'
    string += ''
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p><br>'
    string += ''
    string += result
    string += '<br> <br>'
    return [string, [up+down, up, down],  correct_or_not]


# This function searches for number of UP and DOWN Interfaces on the basis of oper.
def show_ip_interface(i):
    try:
        content = i['contents']
        list = content.split('\n')
    except:
        list = i.splitlines()
    up = 0
    down = 0
    result = ''
    ans= '-1'
    correct_or_not = False
    for item in list:
        # regex for searching the statement which contains UP
        x = re.search('(?s:.*)up', item)
        # regex for searching the statement which contains DOWN
        y = re.search('(?s:.*)down', item)
        if x is None and y is None:
            result += '<p style="color:#000000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        elif x is None:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            down = down + 1
        elif y is None:
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            up = up + 1
        elif x.span()[1] > y.span()[1]:
            result += '<p style="color:#014421;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            up = up + 1
        elif x.span()[1] < y.span()[1]:
            result += '<p style="color:#FF0000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
            down = down + 1
        else:
            result += item
    # These all statements are used for formatting the results to show in result screen.
    if up+down > 0:
        correct_or_not = True
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show ip interface </b></div>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Analysis..</b> </p>'
    string += '<br>'
    string += '<p style="color:#09075d;"><b>'+'Total number of Interfaces      : '.replace(' ', '&nbsp;')
    string += str(up + down) + '</b></p>'
    string += '<p style="color:#014421;"><b>'+'Total number of UP Interfaces   : '.replace(' ', '&nbsp;')
    string += str(up) + '</b></p>'
    string += '<p style="color:#FF0000;"><b>'+'Total number of DOWN Interfaces : '.replace(' ', '&nbsp;')
    string += str(down) + '</b></p>'
    string += '<br>'
    string += '<p style="color:#000000; font-size:20px;"> <b>Data..</b> </p>'
    string += '<br>'
    string += result
    string += '<br><br>'
    return [string, correct_or_not]


# This function searches for number of Vlan Entries.
def show_vlan_summary(i, lst):
    content = i['contents']
    list = content.split('\n')
    result = ''
    count = 0
    for item in list:
        x = re.search('enabled', item)
        y = re.search('disabled', item)
        z = re.search('tagged', item)
        u = re.search('untagged', item)
        data_lst = item.split()
        if x is None and y is None and z is None and u is None:
            # formatted text with color
            result += '<p style="color:#000000;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        else:
            result += '<p style="color:#DE0D82;"> <b>' + item.replace(' ', '&nbsp;') + '</b></p>'
        try:

            k = int(data_lst[1])
            count = count+1
        except:
            pass


    # These all statements are used for formatting the results to show in result screen.
    string = '<div style="color:#0000FF; font-size:30px;"> <b> show vlan summary '+'</b></div>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>'+'Analysis..'+'</b> </p>'
    string += '\n\n'
    string += '<p style="color:#09075d;"><b>' + 'Number of entries : '.replace(' ', '&nbsp;')
    string += str(count) + '</b></p>'
    string += '\n'
    string += '<p style="color:#014421;"> <b>' + 'available bridges from "show bridge vlan" command  :' + str(
        lst) + '</b></p>'
    string += '\n\n'
    string += '<p style="color:#000000; font-size:20px;"> <b>'+ 'Data..'+'</b> </p>'
    string += '\n\n'
    string += result
    string += '\n\n\n'
    return string

# ---------------------------------------------------------------------------------------------------------------
