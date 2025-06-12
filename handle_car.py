import math
import pygame
from value import max_speed, angle_velocity, friction, acceleration

def keyboard_input():
    keys = pygame.key.get_pressed()
    up = keys[pygame.K_z] or keys[pygame.K_UP]
    down = keys[pygame.K_x] or keys[pygame.K_DOWN]
    left = keys[pygame.K_LEFT]
    right = keys[pygame.K_RIGHT]
    return up, down, left, right

def update_car(car, up, down, left, right):
    # 가속/감속
    if up:
        car.speed += acceleration
    elif down:
        car.speed -= acceleration
    else:
        car.speed *= friction
    
    # 속도 제한
    car.speed = max(0, min(car.speed, max_speed))
    
    # 조향 (속도가 있을 때만)
    if car.speed > 0.1:
        if left:
            car.angle += angle_velocity
        elif right:
            car.angle -= angle_velocity
    
    # 각도를 라디안으로 변환
    angle_rad = math.radians(car.angle)
    
    # x, y 이동
    car.x += car.speed * math.cos(angle_rad)
    car.y += car.speed * math.sin(angle_rad) * -1  # pygame은 y축이 반대