
## https://docs.unrealengine.com/5.0/en-US/control-rig-python-scripting-in-unreal-engine/

from importlib import reload as __reload
import sys
import  unreal
unreal.log(" go to control rig packages")
import BrowserActions
# reload(BrowserActions)

def reload(done={},number=0):
    for k,v in sys.modules.items():
        if k not in done:
            if k.startswith('control_rig'):
                number+=1
                unreal.log(f'<-->{number}------> reload module :{k}   --at--   {v} ')
                __reload(v)
                done[k]=v
                reload(done,number)
                break
        else:
            pass

# reload(BrowserActions)
# def package_contents(control_rig):
#   package = __import__('control_rig')
#   return [module_name for module_name in dir(package) if not module_name.startswith("__")]


