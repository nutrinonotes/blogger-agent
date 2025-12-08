import sys
import os
import logging
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SystemCheck")

def check_imports():
    logger.info("Checking imports...")
    try:
        import src.config
        import src.llm_wrapper
        import src.utils.io
        import src.utils.web_utils
        import src.agents.architect
        import src.agents.research
        import src.agents.draft
        import src.agents.verifier
        import src.agents.editor
        import src.agents.visuals
        import src.agents.audio
        import src.agents.publisher
        import src.agents.orchestrator
        logger.info("✅ All modules imported successfully.")
        return True
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error during import: {e}")
        return False

if __name__ == "__main__":
    if check_imports():
        logger.info("System looks consistent.")
        logger.info("To run the full pipeline, execute: python -m src.agents.orchestrator")
        sys.exit(0)
    else:
        sys.exit(1)
