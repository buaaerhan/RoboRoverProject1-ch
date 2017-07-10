import numpy as np


# 你可以建立自己的决策树，基于perception_step()的输出，给throttle, brake 以及 steer 发送指令

def decision_step(Rover):

    # 针对不同的条件，判断在给定的图像数据下，该做出何种动作
    # 这是一个最基本的决策树，你需要完善这个决策树使得自动导航效果更好

    # 示例:
    # 检查是否有进行决策的视觉数据
    if Rover.nav_angles is not None:
        # 检查Rover.mode状态
        if Rover.mode == 'forward': 
            # 检查可导航区域外延
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                # 如果是‘forward’，可导航区域良好，速度低于最大速度，减速 
                if Rover.vel < Rover.max_vel:
                    # 设置减速值
                    Rover.throttle = Rover.throttle_set
                else: 
                    Rover.throttle = 0
                Rover.brake = 0
                # 设置角度范围为+/-15度
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
            # 如果可导航区域缺失，则进入‘stop’模式‘
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # 设置模式为’stop‘并刹车
                    Rover.throttle = 0
                    # 设置刹车值
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'

        # 如果已经是’stop‘模式，则做其他决定
        elif Rover.mode == 'stop':
            # 如果模式为'stop'但是还在运动，则刹车
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # 如果不再运动(vel < 0.2)，则做其他决定
            elif Rover.vel <= 0.2:
                # 现在停止下来且有视觉数据以便查看是否有前进道路
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # 释放刹车，转向
                    Rover.brake = 0
                    # 转向范围+/- 15度,当停止之后，下面一行代码使得四个轮子同时转动
                    Rover.steer = -15 
                # 如果已经停止，但是有足够的可导航区域，则前进!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # 设置减速值
                    Rover.throttle = Rover.throttle_set
                    # 释放刹车
                    Rover.brake = 0
                    # 回正方向舵
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
    # 如果没有修改代码，则随便让小车做些动作 
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # 如果处在捡石块样本的状态，发出捡拾命令
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

