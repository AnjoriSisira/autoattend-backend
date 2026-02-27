import random
from typing import Tuple
from app.ml.base import FaceRecognitionEngineBase

class MockFaceRecognitionEngine(FaceRecognitionEngineBase):
    """
    A mock implementation of the face recognition engine for development purposes.
    Since we don't have the actual ML model yet, this will just return dummy results.
    """
    
    async def match_face(self, image_bytes: bytes) -> Tuple[bool, float, str | None]:
        # Simulate processing time
        # await asyncio.sleep(0.5)
        
        # 80% chance of a "successful" read in the mock
        success = random.random() > 0.2
        
        if success:
            confidence = random.uniform(0.75, 0.99)
            # We don't know who the user is from bytes in a mock, 
            # so usually a service wrapper would handle passing a hint,
            # or the mock just returns a dummy UUID.
            # In a real pipeline, the ML model compares against the DB of encodings.
            dummy_matched_student_id = "00000000-0000-0000-0000-000000000000" 
            return True, confidence, dummy_matched_student_id
            
        return False, 0.0, None

    async def register_face(self, student_id: str, image_bytes: bytes) -> bool:
        """
        Mock registering a face. Always succeeds.
        """
        return True

# Singleton instance
mock_engine = MockFaceRecognitionEngine()
