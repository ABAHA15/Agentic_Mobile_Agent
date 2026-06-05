import cv2

from ultralytics import YOLO

# ============================================
# LOAD YOLO MODEL
# ============================================

yolo_model = YOLO("best.pt")

# ============================================
# DETECT UI ELEMENTS
# ============================================

def detect_ui_elements(image_path):

    image = cv2.imread(image_path)

    results = yolo_model(image)

    detections = []

    for result in results:

        boxes = result.boxes

        for box in boxes:

            # ====================================
            # CLASS ID
            # ====================================

            cls = int(box.cls[0])

            # ====================================
            # CLASS NAME
            # ====================================

            class_name = (
                yolo_model.names[cls]
            )

            # ====================================
            # CONFIDENCE
            # ====================================

            confidence = float(
                box.conf[0]
                .cpu()
                .numpy()
            )

            # ====================================
            # BOUNDING BOX
            # ====================================

            x1, y1, x2, y2 = (

                box.xyxy[0]
                .cpu()
                .numpy()
            )

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            # ====================================
            # STORE DETECTION
            # ====================================

            detections.append({

                "class_name": class_name,

                "confidence": confidence,

                "bbox": (
                    x1,
                    y1,
                    x2,
                    y2
                )
            })

    # ============================================
    # DEBUG PRINT
    # ============================================

    print("\n===================")
    print("YOLO DETECTIONS")
    print("===================")

    for detection in detections:

        print(

            f"{detection['class_name']} | "
            f"{detection['confidence']:.2f} | "
            f"{detection['bbox']}"
        )

    return detections