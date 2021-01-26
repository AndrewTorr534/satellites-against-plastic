from google.cloud import vision
import os
import cv2


def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    img = cv2.imread(path)

    image = vision.Image(content=content)
    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    
    vertexes = []
    if len(objects) != 0:
        for object_ in objects:
            print('\n{} (confidence: {})'.format(object_.name, object_.score))
            print('Normalized bounding polygon vertices: ')
            for vertex in object_.bounding_poly.normalized_vertices:
                print(' - ({}, {})'.format(vertex.x, vertex.y))
                vertexes.append((int(vertex.x * img.shape[1]), int(vertex.y * img.shape[0])))

        for _ in range(len(objects)):
            cv2.rectangle(img, vertexes[_*4], vertexes[_*4+2], (0,0,255), 2)

        
        cv2.imshow("img", img)
        cv2.waitKey(10000)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/edoardo/Desktop/hackathon/lbghack2021team3-d510011500b4.json"
    localize_objects("/Users/edoardo/Desktop/hackathon/satellites-against-plastic/resources/images.jpg")