from ultralytics import YOLO

#model = YOLO('yolov8n.yaml').load('yolov8s.pt')
#model.train(data='../../yolov8 dataSet/data.yaml', epochs=5, imgsz=640)

model = YOLO("./runs/detect/train2/weights/best.pt")

r = model.predict(
   source= '../../Images/Output/1-wire-i2c-click-large_default-12x.jpg',
   conf=0.25,
   save=True,
   save_txt = True
)
print(r[0].names)
