"""Main FastAPI application for Agentic Honey-Pot."""
import logging
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from models import HoneypotRequest, HoneypotResponse, FinalResultPayload
from config import settings
from scam_detector import ScamDetector
from agent import ConversationalAgent
from intelligence_extractor import IntelligenceExtractor
from session_manager import session_manager
from guvi_callback import guvi_callback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize components
scam_detector = ScamDetector()
agent = ConversationalAgent()
intel_extractor = IntelligenceExtractor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    logger.info("🚀 Agentic Honey-Pot starting up...")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"Max conversation turns: {settings.max_conversation_turns}")
    yield
    logger.info("👋 Agentic Honey-Pot shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Agentic Honey-Pot API",
    description="AI-powered honeypot for scam detection and intelligence extraction",
    version="1.0.0",
    lifespan=lifespan
)

# Allow requests from browsers (live_demo.html, presentation, any origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_api_key(x_api_key: str = Header(...)) -> bool:
    """Verify API key from request header."""
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Agentic Honey-Pot",
        "version": "1.0.0",
        "active_sessions": session_manager.get_active_sessions_count()
    }


@app.post("/api/honeypot", response_model=HoneypotResponse)
async def honeypot_endpoint(
    request: HoneypotRequest,
    x_api_key: str = Header(..., alias="x-api-key")
):
    """
    Main honeypot endpoint that receives messages and engages scammers.
    
    Args:
        request: Incoming message request
        x_api_key: API key for authentication
        
    Returns:
        HoneypotResponse with agent's reply
    """
    # Verify API key
    verify_api_key(x_api_key)
    
    try:
        session_id = request.sessionId
        current_message = request.message
        
        logger.info(f"📨 Received message for session {session_id}")
        
        # Get or create session
        session = session_manager.get_session(session_id)
        
        # Add current message to session
        session.add_message(current_message)
        
        # Check if this is the first message
        is_first_message = len(request.conversationHistory) == 0
        
        if is_first_message:
            # Detect scam intent
            is_scam, confidence, explanation = scam_detector.detect(current_message.text)
            session.scam_detected = is_scam
            session.scam_confidence = confidence
            
            logger.info(f"🔍 Scam detection: {is_scam} (confidence: {confidence:.2f})")
            
            if not is_scam:
                # Not a scam, return normal response
                return HoneypotResponse(
                    status="success",
                    reply="Thank you for your message. How can I help you?"
                )
        
        # Extract intelligence from current message
        session.intelligence = intel_extractor.extract(
            current_message.text,
            session.intelligence
        )
        
        # Analyze scammer tactics
        tactics = agent.analyze_scammer_tactics(current_message.text)
        if tactics:
            session.add_note(tactics)
        
        # Generate agent response
        agent_reply = agent.generate_response(
            current_message.text,
            request.conversationHistory
        )
        
        logger.info(f"🤖 Agent reply: {agent_reply}")
        
        # Check if conversation should end
        should_end = session.should_end_conversation(settings.max_conversation_turns)
        
        if should_end:
            logger.info(f"✅ Ending conversation for session {session_id}")
            
            # Prepare final result payload
            final_payload = FinalResultPayload(
                sessionId=session_id,
                scamDetected=session.scam_detected,
                totalMessagesExchanged=session.turn_count,
                extractedIntelligence=session.intelligence,
                agentNotes=session.get_agent_notes_summary()
            )
            
            # Submit to GUVI endpoint
            success = await guvi_callback.submit_final_result(final_payload)
            
            if success:
                logger.info(f"✅ Successfully submitted results to GUVI for session {session_id}")
            else:
                logger.error(f"❌ Failed to submit results to GUVI for session {session_id}")
            
            # Clean up session
            session_manager.delete_session(session_id)
        
        return HoneypotResponse(
            status="success",
            reply=agent_reply
        )
    
    except Exception as e:
        logger.error(f"❌ Error processing request: {e}", exc_info=True)
        return HoneypotResponse(
            status="error",
            message=f"Internal server error: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
