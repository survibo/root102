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

def update_car_physics(car, up, down, left, right, dt=1.0):
    """
    향상된 차량 물리 시뮬레이션
    - 더 현실적인 가속/감속
    - 부드러운 조향
    - 관성과 드리프트 효과
    """
    
    # dt 정규화 (너무 큰 값 방지)
    dt = min(dt, 1.0)
    
    # 각도를 라디안으로 변환
    angle_rad = math.radians(car.angle)
    
    # 차량이 바라보는 방향 벡터
    forward_x = math.cos(angle_rad)
    forward_y = -math.sin(angle_rad)  # pygame의 y축은 아래쪽이 양수
    
    # 1. 가속/감속 처리
    if up:
        # 전진 가속
        car.engine_force = min(car.engine_force + acceleration, max_speed)
    elif down:
        # 후진 또는 브레이크
        if car.speed > 0.1:
            car.engine_force = max(car.engine_force - acceleration * 2, -max_speed * 0.5)
        else:
            car.engine_force = max(car.engine_force - acceleration, -max_speed * 0.5)
    else:
        # 엔진 힘 감소 (관성)
        car.engine_force *= 0.95
    
    # 2. 조향 처리 (속도에 따른 조향력 조정)
    if car.speed > 0.1:  # 움직일 때만 조향 가능
        turn_factor = min(1.0, 3.0 / (car.speed + 1))  # 속도가 빠를수록 조향이 어려워짐
        
        if left and not right:
            car.angular_velocity += angle_velocity * turn_factor
        elif right and not left:
            car.angular_velocity -= angle_velocity * turn_factor
    
    # 각속도 감쇠
    car.angular_velocity *= 0.85
    car.angle += car.angular_velocity
    
    # 3. 힘에서 가속도 계산
    mass = 1.0  # 차량 질량
    acceleration_force = car.engine_force / mass
    
    # 전진 방향 힘
    force_x = acceleration_force * forward_x * 0.3  # 속도 스케일링
    force_y = acceleration_force * forward_y * 0.3
    
    # 4. 속도 업데이트
    car.velocity_x += force_x
    car.velocity_y += force_y
    
    # 5. 드리프트/타이어 마찰 계산
    # 차량이 바라보는 방향과 실제 움직이는 방향의 차이
    dot_product = car.velocity_x * forward_x + car.velocity_y * forward_y
    
    # 측면 미끄러짐 계산
    side_x = car.velocity_x - dot_product * forward_x
    side_y = car.velocity_y - dot_product * forward_y
    
    # 타이어 그립 적용 (측면 미끄러짐 감소)
    grip_factor = 0.8  # 0~1, 클수록 미끄러짐이 적음
    car.velocity_x -= side_x * grip_factor
    car.velocity_y -= side_y * grip_factor
    
    # 6. 마찰 적용
    car.velocity_x *= friction
    car.velocity_y *= friction
    
    # 7. 현재 속도 크기 계산
    car.speed = math.sqrt(car.velocity_x**2 + car.velocity_y**2)
    
    # 8. 최대 속도 제한
    if car.speed > max_speed:
        scale = max_speed / car.speed
        car.velocity_x *= scale
        car.velocity_y *= scale
        car.speed = max_speed
    
    # 9. 위치 업데이트
    car.x += car.velocity_x
    car.y += car.velocity_y
    
    # 10. 속도가 매우 작으면 정지
    if car.speed < 0.01:
        car.velocity_x = 0
        car.velocity_y = 0
        car.speed = 0
        car.engine_force = 0
    
    return car.velocity_x, car.velocity_y

def get_car_stats(car):
    """디버깅용 차량 상태 정보"""
    return {
        'speed': round(car.speed, 2),
        'angle': round(car.angle % 360, 1),
        'engine_force': round(car.engine_force, 2),
        'velocity_x': round(car.velocity_x, 2),
        'velocity_y': round(car.velocity_y, 2)
    }