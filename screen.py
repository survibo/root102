import pygame
from handle_car import keyboard_input, update_car
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

class Car:
    def __init__(self):
        self.x = initial_center_x
        self.y = initial_center_y
        self.angle = 0
        self.speed = 0

car = Car()

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    
    screen.blit(map_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

    # 키보드 입력 및 차량 업데이트
    up, down, left, right = keyboard_input()
    update_car(car, up, down, left, right)
    
    # 차량 렌더링
    rotated_car_img = pygame.transform.rotate(car_img, car.angle)  
    rotated_rect = rotated_car_img.get_rect(center=(car.x, car.y))
    screen.blit(rotated_car_img, rotated_rect.topleft)
    
    print(f"Speed: {car.speed:.2f}, Angle: {car.angle:.1f}")

    pygame.display.flip()

pygame.quit()