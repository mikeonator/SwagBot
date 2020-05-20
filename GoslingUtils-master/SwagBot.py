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
                fast = 2240
                my_goal_to_ball,ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
                goal_to_me = agent.me.location - agent.friend_goal.location
                my_distance = my_goal_to_ball.dot(goal_to_me)
                
                #Determines whether the bot is on their side of the field or not
                amionmyside = False
                if agent.team == 0:
                    if agent.me.location.y < 1:
                        amionmyside = True
                else:
                    if agent.me.location.y > 1:
                        amionmyside = True

                #determines whether the foe is on their side of the field or not
                isfoeontheirside = False
                if agent.team == 0:
                    if agent.foes[0].location.y > 1:
                        isfoeontheirside = True
                else:
                    if agent.foes[0].location.y < 1:
                        isfoeontheirside = True

                #Determines if ball is on friendly side or not
                ballonmyside = False
                if agent.team == 0:
                    if agent.ball.location.y < 1:
                        ballonmyside = True
                else:
                    if agent.ball.location.y > 1:
                        ballonmyside = True


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

                need_boost = (agent.me.boost < 12)
                
                #SHOOT CONDITIONS
                    # ball on opponent half
                    # ball between you and opponent goal 
                    # define some sort of angle from the middle of the goal within which a shot can occur
                    # calculated.
                if ((not me_offsideball) and (not ballonmyside)):
                    if len(hits["goal"]) != 0:
                        agent.push(hits["goal"][0])
                #CLEAR CONDITIONS
                    # ball on your half
                    # enemy on their half
                    # bot up by 2+
                elif((ballonmyside) and (isfoeontheirside)):
                    if len(hits["goal"]) != 0:
                        agent.push(hits["goal"][0])
                #SAVE CONDITIONS
                    #Save1
                        #Ball Going towards friendly goal
                        #Ball on friendly side
                elif((ball_towards_friend_goal) and (ballonmyside)):
                    if len(hits["anywhere_but_my_net"]) != 0:
                        agent.push(hits["anywhere_but_my_net"][0])
                    agent.toxicity("Reactions_Noooo")
                          
                #NEEDBOOST CONDITIONS
                    #BOOSTPAD
                        # ball on friendly side
                        # boost < (amount)
                        # ball not going towards friendly goal
                elif((ballonmyside and need_boost) and (not ball_towards_friend_goal and not close)):
                    boosts = [boost for boost in agent.boosts if boost.active]
                    if (len(boosts) > 0):
                        closest_boost = boosts[0]
                        for boost in boosts:
                            if(boost.location - agent.me.location).magnitude() < (closest_boost.location -agent.me.location).magnitude():
                                closest_boost = boost
                        agent.push(goto_boost(closest_boost))
                    
                    #FATBOOST
                        #if the ball isnt going in the goal
                        #if the foe isnt on the same side of the field as the ball
                elif ((need_boost and foe_offsideball) and ((not close) and (not ball_towards_friend_goal))):
                    #Determines which "fatboost" to go for
                    large_boosts = [boost for boost in agent.boosts if boost.large and boost.active]
                    if (len(large_boosts) > 0):
                        closest_fatboost = large_boosts[0]
                        for boost in large_boosts: 
                                if (boost.location - agent.me.location).magnitude() < (closest_fatboost.location - agent.me.location).magnitude():
                                    closest_fatboost = boost
                        agent.push(goto_boost(closest_fatboost))
                

                #RECOVERY CONDITIONS
                    #Half Flip
                       #if the ball is moving away from you and behind you 
                #elif ball_behind_me < 0: 
                #    agent.push(halfflip(-1))

                #if the ball is going really fast towards bot and higher than double jump then halfflip    
                #elif ((((ball_travels_towards_me < 0) and (agent.ball.velocity.magnitude() >= fast)) and me_to_ball.magnitude.magnitude() <= 2500) and ((agent.ball.position.z >= 261) and (ball_behind_me > 0))):
                #    agent.push(halfflip(-1))

                #if nothing else works
            
            relative_target = agent.ball.location - agent.me.location
            local_target = agent.me.local(relative_target)
            defaultPD(agent, local_target)
            defaultThrottle(agent, 2300)