
import pygame
import cv2
import numpy as np

pygame.mixer.init()

left_sound = pygame.mixer.Sound("sounds/left.wav")
center_sound = pygame.mixer.Sound("sounds/center.wav")
right_sound = pygame.mixer.Sound("sounds/right.wav")

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("Could not open webcam.")
    exit()

previous_y = None
last_hit_frame = 0
frame_count = 0
score = 0
high_score = 0

print("Fast Virtual Drum started. Press Q to exit.")
cv2.namedWindow("Fast Virtual Drum", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Fast Virtual Drum", 1400, 900)

while True:
    ret, frame = camera.read()

    if not ret:
        print("Could not read webcam.")
        break

    frame_count += 1
    height, width = frame.shape[:2]

    cv2.line(frame, (width // 3, 0),
             (width // 3, height), (255, 255, 255), 2)
    cv2.line(frame, (2 * width // 3, 0),
             (2 * width // 3, height), (255, 255, 255), 2)

    cv2.putText(frame, "LEFT", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(frame, "CENTER", (width // 3 + 20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, "RIGHT", (2 * width // 3 + 20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_orange = np.array([8, 150, 120])
    upper_orange = np.array([20, 255, 255])

    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:
        contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)

            center_x = x + w // 2
            center_y = y + h // 2

            cv2.circle(frame, (center_x, center_y),
                       10, (0, 255, 255), -1)

            if previous_y is not None:
                movement = center_y - previous_y

                if movement > 30 and frame_count - last_hit_frame > 5:

                    if center_x < width // 3:
                        left_sound.play()
                        zone = "LEFT DRUM"

                    elif center_x < 2 * width // 3:
                        center_sound.play()
                        zone = "CENTER DRUM"

                    else:
                        right_sound.play()
                        zone = "RIGHT DRUM"

                    score += 1
                    high_score = max(high_score, score)
                    last_hit_frame = frame_count

                    print(zone)

                    cv2.putText(
                        frame, zone, (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                        (0, 0, 255), 3
                    )

                    cv2.putText(
                        frame, "HIT!",
                        (center_x - 35, center_y - 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 255), 3
                    )

            previous_y = center_y

    cv2.putText(
        frame, f"Score: {score}", (10, height - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
        (255, 255, 255), 2
    )

    cv2.putText(
        frame, f"High Score: {high_score}", (10, height - 50),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
        (0, 255, 255), 2
    )

    cv2.imshow("Fast Virtual Drum", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
pygame.quit()

print("Final Score:", score)
print("High Score:", high_score)
