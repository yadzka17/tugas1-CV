import cv2 as kamera
  
camera = kamera.VideoCapture(0)
  
hasil, gambar = camera.read()
  
if hasil:
  
    kamera.imshow("cek", gambar)
  
    kamera.waitKey(0)
    kamera.destroyWindow("cek")
  
else:
    print("Gagal")