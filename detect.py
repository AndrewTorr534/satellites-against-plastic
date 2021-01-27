from google.cloud import vision
import os
import json


def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    client = vision.ImageAnnotatorClient()

    image_name = path.split('/')[-1].split('.')[0]
    path_to_file = "/".join(path.split('/')[:-1])

    with open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    objects = client.object_localization(
        image=image).localized_object_annotations

    if len(objects) != 0:
        for idx, object_ in enumerate(objects):
            with open(f"{path_to_file}/{image_name}_{idx}.json", "w") as out_file:
                json.dump(str(object_), out_file, indent=6)


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/edoardo/Desktop/hackathon/lbghack2021team3-d510011500b4.json"
    localize_objects("/Users/edoardo/Desktop/hackathon/satellites-against-plastic/resources/images.jpg")