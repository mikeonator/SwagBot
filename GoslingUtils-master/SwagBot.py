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
                
                #Determines whether the bot is on their side of the field or not
                onmyside = False
                if agent.team == 0:
                    if agent.me.location.y < 1:
                        onmyside = True
                else:
                    if agent.me.location.y > 1:
                        onmyside = True

                #determines both whether the bot and the opponent are offside (based on the ball)
                me_offsideball = my_distance - 200 > ball_distance
                foe_offsideball = abs(agent.foe_goal.location.y - agent.foes[0].location.y) - 200 > abs(agent.foe_goal.location.y - agent.ball.location.y)

                targets = {"goal":(agent.foe_goal.left_post,agent.foe_goal.right_post), "anywhere_but_my_net":(agent.friend_goal.right_post,agent.friend_goal.left_post)}
                hits = find_hits(agent,targets)
                
                ball_to_friend_left = (agent.ball.location - agent.friend_goal.left_post).normalize()
                ball_to_friend_right = (agent.ball.location - agent.friend_goal.right_post).normalize()

                ball_to_friend = (agent.friend_goal.location - agent.ball.location).normalize()
                ball_to_friend_distance = (agent.friend_goal.location - agent.ball.location).magnitude()
                
                
                ball_travels_towards_me = agent.me.velocity.dot(agent.ball.velocity) #if negative, ball is going towards you 
                me_to_ball = (agent.me.location - agent.ball.location).normalize()
                ball_behind_me = agent.me.velocity.dot(me_to_ball) #if this is negative, the ball is behind you. 
                ball_towards_friend_goal = False
                

                #Determines whether the ball is heading towards the friendly goal
                if (agent.ball.velocity.magnitude() != 0):
                    
                    leftcross = Vector3.dot(agent.ball.velocity.normalize(), (Vector3.cross(Vector3(0,0,1), ball_to_friend_left)))
                    rightcross = Vector3.dot(agent.ball.velocity.normalize(), (Vector3.cross(Vector3(0,0,1), ball_to_friend_right)))

                    if ((leftcross < 0) and (rightcross > 0)):
                        ball_towards_friend_goal = True
                    else:
                        ball_towards_friend_goal = False

                ##we should fine tune the conditions for needboost
                if ((need_boost and foe_offsideball) and not close):
                    #Determines which "fatboost" to go for
                    large_boosts = [boost for boost in agent.boosts if boost.large and boost.active]
                    if (len(large_boosts) > 0):
                        closest_fatboost = large_boosts[0]
                        for boost in large_boosts: 
                                if (boost.location - agent.me.location).magnitude() < (closest_fatboost.location - agent.me.location).magnitude():
                                    closest_fatboost = boost
                        agent.push(goto_boost(closest_fatboost))
                

                                




                # relative_target = agent.ball.location - agent.me.location
                # local_target = agent.me.local(relative_target)
                # defaultPD(agent, local_target)
                # defaultThrottle(agent, 2300)