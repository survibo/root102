import pygame
from handle_car import keyboard_input, update_car_physics, get_car_stats
from value import max_speed, angle_velocity, friction, acceleration

pygame.init()
pygame.font.init()

screen_ratio = 12
result_ratio = screen_ratio/14
map_img = pygame.image.load("easymap.png")
map_img = pygame.transform.scale(map_img, (1400*result_ratio, 900*result_ratio))
screen = pygame.display.set_mode((100*screen_ratio, 900/14*screen_ratio))
car_img = pygame.image.load("car.png")
car_img = pygame.transform.scale(car_img, (40*result_ratio, 40*result_ratio))
car_width = car_img.get_width()
car_height = car_img.get_height()
initial_center_x = (124 + car_width / 2) * result_ratio
initial_center_y = (770 + car_height / 2) * result_ratio

# 폰트 설정 (디버그 정보 출력용)
font = pygame.font.Font(None, 36)

class Car:
    def __init__(self):
        # 위치
        self.x = initial_center_x
        self.y = initial_center_y
        
        # 각도 및 각속도
        self.angle = 0
        self.angular_velocity = 0
        
        # 속도 벡터
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 0
        
        # 엔진 힘
        self.engine_force = 0

# 차량 생성
cars = [Car()]

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # 60FPS로 제한
    
    screen.blit(map_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

    # 키보드 입력 처리
    up, down, left, right = keyboard_input()
    
    for car in cars:
        # 물리 업데이트 (dt 제거)
        move_x, move_y = update_car_physics(car, up, down, left, right)
        
        # 차량 렌더링
        rotated_car_img = pygame.transform.rotate(car_img, car.angle)  
        rotated_rect = rotated_car_img.get_rect(center=(car.x, car.y))
        screen.blit(rotated_car_img, rotated_rect.topleft)
        
        # 디버그 정보 출력
        stats = get_car_stats(car)
        debug_text = f"Speed: {stats['speed']} | Angle: {stats['angle']}° | Engine: {stats['engine_force']}"
        text_surface = font.render(debug_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

    pygame.display.flip()

pygame.quit()