from src.engine.deduplicator import generate_content_hash

def test_generate_content_hash_consistency():
    hash1 = generate_content_hash("ABC Tech", "Data Analyst", "Bangalore", "Looking for Python SQL dev")
    hash2 = generate_content_hash("abc tech", "data analyst", "bangalore", "looking for python sql dev")
    
    assert hash1 == hash2

def test_generate_content_hash_different_jobs():
    hash1 = generate_content_hash("ABC Tech", "Data Analyst", "Bangalore", "Looking for Python SQL dev")
    hash2 = generate_content_hash("XYZ Corp", "Software Engineer", "Hyderabad", "Looking for Java React dev")
    
    assert hash1 != hash2
