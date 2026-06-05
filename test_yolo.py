from ultralytics import YOLO

# Load fine-tuned model
model = YOLO("best.pt")

# Run detection
results = model(
    "test_image.png",
    conf=0.4
)

# Show results
results[0].show()

# Print detected boxes
for box in results[0].boxes:

    cls_id = int(box.cls[0])

    confidence = float(box.conf[0])

    coords = box.xyxy[0].tolist()

    print("Class ID:", cls_id)
    print("Confidence:", confidence)
    print("Coordinates:", coords)
    print("-" * 30)