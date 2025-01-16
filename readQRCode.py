import cv2
import csv 

fileName = "Progetti Gruppo Fight - Evento Live.csv"
startPoint = [0, 0]
posText = 0
thickness = -1
data_list = []
def reloadCSV():
    global data_list
    data_list = []
    with open(fileName, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data_list.append(row)

def saveCSV():
    # Salva i dati aggiornati nel file CSV
    with open(fileName, mode='w', newline='') as file:
        fieldnames = data_list[0].keys()  # Usa le chiavi del primo elemento come intestazioni
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Scrivi l'intestazione
        writer.writerows(data_list)  # Scrivi le righe modificate

reloadCSV()
cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("img", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
while True:
    _, img = cap.read()
    # detect and decode
    data, bbox, _ = detector.detectAndDecode(img)
    # check if there is a QRCode in the image
    if bbox is not None:
        reloadCSV()
        found = False  # Variabile per monitorare se troviamo il valore
        bboxTmp = bbox[0]
        for person in data_list:
            if data == person['OrderNumber']:
                #print("[+] QR Code is valid")
                #print("[+] Nome:", person["Nome"])
                person["IsPresent"] = "1"
                found = True
                
                for i in range(len(bboxTmp)):
                    nextPointIndex = (i+1) % len(bboxTmp)
                    #print(bboxTmp[i])
                    cv2.line(img, tuple(map(int, bboxTmp[i])), tuple(map(int, bboxTmp[nextPointIndex])), (0,255,0), 5)
                
                x, y = map(int, bbox[0][0])  # Coordinate dell'angolo superiore sinistro del QR Code
                cv2.putText(img, person["Nome"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                saveCSV()
                break  # Esce dal ciclo dopo aver trovato il primo elemento
        if not found:
            x, y = map(int, bbox[0][0])  # Coordinate dell'angolo superiore sinistro del QR Code
            for i in range(len(bboxTmp)):
                    nextPointIndex = (i+1) % len(bboxTmp)
                    #print(bboxTmp[i])
                    cv2.line(img, tuple(map(int, bboxTmp[i])), tuple(map(int, bboxTmp[nextPointIndex])), (0,0,255), 5)
            cv2.putText(img, "QR Code non valido", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            #print("[-] QR Code is not valid")
    cv2.rectangle(img, tuple(startPoint), (500, img.shape[0]) , (0, 0, 0), thickness)
    posText = 0
    indice = 1
    for data in data_list:
        if data["IsPresent"] == "1":  
            posText += 50        
            cv2.putText(img, f"{indice} {data['Nome']}", tuple([0, posText]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)   
            indice += 1
    cv2.imshow("img", img)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()