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
                
                friendleftpost = Vector3(1792.0,-4184.0,70.0)
                friendrightpost = Vector3(-1792.0,-4184.0,70.0)
                if agent.team == 0:
                    friendleftpost = Vector3(-1792.0,4184.0,70.0)
                    friendrightpost = Vector3(1792.0,4184.0,70.0)
                

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

                targets = {"goal":(agent.foe_goal.left_post,agent.foe_goal.right_post), "anywhere_but_my_net":(agent.friend_goal.right_post,agent.friend_goal.left_post), "mynet":(agent.friend_goal.left_post, agent.friend_goal.right_post), "notfoenet":(agent.foe_goal.right_post,agent.foe_goal.left_post)}
                hits = find_hits(agent,targets)
                foehits = find_hits(agent,targets,True)
                shotargets =  {'rightthird':((agent.foe_goal.right_post - Vector3(595.17,0,321.3875)),(agent.foe_goal.right_post + Vector3(0,0,321.3875))),'middlethird':((agent.foe_goal.left_post + Vector3(595.17,0,-321.3875)),(agent.foe_goal.right_post + Vector3(-595.17,0,321.3875))),'leftthird':((agent.foe_goal.left_post - Vector3(0,0,321.3875)),(agent.foe_goal.left_post + Vector3(595.17,0,321.3875)))}
                if agent.team != 0:
                    shotargets =  {'rightthird':((agent.foe_goal.right_post - Vector3(-595.17,0,321.3875)),(agent.foe_goal.right_post + Vector3(0,0,321.3875))),'middlethird':((agent.foe_goal.left_post + Vector3(-595.17,0,-321.3875)),(agent.foe_goal.right_post + Vector3(595.17,0,321.3875))),'leftthird':((agent.foe_goal.left_post - Vector3(0,0,321.3875)),(agent.foe_goal.left_post + Vector3(-595.17,0,321.3875)))}
                shots = find_hits(agent,shotargets)

                ball_to_friend_left = (agent.ball.location - agent.friend_goal.left_post).normalize()
                ball_to_foe_left = (agent.ball.location - agent.foe_goal.left_post).normalize()
                ball_to_friend_right = (agent.ball.location - agent.friend_goal.right_post).normalize()
                ball_to_foe_right = (agent.ball.location - agent.foe_goal.right_post).normalize()

                ball_to_friend = (agent.friend_goal.location - agent.ball.location).normalize()
                ball_to_friend_distance = (agent.friend_goal.location - agent.ball.location).magnitude()
                
                
                ball_travels_towards_me = agent.me.velocity.dot(agent.ball.velocity) #if negative, ball is going towards you 
                me_to_ball = (agent.me.location - agent.ball.location).normalize()
                ball_behind_me = agent.me.velocity.dot(me_to_ball) #if this is negative, the ball is behind you. 
                ball_towards_friend_goal = False
                ball_towards_foe_goal = False
                
                
                ballinleftthird = False
                ballinrightthird = False
                ballinmiddlethird = False

                #determines which side of the middle third of the friendly goal that the ball is on
                if agent.ball.location.x < -297.585:
                    if agent.team != 0:
                        ballonleft = True
                    elif agent.team == 0:
                        ballonright = True
                elif agent.ball.location.x > 297.585:
                    if agent.team != 0:
                        ballonright = True
                    elif agent.team == 0:
                        ballonleft = True
                if ((not ballinleftthird) and (not ballinrightthird)):
                    ballinmiddlethird = True
                

                #determines which side of the ball the opponent is on (in relation to the friendly goal)
                opponenttorightofball = False
                opponenttoleftofball = False
                if agent.foes[0].location.x < agent.ball.location.x:
                    if agent.team == 0:
                        opponenttorightofball = True
                    elif agent.team != 0:
                        opponenttoleftofball = True
                elif agent.foes[0].location.x > agent.ball.location.x:
                    if agent.team == 0:
                        opponenttoleftofball = True
                    elif agent.team != 0:
                        opponenttorightofball = True

                #determines which side of the ball the bot is on (in relation to the friendly goal)
                metorightofball = False
                metoleftofball = False
                if agent.me.location.x < agent.ball.location.x:
                    if agent.team == 0:
                        metorightofball = True
                    elif agent.team != 0:
                        metoleftofball = True
                elif agent.foes[0].location.x > agent.ball.location.x:
                    if agent.team == 0:
                        metoleftofball = True
                    elif agent.team != 0:
                        metorightofball = True
                    
                #Determines whether the ball is heading towards the friendly goal or the foe goal or neither
                if (agent.ball.velocity.magnitude() != 0):
                    
                    leftcross = Vector3.dot(agent.ball.velocity.normalize(), (Vector3.cross(Vector3(0,0,1), ball_to_friend_left)))
                    rightcross = Vector3.dot(agent.ball.velocity.normalize(), (Vector3.cross(Vector3(0,0,1), ball_to_friend_right)))
                    leftcrosso = Vector3.dot(agent.ball.velocity.normalize(), (Vector3.cross(Vector3(0,0,1), ball_to_foe_left)))
                    rightcrosso = Vector3.dot(agent.ball.velocity.normalize(), (Vector3.cross(Vector3(0,0,1), ball_to_foe_right)))

                    if ((leftcross < 0) and (rightcross > 0)):
                        ball_towards_friend_goal = True
                    if ((leftcrosso < 0) and (rightcrosso > 0)):
                        ball_towards_foe_goal = True

                #determines foe facing left or right (in relation to friend goal)
                foefacing = agent.foes[0].forward
                foefaceleft = False
                foefaceright = False
                if foefacing.x > 0:
                    if agent.team == 0:
                        foefaceleft = True
                    else:
                        foefaceright = True
                elif foefacing.x < 0:
                    if agent.team == 0:
                        foefaceright = True
                    else:
                        foefaceleft = True

                need_boost = (agent.me.boost < 25)
                
                if((ball_towards_friend_goal) and (ballonmyside)):
                    if len(hits["anywhere_but_my_net"]) != 0:
                        agent.push(hits["anywhere_but_my_net"][0])
                    agent.toxicity("Reactions_Noooo")

                elif ((need_boost and foe_offsideball) and ((not close) and (not ball_towards_friend_goal))):
                    #Determines which "fatboost" to go for
                    large_boosts = [boost for boost in agent.boosts if boost.large and boost.active]
                    if (len(large_boosts) > 0):
                        closest_fatboost = large_boosts[0]
                        for boost in large_boosts: 
                                if (boost.location - agent.me.location).magnitude() < (closest_fatboost.location - agent.me.location).magnitude():
                                    closest_fatboost = boost
                        agent.push(goto_boost(closest_fatboost))




                #Defense
                elif (ballonmyside and ballinrightthird):
                    if opponenttorightofball:
                            if len(hits["anywhere_but_my_net"]) > 0:
                                agent.push(hits["anywhere_but_my_net"][0])
                    else:
                        agent.push(goto(friendrightpost, (friendrightpost - (agent.ball.location + agent.ball.velocity))))
                elif (ballonmyside and ballinleftthird):
                    if opponenttoleftofball:
                            if len(hits["anywhere_but_my_net"]) > 0:
                                agent.push(hits["anywhere_but_my_net"][0])
                    else:
                        agent.push(goto(friendleftpost, (friendleftpost - (agent.ball.location + agent.ball.velocity))))
                elif (ballonmyside and ballinmiddlethird):
                    if (opponenttoleftofball and not foe_offsideball):
                        if len(shots['rightthird']) > 0:
                            agent.push(shots['rightthird'][0])
                        else:
                            if len(hits['goal']) > 0:
                                agent.push(hits['goal'][0])
                    if (opponenttorightofball and not foe_offsideball):
                        if len(shots['leftthird']) > 0:
                            agent.push(shots['leftthird'][0])
                        else:
                            if len(hits['goal']) > 0:
                                agent.push(hits['goal'][0])            
                    
                








                    
                #Offense
                elif ((not ballonmyside) and (ballinrightthird)):
                    if (opponenttorightofball):
                        if (len(shots['leftthird']) > 0) and (len(shots['middlethird']) > 0):
                            if shots['leftthird'][0].intercept_time < shots['middlethird'][0].intercept_time:
                                agent.push(shots['leftthird'][0])  
                            else:
                                agent.push(shots['middlethird'][0])
                    elif (opponenttoleftofball):
                        if metoleftofball:
                            if (len(shots['rightthird']) > 0):
                                agent.push(shots['rightthird'][0])
               
                elif ((not ballonmyside) and (ballinleftthird)):
                    if (opponenttoleftofball):
                        if (len(shots['rightthird']) > 0) and (len(shots['middlethird']) > 0):
                            if shots['rightthird'][0].intercept_time < shots['middlethird'][0].intercept_time:
                                agent.push(shots['rightthird'][0])
                            else:
                                agent.push(shots['middlethird'][0])
                    if (opponenttorightofball):
                        if len(shots['leftthird']) > 0:
                            agent.push(shots['leftthird'][0])

                elif ((not ballonmyside) and (ballinmiddlethird)):
                    if opponenttoleftofball:
                            if (len(shots['leftthird']) > 0):
                                agent.push(shots['leftthird'][0])     
                    elif opponenttorightofball:
                            if (len(shots['rightthird']) > 0):
                                agent.push(shots['rightthird'][0])
                
                if ((agent.foes[0].location - agent.ball.location).magnitude()) > ((agent.me.location - agent.ball.location).magnitude()):
                    if (len(hits['goal']) > 0):
                        agent.push(hits['goal'][0])

            
                #RECOVERY CONDITIONS
                    #Half Flip
                       #if the ball is moving away from you and behind you 
                #elif ball_behind_me < 0: 
                #    agent.push(halfflip(-1))

                #if the ball is going really fast towards bot and higher than double jump then halfflip    
                #elif ((((ball_travels_towards_me < 0) and (agent.ball.velocity.magnitude() >= fast)) and me_to_ball.magnitude.magnitude() <= 2500) and ((agent.ball.position.z >= 261) and (ball_behind_me > 0))):
                #    agent.push(halfflip(-1))

                #if nothing else works
                if len(agent.stack) < 1:
                    #print('alsoboi')
                    if len(hits['anywhere_but_my_net']) > 0:
                        agent.push(hits['anywhere_but_my_net'][0])
                        #print('BOI')
                    else:
                        agent.push(ballchase(agent.ball.location, (agent.foe_goal.location - agent.ball.location)))
                #print("="*8)