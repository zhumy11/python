#!/usr/bin/env python

from subprocess import Popen, PIPE

def getIP():
    p = Popen(['ifconfig'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    return stdout

def getDmi():
    p = Popen(['dmidecode'], stdout=PIPE)
    dmi_con = p.stdout.read()
    return dmi_con
    
def gen(data):
    new_line = ''
    lines = []
    data_list = [i for i in data.split('\n') if i]
    for line in data_list:
        if line[0].strip():
            lines.append(new_line)
            new_line = line + '\n'
        else:
            new_line += line + '\n'
    lines.append(new_line)
    return [i for i in lines if i]

def parseIP(ip_list):
    ip_dic = {}
    ip_list = [i for i in ip_list if not i.startswith('lo')]
    for lines in ip_list:
        line_list = lines.split('\n')
        devname = line_list[0].split()[0]
        macaddr = line_list[0].split()[-1]
        ipaddr = line_list[1].split()[1].split(':')[1]
        ip_dic[devname] = ipaddr
    return ip_dic

def parseDmi(dmi_list):
    dmi_dic = {}
    dmi_list = [i for i in dmi_list if i.startswith('System Information')]
    dmi_list = [i for i in dmi_list[0].split('\n')[1:] if i]
    dic = dict([i.strip().split(':') for i in dmi_list])
    dmi_dic['vender'] = dic['Manufacturer'].strip()
    dmi_dic['product'] = dic['Product Name'].strip()
    dmi_dic['SN'] = dic['Serial Number'].strip()
    return dmi_dic

def getHostname(f):
    with open(f) as fd:
        for line in fd:
            if line.startswith('HOSTNAME'):
                hostname = line.split('=')[1].strip()
                break
    return {'hostname':hostname}

def getOS(f):
    with open(f) as fd:
        for line in fd:
            if line.startswith('CentOS'):
                os = line.strip()
                break
    return {'OS':os}

def getCPU(f):
    num = 0
    with open(f) as fd:
        for line in fd:
            if line.startswith('processor'):
                num += 1
            if line.startswith('model name'):
                cpu_model = line.split(':')[1].strip()
    return {'cpu_model':cpu_model, 'cpu_num':num}

def getMem(f):
    with open(f) as fd:
        for line in fd:
            if line.startswith('MemTotal'):
                mem = int(line.split()[1].strip())
                break
    mem = "%sMB" % int(mem/1024.0)
    return {'memory':mem}

if __name__ == '__main__':
    dic = {}
    ip_con = getIP()
    ip_list = gen(ip_con)
    ip = parseIP(ip_list) 
    dmi_con = getDmi()
    dmi_list = gen(dmi_con)
    dmi = parseDmi(dmi_list)
    hostname = getHostname('/etc/sysconfig/network')
    os = getOS('/etc/issue')
    cpu = getCPU('/proc/cpuinfo')
    mem = getMem('/proc/meminfo')
    dic.update(ip)
    dic.update(dmi)
    dic.update(hostname)
    dic.update(os)
    dic.update(cpu)
    dic.update(mem)
    print dic
