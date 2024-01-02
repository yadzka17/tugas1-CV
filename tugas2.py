import random
import cv2
import pygame
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pecah Balon")

fps = 30
clock = pygame.time.Clock()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

popSound = pygame.mixer.Sound(f"blowsup.wav")

# Ukuran gambar aset
imgNewWidth = 200
imgNewHeight = 450

# Gambar balon pecah
imgBalloon = pygame.transform.scale((pygame.image.load('BallonMerah.png').convert_alpha()),
                            (imgNewWidth, imgNewHeight))
rectBallon = imgBalloon.get_rect()
rectBallon.x, rectBallon.y = 50, 30

imgBalloonbiru = pygame.transform.scale((pygame.image.load('BallonBiru.png').convert_alpha()),
                            (imgNewWidth, imgNewHeight))
rectBallonbiru = imgBalloonbiru.get_rect()
rectBallonbiru.x, rectBallonbiru.y = 50, 30

imgBalloonhijau = pygame.transform.scale((pygame.image.load('BallonHijau.png').convert_alpha()),
                            (imgNewWidth, imgNewHeight))
rectBallonhijau = imgBalloonhijau.get_rect()
rectBallonhijau.x, rectBallonhijau.y = 50, 30

speed = 15
score = 0
startTime = time.time()
totalTime = 30
detector = HandDetector(detectionCon=0.8, maxHands=2)


def resetBalloon(x):
	if x == 'merah':
		rectBallon.x = random.randint(100, img.shape[1] - 100)
		rectBallon.y = img.shape[0] + 50
	elif x == 'biru':
		rectBallonbiru.x = random.randint(100, img.shape[1] - 100)
		rectBallonbiru.y = img.shape[0] + 50
	elif x == 'hijau':
		rectBallonhijau.x = random.randint(100, img.shape[1] - 100)
		rectBallonhijau.y = img.shape[0] + 50


start = True
while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    timeRemain = int(totalTime - (time.time() - startTime))
    if timeRemain < 0:
        window.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 50)
        textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time UP', True, (50, 50, 255))
        textTitle = font.render(f'Pecah Balon', True, (50, 50, 255))
        window.blit(textTitle, (490, 35))
        window.blit(textScore, (450, 350))
        window.blit(textTime, (530, 275))
    else:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        rectBallon.y -= speed
        if rectBallon.y < 0:
            resetBalloon('merah')
            speed += 1

        rectBallonbiru.y -= speed
        if rectBallonbiru.y < 0:
            resetBalloon('biru')
            speed += 1

        rectBallonhijau.y -= speed
        if rectBallonhijau.y < 0:
            resetBalloon('hijau')
            speed += 1

        if hands:
            hand = hands[0]
            x, y = hand['lmList'][8][0:2]

            if rectBallon.collidepoint(x, y):
                pygame.mixer.Sound.play(popSound)
                resetBalloon('merah')
                score += 10
                speed += 1

            if rectBallonbiru.collidepoint(x, y):
                pygame.mixer.Sound.play(popSound)
                resetBalloon('biru')
                score += 10
                speed += 1

            if rectBallonhijau.collidepoint(x, y):
                pygame.mixer.Sound.play(popSound)
                resetBalloon('hijau')
                score += 10
                speed += 1

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        window.blit(imgBalloon, rectBallon)
        window.blit(imgBalloonbiru, rectBallonbiru)
        window.blit(imgBalloonhijau, rectBallonhijau)

        font = pygame.font.Font('freesansbold.ttf', 50)
        textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time {timeRemain}', True, (50, 50, 255))
        textTitle = font.render(f'Pecah Balon', True, (50, 50, 255))
        window.blit(textTitle, (490, 35))
        window.blit(textScore, (35, 35))
        window.blit(textTime, (1000, 35))

    pygame.display.update()
    clock.tick(fps)