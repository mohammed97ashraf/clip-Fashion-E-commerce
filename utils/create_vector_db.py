from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer, util
from datasets import load_dataset
import uuid
from qdrant_client.http.models import PointStruct
from PIL import Image
from io import BytesIO
import base64



client = QdrantClient(":memory:")
client.recreate_collection(collection_name = "mycollection",
vectors_config = {"image": models.VectorParams( size = 512, distance = models.Distance.COSINE ) } )






data = load_dataset(
    "ashraq/fashion-product-images-small",
    split="train"
)





model = SentenceTransformer('clip-ViT-B-32')







def pil_image_to_base64(pil_image):
    """
    Convert a PIL image to a base64-encoded string.

    Args:
        pil_image (PIL.JpegImagePlugin.JpegImageFile): A PIL image object.

    Returns:
        str: The base64-encoded image data.
    """
    byte_io = BytesIO()
    pil_image.save(byte_io, format='JPEG')
    byte_image = byte_io.getvalue()
    base64_image = base64.b64encode(byte_image).decode('utf-8')
    return base64_image

def create_embadding():
    images = data["image"]
    ids = data['id']
    dispaly_name = data['productDisplayName']
    print("embadding started....")
    image_embeddings = model.encode([image for image in images[0:1000]])
    points = []
    for embadding,image,ids,productDisplayName in zip(image_embeddings,images[0:1000],ids[0:1000],dispaly_name[0:1000]):
        #print(str(ids))
        #display(image)
        payload = {"ids":ids,"productDisplayName":productDisplayName,"base_64_image":pil_image_to_base64(image)}
        embeddings = embadding.tolist()
        point_id = str(uuid.uuid4())  # Generate a unique ID for the point
        points.append(PointStruct(id=point_id,payload=payload,vector={"image":embeddings}))
    client.upsert(
        collection_name="mycollection",
        wait=True,
        points=points
    )
    print("embadding created....!")
    
def search_with_text(input_text):
    query_embedding = model.encode(input_text)
    image_hits = client.search(
        collection_name='mycollection',
        query_vector=models.NamedVector(
        name="image",
        vector=query_embedding.tolist()
        ),
        limit=3
        )
    return image_hits