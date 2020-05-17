from tools import  *
from objects import *
from routines import *

#This file is for strategy

class SwagBot(GoslingAgent):
    def run(agent):
        agent.debug_stack()
        #An example of pushing routines to the stack:
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
                        
                    
                
                    
        
