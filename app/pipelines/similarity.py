import numpy as np

class InvalidLengthException(Exception):
    """Exception raised when inputs don't have matching lengths"""
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def __str__(self):
        return f"Vectors a and b not of same length. Got lengths: {len(a)}, {len(b)}."

class InvalidShapeException(Exception):
    """Exception raised when inputs don't have the proper shape """
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def __str__(self):
        return f"Inputs must be one dimensional. Got shapes: {np.shape(a)}, {np.shape(b)}."


def cosine_similarity(a, b):
    """ Computes cosine similarity between two vectors a and b"""
    if a.ndim != 1 or b.ndim != 1:
        raise InvalidShapeException(a,b)

    if len(a) != len(b):
        raise InvalidLengthException(a,b)
    
    mag_a = np.linalg.norm(a)
    mag_b = np.linalg.norm(b)

    return np.dot(a,b)/(mag_a*mag_b)

def genre_average(genre_vectors):
    """Computes the vector average of genre vectors"""
    array = [vector for vector in genre_vectors]
    return np.average(array, axis=0)

def genre_similarity(song, genre_vectors):
    genre_average = genre_average(genre_vectors)
    similarity = cosine_similarity(song, genre_average)
    return similarity*100

