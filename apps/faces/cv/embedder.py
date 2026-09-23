"""Pure-Python face embedding helpers."""
"""Pure face-encoding logic. No Django imports here on purpose."""

import face_recognition
import numpy as np


def get_face_encoding(image_path: str):
    """
    Returns a 128-d embedding (list of floats) for the first face found
    in the image, or None if no face is detected.
    """
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        return None
    return encodings[0].tolist()


def get_all_face_encodings(image_path: str):
    """
    Returns a list of (encoding, face_location) tuples for every face
    found in a class photo. face_location is (top, right, bottom, left).
    """
    image = face_recognition.load_image_file(image_path)
    locations = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image, locations)
    return list(zip(encodings, locations))


def match_encoding(unknown_encoding, known_encodings: list, known_labels: list, tolerance: float = 0.5):
    """
    Compares one unknown encoding against a list of known encodings.
    Returns (label, confidence) for the best match, or (None, 0.0) if no match.
    """
    if not known_encodings:
        return None, 0.0

    known_np = np.array(known_encodings)
    distances = face_recognition.face_distance(known_np, np.array(unknown_encoding))
    best_idx = int(np.argmin(distances))
    best_distance = distances[best_idx]

    if best_distance <= tolerance:
        confidence = round(1 - best_distance, 3)
        return known_labels[best_idx], confidence
    return None, 0.0