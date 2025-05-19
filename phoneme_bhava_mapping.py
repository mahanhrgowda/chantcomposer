
# phoneme_bhava_mapping.py

def get_bhava_vector(text):
    words = text.split()
    return [[len(word)*i % 256 for i in range(6)] for word in words]

def bhava_tags_from_phonemes(vectors):
    return ["Śāntiḥ" if sum(v)%2 == 0 else "Vīraḥ" for v in vectors]
