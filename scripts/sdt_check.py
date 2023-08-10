import linecache

import os
os.system("")  # enables ansi escape characters in terminal

COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

##Set Variable to None
vm=None
vm_name_ip=dict()
gw_vm_list=list()
gw_vm_ip_list=list()
vm_list=list()
cp_ip_list=list()
pool_ip_list=list()
iSCSI_A_start=list()
iSCSI_A_end=list()
iSCSI_B_start=list()
iSCSI_B_end=list()
temp_domain=list()
controller_domain=list()
ere_version_list=list()



## Get the Directory location of file
dir=input('Directory Location of the file : ')
print(dir)

## Open VMAAS json files for reading
try:
    vmaas_file=open(dir+'\_vmaas.json')
    
except:
    print(COLOR["RED"],'\n VMaaS SDT File not found in the directory',dir,COLOR["ENDC"])
    quit()
    
## Open BASE json files for reading
try:
    base_file=open(dir+'\_base.json')
except:
    print(COLOR["RED"],'\n Base Config SDT File not found in the directory',dir,COLOR["ENDC"])
    quit()
       

## Read each line from SDT jason

def vmname(filename):
    temp1=(linecache.getline(dir+filename, i)).lstrip().rstrip().rstrip(',').split()
    temp1=temp1[1].strip('"')
    return temp1

def vmip(filename):
    temp2=(linecache.getline(dir+filename, (i+14))).lstrip().rstrip().split()
    temp2=temp2[1].strip('"')
    return temp2


## Read each line from base jason
for i, ln in enumerate(base_file, start=2):
    if '"purpose": "GL Metal Primary"' in ln:
            external_base=vmname("\_base.json")[0:9]

    elif '"componentId": "nw-007"' in ln:
            iSCSI_A=(linecache.getline(dir+'\_base.json', (i))).lstrip().rstrip().rstrip(',').split('"')[3]
            iSCSI_A_net=(linecache.getline(dir+'\_base.json', (i+7))).lstrip().rstrip().rstrip(',').split('"')[3]
            iSCSI_A_sub=(linecache.getline(dir+'\_base.json', (i+9))).lstrip().rstrip().rstrip(',').split('"')[3]
            
    elif '"componentId": "nw-008"' in ln:
            iSCSI_B=(linecache.getline(dir+'\_base.json', (i))).lstrip().rstrip().rstrip(',').split('"')[3]
            iSCSI_B_net=(linecache.getline(dir+'\_base.json', (i+7))).lstrip().rstrip().rstrip(',').split('"')[3]
            iSCSI_B_sub=(linecache.getline(dir+'\_base.json', (i+9))).lstrip().rstrip().rstrip(',').split('"')[3]
                     
    elif '"domainSearchName":' in ln:
            domain_base=(linecache.getline(dir+'\_base.json', (i-1))).lstrip().rstrip().rstrip(',').split('"')[3]
    
    elif '"primaryDnsIpAddress":' in ln:
            dns_ip=(linecache.getline(dir+'\_base.json', (i-1))).lstrip().rstrip().rstrip(',').split('"')[3]
    #        print(domain)
    #    print('\nBase Config jason do not have FS External subnet defined')
    #    quit()
        
## Read through vmaas jason file
for i, ln in enumerate(vmaas_file):
    if '"role": "ereController"' in ln:
        vm_name_ip['ere_Controller']=vmname("\_vmaas.json")
        vm_name_ip['ere_Controller_ip']=vmip("\_vmaas.json")
        temp_domain=vm_name_ip['ere_Controller'].split('.')
        controller_domain.append(temp_domain[1]+"."+temp_domain[2])
        
    elif '"role": "ereArbiter"' in ln:
        vm_name_ip['ere_Arbiter']=vmname("\_vmaas.json")
        vm_name_ip['ere_Arbiter_ip']=vmip("\_vmaas.json")
        temp_domain=vm_name_ip['ere_Arbiter'].split('.')
        controller_domain.append(temp_domain[1]+"."+temp_domain[2])
        
    elif '"role": "ereShadow"' in ln:
        vm_name_ip['ere_Shadow']=vmname("\_vmaas.json")
        vm_name_ip['ere_Shadow_ip']=vmip("\_vmaas.json")
        temp_domain=vm_name_ip['ere_Shadow'].split('.')
        controller_domain.append(temp_domain[1]+"."+temp_domain[2])
        
    elif '"role": "ereGateway"' in ln:
        gw_vm_list.append(vmname("\_vmaas.json"))
        gw_vm_ip_list.append(vmip("\_vmaas.json"))
        #temp_domain=gw_vm_list.split('.')
        #doamin(temp_domain)
        #print(controller_domain)
        
    elif '"role": "ereSquid"' in ln:
        gw_vm_list.append(vmname("\_vmaas.json"))
        gw_vm_ip_list.append(vmip("\_vmaas.json"))
        #temp_domain=gw_vm_list.split('.')
        #doamin(temp_domain)
        #print(controller_domain)
    
    elif '"cpBridgeInterface"' in ln:
        temp1=(linecache.getline(dir+'\_vmaas.json', (i+7))).lstrip().rstrip().split()[1].strip('"')
        temp2=(linecache.getline(dir+'\_vmaas.json', (i+13))).lstrip().rstrip().split()[1].strip('"')
        temp3=(linecache.getline(dir+'\_vmaas.json', (i+19))).lstrip().rstrip().split()[1].strip('"')
        cp_ip_list=[temp1,temp2,temp3]
        
    elif '"name": "CaaS FS Management"' in ln:
        vm_name_ip['CaaS_FS_name']=(linecache.getline(dir+'\_vmaas.json', (i+1))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        vm_name_ip['CaaS_FS_IP']=(linecache.getline(dir+'\_vmaas.json', (i+15))).lstrip().rstrip().rstrip(',').split()[1].strip('"')
        vm_name_ip['CaaS_FS_Subnet']=(linecache.getline(dir+'\_vmaas.json', (i+16))).lstrip().rstrip().rstrip(',').split()[1].strip('"')
        vm_name_ip['CaaS_FS_Gateway']=(linecache.getline(dir+'\_vmaas.json', (i+17))).lstrip().rstrip().rstrip(',').split()[1].strip('"')
    
    elif '"ereClusterName"' in ln:
        ere_version=(linecache.getline(dir+'\_vmaas.json', (i-1))).lstrip().rstrip().rstrip(',').split('"')[3]
        ere_version_list=(linecache.getline(dir+'\_vmaas.json', (i-1))).lstrip().rstrip().rstrip(',').split('"')[3].split('.')
        ere_Cluster_Name=(linecache.getline(dir+'\_vmaas.json', (i+1))).lstrip().rstrip().rstrip(',').split('"')[3]
        ere_Domain_Name=(linecache.getline(dir+'\_vmaas.json', (i+3))).lstrip().rstrip().rstrip(',').split('"')[3]
        ere_Usr_Name=(linecache.getline(dir+'\_vmaas.json', (i+7))).lstrip().rstrip().rstrip(',').split('"')[3]
        ere_Pwd_Name=(linecache.getline(dir+'\_vmaas.json', (i+8))).lstrip().rstrip().rstrip(',').split('"')[3]

        
    elif '"purpose": "glmetal_managed"' in ln:
        temp1=(linecache.getline(dir+'\_vmaas.json', (i+2))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        temp2=(linecache.getline(dir+'\_vmaas.json', (i+3))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        temp3=(linecache.getline(dir+'\_vmaas.json', (i+7))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        temp4=(linecache.getline(dir+'\_vmaas.json', (i+8))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        temp5=(linecache.getline(dir+'\_vmaas.json', (i+12))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        temp6=(linecache.getline(dir+'\_vmaas.json', (i+13))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        temp7=(linecache.getline(dir+'\_vmaas.json', (i+17))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        temp8=(linecache.getline(dir+'\_vmaas.json', (i+18))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        temp9=(linecache.getline(dir+'\_vmaas.json', (i+22))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        temp10=(linecache.getline(dir+'\_vmaas.json', (i+23))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        pool_ip_list=[temp1,temp2,temp3,temp4,temp5,temp6,temp7,temp8,temp9,temp10]
        
    elif '"This data is for FS External IPs to be used by the CAAS Service"' in ln:
        external_vmaas=(linecache.getline(dir+'\_vmaas.json', (i+2))).lstrip().rstrip().rstrip(',').split('"')[3][0:9]
    
    elif '"$comment": "This data is for iSCSIA IPs to be used by the CAAS Service"' in ln:
        temp1=(linecache.getline(dir+'\_vmaas.json', (i+2))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        iSCSI_A_start.append(temp1)
        temp2=(linecache.getline(dir+'\_vmaas.json', (i+3))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        iSCSI_A_end.append(temp2)
    
    elif '"$comment": "This data is for iSCSIB IPs to be used by the CAAS Service"' in ln:
        temp1=(linecache.getline(dir+'\_vmaas.json', (i+2))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        iSCSI_B_start.append(temp1)
        temp2=(linecache.getline(dir+'\_vmaas.json', (i+3))).lstrip().rstrip().rstrip(',').split('"')[3].strip('"')
        iSCSI_B_end.append(temp2)
        
print(COLOR["HEADER"],'\nMake sure the IPs and Names Matches the Standard IPs\n',COLOR["ENDC"])

print(vm_name_ip['ere_Controller'],':',vm_name_ip['ere_Controller_ip'])
if (vm_name_ip['ere_Controller_ip']=='172.28.216.155'):
    print(COLOR["GREEN"],'ERE Controller IP is Correct\n',COLOR["ENDC"])
else:    
    print(COLOR["RED"],'DEVIATION - Expect IP for ERE Controller : 172.28.216.155\n',COLOR["ENDC"]) 

print(vm_name_ip['ere_Arbiter'],':',vm_name_ip['ere_Arbiter_ip'])
if (vm_name_ip['ere_Arbiter_ip']=='172.28.216.156'):
    print(COLOR["GREEN"],'ERE Arbiter IP is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect IP for ERE Arbiter : 172.28.216.156\n',COLOR["ENDC"]) 

print(vm_name_ip['ere_Shadow'],':',vm_name_ip['ere_Shadow_ip'])
if (vm_name_ip['ere_Shadow_ip']=='172.28.216.157'):
    print(COLOR["GREEN"],'ERE Shadow IP is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect IP for ERE Shadow : 172.28.216.157\n',COLOR["ENDC"]) 

print(gw_vm_list[0],':',gw_vm_ip_list[0])
if (gw_vm_ip_list[0]=='172.28.216.158'):
    print(COLOR["GREEN"],'ERE Gateway 1 IP is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect IP for ERE Gateway 1 : 172.28.216.159\n',COLOR["ENDC"])

print(gw_vm_list[1],':',gw_vm_ip_list[1])
if (gw_vm_ip_list[1]=='172.28.216.159'):
    print(COLOR["GREEN"],'ERE Gateway 2 IP is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect IP for ERE Gateway 2 : 172.28.216.159\n',COLOR["ENDC"])

print(gw_vm_list[2],':',gw_vm_ip_list[2])
if (gw_vm_ip_list[2]=='172.28.216.160'):
    print(COLOR["GREEN"],'ERE Squid IP is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect IP for Squid VM : 172.28.216.160\n',COLOR["ENDC"])

print('CP Bridge Interface IPs',':',cp_ip_list[0],',',cp_ip_list[1],',',cp_ip_list[2])
if(cp_ip_list[0]=='172.28.216.152' and cp_ip_list[1]=='172.28.216.153' and cp_ip_list[2]=='172.28.216.154'):
    print(COLOR["GREEN"],'CaaS IPs for the CP Bridge is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect IPs for CP Bridge Interface : 172.28.216.152 , 172.28.216.153 , 172.28.216.154\n',COLOR["ENDC"])

print('CaaS IP Pool for glmetal_managed',':',pool_ip_list[0],'-',pool_ip_list[1])
if(pool_ip_list[0]=='172.28.216.2' and pool_ip_list[1]=='172.28.216.151'):
    print(COLOR["GREEN"],'CaaS IP Pool for glmetal_managed is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect IP Pool for glmetal_managed : 172.28.216.2 - 172.28.216.151\n',COLOR["ENDC"])

print('CaaS IP Pool for containers_platform',':',pool_ip_list[2],'-',pool_ip_list[3])
if(pool_ip_list[2]=='172.28.216.152' and pool_ip_list[3]=='172.28.216.211'):
    print(COLOR["GREEN"],'CaaS IP Pool for containers_platform is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect IP Pool for containers_platform : 172.28.216.152 - 172.28.216.211\n',COLOR["ENDC"])

print('CaaS IP Pool for vm_service',':',pool_ip_list[4],'-',pool_ip_list[5])
if(pool_ip_list[4]=='172.28.216.212' and pool_ip_list[5]=='172.28.221.254'):
    print(COLOR["GREEN"],'CaaS IP Pool for vm_service is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect IP Pool for containers_platform : 172.28.216.212 - 172.28.221.254\n',COLOR["ENDC"])

print('CaaS Pool IPs for bm_service',':',pool_ip_list[6],'-',pool_ip_list[7])
if(pool_ip_list[6]=='172.28.221.255' and pool_ip_list[7]=='172.28.222.254'):
    print(COLOR["GREEN"],'CaaS IP Pool for bm_service is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect IP Pool for bm_service : 172.28.221.255 - 172.28.222.254\n',COLOR["ENDC"])
      
print('CaaS Pool IPs for expansion_ips',':',pool_ip_list[8],'-',pool_ip_list[9])
if(pool_ip_list[8]=='172.28.222.255' and pool_ip_list[9]=='172.28.223.254'):
    print(COLOR["GREEN"],'CaaS IP Pool for expansion_ips is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect IP Pool for expansion_ips : 172.28.222.255 - 172.28.223.254\n',COLOR["ENDC"])

print('CaaS FS Network Name' ,':', vm_name_ip['CaaS_FS_name'])

if(vm_name_ip['CaaS_FS_name']=='CaaS FS Management'):
    print(COLOR["GREEN"],'CaaS FS Network Name is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect Name for CaaS FS Network : CaaS FS Management\n',COLOR["ENDC"]) 

print('CaaS FS Subnet' ,':', vm_name_ip['CaaS_FS_IP'])

if(vm_name_ip['CaaS_FS_IP']=='172.28.216.0'):
    print(COLOR["GREEN"],'CaaS FS Network is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect CaaS FS Network : 172.28.216.0\n') 

print('CaaS FS Subnet' ,':', vm_name_ip['CaaS_FS_Subnet'])
if(vm_name_ip['CaaS_FS_Subnet']=='255.255.248.0'):
    print(COLOR["GREEN"],'CaaS FS Subnet is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect CaaS FS Subnet : 255.255.248.0\n',COLOR["ENDC"]) 

print('CaaS FS Gateway' ,':', vm_name_ip['CaaS_FS_Gateway'])
if(vm_name_ip['CaaS_FS_Gateway']=='172.28.216.1'):
    print(COLOR["GREEN"],'CaaS FS Gateway is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect CaaS FS Gateway : 172.28.216.1\n',COLOR["ENDC"]) 

print('FS External Subnet' ,':', f"{external_vmaas}{'x'}")
if(external_vmaas==external_base):
    print(COLOR["GREEN"],'FS External Subnet for CaaS is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'DEVIATION - Expect CaaS FS Gateway' ':' f"{external_base}{'.x'}",COLOR["ENDC"]) 
    
print('Domain in Base Config', ':', domain_base)
for i, wrd in enumerate(controller_domain): 
    if(domain_base==wrd):
        if (i==(len(controller_domain) - 1)):
            print(COLOR["GREEN"],'Domain name in Base Config is same for all the Controllers in VMCaaS SDT\n',COLOR["ENDC"])
        else:
            continue
    else:
        print(COLOR["RED"],'DEVIATION - Expect Domain in VMCaaS for Controllers is :',domain_base,'\n',COLOR["ENDC"])
        
if (dns_ip is not None):
    print('\nPrimary DNS set in Base Config is :', dns_ip)
    print(COLOR["GREEN"],'Primary DNS is set \n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'\nPrimary DNS is not set in Base Config\n',COLOR["ENDC"])
        
print(COLOR["BLUE"],'iSCSI_A Network Details',COLOR["ENDC"]) 
print('Network Name','   :',iSCSI_A)
print ('iSCSI_A Network',':',iSCSI_A_net)
print ('iSCSI_A Subnet',' :',iSCSI_A_sub)
print ('Storage iSCSI A containers_platform Pool',':',iSCSI_A_start[0],'-',iSCSI_A_end[0])
print ('Storage iSCSI A containers_service Pool',' :',iSCSI_A_start[1],'-',iSCSI_A_end[1])
print ('Storage iSCSI A expansion_ips Pool','      :',iSCSI_A_start[2],'-',iSCSI_A_end[2])
if(iSCSI_A_sub=='255.255.248.0' and iSCSI_A_net=='172.28.16.0' and iSCSI_A_start[0]=='172.28.16.170' and iSCSI_A_end[0]=='172.28.16.219' and iSCSI_A_start[1]=='172.28.16.220' and iSCSI_A_end[1]=='172.28.22.252' and iSCSI_A_start[2]=='172.28.22.253' and iSCSI_A_end[2]=='172.28.23.254'):
    print(COLOR["GREEN"],'iSCSI_A Network is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'\nDEVIATION - Expected iSCSI_A Network' ,'-', 'Network:172.28.16.0 and Subnet:255.255.248.0\n',COLOR["ENDC"]) 

print(COLOR["BLUE"],'\niSCSI_B Network Details',COLOR["ENDC"]) 
print('Network Name','   :',iSCSI_B)
print ('iSCSI_B Network',':',iSCSI_B_net)
print ('iSCSI_B Subnet',' :',iSCSI_B_sub)
print ('Storage iSCSI B containers_platform Pool',':',iSCSI_B_start[0],'-',iSCSI_B_end[0])
print ('Storage iSCSI B containers_service Pool',' :',iSCSI_B_start[1],'-',iSCSI_B_end[1])
print ('Storage iSCSI B expansion_ips Pool','      :',iSCSI_B_start[2],'-',iSCSI_B_end[2])
if(iSCSI_B_sub=='255.255.248.0' and iSCSI_B_net=='172.28.24.0' and iSCSI_B_start[0]=='172.28.24.170' and iSCSI_B_end[0]=='172.28.24.219' and iSCSI_B_start[1]=='172.28.24.220' and iSCSI_B_end[1]=='172.28.30.252' and iSCSI_B_start[2]=='172.28.30.253' and iSCSI_B_end[2]=='172.28.31.254'):
    print(COLOR["GREEN"],'iSCSI_B Network is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'\nDEVIATION - Expected iSCSI_B Network' ,'-', 'Network:172.28.24.0 and Subnet:255.255.248.0\n',COLOR["ENDC"]) 

print(COLOR["BLUE"],'\nERE Details',COLOR["ENDC"]) 
print('\nERE Version :',ere_version)
if (len(ere_version_list)<3):
    print(COLOR["RED"],'ERE Minor Version Missing\n',COLOR["ENDC"])
else:
    print(COLOR["HEADER"],'Confirm ERE version with Team\n',COLOR["ENDC"])

print('ERE Cluster Name :', ere_Cluster_Name)
if (ere_Cluster_Name == 'gl-caas-ere-ha'):
    print(COLOR["GREEN"],'ERE Cluster name is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'ERE Cluster name is non standard, Expected is gl-caas-ere-ha\n',COLOR["ENDC"])

print('ERE Domain Name :', ere_Domain_Name)
if (ere_Domain_Name == 'hpecplocal'):
    print(COLOR["GREEN"],'ERE Domain name is Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'ERE Domain name is non standard, Expected is hpecplocal\n',COLOR["ENDC"])
    
print('ERE Credentials :', ere_Usr_Name,'/',ere_Pwd_Name)
if (ere_Usr_Name == 'admin' and ere_Pwd_Name == 'admin123'):
    print(COLOR["GREEN"],'ERE Credentials are Correct\n',COLOR["ENDC"])
else:
    print(COLOR["RED"],'ERE Credentials are non standard, Expected is admin/admin123\n',COLOR["ENDC"])