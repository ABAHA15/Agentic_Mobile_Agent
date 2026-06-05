import easyocr

reader = easyocr.Reader(
    ['en'],
    gpu=False
)


def extract_screen_text(
        image_path
):

    results = reader.readtext(
        image_path
    )

    text = ""

    for result in results:
        text += result[1] + " "

    return text