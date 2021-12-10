# sistem_deteksi_kantuk_iot
Sistem Deteksi Kantuk ini dibuat untuk mobil yang berbasis Internet of Things (IoT) yang dimana mendeteksi kantuknya melalui wajah yang nantinya wajah dapat di tangkap oleh kamera yang di taruh di atas dashboard mobil yang data wajah tersebut akan di olah oleh raspberry pi untuk mendeteksi kantuk jika terdeteksi kantuk maka buzzer akan berbunyi dan akan mengirim notifikasi ke telegram untuk memberitahu pihak keluarga. sistem yang dibangun pertama akan mendeteksi mata lelah terlebih dahulu yang dimana mata lelah dapat di deteksi jika pengemudi berkedip dibawah 8 kali per menit sebagai tanda awal ciri seseorang akan mengantuk. Untuk deteksi kantuknya sendiri akan di deteksi melalui menguap dimana menguap tanda awal seseorang mengantuk. Sistem akan mendeteksi jika seseorang tersebut menguap dengan mendeteksi jika mulut pengemudi terbuka lebih dari 4 detik maka akan dinyatakan menguap. Untuk deteksi kantuk yang kedua adalah microsleep dimana microsleep sendiri adalah kantuk berat. Sistem yang akan dibangun akan mendeteksi microsleep jika pengemudi memenjamkan matanya lebih dari 3 detik. Sistem Iot yang dibangun menggunakan hardware sebagai berikut :

1. Raspberry PI sebagai Microcontroller
2. Buzzer Active 5V
3. Kabel Jumper Female Male
4. Untuk daya menggunakan powerbank

Untuk library yang digunakan untuk membangun sistem ini sebagai berikut :

1. Time untuk melakukan hitung waktu
2. Argparse untuk melakukan argument processing
3. Imutils untuk rezise ukuran frame
4. Cv2 untuk melakukan conversi ke grayscale
5. Telepot untuk terhubung dengan telegram bot
6. VideoStream untuk mengambil gambar
7. dlib untuk facial landmark
8. scipy.spatial distance untuk menhitung jarak pada bagian mata dan mulut
9. gpiozero buzzer untuk menyalakan buzzer agar bersuara

Pada telegram bot tidak hanya mengirim pesan jika pengemudi mengantuk dan ada fungsi lainnya sebagai berikut :
1. /daftar untuk mendaftarkan diri agar dapat notifikasi jika pengemudi mengantuk
2. /info melihat menu yang dapat di akses
3. /foto untuk mengirim foto ke keluarga yang melakukan command tersebut agar dapat melihat keadaan pengemudi
