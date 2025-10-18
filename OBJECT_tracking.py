import cv2
import time
import math

p1 = 530
p2 = 300

xs = []
ys = []

video = cv2.VideoCapture("bb3.mp4")

#cargar rastreador
tracker = cv2.TrackerCSRT_create()

#ller el primer cuadro del video
returned, img = video.read()

#seleccionar el cuadro delimitador en la img
bbox = cv2.selectROI("rastreando", img, False)

#inicializar el rastreador en la img y el cuadro delimitador
tracker.init(img, bbox)

print(bbox)

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])

    cv2.rectangle(img,(x,y),((x+w), (y+h)),(255,0,255),3,1)

    cv2.putText(img, "Rstreando", (75,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,255,0),2)

def goal_track(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])

    c1 = int(x + w/2)
    c2 = int(y + h/2)

    cv2.circle(img, (c1,c2),2, (0,0,255), 5)

    cv2.circle(img,(int(p1), int(p2)),2,(0,0,255),3)

    #calcular la distancia
    dist = math.sqrt(((c1-p1)**2)+ ((c2-p2)**2))
    print(dist)

    if (dist < 20):
        cv2.putText(img, "Canasta", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 3)
        xs.append(c1)
        ys.append(c2)

    for i in range(len(xs)-1):
        cv2.circle(img, (xs[i], ys[i]), 2, (0,0,255), 5)

while True:
    check,img = video.read()

    #actualizar el rastreador y obtener la nueva posicion del cuadro delimitador
    success, bbox = tracker.update(img)

    if success:
        drawBox( img, bbox)
    else:
        cv2.putText(img, "No se puede rastrear", (75,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,0,255),2)

    goal_track(img, bbox)
    

    cv2.imshow("Resultado", img)

    key = cv2.waitKey(25)

    if key == 32:
        print("Detenido")
        break

video.release()
cv2.destroyAllWindows()