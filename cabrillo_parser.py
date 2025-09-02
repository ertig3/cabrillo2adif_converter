#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cabrillo Parser for Cabrillo2ADIF Converter
Date: 2025-09-02 19:20:13
User: ertig3
"""

import logging
import re
from datetime import datetime
from pathlib import Path

class CabrilloQSO:
    """Represents a single QSO from Cabrillo log"""
    
    def __init__(self):
        self.frequency = ""
        self.mode = ""
        self.date = ""
        self.time = ""
        self.my_call = ""
        self.my_rst_sent = ""
        self.my_exchange_sent = ""
        self.dx_call = ""
        self.dx_rst_rcvd = ""
        self.dx_exchange_rcvd = ""
        self.transmitter_id = ""
        self.raw_line = ""

class CabrilloParser:
    """Parses Cabrillo contest log files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.contest_info = {}
        self.qsos = []
        
        self.logger.info("Cabrillo parser initialized")
    
    def parse_file(self, filename):
        """Parse Cabrillo file and return QSOs"""
        self.qsos = []
        self.contest_info = {}
        
        try:
            file_path = Path(filename)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {filename}")
            
            self.logger.info(f"Parsing Cabrillo file: {filename}")
            
            # Try different encodings
            content = None
            encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                        content = f.read()
                    self.logger.info(f"Successfully read file with {encoding} encoding")
                    break
                except Exception as e:
                    self.logger.warning(f"Failed to read with {encoding}: {e}")
                    continue
            
            if not content:
                raise Exception("Could not read file with any encoding")
            
            lines = content.split('\n')
            qso_count = 0
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                if not line or line.startswith('#'):
                    continue
                
                try:
                    if line.upper().startswith('QSO:'):
                        qso = self._parse_qso_line(line)
                        if qso:
                            self.qsos.append(qso)
                            qso_count += 1
                            self.logger.debug(f"Parsed QSO {qso_count}: {qso.dx_call}")
                    else:
                        self._parse_header_line(line)
                        
                except Exception as e:
                    self.logger.warning(f"Error parsing line {line_num}: {e}")
                    self.logger.debug(f"Problematic line: {line}")
                    continue
            
            self.logger.info(f"Parsed {qso_count} QSOs from {filename}")
            
            if qso_count == 0:
                self.logger.warning("No QSOs found - checking file format")
                self._debug_file_content(content)
            
            return self.qsos
            
        except Exception as e:
            self.logger.error(f"Error parsing Cabrillo file: {e}")
            raise
    
    def _debug_file_content(self, content):
        """Debug file content to understand format"""
        lines = content.split('\n')
        qso_lines = [line for line in lines if 'QSO' in line.upper()]
        
        self.logger.info(f"Found {len(qso_lines)} lines containing 'QSO'")
        
        for i, line in enumerate(qso_lines[:5]):  # Show first 5 QSO lines
            self.logger.info(f"QSO line {i+1}: {repr(line)}")
            
        # Check for common variations
        variations = ['QSO:', 'qso:', 'QSO ', 'qso ']
        for var in variations:
            count = len([line for line in lines if line.strip().startswith(var)])
            if count > 0:
                self.logger.info(f"Found {count} lines starting with '{var}'")
    
    def _parse_qso_line(self, line):
        """Parse a QSO line with flexible format handling"""
        try:
            self.logger.debug(f"Parsing QSO line: {line}")
            
            # Remove "QSO:" prefix and clean whitespace
            if line.upper().startswith('QSO:'):
                line_data = line[4:].strip()
            else:
                line_data = line.strip()
            
            # Split by whitespace, handling multiple spaces
            parts = line_data.split()
            
            if len(parts) < 10:
                self.logger.warning(f"QSO line has only {len(parts)} parts, need at least 10: {line}")
                # Try to parse what we have
                if len(parts) < 6:
                    return None
            
            qso = CabrilloQSO()
            qso.raw_line = line
            
            try:
                # Standard Cabrillo format:
                # freq mode date time mycall sent_rst sent_ex dxcall rcvd_rst rcvd_ex [transmitter]
                qso.frequency = parts[0] if len(parts) > 0 else ""
                qso.mode = parts[1] if len(parts) > 1 else ""
                qso.date = parts[2] if len(parts) > 2 else ""
                qso.time = parts[3] if len(parts) > 3 else ""
                qso.my_call = parts[4] if len(parts) > 4 else ""
                qso.my_rst_sent = parts[5] if len(parts) > 5 else ""
                qso.my_exchange_sent = parts[6] if len(parts) > 6 else ""
                qso.dx_call = parts[7] if len(parts) > 7 else ""
                qso.dx_rst_rcvd = parts[8] if len(parts) > 8 else ""
                qso.dx_exchange_rcvd = parts[9] if len(parts) > 9 else ""
                
                if len(parts) > 10:
                    qso.transmitter_id = parts[10]
                
                # Alternative format handling - some logs have different field order
                if not qso.dx_call and len(parts) > 7:
                    # Try alternative parsing
                    self.logger.debug("Trying alternative QSO format")
                    
                # Validate essential fields
                if not qso.dx_call:
                    self.logger.warning(f"No DX call found in QSO: {line}")
                    return None
                
                if not qso.my_call:
                    self.logger.warning(f"No station call found in QSO: {line}")
                    return None
                
                # Clean up callsigns
                qso.dx_call = qso.dx_call.strip().upper()
                qso.my_call = qso.my_call.strip().upper()
                
                # Validate frequency
                if qso.frequency:
                    try:
                        float(qso.frequency)
                    except ValueError:
                        self.logger.warning(f"Invalid frequency: {qso.frequency}")
                        qso.frequency = ""
                
                # Validate date format
                if qso.date:
                    if not self._validate_date(qso.date):
                        self.logger.warning(f"Invalid date format: {qso.date}")
                        qso.date = ""
                
                # Validate time format
                if qso.time:
                    if not self._validate_time(qso.time):
                        self.logger.warning(f"Invalid time format: {qso.time}")
                        qso.time = ""
                
                self.logger.debug(f"Successfully parsed QSO: {qso.my_call} -> {qso.dx_call}")
                return qso
                
            except Exception as e:
                self.logger.error(f"Error parsing QSO fields: {e}")
                return None
            
        except Exception as e:
            self.logger.error(f"Error parsing QSO line: {e}")
            return None
    
    def _validate_date(self, date_str):
        """Validate date format"""
        try:
            # Try different date formats
            formats = ['%Y-%m-%d', '%Y%m%d', '%m/%d/%Y', '%d.%m.%Y']
            for fmt in formats:
                try:
                    datetime.strptime(date_str, fmt)
                    return True
                except ValueError:
                    continue
            return False
        except:
            return False
    
    def _validate_time(self, time_str):
        """Validate time format"""
        try:
            # Common time formats: HHMM, HH:MM
            time_clean = time_str.replace(':', '')
            if len(time_clean) == 4 and time_clean.isdigit():
                hour = int(time_clean[:2])
                minute = int(time_clean[2:])
                return 0 <= hour <= 23 and 0 <= minute <= 59
            return False
        except:
            return False
    
    def _parse_header_line(self, line):
        """Parse header line and extract contest information"""
        try:
            if ':' not in line:
                return
            
            key, value = line.split(':', 1)
            key = key.strip().upper()
            value = value.strip()
            
            # Store important contest information
            header_fields = {
                'CONTEST': 'contest',
                'CALLSIGN': 'callsign',
                'CATEGORY-OPERATOR': 'category_operator',
                'CATEGORY-TRANSMITTER': 'category_transmitter',
                'CATEGORY-POWER': 'category_power',
                'CATEGORY-BAND': 'category_band',
                'CATEGORY-MODE': 'category_mode',
                'CLAIMED-SCORE': 'claimed_score',
                'CLUB': 'club',
                'LOCATION': 'location',
                'NAME': 'name',
                'EMAIL': 'email',
                'OPERATORS': 'operators',
                'CREATED-BY': 'created_by'
            }
            
            if key in header_fields:
                self.contest_info[header_fields[key]] = value
            elif key == 'ADDRESS':
                if 'address' not in self.contest_info:
                    self.contest_info['address'] = []
                self.contest_info['address'].append(value)
            
        except Exception as e:
            self.logger.warning(f"Error parsing header line: {e}")
    
    def get_contest_info(self):
        """Return parsed contest information"""
        return self.contest_info.copy()
    
    def get_qso_count(self):
        """Return number of parsed QSOs"""
        return len(self.qsos)
    
    def validate_qsos(self):
        """Validate parsed QSOs"""
        valid_qsos = []
        invalid_count = 0
        
        for qso in self.qsos:
            if self._validate_qso(qso):
                valid_qsos.append(qso)
            else:
                invalid_count += 1
                self.logger.debug(f"Invalid QSO: {qso.raw_line}")
        
        if invalid_count > 0:
            self.logger.warning(f"Found {invalid_count} invalid QSOs")
        
        return valid_qsos
    
    def _validate_qso(self, qso):
        """Validate a single QSO"""
        try:
            # Check required fields
            if not qso.my_call or not qso.dx_call:
                return False
            
            # Basic callsign validation
            if len(qso.my_call) < 3 or len(qso.dx_call) < 3:
                return False
            
            return True
            
        except Exception:
            return False
    
    def get_statistics(self):
        """Return parsing statistics"""
        stats = {
            'total_qsos': len(self.qsos),
            'valid_qsos': len(self.validate_qsos()),
            'contest_name': self.contest_info.get('contest', 'Unknown'),
            'station_call': self.contest_info.get('callsign', 'Unknown'),
            'modes': set(),
            'bands': set()
        }
        
        for qso in self.qsos:
            if qso.mode:
                stats['modes'].add(qso.mode.upper())
            
            # Extract band from frequency
            if qso.frequency:
                try:
                    freq = float(qso.frequency)
                    if freq >= 1800 and freq <= 2000:
                        stats['bands'].add('160M')
                    elif freq >= 3500 and freq <= 4000:
                        stats['bands'].add('80M')
                    elif freq >= 7000 and freq <= 7300:
                        stats['bands'].add('40M')
                    elif freq >= 14000 and freq <= 14350:
                        stats['bands'].add('20M')
                    elif freq >= 21000 and freq <= 21450:
                        stats['bands'].add('15M')
                    elif freq >= 28000 and freq <= 29700:
                        stats['bands'].add('10M')
                    elif freq >= 50000 and freq <= 54000:
                        stats['bands'].add('6M')
                    elif freq >= 144000 and freq <= 148000:
                        stats['bands'].add('2M')
                except ValueError:
                    pass
        
        # Convert sets to lists
        stats['modes'] = list(stats['modes'])
        stats['bands'] = list(stats['bands'])
        
        return stats
    
    def debug_parse_file(self, filename):
        """Debug version of parse_file with detailed logging"""
        try:
            file_path = Path(filename)
            self.logger.info(f"Debug parsing: {filename}")
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            self.logger.info(f"File has {len(lines)} lines")
            
            # Look for QSO lines
            qso_lines = []
            for i, line in enumerate(lines):
                if 'QSO' in line.upper():
                    qso_lines.append((i+1, line.strip()))
            
            self.logger.info(f"Found {len(qso_lines)} potential QSO lines")
            
            # Show first few QSO lines
            for line_num, line in qso_lines[:3]:
                self.logger.info(f"Line {line_num}: {repr(line)}")
                parts = line.split()
                self.logger.info(f"  Parts ({len(parts)}): {parts}")
            
            return qso_lines
            
        except Exception as e:
            self.logger.error(f"Debug parse error: {e}")
            return []