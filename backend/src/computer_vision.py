from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from dataclasses import dataclass
import error
import time


@dataclass(frozen=True)
class ImageTag:
    name: str
    confidence: float


@dataclass(frozen=True)
class ImageCaption:
    text: str
    confidence: float
    

class Vision:
    def __init__(self, subscription_key, endpoint) -> None:
        self._client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    def tags(self, image_url) -> list[ImageTag] | error.Error:
        result = self._client.tag_image(image_url, language="ja")
        try:
            return [ImageTag(tag.name, tag.confidence) for tag in result.tags]
        except:
            return error.Error("Vision Error: tag_image")
    
    def description(self, image_url):
        result = self._client.describe_image(image_url, language="ja")
        try:
            return [ImageTag(tag, None) for tag in result.tags], [ImageCaption(caption.text, caption.confidence) for caption in result.captions]
        except:
            return error.Error("Vision Error: tag_image")
    
    def read(self, image_url):
        read_response = self._client.read(image_url, language="ja", raw=True)

        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]

        while True:
            read_result = self._client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        if read_result.status == OperationStatusCodes.succeeded:
            return [" ".join([line.text for line in x.lines]) for x in read_result.analyze_result.read_results]

