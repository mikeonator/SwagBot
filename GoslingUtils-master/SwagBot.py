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

                close = ((agent.me.location - agent.ball.location).magnitude() < 2000)
                need_boost = (agent.me.boost < 20)
                my_goal_to_ball,ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
                goal_to_me = agent.me.location - agent.friend_goal.location
                my_distance = my_goal_to_ball.dot(goal_to_me)


                me_offside = my_distance - 200 > ball_distance
                foe_offside = abs(agent.foe_goal.location.y - agent.foes[0].location.y) - 200 > abs(agent.foe_goal.location.y - agent.ball.location.y)

                if need_boost and foe_offside:
                    large_boosts = [boost for boost in agent.boosts if boost.large and boost.active]
                    if (len(large_boosts) > 0):
                        closest_fatboost = large_boosts[0]
                        for boost in large_boosts: 
                                if (boost.location - agent.me.location).magnitude() < (closest_fatboost.location - agent.me.location).magnitude():
                                    closest_fatboost = boost
                        agent.push(goto_boost(closest_fatboost))   
                elif(not(agent.kickoff_flag)):
                    targets = {"goal":(opponent_left_post,opponent_right_post), "anywhere_but_my_net":(my_right_post,my_left_post)}
                    hits = find_hits(agent,targets)
                    print(hits)
                    relative_target = agent.ball.location - agent.me.location
                    local_target = agent.me.local(relative_target)
                    defaultPD(agent, local_target)
                    defaultThrottle(agent, 2300)
                        
                    
                
                    
        
