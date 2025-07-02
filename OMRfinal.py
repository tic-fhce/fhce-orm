import cv2
import matplotlib.pyplot as plt
import respuestascorrectas 

def designarLetra(matPuntos):
    
    # A 65 - 75
    # B 95 - 100
    # C 122 - 133
    # D 150 - 163 
    # E 178 - 190 
    if len(matPuntos)==0:
        return -2   #significa no hay respuesta, -2 resp vacia 
    elif len(matPuntos)>1: 
        return -1   #significa que hay mas de una opc marcada, -1 error, preg descalificada
    else: 
        pt = matPuntos[0][0]
        if pt>=65 and pt<=75:
            return 1    #posicion respuestas[1] --> A
        elif pt>=95 and pt<=100:
            return 2    #posicion respuestas[2] --> B
        elif pt>=122 and pt<=133:
            return 3    #posicion respuestas[3] --> C
        elif pt>=150 and pt<=163:
            return 4    #posicion respuestas[4] --> D
        elif pt>=178 and pt<=190:
            return 5    #posicion respuestas[5] --> E
        else:
            return -1    #posicion no valida, -1 preg descalificada


def obtenerRespuesta(img):
    centers = []
    #bordes de las regiones blancas, bordes externos, todos los putnos 
    contornos = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contornos = contornos[0] if len(contornos) == 2 else contornos[1]

    # m00 area 
    # m10 coordenadas x
    # m01 coordenadas y
    i = 1
    for cntr in contornos:
        M = cv2.moments(cntr)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        pt = (cx,cy)
        centers.append(pt)
        # cv2.circle(resultado, (cx, cy), 10, (0, 0, 255), -1)
        # cv2.putText(resultado, "x: "+ str(cx) +" y: "+str(cy), (cx, cy), 1,1,(0,0,0), 1)
        i = i + 1
    # print(centers)
    return designarLetra(centers)



# Cargar imagen
img = cv2.imread(r"C:\Users\mayra\OneDrive\Escritorio\RECONOCIMIENTO_EXAMENES\examen3.jpeg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convertir de BGR a RGB 

h, w = img.shape[:2]
cv2.imshow("img", img)
cv2.waitKey(0)
img = img[155:h-125, 75:w-57] 
h, w = img.shape[:2]
cv2.imshow("img", img)
cv2.waitKey(0)

#colores de la iamgen 
colorMin = (31, 31, 31)
colorMax = (50, 50, 50)
thresh = cv2.inRange(img, colorMin, colorMax)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
# cerrar los circulos
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
# eliminar el ruido 
morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
img = morph

# mostrar resultados
cv2.imshow("thresh", thresh)
cv2.imshow("morph", morph)

# segmentar la imagen en tres automaticamente 
numCol = 3
particion = w//numCol
vecImg = []
i = 0
for f in range (particion, w+1, particion):
    # print(f"i: {i}, f: {f}")
    newimg = img[:h, i:f]
    vecImg.append(newimg)
    i = f
# for k in vecImg:
#     cv2.imshow("img", k)
#     cv2.waitKey(0)

# bien, ahora de cada imagen segmentada se debe ubicar cada circulo
# ventanita que recorrera cada fila 
numFil = 25
particionCol = h//numFil

respuestas = []
# print('hola')
for k in vecImg:
    i = 0
    for f in range (particionCol,h+1,particionCol):
        # print(f"i: {i}, f: {f}")
        newimg = k[i:f, :w]
        # cv2.imshow("img", newim g)
        # cv2.waitKey(0) 
        # ahora ingresa a la funcion para obtener la coordenada y recibir que opcion es
        resp = obtenerRespuesta(newimg)
        respuestas.append(resp)
        i = f

print(respuestas)
# comparamos con la matriz de respuestas correctas
resultados=[]
i=0
# print("bucle respuestas X")
# for x in respuestas:
#     print(x)

for x in respuestas:
    if x > 0:
        if respuestascorrectas.respCorrectas[i][x] == 1:
            resultados.append(1)
        else:
            resultados.append(0)
        
    else: 
        resultados.append(0)
    i+=1

respT=resultados.count(1)
respF=resultados.count(0)
print(f"Total: {respT}/{respT+respF}")
cv2.waitKey(0)