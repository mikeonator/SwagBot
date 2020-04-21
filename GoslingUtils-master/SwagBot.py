from tools import  *
from objects import *
from routines import *


#This file is for strategy

class SwagBot(GoslingAgent):
    def run(agent):
        #An example of using raw utilities:
        relative_target = agent.ball.location - agent.me.location
        local_target = agent.me.local(relative_target)
        defaultPD(agent, local_target)
        defaultThrottle(agent, 2300)

        #An example of pushing routines to the stack:
        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff())  
            else:
                close = ((agent.me.location - agent.ball.location).magnitude() > 2000)
                need_boost = (agent.me.boost > 20)

                large_boosts = [boost for boost in agent.boosts if boost.large and boost.active()]
                closest_fatboost = large_boosts[0]
                closest_fat_distance = (large_boosts[0].location - agent.me.location).magnitude()

                if (len(large_boosts) > 0):
                    for item in large_boosts:
                        item_distance = (item.location - agent.me.location).magnitude()
                        if item_distance < closest_fat_distance:
                            closest_fatboost = item
                            closest_fat_distance = item_distance
                    if need_boost:
                        agent.push(goto_boost(closest_fatboost))
                else:
                    agent.push(atba())
                
                    
        
