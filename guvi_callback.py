"""GUVI callback integration for final result submission."""
import httpx
import logging
from models import FinalResultPayload
from config import settings

logger = logging.getLogger(__name__)


class GUVICallback:
    """Handles submission of final results to GUVI evaluation endpoint."""
    
    def __init__(self):
        self.callback_url = settings.guvi_callback_url
        self.max_retries = 3
        self.timeout = 10.0
    
    async def submit_final_result(self, payload: FinalResultPayload) -> bool:
        """
        Submit final extracted intelligence to GUVI endpoint.
        
        Args:
            payload: FinalResultPayload with all extracted data
            
        Returns:
            True if submission successful, False otherwise
        """
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        self.callback_url,
                        json=payload.model_dump(),
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        logger.info(f"Successfully submitted results for session {payload.sessionId}")
                        return True
                    else:
                        logger.warning(
                            f"GUVI callback failed (attempt {attempt + 1}/{self.max_retries}): "
                            f"Status {response.status_code}, Response: {response.text}"
                        )
                
            except httpx.TimeoutException:
                logger.error(f"GUVI callback timeout (attempt {attempt + 1}/{self.max_retries})")
            
            except Exception as e:
                logger.error(f"GUVI callback error (attempt {attempt + 1}/{self.max_retries}): {e}")
            
            # Wait before retry (exponential backoff)
            if attempt < self.max_retries - 1:
                await asyncio.sleep(2 ** attempt)
        
        logger.error(f"Failed to submit results for session {payload.sessionId} after {self.max_retries} attempts")
        return False


# Import asyncio for sleep
import asyncio


# Global callback instance
guvi_callback = GUVICallback()
