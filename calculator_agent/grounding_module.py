from transformers import (
    AutoProcessor,
    AutoModelForZeroShotObjectDetection
)

from PIL import Image
import torch


DEVICE = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print("\nLoading GroundingDINO once...")


processor = AutoProcessor.from_pretrained(
    "IDEA-Research/grounding-dino-base"
)

model = AutoModelForZeroShotObjectDetection.from_pretrained(
    "IDEA-Research/grounding-dino-base"
).to(DEVICE)


def detect_ui_element(

    image_path,
    text_prompt

):

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

        inputs = processor(

            images=image,

            text=text_prompt,

            return_tensors="pt"

        ).to(DEVICE)

        with torch.no_grad():

            outputs = model(**inputs)

        results = processor.post_process_grounded_object_detection(

            outputs,

            inputs.input_ids,

            box_threshold=0.3,

            text_threshold=0.25,

            target_sizes=[image.size[::-1]]

        )

        result = results[0]

        boxes = result["boxes"]

        scores = result["scores"]

        if len(boxes) == 0:

            print("\nNo UI Element Detected")

            return None

        best_box = boxes[0]
        best_score = scores[0]

        print("\nGrounding Score:")
        print(float(best_score))

        x1, y1, x2, y2 = best_box.tolist()

        center_x = int(
            (x1 + x2) / 2
        )

        center_y = int(
            (y1 + y2) / 2
        )

        print("\nGroundingDINO Coordinate:")
        print((center_x, center_y))

        return (
            center_x,
            center_y
        )

    except Exception as e:

        print("\nGroundingDINO Error:")
        print(str(e))

        return None