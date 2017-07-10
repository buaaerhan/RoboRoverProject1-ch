import numpy as np
import cv2

# 区分在阈值以上的像素
# RGB三个通道的值全都>160时，可以很好的识别出地面区域的像素
def color_thresh(img, rgb_thresh=([160,255], [160,255], [160,255])):
    # 创建一个零数组，大小与img相同，但是只有一个通道
    color_select = np.zeros_like(img[:,:,0])
    # 需要每一个RGB通道的值全都在阈值范围内，相应数组位置的值才会被置为True
    above_thresh = ((img[:,:,0] > rgb_thresh[0][0])&(img[:,:,0] < rgb_thresh[0][1])) \
                & ((img[:,:,1] > rgb_thresh[1][0])&(img[:,:,1] < rgb_thresh[1][1])) \
                & ((img[:,:,2] > rgb_thresh[2][0])&(img[:,:,2] < rgb_thresh[2][1]))
    # 与数组True位置对应的图片像素的值被设为1
    color_select[above_thresh] = 1
    # 返回一个二值图像
    return color_select


# 定义函数，将图片像素转换到小车本体坐标系下Define a function to convert from image coords to rover coords
def rover_coords(binary_img):
    # 识别非零像素点
    ypos, xpos = binary_img.nonzero()
    # 计算每个像素点相对于小车的位置，也就是相对于图片底部中点的位置  
    x_pixel = -(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[1]/2 ).astype(np.float)
    return x_pixel, y_pixel


# 定义函数，将像素点坐标转换到极坐标系下
def to_polar_coords(x_pixel, y_pixel):
    # 转换(x_pixel, y_pixel)到极坐标系下的(distance, angle)
    # 计算每个像素点的距离大小
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # 计算每个像素点相对于竖直方向的角度
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

# 定义函数，将小车坐标系下的像素点转换到世界坐标系
def rotate_pix(xpix, ypix, yaw):
    # 将偏航角转换成弧度
    yaw_rad = yaw * np.pi / 180
    xpix_rotated = (xpix * np.cos(yaw_rad)) - (ypix * np.sin(yaw_rad))
                            
    ypix_rotated = (xpix * np.sin(yaw_rad)) + (ypix * np.cos(yaw_rad))
    # 返回结果  
    return xpix_rotated, ypix_rotated

def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale): 
    # 放缩和平移
    xpix_translated = (xpix_rot / scale) + xpos
    ypix_translated = (ypix_rot / scale) + ypos
    # 返回结果  
    return xpix_translated, ypix_translated


# 定义函数，进行旋转，平移和截断操作
# 如果上面两个函数定义好了，那么这个函数应当正常工作
def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
    # 旋转操作
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    # 平移操作
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    # 截断操作(转换成整数)
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
    # 返回结果
    return x_pix_world, y_pix_world

# 定义函数，进行视角转换
def perspect_transform(img, src, dst):
           
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# 保持图像大小与输入图像相同
    
    return warped


# 依次调用上面函数，并更新小车状态
def perception_step(Rover):
    # 转换视角，更新Rover()
    # TODO: 
    # 注意: 图片来源于Rover.img
    image = Rover.img
    
    # 1) 定义源点和目标点，以便进行视角转换
    source = np.float32([[0, image.shape[0]/2],
                 [0, image.shape[0]], 
                 [image.shape[1], image.shape[0]], 
                 [image.shape[1], image.shape[0]/2]])
    destination = np.float32([[1, 0], 
                 [image.shape[1]*7/15, image.shape[0]], 
                 [image.shape[1]*8/15, image.shape[0]], 
                 [image.shape[1], 0]])
    
    # 2) 进行视角转换
    warped = perspect_transform(image, source, destination)
    
    
    # 3) 进行图像阈值分割，以便识别出可导航区域/障碍物/石块样本
    obstacles_threshold = ([0,80],[0,80],[0,80])
    rock_threshold = ([100,255],[100,255],[0,50])
    terrain_threshold = ([160,255],[160,255],[160,255])
    
    obstacles = color_thresh(warped,obstacles_threshold)
    rock = color_thresh(warped,rock_threshold)
    terrain = color_thresh(warped,terrain_threshold)
    
    # 4) 更新Rover.vision_image (在左侧显示)
        # Example: Rover.vision_image[:,:,0] = obstacle color-thresholded binary image
        #          Rover.vision_image[:,:,1] = rock_sample color-thresholded binary image
        #          Rover.vision_image[:,:,2] = navigable terrain color-thresholded binary image
    Rover.vision_image[:,:,0] = obstacles*255 # 注意这里只能使用像素值范围为0-255的图片
    Rover.vision_image[:,:,1] = rock*255  #不能直接使用0-1二值图像，否则无法显示
    Rover.vision_image[:,:,2] = terrain*255
        
    # 5) 将图片像素坐标转换到小车坐标系下
    # 障碍物
    x_pix_obstacles, y_pix_obstacles = rover_coords(obstacles)
    
    # 石块样本
    x_pix_rock, y_pix_rock = rover_coords(rock)
    
    # 可导航区域
    x_pix_terrain, y_pix_terrain = rover_coords(terrain)
    
    
    
    # 6) 将小车坐标系下的像素坐标转换到世界坐标系下
    world_size = 200
    scale = 15
    x_world_obstacles, y_world_obstacles = pix_to_world(x_pix_obstacles,y_pix_obstacles,Rover.pos[0],Rover.pos[1],Rover.yaw,world_size,scale)
    x_world_rock, y_world_rock = pix_to_world(x_pix_rock,y_pix_rock,Rover.pos[0],Rover.pos[1],Rover.yaw,world_size,scale)
    x_world_terrain, y_world_terrain = pix_to_world(x_pix_terrain,y_pix_terrain,Rover.pos[0],Rover.pos[1],Rover.yaw,world_size,scale)
    
    # 7) 更新世界地图(在屏幕右侧显示)
        # 示例: Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1
        #          Rover.worldmap[rock_y_world, rock_x_world, 1] += 1
        #          Rover.worldmap[navigable_y_world, navigable_x_world, 2] += 1
    Rover.worldmap[y_world_obstacles, x_world_obstacles, 0] += 1
    Rover.worldmap[y_world_rock, x_world_rock, 1] += 1
    Rover.worldmap[y_world_terrain, x_world_terrain, 2] += 1    
    
        
    # 8) 将小车坐标系下的像素坐标转换到极坐标系下
    rover_centric_pixel_distances,rover_centric_angles = to_polar_coords(x_pix_terrain,y_pix_terrain)
    
    # 更新像素的距离和角度
        # Rover.nav_dists = rover_centric_pixel_distances
        # Rover.nav_angles = rover_centric_angles
    Rover.nav_dists = rover_centric_pixel_distances
    Rover.nav_angles = rover_centric_angles
 
    
    # 返回更新后的Rover
    return Rover
