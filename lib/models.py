from ultralytics import YOLO

def create_model() -> YOLO:
    return YOLO("./lib/yolo_trained.pt") 
