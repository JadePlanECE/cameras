import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter(
    'output.avi',
    fourcc,
    30.0,
    (3840, 2160)
)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    out.write(frame)

    cv2.imshow("Recording", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()