# Import System Utilities Used by the script
import os
import sys
import time
import socket
import zipfile

script_path = '/opt/wsadminScripts/'
change_hlq  = '/opt/changes/'

# Make the methods used accessible in the path
sys.path.append(script_path)
sys.path.append(script_path + 'ConfigureLoggingMethods')
sys.path.append(script_path + 'ChangeScheduleMethods')
sys.path.append(script_path + 'TaskScheduleMethods')
sys.path.append(script_path + 'ServerTaskMethods')
sys.path.append(script_path + 'ApplicationTaskMethods')
sys.path.append(script_path + 'JobTaskMethods')
sys.path.append(script_path + 'ServicesTaskMethods')
sys.path.append(script_path + 'ResourcesTaskMethods')
sys.path.append(script_path + 'RuntimeTaskMethods')
sys.path.append(script_path + 'SecurityTaskMethods')
sys.path.append(script_path + 'OperationalTaskMethods')
sys.path.append(script_path + 'EnvironmentTaskMethods')
sys.path.append(script_path + 'SystemTaskMethods')
sys.path.append(script_path + 'UserandgroupTaskMethods')
sys.path.append(script_path + 'MonitoringTaskMethods')
sys.path.append(script_path + 'TroubleshootingTaskMethods')
sys.path.append(script_path + 'ServiceintegrationTaskMethods')
sys.path.append(script_path + 'UddiTaskMethods')
sys.path.append(script_path + 'Utilities')

# Import the JSON classes
from org.json import *
from java.io import *

# Import the jython classes
from ConfigureLoggingMethods       import *
from ChangeScheduleMethods         import *
from TaskScheduleMethods           import *
from ServerTaskMethods             import *
from ApplicationTaskMethods        import *
from JobTaskMethods                import *
from ServicesTaskMethods           import *
from ResourcesTaskMethods          import *
from RuntimeTaskMethods            import *
from SecurityTaskMethods           import *
from OperationalTaskMethods        import *
from EnvironmentTaskMethods        import *
from SystemTaskMethods             import *
from UserandgroupTaskMethods       import *
from MonitoringTaskMethods         import *
from TroubleshootingTaskMethods    import *
from ServiceintegrationTaskMethods import *
from UddiTaskMethods               import *

# Setup the log4j framework
mylogger = log4jsetup()

# Set the Task Dictionary from the Input
scheduleDict  = changeSchedule(mylogger,sys.argv)
scheduleSteps = scheduleDict.keys()

# Sort Steps into Sequence
scheduleSteps.sort()

# Setup the logger parameter list passed around all methods
loggerDict = {}
loggerDict["log_Level"] = 3
loggerDict["log_Method"]       = mylogger.info
loggerDict["audit_Step_Msg"]   = "audit Script Source - "
loggerDict["audit_Source_Msg"] = "audit Method Source - "
loggerDict["audit_Sub_Msg"]    = "audit Message Output"
loggerDict["changeFolder"]     = change_hlq 
loggerDict["changeNumber"]     = scheduleDict["changeID"]

for stepValue in scheduleSteps:
  stepID = "TaskID - Step - ",stepValue
  if   scheduleDict[stepValue].find('Servers')               != -1 : serverTasks(loggerDict,scheduleDict[stepValue]) 
  elif scheduleDict[stepValue].find('Applications')          != -1 : applicationTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('Jobs')                  != -1 : jobTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('Services')              != -1 : servicesTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('Resources')             != -1 : resourcesTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('RuntimeOperations')     != -1 : runtimeTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('Security')              != -1 : securityTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('OperationalPolicies')   != -1 : operationalTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('ENVIRONMENT_TASKS')     != -1 : environmentTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('SystemAdministration')  != -1 : systemTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('UsersAndGroups')        != -1 : userandgroupTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('Monitoring and Tuning') != -1 : monitoringTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('Troubleshooting')       != -1 : troubleshootingTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('ServiceIntegration')    != -1 : serviceintegrationTasks(loggerDict,scheduleDict[stepValue])
  elif scheduleDict[stepValue].find('UDDI')                  != -1 : uddiTasks(loggerDict,scheduleDict[stepValue])
