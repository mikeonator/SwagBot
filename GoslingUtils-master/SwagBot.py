from tools import  *
from objects import *
from routines import *
from inputs import get_gamepad
import os
import ast

#This file is for strategy

class SwagBot(GoslingAgent):
    def run(agent):
        agent.inputsave = {"AButton":[], "BButton":[], "RightTrig":[], "LeftTrig":[], "Yaw":[], "Pitch":[], "Time":[]}
        indict = open(os.getcwd() + "/SavedOutput.txt","r")
        agent.inputsave = ast.literal_eval(indict.read())
        print(str(agent.inputsave))

        agent.debug_stack()
        #An example of pushing routines to the stack:

        events = get_gamepad()
        agent.inputsave["Time"].append(agent.time)
        for event in events:
            if event.code == "BTN_EAST":
                agent.inputsave["BButton"].append(event.state)
            else:
                agent.inputsave["BButton"].append(0)
            if event.code == "BTN_SOUTH":
                agent.inputsave["AButton"].append(event.state)
            else:
                agent.inputsave["AButton"].append(0)
            if event.code == "ButtonABS_Z":
                savestate = int(event.state)
                outstate = (savestate)/255
                agent.inputsave["LeftTrig"].append(outstate)
            else:
                agent.inputsave["LeftTrig"].append(0)
            if event.code == "ButtonABS_RZ":
                savestate = int(event.state)
                outstate = (savestate)/255
                agent.inputsave["RightTrig"].append(outstate)
            else:
                agent.inputsave["RightTrig"].append(0)
            if event.code == "ButtonABS_X":
                savestate = int(event.state)
                outstate = float()
                if savestate > 0:
                    outstate = (savestate)/32767
                else:
                    outstate = (savestate)/32768
                agent.inputsave["Yaw"].append(outstate)
            else:
                agent.inputsave["Yaw"].append(0)
            if event.code == "ButtonABS_Y":
                savestate = int(event.state)
                outstate = float()
                if savestate > 0:
                    outstate = (savestate)/32767
                else:
                    outstate = (savestate)/32768
                agent.inputsave["Pitch"].append(outstate)
            else:
                agent.inputsave["Pitch"].append(0)
        print(str(agent.inputsave))
        outF = open(os.getcwd() + "/SavedOutput.txt", "w")
        outF.write(str(agent.inputsave))
        outF.close()


            

        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff())
            else:
                close = ((agent.me.location - agent.ball.location).magnitude() > 2000)
                need_boost = (agent.me.boost < 20)
                if need_boost:
                    large_boosts = [boost for boost in agent.boosts if boost.large and boost.active]
                    if (len(large_boosts) > 0):
                        closest_fatboost = large_boosts[0]
                        for boost in large_boosts: 
                                if (boost.location - agent.me.location).magnitude() < (closest_fatboost.location - agent.me.location).magnitude():
                                    closest_fatboost = boost
                        agent.push(goto_boost(closest_fatboost))   
                else:
                    relative_target = agent.ball.location - agent.me.location
                    local_target = agent.me.local(relative_target)
                    defaultPD(agent, local_target)
                    defaultThrottle(agent, 2300)
                        
                    
                
                    
        
