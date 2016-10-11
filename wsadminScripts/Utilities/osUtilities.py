#import inspect
import sys

def write_log(loggerDict):
  result = 0
  if   loggerDict["log_Level"] == 3: result = loggerDict["log_Method"](loggerDict["audit_Step_Msg"]+' : Method - '+sys._getframe().f_back.f_code.co_name+' - '+loggerDict["audit_Sub_Msg"])
  elif loggerDict["log_Level"] == 2: result = loggerDict["log_Method"](loggerDict["audit_Step_Msg"]+' : Method - '+sys._getframe().f_back.f_code.co_name+' - '+loggerDict["audit_Sub_Msg"])
  elif loggerDict["log_Level"] == 1: result = loggerDict["log_Method"](loggerDict["audit_Step_Msg"]+' : Method - '+sys._getframe().f_back.f_code.co_name+' - '+loggerDict["audit_Sub_Msg"])
  elif loggerDict["log_Level"] == 4: nop =1
  else :
    result = loggerDict["log_Method"](loggerDict["audit_Step_Msg"]+' '+'write_log'+' '+'logChoice (%s) is invalid' %(logChoice))
  return result






