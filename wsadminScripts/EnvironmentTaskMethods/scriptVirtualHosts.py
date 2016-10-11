
import os.path
import time

from osUtilities import *
from wasUtilities import *

# Import the Java libraries to do the JSON Parsing
from org.json import *

# Import the Java libraries to do the XML Parsing
import javax.xml.parsers.DocumentBuilder
import javax.xml.parsers.DocumentBuilderFactory
import javax.xml.parsers.ParserConfigurationException

def checkVirtualHostList(loggerDict,wasObjects):
  loggerDict['audit_Sub_Msg'] = " "
  write_log(loggerDict)
  print "checkVirtualHostList =",AdminConfig.list('VirtualHost',AdminConfig.getid(setScopeStr(loggerDict,wasObjects))).splitlines()
  return AdminConfig.list('VirtualHost',AdminConfig.getid(setScopeStr(loggerDict,wasObjects))).splitlines()

def checkVirtualHostExists(loggerDict,wasObjects):
  loggerDict['audit_Sub_Msg'] = " "
  write_log(loggerDict)
  return AdminConfig.getid(setScopeStr(loggerDict,wasObjects)+"/VirtualHost:"+wasObjects.get('ObjectName')+"/").splitlines()

def checkHostAliasList(loggerDict,wasObjects):
  loggerDict['audit_Sub_Msg'] = " "
  write_log(loggerDict)
  variableList = []
  if wasObjects.get('ObjectName') == 'All':
    IDentList = checkVirtualHostList(loggerDict,wasObjects)
    for entry in IDentList:
      for variableEntry in AdminConfig.list('HostAlias',entry).splitlines():
        variableList.append(variableEntry)
  else :
    IDentList = checkVirtualHostExist(loggerDict,wasObjects)
    for variableEntry in AdminConfig.list('HostAlias',IDentList).splitlines():
      variableList.append(variableEntry)
  return variableList

def checkHostAliasExists(loggerDict,wasObjects):
  loggerDict['audit_Sub_Msg'] = " "
  write_log(loggerDict)
  return AdminConfig.getid(setScopeStr(loggerDict,wasObjects)+"/VirtualHost:"+wasObjects.get('ObjectName')+"/")

def checkMimeEntryList(loggerDict,wasObjects):
  loggerDict['audit_Sub_Msg'] = " "
  write_log(loggerDict)
  variableList = []
  if wasObjects.get('ObjectName') == 'All':
    IDentList = checkVirtualHostList(loggerDict,wasObjects)
    for entry in IDentList:
      for variableEntry in AdminConfig.list('MimeEntry',entry).splitlines():
        variableList.append(variableEntry)
  else :
    IDentList = checkVirtualHostExist(loggerDict,wasObjects)
    for variableEntry in AdminConfig.list('HostAlias',IDentList).splitlines():
      variableList.append(variableEntry)
  return variableList

def checkMimeEntryExists(loggerDict,wasObjects):
  loggerDict['audit_Sub_Msg'] = " "
  write_log(loggerDict)
  return AdminConfig.getid(setScopeStr(loggerDict,wasObjects)+"/VirtualHost:"+wasObjects.get('hostname')+"/")

########### Virtual Hosts Methods

def functionVirtualHosts(loggerDict,wasObjects):
  loggerDict['audit_Step_Msg']    = "scriptVirtualHosts"
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 4
  write_log(loggerDict )
  if   wasObjects.get('Function') == 'List'   : listVirtualHosts(loggerDict,wasObjects)
  elif wasObjects.get('Function') == 'Remove' : removeVirtualHosts(loggerDict,wasObjects)
  elif wasObjects.get('Function') == 'Create' : createVirtualHosts(loggerDict,wasObjects)
  else                         :
    loggerDict['audit_Sub_Msg'] = "The requested function %s is not allowed for Virtual Hosts" %(wasObjects.get('Function'))
    write_log(loggerDict )

def functionHostAlias(loggerDict,wasObjects):
  loggerDict['audit_Step_Msg']    = "scriptHostAlias"
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 4
  write_log(loggerDict )
  if   wasObjects.get('Function') == 'List'   : listHostAlias(loggerDict,wasObjects)
  elif wasObjects.get('Function') == 'Remove' : removeHostAlias(loggerDict,wasObjects)
  elif wasObjects.get('Function') == 'Create' : createHostAlias(loggerDict,wasObjects)
  elif wasObjects.get('Function') == 'Modify' : modifyHostAlias(loggerDict,wasObjects)
  else                         :
    loggerDict["log_Level"] = 3
    loggerDict['audit_Sub_Msg'] = "The requested function %s is not allowed for HostAlias" %(wasObjects.get('Function'))
    write_log(loggerDict )

def functionMimeEntry(loggerDict,wasObjects):
  loggerDict['audit_Step_Msg']    = "scriptMimeEntry"
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 4
  write_log(loggerDict )
  if   wasObjects.get('Function') == 'List'   : listMimeEntry(loggerDict,wasObjects)
  elif wasObjects.get('Function') == 'Remove' : removeMimeEntry(loggerDict,wasObjects)
  elif wasObjects.get('Function') == 'Create' : createMimeEntry(loggerDict,wasObjects)
  elif wasObjects.get('Function') == 'Modify' : modifyMimeEntry(loggerDict,wasObjects)
  else                         :
    loggerDict['audit_Sub_Msg'] = "The requested function %s is not allowed for MimeEntries" %(wasObjects.get('Function'))
    write_log(loggerDict )


#########################################################
#  List Environment objects
#########################################################

def listVirtualHosts(loggerDict,wasObjects):
# Set up and write audit Trail
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict )
  IDentList = {}
  if wasObjects.get('Scope') != 'Cell' :
    loggerDict['audit_Sub_Msg'] = "Request set at incorrect Scope - must be at 'Cell' scope"
    loggerDict["log_Level"] = 3
    write_log(loggerDict ) 
    return
# Check what type of list is required, All, Individual, or Template
  if   wasObjects.get('ObjectName') == "All"       : IDentList = checkVirtualHostList(loggerDict,wasObjects)
  elif wasObjects.get('ObjectName') == "Defaults"  : IDentList = AdminConfig.defaults('VirtualHost').splitlines()
  elif wasObjects.get('ObjectName') == "Required"  : IDentList = AdminConfig.required('VirtualHost').splitlines()
  elif wasObjects.get('ObjectName') == "Attributes": IDentList = AdminConfig.attributes('VirtualHost').splitlines()
  else                                       : IDentList = checkVirtualHostExists(loggerDict,wasObjects)
  i = 0
  if wasObjects.get('ObjectName') in ['Attributes','Required','Defaults']:
# If a template output is required, setup the output file 
    timeStamp = time.strftime('%H_%M_%S')
    writer_output = loggerDict['changeFolder']+loggerDict['changeNumber']+'/'+loggerDict['changeNumber']+wasObjects.get('ObjectName')+"OutputVirtualHostFile-"+timeStamp+".json"
    myOutput = open(writer_output,'a')
    outputStr = '{"EnvironmentTask":['
    myOutput.write(outputStr)
    outputStr = '{"ObjectType":"VirtualHost","Scope":"' + wasObjects.get('Scope') + '","ScopeName":"' +wasObjects.get('ScopeName') + '","Function":"'+wasObjects.get('ObjectName')+'",'

    if wasObjects.get('ObjectName') in ['Required','Defaults']:
#   If the template relates to Input structure
      lenToDefaultStr = 0
      if wasObjects.get('ObjectName') == "Defaults": lenToDefaultStr = IDentList[0].find('Default')
      if wasObjects.get('ObjectName') == "Required": lenToDefaultStr = IDentList[0].find('Type')
      j = 1
      while j < len(IDentList):
        split_MimeEntry = IDentList[j].split(" ")
        if lenToDefaultStr > len(IDentList[j].strip()): defValue = IDentList[j].split()[1]
        else                                          : defValue = IDentList[j][lenToDefaultStr:]
        outputStr = outputStr +'"' + split_MimeEntry[0].strip()+ '":"' +  defValue + '",'
        j = j + 1
    else :
#   Else  print out a list of required attributes    
      j = 0
      while j < len(IDentList):
        split_virtualHost = IDentList[j].split(" ",1)
        outputStr = outputStr +'"' + split_virtualHost[0].strip()+ '":"' + split_virtualHost[1].strip() + '",'
        j = j + 1
    outputStr = outputStr[:-1] + '}]}'
    myOutput.write(outputStr)
    myOutput.close()
    loggerDict['audit_Sub_Msg'] = "File %s for VirtualHosts Created" %(writer_output)
    write_log(loggerDict )
    IDentList = {}
  elif wasObjects.get('ObjectName') == "All" :
# Else print out the requested list
    if len(IDentList) > 0 :
      if wasObjects.get('ListOutputFormat') == "json" :
        timeStamp = time.strftime('%H_%M_%S')
        writer_output = loggerDict['changeFolder']+loggerDict['changeNumber']+'/'+loggerDict['changeNumber']+wasObjects.get('ObjectName')+"OutputVirtualHostFile-"+timeStamp+".json"
        myOutput = open(writer_output,'a')
        outputStr = '{"EnvironmentTask":['
        myOutput.write(outputStr)
    else :
      loggerDict['audit_Sub_Msg'] = "There are no Virtual Hosts %s defined " %( wasObjects.get('ObjectName'))
      write_log(loggerDict )
      loggerDict['audit_Sub_Msg'] = " "
      return
    outputStrPrefix = '{"ObjectType":"VirtualHost","Scope":"' + wasObjects.get('Scope') + '","ScopeName":"' +wasObjects.get('ScopeName') + '","Function":"Listed","ObjectName":'
    i = 0
    while i < len(IDentList):
      outputStr = outputStrPrefix
      virtualHost = AdminConfig.showAttribute(IDentList[i],'name')
      i = i + 1
      outputStr = outputStr +'"' + virtualHost + '" }'
      if i != len(IDentList) :
        outputStr = outputStr +',\n'
      else :
        outputStr = outputStr +'\n'
      myOutput.write(outputStr)
    if len(IDentList) > 0 :
      outputStr = ']}'
      myOutput.write(outputStr)
      myOutput.close()
      loggerDict['audit_Sub_Msg'] = "File %s for VirtualHosts Created" %(writer_output)
      write_log(loggerDict )
  elif len(IDentList) == 0:
    loggerDict['audit_Sub_Msg'] = "There is no Virtual Host %s defined " %( wasObjects.get('ObjectName'))
    write_log(loggerDict )
    loggerDict['audit_Sub_Msg'] = " "
    return
  else :
    HostAliasList = AdminConfig.list('HostAlias', AdminConfig.getid(setScopeStr(loggerDict,wasObjects) +'/VirtualHost:'+wasObjects.get('ObjectName')+'/')).splitlines()
    hostnameList = []
    for entry in HostAliasList :
      hostDict = {}
      hostDict['hostname'] = AdminConfig.showAttribute(entry,'hostname')
      hostDict['port']     = AdminConfig.showAttribute(entry,'port')
      hostnameList.append(hostDict)
    hostnameList.sort()
    if wasObjects.get('ListOutputFormat') == "json" :
      timeStamp = time.strftime('%H_%M_%S') 
      writer_output = loggerDict['changeFolder']+loggerDict['changeNumber']+'/'+loggerDict['changeNumber']+wasObjects.get('ObjectName')+"OutputVirtualHostFile-"+timeStamp+".json"
      myOutput = open(writer_output,'a')
      outputStr = '{"EnvironmentTask":[\n'
      myOutput.write(outputStr)
    else :
      loggerDict['audit_Sub_Msg'] = "There is no Virtual Host %s defined " %( wasObjects.get('ObjectName'))
      write_log(loggerDict )
      loggerDict['audit_Sub_Msg'] = ""
    outputStrPrefix = '{"ObjectType":"VirtualHost","Scope":"' + wasObjects.get('Scope') + '","ScopeName":"' +wasObjects.get('ScopeName') + '","Function":"Listed","ObjectName":"'+wasObjects.get('ObjectName')+'",'
    i = 0
    while i < len(hostnameList):
      hostnameDict = hostnameList[i]
      outputStr = outputStrPrefix +'"hostname":"' + hostnameDict['hostname'] + '","port":'+ hostnameDict['port']+'"},\n'
      i = i + 1
      myOutput.write(outputStr)

    MimeEntryList = AdminConfig.list('MimeEntry', AdminConfig.getid(setScopeStr(loggerDict,wasObjects) +'/VirtualHost:'+wasObjects.get('ObjectName')+'/')).splitlines()
    mimeentryList = []
    for entry in MimeEntryList :
      mimeDict = {}
      mimeDict['extensions'] = AdminConfig.showAttribute(entry,'extensions')
      mimeDict['type']       = AdminConfig.showAttribute(entry,'type')
      mimeentryList.append(mimeDict)
    mimeentryList.sort()
    outputStrPrefix = '{"ObjectType":"VirtualHost","Scope":"' + wasObjects.get('Scope') + '","ScopeName":"' +wasObjects.get('ScopeName') + '","Function":"Listed","ObjectName":"'+wasObjects.get('ObjectName')+'",'
    i = 0
    while i < len(mimeentryList):
      mimeentryDict = mimeentryList[i]
      outputStr = outputStrPrefix +'"extensions":"' + mimeentryDict['extensions'] + '","type":'+ mimeentryDict['type']+'"}'
      i = i + 1
      if i < len(mimeentryList):
        outputStr =  outputStr + ',\n'
      else :
        outputStr =  outputStr + '\n'
      myOutput.write(outputStr)
    outputStr = ']}'
    myOutput.write(outputStr)
    myOutput.close()
    loggerDict['audit_Sub_Msg'] = "File %s for VirtualHosts Detail Created" %(writer_output)
    write_log(loggerDict )

def listHostAlias(loggerDict,wasObjects):
# Set up and write audit Trail
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict )
  IDentList = {}
  outputType = ''
  if wasObjects.get('Scope') != 'Cell' :
    loggerDict['audit_Sub_Msg'] = "Request set at incorrect Scope - must be at 'Cell' scope"
    loggerDict["log_Level"] = 3
    write_log(loggerDict )
    return
# Check what type of list is required, All, Individual, or Template
  if   wasObjects.get('ObjectName') == "All"        : IDentList = checkHostAliasList(loggerDict,wasObjects)
  elif wasObjects.get('ObjectName') == "Defaults"   : IDentList = AdminConfig.defaults('HostAlias').splitlines()
  elif wasObjects.get('ObjectName') == "Required"   : IDentList = AdminConfig.required('HostAlias').splitlines()
  elif wasObjects.get('ObjectName') == "Attributes" : IDentList = AdminConfig.attributes('HostAlias').splitlines()
  else                                        : IDentList = checkHostAliasExists(loggerDict,wasObjects)
  i = 0
  if wasObjects.get('ObjectName') in ['Attributes','Required','Defaults']:
# If a template output is required, setup the output file
    timeStamp = time.strftime('%H_%M_%S')
    writer_output = loggerDict['changeFolder']+loggerDict['changeNumber']+'/'+loggerDict['changeNumber']+wasObjects.get('ObjectName')+"OutputHostAliasFile-"+timeStamp+".json"
    myOutput = open(writer_output,'a')
    outputStr = '{"EnvironmentTask":['
    myOutput.write(outputStr)
    outputStr = '{"ObjectType":"HostAlias","Scope":"' + wasObjects.get('Scope') + '","ScopeName":"' +wasObjects.get('ScopeName') + '","Function":"'+wasObjects.get('ObjectName')+'",'
    if wasObjects.get('ObjectName') in ['Required','Defaults']:
#   If the template relates to Input structure
      lenToDefaultStr = 0
      if wasObjects.get('ObjectName') == "Defaults":
        lenToDefaultStr = IDentList[0].find('Default')
      if wasObjects.get('ObjectName') == "Required":
        lenToDefaultStr = IDentList[0].find('Type')
      j = 1
      while j < len(IDentList):
        split_MimeEntry = IDentList[j].split(" ")
        if lenToDefaultStr > len(IDentList[j].strip()):
           defValue = IDentList[j].split()[1]
        else :
           defValue = IDentList[j][lenToDefaultStr:]
        outputStr = outputStr +'"' + split_MimeEntry[0].strip()+ '":"' +  defValue + '",'
        j = j + 1
    else :
#   Else  print out a list of required attributes
      j = 0
      while j < len(IDentList):
        split_HostAlias = IDentList[j].split(" ",1)
        outputStr = outputStr +'"' + split_HostAlias[0].strip()+ '":"' + split_HostAlias[1].strip() + '",'
        j = j + 1
    outputStr = outputStr[:-1] + '}]}'
    myOutput.write(outputStr)
    myOutput.close()
    loggerDict['audit_Sub_Msg'] = "File %s for HostsAlias Created" %(writer_output)
    write_log(loggerDict )
    IDentList = {}
  elif wasObjects.get('ObjectName') == "All" :
# Else print out the requested list
    if len(IDentList) > 0 :
      if wasObjects.get('ListOutputFormat') == "json" :
        timeStamp = time.strftime('%H_%M_%S')
        writer_output = loggerDict['changeFolder']+loggerDict['changeNumber']+'/'+loggerDict['changeNumber']+wasObjects.get('ObjectName')+"OutputHostAliasFile-"+timeStamp+".json"
        myOutput = open(writer_output,'a')
        outputStr = '{"EnvironmentTask":['
        myOutput.write(outputStr)
    else :
      loggerDict['audit_Sub_Msg'] = "There is no Host Alias %s defined " %( wasObjects.get('ObjectName'))
      write_log(loggerDict )
      loggerDict['audit_Sub_Msg'] = ""
    outputStrPrefix = '{"ObjectType":"HostAlias","Scope":"' + wasObjects.get('Scope') + '","ScopeName":"' +wasObjects.get('ScopeName') + '","Function":"Listed","hostname":'
    i = 0
    while i < len(IDentList):
      outputStr = outputStrPrefix
      hostAlias = AdminConfig.showAttribute(IDentList[i],'hostname')
      i = i + 1
      outputStr = outputStr +'"' + hostAlias + '" }'
      if i != len(IDentList) :
        outputStr = outputStr +',\n'
      else :
        outputStr = outputStr +'\n'
      myOutput.write(outputStr)
    if len(IDentList) > 0 :
      outputStr = ']}'
      myOutput.write(outputStr)
      myOutput.close()
      loggerDict['audit_Sub_Msg'] = "File %s for HostAlias Created" %(writer_output)
      write_log(loggerDict )
  else :
    VirtHostList = AdminConfig.getid(setScopeStr(loggerDict,wasObjects) +'/VirtualHost:/').splitlines()
    hostnameList = []
    for virt_entry in VirtHostList :
      HostAliasList = AdminConfig.showAttribute(virt_entry,'aliases')[1:-1].split()
      for host_entry in HostAliasList:
         if AdminConfig.showAttribute(host_entry,'hostname') == wasObjects.get('ObjectName'):
           hostDict = {}
           hostDict['name']     = AdminConfig.showAttribute(virt_entry,'name')
           hostDict['hostname'] = AdminConfig.showAttribute(host_entry,'hostname') 
           hostDict['port']     = AdminConfig.showAttribute(host_entry,'port')     
           hostnameList.append(hostDict)
    hostnameList.sort()
    if wasObjects.get('ListOutputFormat') == "json" :
      timeStamp = time.strftime('%H_%M_%S')
      writer_output = loggerDict['changeFolder']+loggerDict['changeNumber']+'/'+loggerDict['changeNumber']+wasObjects.get('ObjectName')+"OutputHostAliasFile-"+timeStamp+".json"
      myOutput = open(writer_output,'a')
      outputStr = '{"EnvironmentTask":[\n'
      myOutput.write(outputStr)
    elif wasOjects.has('ListOutputFormat') :
      loggerDict['audit_Sub_Msg'] = " File Format %s not currently supported " %( wasObjects.get('ObjectName'))
      write_log(loggerDict )
      loggerDict['audit_Sub_Msg'] = ""
      return
    else :
      loggerDict['audit_Sub_Msg'] = " File Format not specifieded " 
      write_log(loggerDict )
      loggerDict['audit_Sub_Msg'] = ""
      return
    outputStrPrefix = '{"ObjectType":"HostAlias","Scope":"' + wasObjects.get('Scope') + '","ScopeName":"' +wasObjects.get('ScopeName') + '","Function":"Listed", '
    i = 0
    while i < len(hostnameList):
      hostnameDict = hostnameList[i]
      outputStr = outputStrPrefix +'"ObjectName":"' + hostnameDict['hostname'] + '" , "port":"'+ hostnameDict['port']+'" , "virtualhostname":"'+hostnameDict['name']+'"}'
      i = i + 1
      if i < len(hostnameList):
        outputStr =  outputStr + ',\n'
      else :
        outputStr =  outputStr + '\n'
      myOutput.write(outputStr)
    if len(hostnameList) > 0 :
      outputStr = ']}'
      myOutput.write(outputStr)
      myOutput.close()
      loggerDict['audit_Sub_Msg'] = "File %s for HostAlias Created" %(writer_output)
      write_log(loggerDict )

def listMimeEntry(loggerDict,wasObjects):
# Set up and write audit Trail
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict )
  IDentList = {}
  outputType = ''
# Check what type of list is required, All, Individual, or Template
  if   wasObjects.get('ObjectName') == "All":
    IDentList = checkMimeEntryList(loggerDict,wasObjects)
  elif wasObjects.get('ObjectName') == "Defaults":
    if wasObjects.get('Scope') != 'Cell' : return
    outputType = "Defaults"
    IDentList = AdminConfig.defaults('MimeEntry').splitlines()
  elif wasObjects.get('ObjectName') == "Required":
    if wasObjects.get('Scope') != 'Cell' : return
    outputType = "Required"
    IDentList = AdminConfig.required('MimeEntry').splitlines()
  elif wasObjects.get('ObjectName') == "Attributes":
    if wasObjects.get('Scope') != 'Cell' : return
    outputType = "Attributes"
    IDentList = AdminConfig.attributes('MimeEntry').splitlines()

  i = 0
  if outputType in ['Attributes','Required','Defaults']:
# If a template output is required, setup the output file
    timeStamp = time.strftime('%H_%M_%S')
    writer_output = loggerDict['changeFolder']+loggerDict['changeNumber']+'/'+loggerDict['changeNumber']+outputType+"OutputMimeEntryFile-"+timeStamp+".json"
    myOutput = open(writer_output,'a')
    outputStr = '{"EnvironmentTask":['
    myOutput.write(outputStr)
    outputStr = '{"ObjectType":"MimeEntry","Scope":"' + wasObjects.get('Scope') + '","ScopeName":"' +wasObjects.get('ScopeName') + '","Function":"'+outputType+'",'

    if outputType in ['Required','Defaults']:
#   If the template relates to Input structure
      lenToDefaultStr = 0
      if outputType == "Defaults":
        lenToDefaultStr = IDentList[0].find('Default')
      if outputType == "Required":
        lenToDefaultStr = IDentList[0].find('Type')
      j = 1
      while j < len(IDentList):
        split_MimeEntry = IDentList[j].split(" ")
        if lenToDefaultStr > len(IDentList[j].strip()):
           defValue = IDentList[j].split()[1]
        else :
           defValue = IDentList[j][lenToDefaultStr:]
        outputStr = outputStr +'"' + split_MimeEntry[0].strip()+ '":"' +  defValue + '",'
        j = j + 1
    else :
#   Else  print out a list of required attributes
      j = 0
      while j < len(IDentList):
        split_MimeEntry = IDentList[j].split(" ",1)
        outputStr = outputStr +'"' + split_MimeEntry[0].strip()+ '":"' + split_MimeEntry[1].strip() + '",'
        j = j + 1
    outputStr = outputStr[:-1] + '}]}'
    myOutput.write(outputStr)
    myOutput.close()
    loggerDict['audit_Sub_Msg'] = "File %s for MimeEntry Created" %(writer_output)
    write_log(loggerDict )
    IDentList = {}
  elif wasObjects.get('ObjectName') == 'All' :
# Else print out the requested list
    if len(IDentList) > 0 :
      if wasObjects.get('ListOutputFormat') == "json" :
        timeStamp = time.strftime('%H_%M_%S')
        writer_output = loggerDict['changeFolder']+loggerDict['changeNumber']+'/'+loggerDict['changeNumber']+outputType+"OutputMimeEntryFile-"+timeStamp+".json"
        myOutput = open(writer_output,'a')
        outputStr = '{"EnvironmentTask":['
        myOutput.write(outputStr)
    else :
      loggerDict['audit_Sub_Msg'] = "There is no Host Alias %s defined " %( wasObjects.get('ObjectName'))
      write_log(loggerDict )
      loggerDict['audit_Sub_Msg'] = ""
    outputStrPrefix = '{"ObjectType":"MimeEntry","Scope":"' + wasObjects.get('Scope') + '","ScopeName":"' +wasObjects.get('ScopeName') + '","Function":"Listed","extensions":'
    i = 0
    while i < len(IDentList):
      outputStr = outputStrPrefix
      mimeEntry = AdminConfig.showAttribute(IDentList[i],'extensions')
      i = i + 1
      outputStr = outputStr +'"' + mimeEntry + '" }'
      if i != len(IDentList) :
        outputStr = outputStr +',\n'
      else :
        outputStr = outputStr +'\n'
      myOutput.write(outputStr)
    if len(IDentList) > 0 :
      outputStr = ']}'
      myOutput.write(outputStr)
      myOutput.close()
      loggerDict['audit_Sub_Msg'] = "File %s for MimeEntry Created" %(writer_output)
      write_log(loggerDict )
  else :
    VirtHostList = AdminConfig.getid(setScopeStr(loggerDict,wasObjects) +'/VirtualHost:/').splitlines()
    mimeentryList = []
    for virt_entry in VirtHostList :
      MimeEntryList = AdminConfig.showAttribute(virt_entry,'mimeTypes')[1:-1].split()
      for mime_entry in MimeEntryList:
         if AdminConfig.showAttribute(mime_entry,'type') == wasObjects.get('ObjectName'):
           mimeDict = {}
           mimeDict['name']        = AdminConfig.showAttribute(virt_entry,'name')
           mimeDict['type']        = AdminConfig.showAttribute(mime_entry,'type')
           mimeDict['extensions']  = AdminConfig.showAttribute(mime_entry,'extensions')
           mimeentryList.append(mimeDict)
    mimeentryList.sort()
    if wasObjects.get('ListOutputFormat') == "json" :
      timeStamp = time.strftime('%H_%M_%S')
      writer_output = loggerDict['changeFolder']+loggerDict['changeNumber']+'/'+loggerDict['changeNumber']+"MimeEntryDetail"+"OutputMimeEntryFile-"+timeStamp+".json"
      myOutput = open(writer_output,'a')
      outputStr = '{"EnvironmentTask":[\n'
      myOutput.write(outputStr)
    elif wasOjects.has('ListOutputFormat') :
      loggerDict['audit_Sub_Msg'] = " File Format %s not currently supported " %( wasObjects.get('ListOutputFormat'))
      write_log(loggerDict )
      loggerDict['audit_Sub_Msg'] = ""
      return
    else :
      loggerDict['audit_Sub_Msg'] = " File Format not specifieded "
      write_log(loggerDict )
      loggerDict['audit_Sub_Msg'] = ""
      return
    outputStrPrefix = '{"ObjectType":"MimeEntry","Scope":"' + wasObjects.get('Scope') + '","ScopeName":"' +wasObjects.get('ScopeName') + '","Function":"Listed", '
    i = 0
    while i < len(mimeentryList):
      mimeentryDict = mimeentryList[i]
      outputStr = outputStrPrefix +'"ObjectName":"' + mimeentryDict['type'] + '" , "extensions":"'+ mimeentryDict['extensions']+'" , "virtualhostname":"'+mimeentryDict['name']+'"}'
      i = i + 1
      if i < len(mimeentryList):
        outputStr =  outputStr + ',\n'
      else :
        outputStr =  outputStr + '\n'
      myOutput.write(outputStr)
    if len(mimeentryList) > 0 :
      outputStr = ']}'
      myOutput.write(outputStr)
      myOutput.close()
      loggerDict['audit_Sub_Msg'] = "File %s for MimeEntry Created" %(writer_output)
      write_log(loggerDict )

#########################################################
#  Remove Environment objects
#########################################################

def removeVirtualHosts(loggerDict,wasObjects):
# Set up and write audit Trail
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict )

# Check if the Virtual Host Exists
  VIDentList = checkVirtualHostExists(loggerDict,wasObjects)
  if len(VIDentList) == 0:
    loggerDict['audit_Sub_Msg'] = "The Virtual Host %s Does not Exist." %(wasObjects.get('ObjectName'))
    loggerDict["log_Level"] = 3
    write_log(loggerDict )
    return
# The VirtualHost was found
  aliasID = AdminConfig.showAttribute(VIDentList[0],'aliases')
  returnID = aliasID[1:-1].split(' ')
  if len(returnID[0]) >0:
    for entry in returnID:
      removeName = AdminConfig.showAttribute(entry,'hostname')
      AdminConfig.remove(entry)
      loggerDict['audit_Source_Msg'] = "removeHostAlias"
      loggerDict['audit_Sub_Msg'] = "HostAlias %s removed for VirtualHost %s" %(removeName , wasObjects.get('ObjectName'))
      loggerDict["log_Level"] = 3
      write_log(loggerDict )
  removeID = AdminConfig.remove(VIDentList[0])
  saveConfiguration(loggerDict,"Y")
  loggerDict['audit_Sub_Msg'] = "Remove of Virtual Host %s successful." %(wasObjects.get('ObjectName'))
  write_log(loggerDict )

def removeHostAlias(loggerDict,wasObjects):
# Set up and write audit Trail
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict )
# Check if the Host Alias Exists
  tempObjects = JSONObject('{}')
  tempObjects.put("ObjectName",wasObjects.get('name'))
  tempObjects.put("Scope",wasObjects.get('Scope'))
  VIDentList = checkVirtualHostExists(loggerDict,tempObjects)
  if len(VIDentList) == 0:
    loggerDict['audit_Sub_Msg'] = "The Virtual Host %s Does not Exist." %(wasObjects.get('name'))
    loggerDict["log_Level"] = 3
    write_log(loggerDict )
    return
# The VirtualHost was found
  aliasID = AdminConfig.showAttribute(VIDentList[0],'aliases')
  returnID = aliasID[1:-1].split(' ')
  if len(returnID[0]) >0:
    for entry in returnID:
      if wasObjects.get('ObjectName') == AdminConfig.showAttribute(entry,'hostname'):
        AdminConfig.remove(entry)
        saveConfiguration(loggerDict,"Y")
        loggerDict['audit_Sub_Msg'] = "Alias %s removed for VirtualHost %s" %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
        loggerDict["log_Level"] = 3
        write_log(loggerDict )
        return
  loggerDict['audit_Sub_Msg'] = "Remove of HostAlias %s failed. HostAlias does not exist for VirtualHost %s"  %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
  write_log(loggerDict )

def removeMimeEntry(loggerDict,wasObjects):
# Set up and write audit Trail
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict )
# Check if the MimeEntry Exists
  tempObjects = JSONObject('{}')
  tempObjects.put("ObjectName",wasObjects.get('name'))
  tempObjects.put("Scope",wasObjects.get('Scope'))
  VIDentList = checkVirtualHostExists(loggerDict,tempObjects)
  if len(VIDentList) == 0:
    loggerDict['audit_Sub_Msg'] = "The Virtual Host %s Does not Exist." %(wasObjects.get('name'))
    loggerDict["log_Level"] = 3
    write_log(loggerDict )
    return
# The VirtualHost was found
  mimeID = AdminConfig.showAttribute(VIDentList[0],'mimeTypes')
  returnID = mimeID[1:-1].split(' ')
  if len(returnID[0]) >0:
    for entry in returnID:
      if wasObjects.get('ObjectName') == AdminConfig.showAttribute(entry,'type'):
        AdminConfig.remove(entry)
        saveConfiguration(loggerDict,"Y")
        loggerDict['audit_Sub_Msg'] = "MimeEntry %s removed for VirtualHost %s" %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
        loggerDict["log_Level"] = 3
        write_log(loggerDict )
        return
  loggerDict['audit_Sub_Msg'] = "Remove of MimeEntry %s failed. MimeEntry does not exist for VirtualHost %s"  %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
  write_log(loggerDict )

#########################################################
#  Create Environment objects
#########################################################

def createVirtualHosts(loggerDict,wasObjects):
# Set up and write audit Trail
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict )

# Check if the Virtual Host Exists
  IDentList = checkVirtualHostExists(loggerDict,wasObjects)
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  returnID = ''
  if len(IDentList) == 0:
# If the Virtual Host does not Exist, create it
    returnID = AdminConfig.create('VirtualHost', AdminConfig.getid(setScopeStr(loggerDict,wasObjects)), [['name' , wasObjects.get('ObjectName') ]])
    loggerDict['audit_Sub_Msg'] = " "
    loggerDict['log_Level'] = 3
    saveConfiguration(loggerDict,"Y")
    loggerDict['audit_Sub_Msg'] = "Create of Virtual Host %s successful." %(wasObjects.get('ObjectName'))
  else :
# Else flag that it already Exists
    loggerDict['audit_Sub_Msg'] = "Create of Virtual Host %s failed. Virtual Host already exists "  %(wasObjects.get('ObjectName'))
  write_log(loggerDict )
  return returnID

def createHostAlias(loggerDict,wasObjects):
# Set up and write audit Trail
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict )
# Check if the Host Alias Exists
  tempObjects = JSONObject('{}')
  tempObjects.put("ObjectName",wasObjects.get('name'))
  tempObjects.put("Scope",wasObjects.get('Scope'))
  VIDentList = checkVirtualHostExists(loggerDict,tempObjects)
  if len(VIDentList) == 0:
    VIDentList = createVirtualHosts(loggerDict,tempObjects).splitlines()
    saveConfiguration(loggerDict,"Y")
# The VirtualHost was found
  aliasID = AdminConfig.showAttribute(VIDentList[0],'aliases')
  returnID = aliasID[1:-1].split(' ')
  if returnID[0] != '':
    for entry in returnID:
      if wasObjects.get('ObjectName') == AdminConfig.showAttribute(entry,'hostname'):
        loggerDict['audit_Sub_Msg'] = "Alias %s already exist for VirtualHost %s" %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
        loggerDict["log_Level"] = 3
        write_log(loggerDict )
        return
  parmStr = "["
  parmStr = parmStr + ' [ hostname "' +wasObjects.get('ObjectName') + '"]'
  if wasObjects.has('port') :
    parmStr = parmStr + ' [ port "'+wasObjects.get('port')  + '"]'
  parmStr = parmStr + ']'
  mycreate = AdminConfig.create('HostAlias', VIDentList[0], parmStr)
  saveConfiguration(loggerDict,"Y")
  loggerDict['audit_Sub_Msg'] = "Alias %s created for VirtualHost %s "  %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
  loggerDict["log_Level"] = 3
  write_log(loggerDict )

def createMimeEntry(loggerDict,wasObjects):
# Set up and write audit Trail
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict )
# Check if the MimeEntry Exists
  tempObjects = JSONObject('{}')
  tempObjects.put("ObjectName",wasObjects.get('name'))
  tempObjects.put("Scope",wasObjects.get('Scope'))
  VIDentList = checkVirtualHostExists(loggerDict,tempObjects)
  if len(VIDentList) == 0:
    VIDentList = createVirtualHosts(loggerDict,tempObjects).splitlines()
  mimeID = AdminConfig.showAttribute(VIDentList[0],'mimeTypes')
  returnID = mimeID[1:-1].split(' ')
  if returnID[0] != '':
    for entry in returnID:
      if wasObjects.get('ObjectName') == AdminConfig.showAttribute(entry,'type'):
        loggerDict['audit_Sub_Msg'] = " "
        loggerDict["log_Level"] = 3
        write_log(loggerDict )
        return 
# If the MimeEntry does not Exist, create it
  parmStr = "["
  parmStr = parmStr + ' [ type "' +wasObjects.get('ObjectName') + '"]'
  if wasObjects.has('extensions') :
    parmStr = parmStr + ' [ extensions "'+wasObjects.get('extensions')  + '"]'
  parmStr = parmStr + ']'
  AdminConfig.create('MimeEntry', VIDentList[0], parmStr)
  saveConfiguration(loggerDict,"Y")
  loggerDict['audit_Sub_Msg'] = "MimeEntry %s created for VirtualHost %s "  %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
  loggerDict["log_Level"] = 3
  write_log(loggerDict )

def modifyHostAlias(loggerDict,wasObjects):
# Set up and write audit Trail
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict )
# Check if the Host Alias Exists
  tempObjects = JSONObject('{}')
  tempObjects.put("ObjectName",wasObjects.get('name'))
  tempObjects.put("Scope",wasObjects.get('Scope'))
  VIDentList = checkVirtualHostExists(loggerDict,tempObjects)
  if len(VIDentList) == 0:
    loggerDict['audit_Sub_Msg'] = "The Virtual Host %s Does not Exist." %(wasObjects.get('name'))
    loggerDict["log_Level"] = 3
    write_log(loggerDict )
    return
# The VirtualHost was found
  aliasID = AdminConfig.showAttribute(VIDentList[0],'aliases')
  returnID = aliasID[1:-1].split(' ')
  if len(returnID[0]) >0:
    for entry in returnID:
      if wasObjects.get('ObjectName') == AdminConfig.showAttribute(entry,'hostname'):
        parmStr = "["
        if wasObjects.has('port') :
          parmStr = parmStr + ' [ port "'+wasObjects.get('port')  + '"]'
        parmStr = parmStr + ']'
        if parmStr != "[]":
          AdminConfig.modify(entry,parmStr)
          saveConfiguration(loggerDict,"Y")
          loggerDict['audit_Sub_Msg'] = "HostAlias %s modified for VirtualHost %s" %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
        else :
          loggerDict['audit_Sub_Msg'] = "HostAlias %s unmodified for VirtualHost %s" %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
        loggerDict["log_Level"] = 3
        write_log(loggerDict )
        return
  loggerDict['audit_Source_Msg'] = "modifyHostAlias"
  loggerDict['audit_Sub_Msg'] = "Modify of HostAlias %s failed. HostAlias does not exist for VirtualHost %s"  %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
  write_log(loggerDict )

def modifyMimeEntry(loggerDict,wasObjects):
# Set up and write audit Trail
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict )
# Check if the Mime Entry Exists
  tempObjects = JSONObject('{}')
  tempObjects.put("ObjectName",wasObjects.get('name'))
  tempObjects.put("Scope",wasObjects.get('Scope'))
  VIDentList = checkVirtualHostExists(loggerDict,tempObjects)
  if len(VIDentList) == 0:
    loggerDict['audit_Sub_Msg'] = "The Virtual Host %s Does not Exist." %(wasObjects.get('name'))
    loggerDict["log_Level"] = 3
    write_log(loggerDict )
    return
# The VirtualHost was found
  mimeID = AdminConfig.showAttribute(VIDentList[0],'mimeTypes')
  returnID = mimeID[1:-1].split(' ')
  if len(returnID[0]) >0:
    for entry in returnID:
      if wasObjects.get('ObjectName') == AdminConfig.showAttribute(entry,'type'):
        parmStr = "["
        if wasObjects.has('extensions') :
          parmStr = parmStr + ' [ extensions "'+wasObjects.get('extensions')  + '"]'
        parmStr = parmStr + ']'
        if parmStr != "[]":
          AdminConfig.modify(entry,parmStr)
          saveConfiguration(loggerDict,"Y")
          loggerDict['audit_Sub_Msg'] = "MimeEntry %s modified for VirtualHost %s" %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
        else :
          loggerDict['audit_Sub_Msg'] = "MimeEntrys %s unmodified for VirtualHost %s" %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
        loggerDict["log_Level"] = 3
        write_log(loggerDict )
        return
  loggerDict['audit_Sub_Msg'] = "Modify of MimeEntry %s failed. MimeEntry does not exist for VirtualHost %s"  %(wasObjects.get('ObjectName'), tempObjects.get('ObjectName'))
  write_log(loggerDict )
