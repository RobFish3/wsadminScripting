from getTopologyElements import *

def setScopeStr(loggerDict,wasObjects):
  loggerDict['audit_Source_Msg'] = "setScopeStr"
  loggerDict['audit_Sub_Msg'] = " "
#  write_log(loggerDict)
  if   wasObjects.get('Scope') == 'Cell'   : return  "/Cell:"+getCellName()
  elif wasObjects.get('Scope') == 'Cluster': return  "/Cell:"+getCellName()+'/ServerCluster:'+wasObjects.get('ScopeName')
  elif wasObjects.get('Scope') == 'Node'   : return  "/Cell:"+getCellName()+'/Node:'+wasObjects.get('ScopeName')
  elif wasObjects.get('Scope') == 'Server' : return  "/Cell:"+getCellName()+'/Node:'+getServerNodeDictionary(loggerDict)[wasObjects.get('ScopeName')] +'/Server:'+wasObjects.get('ScopeName')
  else :
    loggerDict['audit_Sub_Msg'] = "Invalid Scope Set for this Call"

def saveConfiguration(loggerDict,commit):
  loggerDict['audit_Source_Msg'] = "saveConfiguration"
  if commit == "Y" :
    y = AdminConfig.save()
    loggerDict["log_Level"] = 3
    loggerDict["audit_Sub_Msg"] = "Configuration saved " + y
    write_log(loggerDict)
  else :
    y = AdminConfig.reset()
    loggerDict["log_Level"] = 3
    loggerDict["audit_Sub_Msg"] = "Configuration Reset " + y
    write_log(loggerDict)
  return
