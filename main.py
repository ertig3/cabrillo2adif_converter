#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cabrillo2ADIF Converter v0.9
Professional Contest Log Conversion
Date: 2025-09-02 19:23:22
User: ertig3
"""

import sys
import os
import logging
from datetime import datetime
from pathlib import Path

from settings import SettingsManager
from translations import translator
from gui import Cabrillo2ADIFConverterGUI

def setup_logging():
    """Configure application logging"""
    if getattr(sys, 'frozen', False):
        app_path = Path(sys.executable).parent
    else:
        app_path = Path(__file__).parent
    
    log_file = app_path / 'converter.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def main():
    """Main application entry point"""
    logger = setup_logging()
    
    try:
        logger.info("Cabrillo2ADIF Converter v0.9 starting")
        logger.info(f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        settings = SettingsManager()
        translator.set_language(settings.get('language', 'en'))
        
        app = Cabrillo2ADIFConverterGUI(settings)
        app.run()
        
        logger.info("Application closed")
        
    except ImportError as e:
        print(f"Missing required files: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()