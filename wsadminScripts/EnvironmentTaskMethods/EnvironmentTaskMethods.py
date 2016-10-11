
import os.path
from osUtilities import *
from wasUtilities import *
from scriptVirtualHosts import *
from scriptWebSphereVariable import *
from scriptSharedLibrary import *
from scriptURIGroups import *
from scriptReplicationDomain import *

# Import the Java libraries to do the JSON Parsing
from org.json import *

# Import the Java libraries to do the XML Parsing
import javax.xml.parsers.DocumentBuilder
import javax.xml.parsers.DocumentBuilderFactory
import javax.xml.parsers.ParserConfigurationException
# Admin Console Environment Definitions :-
#
#
# Virtual Hosts
#      - List
#      - Delete
#      - Create
#      - Modify
# Update global Web server plug-in configuration
# WebSphere Variables
#    - At scope            cell, node, cluster and server
#      - List              listWebSphereVariables
#      - Delete            removeWebSphereVariables
#      - Create            createWebSphereVariables
#      - Modify            modifyWebSphereVariables
# Shared Libraries
#    - At scope
#      - List
#      - Delete
#      - Create
#      - Modify
# SIP application routers
#      - List
#      - Delete
#      - Create
#      - Modify
# Replication Domains
#      - List
#      - Delete
#      - Create
#      - Modify
# URI Groups
#      - List
#      - Delete
#      - Create
#      - Modify
# Naming :-
#   Name space bindings
#    - At scope
#      - List
#      - Delete
#      - Create
#      - Modify
#   Foreign ccell bundle
#      - List
#      - Delete
#      - Create
#      - Modify
#   CORBA naming service users
#      - List
#      - Delete
#      - Create
#      - Modify
#   CORBA naming service groups
#      - List
#      - Delete
#      - Create
#      - Modify
# OSGi bundle repositories :-
#   Bundle cache
#      - List
#      - Download again
#      - Refresh
#   External bundle repositories 
#      - List
#      - Delete
#      - Create
#      - Modify
#   Internal bundle repository
#      - List
#      - Delete
#      - Create
#      - Modify
def environmentTasks(loggerDict,taskFile):
  loggerDict["audit_Sub_Msg"] = "environmentTasks - Function Entry"
  loggerDict['audit_Sub_Msg'] = " "
  loggerDict["log_Level"] = 3
  write_log(loggerDict)
  taskPath = loggerDict["changeFolder"]+loggerDict["changeNumber"] + '/' + taskFile
  if os.path.isfile(taskPath):
    if taskPath.split('.',1)[-1] == 'json':
      lineString = open(taskPath,'r').read()
      parsedJSON = JSONObject(lineString)
      i = 0
      while i < parsedJSON.get("EnvironmentTask").length():
        wasObjectType = parsedJSON.get("EnvironmentTask").get(i).get('ObjectType')
        wasObjects = parsedJSON.get("EnvironmentTask").get(i)
        if   wasObjectType == "VirtualHost"              : functionVirtualHosts(loggerDict,wasObjects)
        elif wasObjectType == "HostAlias"                : functionHostAlias(loggerDict,wasObjects)
        elif wasObjectType == "MimeEntry"                : functionMimeEntry(loggerDict,wasObjects)
        elif wasObjectType == "WebSphereVariables"       : functionWebSphereVariable(loggerDict,wasObjects)
        elif wasObjectType == "SharedLibrary"            : functionSharedLibrary(loggerDict,wasObjects)
        elif wasObjectType == "SIPApplicationRouter"     : functionSIPApplicationRouter(loggerDict,wasObjects)
        elif wasObjectType == "ReplicationDomain"        : functionReplicationDomain(loggerDict,wasObjects)
        elif wasObjectType == "URIGroup"                 : functionURIGroups(loggerDict,wasObjects)
        elif wasObjectType == "NameSpaceBinding"         : functionNameSpaceBinding(loggerDict,wasObjects)
        elif wasObjectType == "ForeignCellBinding"       : functionForeignCellBinding(loggerDict,wasObjects)
        elif wasObjectType == "CORBANamingServiceUsers"  : functionCORBANamingServiceUsers(loggerDict,wasObjects)
        elif wasObjectType == "CORBANamingServiceGroups" : functionCORBANamingServiceGroups(loggerDict,wasObjects)
        elif wasObjectType == "BundleCache"              : functionBundleCache(loggerDict,wasObjects)
        elif wasObjectType == "ExternalBundleRepository" : functionExternalBundleRepository(loggerDict,wasObjects)
        elif wasObjectType == "InternalBundleRepository" : functionInternalBundleRepository(loggerDict,wasObjects)
        else :
          loggerDict['audit_Sub_Msg'] = "Invalid EnvironmentTask entered = ",taskPath
          loggerDict["log_Level"] = 3
          write_log(loggerDict)
        i = i + 1
    elif taskPath.split('.',1)[-1] == 'xml':
      loggerDict['audit_Sub_Msg'] = "File type xml in progress = ",taskPath
      loggerDict["log_Level"] = 3
      write_log(loggerDict)
    elif taskPath.split('.',1)[-1] == 'props':
      loggerDict['audit_Sub_Msg'] = "File type props in progress = ",taskPath
      loggerDict["log_Level"] = 3
      write_log(loggerDict)
    else :
      loggerDict['audit_Sub_Msg'] = "File type not valid = ",taskPath
      loggerDict["log_Level"] = 3
      write_log(loggerDict)
  else :
	loggerDict['audit_Sub_Msg'] = "File not found = ",taskPath
    loggerDict["log_Level"] = 3
    write_log(loggerDict)
  return

######################################################################################################################

