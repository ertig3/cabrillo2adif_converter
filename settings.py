#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Manager for Cabrillo2ADIF Converter
Date: 2025-09-02 19:31:37
User: ertig3
"""

import json
import os
import logging
from pathlib import Path

class SettingsManager:
    """Application settings manager"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.default_settings = {
            'language': 'en',
            'first_run': True,
            'window_geometry': '1200x900',
            'output_directory': '',
            'last_input_dir': '',
            'last_output_dir': '',
            'theme': 'dark',
            'auto_preview': True
        }
        
        self.settings_dir = Path.home() / '.cabrillo2adif_converter'
        self.settings_file = self.settings_dir / 'settings.json'
        
        self.settings = self.default_settings.copy()
        
        self.settings_dir.mkdir(exist_ok=True)
        self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
                self.logger.info("Settings loaded")
            else:
                self.logger.info("Using default settings")
        except Exception as e:
            self.logger.warning(f"Settings load error: {e}")
            self.settings = self.default_settings.copy()
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            self.logger.info("Settings saved")
        except Exception as e:
            self.logger.error(f"Settings save error: {e}")
    
    def get(self, key, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def is_first_run(self):
        """Check if first run"""
        return self.settings.get('first_run', True)
    
    def mark_first_run_complete(self):
        """Mark first run complete"""
        self.set('first_run', False)
    
    def get_output_directory(self):
        """Get output directory"""
        if not self.settings.get('output_directory'):
            default_dir = Path.home() / 'Documents' / 'Cabrillo2ADIF_Output'
            default_dir.mkdir(exist_ok=True)
            self.set('output_directory', str(default_dir))
        return self.settings['output_directory']
    
    def get_theme(self):
        """Get UI theme"""
        return self.settings.get('theme', 'dark')
    
    def set_theme(self, theme):
        """Set UI theme"""
        self.set('theme', theme)