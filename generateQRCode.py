import qrcode
import csv

fileName = "Progetti Gruppo Fight - Evento Live.csv"
path = ".//QRCode//"

with open(fileName, mode='r') as file:
    csv_reader = csv.DictReader(file)

    data_list = []

    for row in csv_reader:
        data_list.append(row)

for data in data_list:
    print(data)
    qr = qrcode.make(data['OrderNumber'])
    qr.save(path + data['Nome'] + ".png")