from tools import  *
from objects import *
from routines import *

#This file is for strategy

class SwagBot(GoslingAgent):
    def run(agent):
        agent.debug_stack()
        #An example of pushing routines to the stack:

        if False:#len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff())
            else:
                x = 5000
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
                    targets = {"goal":(agent.foe_goal.left_post,agent.foe_goal.right_post), "anywhere_but_my_net":(agent.friend_goal.right_post,agent.friend_goal.left_post)}
                    hits = find_hits(agent,targets)
                    
                    ball_to_friend_left = (agent.ball.location - agent.friend_goal.left_post).normalize()
                    ball_to_friend_right = (agent.ball.location - agent.friend_goal.right_post).normalize()

                    ball_to_friend = (agent.friend_goal.location - agent.ball.location).normalize()
                    ball_to_friend_distance = (agent.friend_goal.location - agent.ball.location).magnitude()
                    ball_towards_friend_goal = ball_to_friend.dot(agent.ball.velocity)
                    
                    ball_travels_towards_me = agent.me.velocity.dot(agent.ball.velocity) #if negative, ball is going towards you 
                    me_to_ball = (agent.me.location - agent.ball.location).normalize()
                    ball_behind_me = agent.me.velocity.dot(me_to_ball) #if this is negative, the ball is behind you. 

                    if ball_towards_friend_goal > 0 and ball_to_friend_distance > 2000:
                        agent.push(hits["anywhere_but_my_net"][0])    

                    elif ball_travels_towards_me < 0 and agent.ball.velocity > 2240: 
                        agent.push(halfflip)
                        agent.push(hits["anywhere_but_my_net"][0])
                
                    elif ((ball_travels_towards_me < 0) and (agent.ball.velocity <= 2240) and (ball_behind_me > 0)): 
                        agent.push(hits["goal"][0])

                    agent.line(agent.ball.location, agent.friend_goal.left_post)
                    agent.line(agent.ball.location, agent.friend_goal.right_post)
                    agent.line(agent.ball.location, (agent.ball.location + agent.ball.velocity))

                    friendleftpostmag = (((ball_to_friend_left[0]**2) + (ball_to_friend_left[1]**2))**(1/2))
                    friendrightpostmag = (((ball_to_friend_right[0]**2) + (ball_to_friend_right[1]**2))**(1/2))
                    ballvelmag = (((agent.ball.velocity[0]**2) + (agent.ball.velocity[1]**2))**(1/2))

                    friendleftang = abs(math.acos(ball_to_friend_left[1]/friendleftpostmag))
                    friendrightang = abs(math.acos(ball_to_friend_right[1]/friendrightpostmag))
                    ballvelang = abs(math.acos(agent.ball.velocity[1]/ballvelmag))

                    if ballvelang in range(friendleftang,friendrightang):
                        agent.textpos("BALLTOWARDSGOAL")
                    else:
                        agent.textpos("BALLNOTTOWARDSGOAL")



                    #print(ball_to_friend_left)
                    #print(agent.ball.velocity)
                    #print("_"*7)
                    #ball_going_in_my_goal =

                    
                    #if len(hits["goal"]) > 0:
                        #agent.push(hits["goal"][0])
                    #elif len(hits["anywhere_but_my_net"]) > 0:
                        #agent.push(hits["anywhere_but_my_net"][0])

                    #relative_target = agent.ball.location - agent.me.location
                    #local_target = agent.me.local(relative_target)
                    #defaultPD(agent, local_target)
                    #defaultThrottle(agent, 2300)
                        
                    
                
                    
        
