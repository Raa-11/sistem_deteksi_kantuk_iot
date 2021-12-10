# import paket-paket yang diperlukan
import time
import argparse
import imutils
import cv2
import telepot
import csv
from telepot.loop import MessageLoop
from imutils.video import VideoStream
import dlib
from imutils import face_utils
from scipy.spatial import distance as dist
from gpiozero import Buzzer

def aspek_rasio_mata(mata):
    # Menghitung jarak euclidean antara dua set
    # landmark mata vertikal (x, y) -dikordinasikan
    A = dist.euclidean(mata[1], mata[5])
    B = dist.euclidean(mata[2], mata[4])

    # hitung jarak euclidean antara horizontal
    # mata landmark (x, y) -coordinate
    C = dist.euclidean(mata[0], mata[3])

    # menghitung rasio aspek mata
    arm = (A + B) / (2.0 * C)

    # mengembalikan aspek rasio mata
    return arm

def final_arm(bentuk):
    # ambil indeks landmark wajah untuk masing-masing mata kiri dan mata kanan
    (KRmulai, KRakhir) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (KNNmulai, KNNakhir) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # ekstrak koordinat mata kiri dan kanan, lalu gunakan
    # Koordinat untuk menghitung rasio aspek mata untuk kedua mata
    Matakiri = bentuk[KRmulai:KRakhir]
    Matakanan = bentuk[KNNmulai:KNNakhir]
    Kiriarm = aspek_rasio_mata(Matakiri)
    Kananarm = aspek_rasio_mata(Matakanan)

    # rata-rata rasio aspek mata bersama untuk kedua mata
    arm = (Kiriarm + Kananarm) / 2.0

    # mengembalikan aspek rasio mata, mata kiri dan mata kanan
    return (arm, Matakiri, Matakanan)

def aspek_rasio_mulut(mulut):
    # Menghitung jarak euclidean antara dua set
    # landmark mata vertikal (x, y) -dikordinasikan
    A = dist.euclidean(mulut[2], mulut[10])
    B = dist.euclidean(mulut[3], mulut[9])
    C = dist.euclidean(mulut[4], mulut[8])

    # hitung jarak euclidean antara horizontal
    # mata landmark (x, y) -coordinate
    D = dist.euclidean(mulut[0], mulut[6])

    # menghitung rasio aspek mulut
    arb = (A + B + C)/ (3 * D)

    # mengembalikan aspek rasio mata
    return arb

def final_mar(bentuk):
    # ambil indeks landmark mulut
    (Mulutawal, Mulutakhir) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

    # ekstrak koordinat mulut, lalu gunakan
    # Koordinat untuk menghitung rasio aspek mata untuk kedua mata
    Mulut1 = bentuk[Mulutawal:Mulutakhir]
    arb = aspek_rasio_mulut(Mulut1)

    # mengembalikan nilai aspek rasio mulut, dan mulut
    return (arb, Mulut1)

def kirim_pesan(pesan):
    global header
    global chat_id
    global img_counter
    chat_id = pesan['chat']['id']
    command = pesan['text']

    if (command == '/daftar'):
        fields = [str(chat_id)]
        validasi = False
        with open("daftar.csv", 'r') as read_csv:
            reader = csv.reader(read_csv)
            for row in reader:
                if(row[0] == str(chat_id)):
                    validasi = True
        if (validasi == False):
            with open('daftar.csv', 'a+', newline='') as write_csv:
                writer = csv.writer(write_csv)
                writer.writerow(fields)
                telegram_bot.sendMessage(chat_id, str("Anda sudah terdaftar"))
        else:
            telegram_bot.sendMessage(chat_id, str("Anda telah terdaftar"))
        read_csv.close()
    elif (command == '/foto'):
        img_name = "camera.png"
        cv2.imwrite(img_name, frame)
        telegram_bot.sendPhoto(chat_id, open('camera.png', 'rb'))
    elif(command == '/info'):
        telegram_bot.sendMessage(chat_id, str("Selamat Datang di Sistem Deteksi Kantuk dan Kelelahan"))
        telegram_bot.sendMessage(chat_id, str("/daftar untuk menerima notifikasi jika pengemudi sedang kelelahan atau mengantuk"))
        telegram_bot.sendMessage(chat_id, str("/info untuk melihat menu sistem"))
        telegram_bot.sendMessage(chat_id, str("/foto untuk mengirim foto pengemudi"))

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--webcam", type=int, default=0, help="index of webcam on system")
args = vars(ap.parse_args())
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
telegram_bot = telepot.Bot('1906430790:AAHLxAbQfSSCvCtUw0JqweLWbTQNrRPWlxE')
MessageLoop(telegram_bot, kirim_pesan).run_as_thread()
buzzer = Buzzer(4)

# menginisialisasi
microsleep = 0.20
menguap1 = 0.50
startTime = 0
Mulutdetik = 0
Muluttotal = 0
Matadetik = 0
Matatotal = 0
detik = 0
total = 0
kedip = 0
EYE_AR_CONSEC_FRAMES = 1
totalkedip = 0
totalkedip2 = 0

print("-> Starting Video Stream")
vs = VideoStream(src=args["webcam"]).start()
while True:
    if (startTime == True):
        startTime = time.time()

    frame = vs.read()
    frame = imutils.resize(frame, width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)

    if(len(rects) >= 1):
        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            #(x, y, w, h) = face_utils.rect_to_bb(rect)
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            #for (i, (x, y)) in enumerate(shape):
                #cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

            mata = final_arm(shape)
            arm = mata[0]
            Matakiri = mata[1]
            Matakanan = mata[2]

            leftEyeHull = cv2.convexHull(Matakiri)
            rightEyeHull = cv2.convexHull(Matakanan)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            mulut = final_mar(shape)
            arb = mulut[0]
            Mulut1 = mulut[1]

            mouthHull = cv2.convexHull(Mulut1)

            cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
            if(arm < microsleep):
                kedip += 1
            else:
                if kedip >= EYE_AR_CONSEC_FRAMES:
                    totalkedip += 1
                    kedip = 0

            detik = round(time.time() - startTime, 0)
            if(total == 0):
                total = detik + 60
            if(total == detik):
                totalkedip2 = totalkedip
                detik = 0
                total = 0
                totalkedip = 0
                if (totalkedip2 <= 8):
                    with open('daftar.csv', 'r') as read_file:
                        reader = csv.DictReader(read_file)
                        for row in reader:
                            telegram_bot.sendMessage(row['id'], str("Mata Pengemudi sudah lelah harap hubungi untuk beristirahat"))
                    read_file.close()
                    #cv2.putText(frame, "Mata Lelah", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    totalkedip2 = 0
                    buzzer.on()
                    time.sleep(3)
                    buzzer.off()

            if (arm < microsleep):
                Matadetik = round(time.time() - startTime, 0)
                if(Matatotal == 0):
                    Matatotal = Matadetik + 3
                if(Matatotal == Matadetik):
                    with open('daftar.csv', 'r') as read_file:
                        reader = csv.DictReader(read_file)
                        for row in reader:
                            telegram_bot.sendMessage(row['id'], str("Pengemudi mengantuk microsleep segera hubungi !!!"))
                    read_file.close()
                    #cv2.putText(frame, "Microsleep", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    startTime = 0
                    buzzer.on()
                    time.sleep(1)
            else:
                buzzer.off()
                Matatotal = 0

            if (arb > menguap1):
                Mulutdetik = round(time.time() - startTime, 0)
                if (Muluttotal == 0):
                    Muluttotal = Mulutdetik + 4
                if (Muluttotal == Mulutdetik):
                    with open('daftar.csv', 'r') as read_file:
                        reader = csv.DictReader(read_file)
                        for row in reader:
                            telegram_bot.sendMessage(row['id'], str("Pengemudi mengantuk menguap segera hubungi !!!"))
                    read_file.close()
                    #cv2.putText(frame, "Menguap!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    startTime = 0
                    buzzer.on()
                    time.sleep(3)
                    Muluttotal = 0
            else:
                buzzer.off()
                

            cv2.putText(frame, "EAR: {:.2f}".format(arm), (220, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, "MAR: {:.2f}".format(arb), (220, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, "Blinks: {}".format(totalkedip), (220, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Deteksi Kantuk", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
