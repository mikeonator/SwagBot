events = get_gamepad()
            if (agent.game.time_remaining == 299.9583435058594):
                boi = open(os.getcwd() + "/SavedOutput.txt", "w")
                boi.write('{"AButton":[0], "BButton":[0], "RightBump":[0], "RightTrig":[0], "LeftTrig":[0], "Yaw":[0], "Pitch":[0], "Time":[' + str(agent.time) + ']}')
                boi.close()
            agent.inputsave = {"AButton":[], "BButton":[], "RightBump":[], "RightTrig":[], "LeftTrig":[], "Yaw":[], "Pitch":[], "Time":[]}
            indict = open(os.getcwd() + "/SavedOutput.txt","r")
            agent.inputsave = ast.literal_eval(indict.read())
            BButton = False
            AButton = False
            RightBump = False
            LeftTrig = False
            RightTrig = False
            Yaw = False
            Pitch = False

            for event in events:
                if event.state != 0:
                    if event.code == "BTN_EAST":
                        agent.inputsave["BButton"].append(event.state)
                        BButton = True

                    if event.code == "BTN_SOUTH":
                        AButton = True
                        agent.inputsave["AButton"].append(event.state)

                    if event.code == "BTN_TR":
                        RightBump = True
                        agent.inputsave["RightBump"].append(event.state)

                    if event.code == "ABS_Z":
                        LeftTrig = True
                        savestate = int(event.state)
                        outstate = (savestate)/255
                        agent.inputsave["LeftTrig"].append(outstate)

                    if event.code == "ABS_RZ":
                        RightTrig = True
                        savestate = int(event.state)
                        outstate = (savestate)/255
                        agent.inputsave["RightTrig"].append(outstate)

                    if event.code == "ABS_X":
                        Yaw = True
                        savestate = int(event.state)
                        outstate = float()
                        if savestate > 0:
                            outstate = (savestate)/32767
                        else:
                            outstate = (savestate)/32768
                        agent.inputsave["Yaw"].append(outstate)

                    if event.code == "ABS_Y":
                        Pitch = True
                        savestate = int(event.state)
                        outstate = float()
                        if savestate > 0:
                            outstate = (savestate)/32767
                        else:
                            outstate = (savestate)/32768
                        agent.inputsave["Pitch"].append(outstate)
            
            if (AButton or BButton or RightBump or LeftTrig or RightTrig or Pitch or Yaw):
                print('brih')
                agent.inputsave["Time"].append((agent.time - agent.inputsave['Time'][0]))

                if (not (AButton)):
                    agent.inputsave["AButton"].append(0)
                
                if (not (BButton)):
                    agent.inputsave["BButton"].append(0)
                
                if (not (RightBump)):
                    agent.inputsave["RightBump"].append(0)
                
                if (not (LeftTrig)):
                    agent.inputsave["LeftTrig"].append(0)
                
                if (not (RightTrig)):
                    agent.inputsave["RightTrig"].append(0)
                
                if (not (Pitch)):
                    agent.inputsave["Pitch"].append(0)
                
                if (not (Yaw)):
                    agent.inputsave["Yaw"].append(0)

            outF = open(os.getcwd() + "/SavedOutput.txt", "w")
            outF.write(str(agent.inputsave))
            outF.close()