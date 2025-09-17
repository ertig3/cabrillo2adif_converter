#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADIF Generator for Cabrillo2ADIF Converter
Date: 2025-09-02 19:31:37
User: ertig3
"""

import logging
from datetime import datetime
from band_converter import BandConverter

class ADIFGenerator:
    """Generates ADIF format from Cabrillo QSOs"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.band_converter = BandConverter()
        self.conversion_stats = {
            'total_qsos': 0,
            'qsos_with_mode': 0,
            'qsos_without_mode': 0,
            'qsos_with_frequency': 0,
            'qsos_without_frequency': 0
        }
        
        self.mode_mappings = {
            'CW': 'CW',
            'PH': 'SSB',
            'SSB': 'SSB',
            'USB': 'SSB',
            'LSB': 'SSB',
            'AM': 'AM',
            'FM': 'FM',
            'RTTY': 'RTTY',
            'PSK31': 'PSK31',
            'PSK63': 'PSK63',
            'MFSK': 'MFSK',
            'JT65': 'JT65',
            'JT9': 'JT9',
            'FT8': 'FT8',
            'FT4': 'FT4',
            'MSK144': 'MSK144'
        }
        
        self.logger.info("ADIF generator initialized")
    
    def generate(self, qsos, contest_info=None):
        """Generate ADIF content from QSOs"""
        self.conversion_stats = {
            'total_qsos': len(qsos),
            'qsos_with_mode': 0,
            'qsos_without_mode': 0,
            'qsos_with_frequency': 0,
            'qsos_without_frequency': 0
        }
        
        self.logger.info(f"Generating ADIF for {len(qsos)} QSOs")
        
        adif_content = self._generate_header(contest_info)
        
        for qso in qsos:
            qso_adif = self._generate_qso_adif(qso)
            if qso_adif:
                adif_content += qso_adif + "\n"
        
        adif_content += "<EOH>\n"
        
        self.logger.info("ADIF generation completed")
        return adif_content
    
    def _generate_header(self, contest_info=None):
        """Generate ADIF header"""
        header = "ADIF Export from Cabrillo2ADIF Converter v0.9\n"
        header += f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        header += "User: ertig3\n"
        header += "\n"
        header += "<ADIF_VER:5>3.1.4\n"
        header += "<PROGRAMID:20>Cabrillo2ADIF_v0.9\n"
        header += f"<CREATED_TIMESTAMP:15>{datetime.utcnow().strftime('%Y%m%d %H%M%S')}\n"
        
        if contest_info:
            # Standard ADIF fields
            if 'contest' in contest_info:
                contest_name = contest_info['contest']
                header += f"<CONTEST_ID:{len(contest_name)}>{contest_name}\n"
            
            if 'callsign' in contest_info:
                station_call = contest_info['callsign']
                header += f"<STATION_CALLSIGN:{len(station_call)}>{station_call}\n"
            
            if 'category_operator' in contest_info:
                header += f"<CATEGORY_OPERATOR:{len(contest_info['category_operator'])}>{contest_info['category_operator']}\n"
            
            if 'category_power' in contest_info:
                header += f"<CATEGORY_POWER:{len(contest_info['category_power'])}>{contest_info['category_power']}\n"
            
            # Additional standard ADIF category fields
            if 'category_transmitter' in contest_info:
                header += f"<CATEGORY_TRANSMITTER:{len(contest_info['category_transmitter'])}>{contest_info['category_transmitter']}\n"
            
            if 'category_band' in contest_info:
                header += f"<CATEGORY_BAND:{len(contest_info['category_band'])}>{contest_info['category_band']}\n"
            
            if 'category_mode' in contest_info:
                header += f"<CATEGORY_MODE:{len(contest_info['category_mode'])}>{contest_info['category_mode']}\n"
            
            if 'claimed_score' in contest_info:
                header += f"<CLAIMED_SCORE:{len(contest_info['claimed_score'])}>{contest_info['claimed_score']}\n"
            
            if 'name' in contest_info:
                header += f"<NAME:{len(contest_info['name'])}>{contest_info['name']}\n"
            
            if 'email' in contest_info:
                header += f"<EMAIL:{len(contest_info['email'])}>{contest_info['email']}\n"
            
            # Handle OPERATOR/OPERATORS field with deduplication and uppercase
            if 'operators' in contest_info:
                operators_str = contest_info['operators']
                # Split by comma or space, deduplicate, and convert to uppercase
                operators_list = []
                for op in operators_str.replace(',', ' ').split():
                    op_clean = op.strip().upper()
                    if op_clean and op_clean not in operators_list:
                        operators_list.append(op_clean)
                
                if operators_list:
                    # Use first operator for OPERATOR field
                    first_operator = operators_list[0]
                    header += f"<OPERATOR:{len(first_operator)}>{first_operator}\n"
                    
                    # Store all operators in OPERATORS field if more than one
                    if len(operators_list) > 1:
                        all_operators = ','.join(operators_list)
                        header += f"<OPERATORS:{len(all_operators)}>{all_operators}\n"
            
            # Application-specific fields for preserving Cabrillo data
            if 'club' in contest_info:
                header += f"<APP_C2A_CLUB:{len(contest_info['club'])}>{contest_info['club']}\n"
            
            if 'location' in contest_info:
                location = contest_info['location']
                header += f"<APP_C2A_LOCATION:{len(location)}>{location}\n"
                
                # Heuristic: if location is 2 letters, also set MY_STATE
                if len(location) == 2 and location.isalpha():
                    state_code = location.upper()
                    header += f"<MY_STATE:{len(state_code)}>{state_code}\n"
            
            if 'created_by' in contest_info:
                header += f"<APP_C2A_CREATED_BY:{len(contest_info['created_by'])}>{contest_info['created_by']}\n"
        
        header += "\n"
        return header
    
    def _generate_qso_adif(self, qso):
        """Generate ADIF record for single QSO"""
        try:
            adif_fields = []
            
            if qso.dx_call:
                call = qso.dx_call.upper()
                adif_fields.append(f"<CALL:{len(call)}>{call}")
            else:
                self.logger.warning("QSO missing call sign, skipping")
                return ""
            
            if qso.date:
                try:
                    date_obj = datetime.strptime(qso.date, '%Y-%m-%d')
                    qso_date = date_obj.strftime('%Y%m%d')
                    adif_fields.append(f"<QSO_DATE:8>{qso_date}")
                except ValueError:
                    self.logger.warning(f"Invalid date format: {qso.date}")
                    return ""
            
            if qso.time:
                time_str = qso.time.zfill(4)
                if len(time_str) == 4:
                    adif_fields.append(f"<TIME_ON:4>{time_str}")
                else:
                    self.logger.warning(f"Invalid time format: {qso.time}")
            
            if qso.frequency:
                try:
                    freq = float(qso.frequency)
                    if freq > 1000000:
                        freq_mhz = freq / 1000000
                    elif freq > 1000:
                        freq_mhz = freq / 1000
                    else:
                        freq_mhz = freq
                    
                    freq_str = f"{freq_mhz:.6f}".rstrip('0').rstrip('.')
                    adif_fields.append(f"<FREQ:{len(freq_str)}>{freq_str}")
                    
                    band = self.band_converter.frequency_to_band(qso.frequency)
                    if band != "UNKNOWN":
                        adif_fields.append(f"<BAND:{len(band)}>{band}")
                    
                    self.conversion_stats['qsos_with_frequency'] += 1
                    
                except ValueError:
                    self.logger.warning(f"Invalid frequency: {qso.frequency}")
                    self.conversion_stats['qsos_without_frequency'] += 1
            else:
                self.conversion_stats['qsos_without_frequency'] += 1
            
            if qso.mode:
                adif_mode = self._convert_mode(qso.mode)
                adif_fields.append(f"<MODE:{len(adif_mode)}>{adif_mode}")
                self.conversion_stats['qsos_with_mode'] += 1
            else:
                self.conversion_stats['qsos_without_mode'] += 1
            
            if qso.my_rst_sent:
                rst_sent = str(qso.my_rst_sent)
                adif_fields.append(f"<RST_SENT:{len(rst_sent)}>{rst_sent}")
            
            if qso.dx_rst_rcvd:
                rst_rcvd = str(qso.dx_rst_rcvd)
                adif_fields.append(f"<RST_RCVD:{len(rst_rcvd)}>{rst_rcvd}")
            
            if qso.my_exchange_sent:
                exchange_sent = str(qso.my_exchange_sent)
                adif_fields.append(f"<STX_STRING:{len(exchange_sent)}>{exchange_sent}")
            
            if qso.dx_exchange_rcvd:
                exchange_rcvd = str(qso.dx_exchange_rcvd)
                adif_fields.append(f"<SRX_STRING:{len(exchange_rcvd)}>{exchange_rcvd}")
            
            if qso.my_call:
                my_call = qso.my_call.upper()
                adif_fields.append(f"<STATION_CALLSIGN:{len(my_call)}>{my_call}")
            
            if qso.transmitter_id:
                tx_id = str(qso.transmitter_id)
                adif_fields.append(f"<APP_C2A_TXID:{len(tx_id)}>{tx_id}")
            
            adif_record = " ".join(adif_fields) + " <EOR>"
            return adif_record
            
        except Exception as e:
            self.logger.error(f"Error generating ADIF for QSO: {e}")
            return ""
    
    def _convert_mode(self, cabrillo_mode):
        """Convert Cabrillo mode to ADIF mode"""
        mode_upper = cabrillo_mode.upper()
        return self.mode_mappings.get(mode_upper, mode_upper)
    
    def get_conversion_stats(self):
        """Return conversion statistics"""
        return self.conversion_stats.copy()
    
    def validate_adif(self, adif_content):
        """Validate generated ADIF content"""
        try:
            lines = adif_content.split('\n')
            qso_count = 0
            header_found = False
            
            for line in lines:
                if '<ADIF_VER:' in line:
                    header_found = True
                if '<EOR>' in line:
                    qso_count += 1
            
            validation_result = {
                'valid': header_found and qso_count > 0,
                'header_found': header_found,
                'qso_count': qso_count,
                'total_lines': len(lines)
            }
            
            self.logger.info(f"ADIF validation: {validation_result}")
            return validation_result
            
        except Exception as e:
            self.logger.error(f"ADIF validation error: {e}")
            return {'valid': False, 'error': str(e)}
    
    def get_supported_modes(self):
        """Return list of supported modes"""
        return list(self.mode_mappings.keys())
    
    def format_adif_field(self, field_name, value):
        """Format single ADIF field"""
        if not value:
            return ""
        
        value_str = str(value)
        return f"<{field_name}:{len(value_str)}>{value_str}"