#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADIF Generator for Cabrillo2ADIF Converter
Comprehensive mapping of Cabrillo header + QSO data to ADIF.
Features:
 - OPERATOR / OPERATORS handling (first + full list when >1)
 - All Cabrillo CATEGORY-* fields preserved
 - CLAIMED-SCORE, NAME, EMAIL, ADDRESS, CLUB, LOCATION, CREATED-BY preserved
 - LOCATION heuristic to MY_STATE when 2-letter region (e.g. US/VE state)
 - transmitter_id preserved as APP_C2A_TXID (no misuse of TX_PWR)
 - Additional original software recorded in APP_C2A_CREATED_BY
 - Club stored as APP_C2A_CLUB
Date: 2025-09-17
User: ertig3
"""

import logging
from datetime import datetime
import re
from band_converter import BandConverter

class ADIFGenerator:
    """Generates ADIF format from Cabrillo QSOs with maximal information retention."""

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
        """Generate ADIF content from QSOs list + contest info dict."""
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
        """Generate ADIF header with maximal Cabrillo->ADIF mapping."""
        header = "ADIF Export from Cabrillo2ADIF Converter v0.9\n"
        header += f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        header += "User: ertig3\n"
        header += "\n"
        header += "<ADIF_VER:5>3.1.4\n"
        header += "<PROGRAMID:20>Cabrillo2ADIF_v0.9\n"
        header += f"<CREATED_TIMESTAMP:15>{datetime.utcnow().strftime('%Y%m%d %H%M%S')}\n"

        if contest_info:
            # Core direct mappings
            if 'contest' in contest_info:
                val = contest_info['contest']
                header += f"<CONTEST_ID:{len(val)}>{val}\n"

            if 'callsign' in contest_info:
                val = contest_info['callsign']
                header += f"<STATION_CALLSIGN:{len(val)}>{val}\n"

            if 'category_operator' in contest_info:
                val = contest_info['category_operator']
                header += f"<CATEGORY_OPERATOR:{len(val)}>{val}\n"

            if 'category_power' in contest_info:
                val = contest_info['category_power']
                header += f"<CATEGORY_POWER:{len(val)}>{val}\n"

            # Additional category fields
            if 'category_transmitter' in contest_info:
                val = contest_info['category_transmitter']
                header += f"<CATEGORY_TRANSMITTER:{len(val)}>{val}\n"

            if 'category_band' in contest_info:
                val = contest_info['category_band']
                header += f"<CATEGORY_BAND:{len(val)}>{val}\n"

            if 'category_mode' in contest_info:
                val = contest_info['category_mode']
                header += f"<CATEGORY_MODE:{len(val)}>{val}\n"

            # Claimed score (ADIF standard field)
            if 'claimed_score' in contest_info:
                val = contest_info['claimed_score']
                header += f"<CLAIMED_SCORE:{len(val)}>{val}\n"

            # Name & Email
            if 'name' in contest_info:
                val = contest_info['name']
                header += f"<NAME:{len(val)}>{val}\n"

            if 'email' in contest_info:
                val = contest_info['email']
                header += f"<EMAIL:{len(val)}>{val}\n"

            # Club as application-specific field
            if 'club' in contest_info:
                val = contest_info['club']
                header += f"<APP_C2A_CLUB:{len(val)}>{val}\n"

            # Location handling + heuristic for MY_STATE
            if 'location' in contest_info:
                raw_loc = contest_info['location']
                loc_up = raw_loc.upper()
                header += f"<APP_C2A_LOCATION:{len(loc_up)}>{loc_up}\n"
                if re.fullmatch(r'[A-Z]{2}', loc_up):  # Potential state/region code
                    header += f"<MY_STATE:{len(loc_up)}>{loc_up}\n"

            # Address (list -> single line)
            if 'address' in contest_info and isinstance(contest_info['address'], list):
                addr_join = ", ".join([a for a in contest_info['address'] if a.strip()])
                if addr_join:
                    header += f"<ADDRESS:{len(addr_join)}>{addr_join}\n"

            # Original software
            if 'created_by' in contest_info:
                val = contest_info['created_by']
                header += f"<APP_C2A_CREATED_BY:{len(val)}>{val}\n"

            # Operators handling (primary + list)
            if 'operators' in contest_info and contest_info['operators']:
                raw_ops = contest_info['operators'].strip()
                if raw_ops:
                    split_ops = [o.strip().upper() for o in re.split(r'[\s,;]+', raw_ops) if o.strip()]
                    seen = set()
                    unique_ops = []
                    for op in split_ops:
                        if op not in seen:
                            seen.add(op)
                            unique_ops.append(op)
                    if unique_ops:
                        primary = unique_ops[0]
                        header += f"<OPERATOR:{len(primary)}>{primary}\n"
                        if len(unique_ops) > 1:
                            ops_field = ",".join(unique_ops)
                            header += f"<OPERATORS:{len(ops_field)}>{ops_field}\n"

        header += "\n"
        return header

    def _generate_qso_adif(self, qso):
        """Generate ADIF record for a single QSO."""
        try:
            adif_fields = []

            if qso.dx_call:
                call = qso.dx_call.upper()
                adif_fields.append(f"<CALL:{len(call)}>{call}")
            else:
                self.logger.warning("QSO missing call sign, skipping")
                return ""

            if qso.date:
                # Accept already normalized YYYY-MM-DD only here (parser ensures formatting)
                try:
                    date_obj = datetime.strptime(qso.date, '%Y-%m-%d')
                    qso_date = date_obj.strftime('%Y%m%d')
                    adif_fields.append(f"<QSO_DATE:8>{qso_date}")
                except ValueError:
                    self.logger.warning(f"Invalid date format: {qso.date}")
                    return ""

            if qso.time:
                time_str = qso.time.replace(':', '').zfill(4)
                if len(time_str) == 4 and time_str.isdigit():
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

            # Preserve transmitter id (no assumption it is power)
            if qso.transmitter_id:
                txid = str(qso.transmitter_id)
                adif_fields.append(f"<APP_C2A_TXID:{len(txid)}>{txid}")

            adif_record = " ".join(adif_fields) + " <EOR>"
            return adif_record

        except Exception as e:
            self.logger.error(f"Error generating ADIF for QSO: {e}")
            return ""

    def _convert_mode(self, cabrillo_mode):
        """Convert Cabrillo mode to ADIF mode (mapping fallback to original)."""
        mode_upper = cabrillo_mode.upper()
        return self.mode_mappings.get(mode_upper, mode_upper)

    def get_conversion_stats(self):
        """Return conversion statistics."""
        return self.conversion_stats.copy()

    def validate_adif(self, adif_content):
        """Basic validation: header presence + QSO count."""
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
        """Return list of supported input modes (Cabrillo)."""
        return list(self.mode_mappings.keys())

    def format_adif_field(self, field_name, value):
        """Format single ADIF field generically."""
        if value is None or value == "":
            return ""
        value_str = str(value)
        return f"<{{field_name}}:{{len(value_str)}}>{{value_str}}"