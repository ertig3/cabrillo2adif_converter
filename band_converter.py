#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Band Converter for Cabrillo2ADIF Converter
Date: 2025-09-02 19:31:37
User: ertig3
"""

import logging

class BandConverter:
    """Frequency to band converter"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.bands = {
            (135700, 137800): "2200M",
            (472000, 479000): "630M",
            (1800000, 2000000): "160M",
            (3500000, 4000000): "80M",
            (5330500, 5406500): "60M",
            (7000000, 7300000): "40M",
            (10100000, 10150000): "30M",
            (14000000, 14350000): "20M",
            (18068000, 18168000): "17M",
            (21000000, 21450000): "15M",
            (24890000, 24990000): "12M",
            (28000000, 29700000): "10M",
            (50000000, 54000000): "6M",
            (70000000, 70500000): "4M",
            (144000000, 148000000): "2M",
            (222000000, 225000000): "1.25M",
            (430000000, 440000000): "70CM",
            (902000000, 928000000): "33CM",
            (1240000000, 1300000000): "23CM",
            (2300000000, 2450000000): "13CM",
            (3300000000, 3500000000): "9CM",
            (5650000000, 5925000000): "6CM",
            (10000000000, 10500000000): "3CM",
        }
        
        self.logger.info("Band converter initialized")
    
    def frequency_to_band(self, frequency_str):
        """Convert frequency to band"""
        try:
            freq_hz = self._normalize_frequency(frequency_str)
            
            if freq_hz is None:
                self.logger.warning(f"Invalid frequency: {frequency_str}")
                return "UNKNOWN"
            
            for (freq_min, freq_max), band in self.bands.items():
                if freq_min <= freq_hz <= freq_max:
                    return band
            
            self.logger.warning(f"No band for frequency: {freq_hz} Hz")
            return "UNKNOWN"
            
        except Exception as e:
            self.logger.error(f"Band conversion error: {e}")
            return "UNKNOWN"
    
    def _normalize_frequency(self, freq_str):
        """Normalize frequency to Hz"""
        try:
            freq_clean = ''.join(c for c in str(freq_str) if c.isdigit() or c == '.')
            
            if not freq_clean:
                return None
            
            freq_num = float(freq_clean)
            
            if freq_num < 1000:
                return int(freq_num * 1000000)
            elif freq_num < 1000000:
                return int(freq_num * 1000)
            elif freq_num < 1000000000:
                return int(freq_num)
            else:
                return int(freq_num)
                
        except (ValueError, TypeError):
            return None
    
    def get_all_bands(self):
        """Get all supported bands"""
        return sorted(set(self.bands.values()))