#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translation System for Cabrillo2ADIF Converter
Date: 2025-09-02 19:23:22
User: ertig3
"""

class Translations:
    """Application translation manager"""
    
    def __init__(self):
        self.translations = {
            'en': {
                'app_title': 'Cabrillo2ADIF Converter',
                'app_subtitle': 'Contest Log Conversion to ADIF 3.1.4',
                'version': 'v0.9',
                
                'menu_file': 'File',
                'menu_edit': 'Edit',
                'menu_tools': 'Tools',
                'menu_help': 'Help',
                'menu_open': 'Open Cabrillo File',
                'menu_save': 'Save ADIF As',
                'menu_open_folder': 'Open Output Folder',
                'menu_exit': 'Exit',
                'menu_clear': 'Clear Preview',
                'menu_reset': 'Reset All',
                'menu_language': 'Language',
                'menu_about': 'About',
                'menu_help_content': 'Help',
                
                'files_section': 'File Selection',
                'input_file_label': 'Cabrillo Input File:',
                'output_file_label': 'ADIF Output File:',
                'browse_button': 'Browse',
                'save_as_button': 'Save As',
                
                'conversion_section': 'Conversion',
                'qso_count': 'QSO Count:',
                'status_label': 'Status:',
                'convert_button': 'START CONVERSION',
                'converting_button': 'Converting...',
                
                'preview_section': 'ADIF Preview & Log',
                'clear_button': 'Clear',
                'save_button': 'Save Log',
                'copy_button': 'Copy',
                'preview_info': 'Live preview of conversion output',
                
                'status_ready': 'Ready',
                'status_file_loaded': 'File loaded',
                'status_converting': 'Converting...',
                'status_success': 'Conversion successful',
                'status_error': 'Conversion failed',
                'status_cleared': 'Preview cleared',
                'status_reset': 'Fields reset',
                
                'welcome_title': 'Cabrillo2ADIF Converter v0.9',
                'welcome_intro': 'Contest Log Converter',
                'welcome_instructions': 'QUICK START:',
                'welcome_step1': '1. Select Cabrillo file',
                'welcome_step2': '2. Choose output location',
                'welcome_step3': '3. Click START CONVERSION',
                'welcome_step4': '4. Review results',
                'welcome_features': 'FEATURES:',
                'welcome_bands': 'SUPPORTED BANDS:',
                'welcome_shortcuts': 'SHORTCUTS:',
                'welcome_ready': 'Ready for conversion!',
                
                'error_title': 'Error',
                'warning_title': 'Warning',
                'info_title': 'Information',
                'success_title': 'Success',
                
                'error_no_input': 'Please select a Cabrillo file',
                'error_file_not_found': 'Cabrillo file not found',
                'error_no_output': 'Please select output file',
                'error_no_qsos': 'No QSOs found in file',
                'error_conversion': 'Conversion failed',
                
                'success_conversion': 'Conversion completed',
                'success_saved': 'Log saved',
                'success_copied': 'Copied to clipboard',
                
                'select_cabrillo': 'Select Cabrillo File',
                'save_adif': 'Save ADIF File',
                'save_log': 'Save Log',
                
                'about_title': 'About Cabrillo2ADIF Converter',
                'about_version': 'Version: 0.9',
                'about_created': 'Created: 2025-09-02',
                'about_purpose': 'Contest Log Conversion',
                
                'help_title': 'Help',
                'help_quickstart': 'QUICK START:',
                'help_formats': 'FORMATS:',
                'help_features': 'FEATURES:',
                
                'conversion_started': 'CONVERSION STARTED',
                'conversion_completed': 'CONVERSION COMPLETED',
                'parsing_cabrillo': 'Parsing Cabrillo file',
                'generating_adif': 'Generating ADIF',
                'saving_file': 'Saving file',
                'qsos_converted': 'QSOs converted',
                'duration': 'Duration',
                'adif_preview': 'ADIF PREVIEW',
                
                'bands_hf': 'HF Bands',
                'bands_vhf_uhf': 'VHF/UHF Bands',
                
                'close': 'Close',
                'ok': 'OK',
                'cancel': 'Cancel',
                'yes': 'Yes',
                'no': 'No',
                'unknown': 'Unknown',
                'seconds': 'seconds'
            },
            
            'de': {
                'app_title': 'Cabrillo2ADIF Konverter',
                'app_subtitle': 'Contest-Log Konvertierung zu ADIF 3.1.4',
                'version': 'v0.9',
                
                'menu_file': 'Datei',
                'menu_edit': 'Bearbeiten',
                'menu_tools': 'Extras',
                'menu_help': 'Hilfe',
                'menu_open': 'Cabrillo-Datei öffnen',
                'menu_save': 'ADIF speichern als',
                'menu_open_folder': 'Ausgabeordner öffnen',
                'menu_exit': 'Beenden',
                'menu_clear': 'Vorschau löschen',
                'menu_reset': 'Zurücksetzen',
                'menu_language': 'Sprache',
                'menu_about': 'Über',
                'menu_help_content': 'Hilfe',
                
                'files_section': 'Datei-Auswahl',
                'input_file_label': 'Cabrillo-Eingabe:',
                'output_file_label': 'ADIF-Ausgabe:',
                'browse_button': 'Durchsuchen',
                'save_as_button': 'Speichern als',
                
                'conversion_section': 'Konvertierung',
                'qso_count': 'QSO-Anzahl:',
                'status_label': 'Status:',
                'convert_button': 'KONVERTIERUNG STARTEN',
                'converting_button': 'Konvertiert...',
                
                'preview_section': 'ADIF-Vorschau & Log',
                'clear_button': 'Löschen',
                'save_button': 'Log speichern',
                'copy_button': 'Kopieren',
                'preview_info': 'Live-Vorschau der Ausgabe',
                
                'status_ready': 'Bereit',
                'status_file_loaded': 'Datei geladen',
                'status_converting': 'Konvertiert...',
                'status_success': 'Konvertierung erfolgreich',
                'status_error': 'Konvertierung fehlgeschlagen',
                'status_cleared': 'Vorschau gelöscht',
                'status_reset': 'Felder zurückgesetzt',
                
                'welcome_title': 'Cabrillo2ADIF Konverter v0.9',
                'welcome_intro': 'Contest-Log Konverter',
                'welcome_instructions': 'SCHNELLSTART:',
                'welcome_step1': '1. Cabrillo-Datei wählen',
                'welcome_step2': '2. Ausgabeort bestimmen',
                'welcome_step3': '3. KONVERTIERUNG STARTEN klicken',
                'welcome_step4': '4. Ergebnisse prüfen',
                'welcome_features': 'FEATURES:',
                'welcome_bands': 'UNTERSTÜTZTE BÄNDER:',
                'welcome_shortcuts': 'SHORTCUTS:',
                'welcome_ready': 'Bereit für Konvertierung!',
                
                'error_title': 'Fehler',
                'warning_title': 'Warnung',
                'info_title': 'Information',
                'success_title': 'Erfolgreich',
                
                'error_no_input': 'Bitte Cabrillo-Datei wählen',
                'error_file_not_found': 'Cabrillo-Datei nicht gefunden',
                'error_no_output': 'Bitte Ausgabedatei wählen',
                'error_no_qsos': 'Keine QSOs in Datei gefunden',
                'error_conversion': 'Konvertierung fehlgeschlagen',
                
                'success_conversion': 'Konvertierung abgeschlossen',
                'success_saved': 'Log gespeichert',
                'success_copied': 'In Zwischenablage kopiert',
                
                'select_cabrillo': 'Cabrillo-Datei auswählen',
                'save_adif': 'ADIF-Datei speichern',
                'save_log': 'Log speichern',
                
                'about_title': 'Über Cabrillo2ADIF Konverter',
                'about_version': 'Version: 0.9',
                'about_created': 'Erstellt: 2025-09-02',
                'about_purpose': 'Contest-Log Konvertierung',
                
                'help_title': 'Hilfe',
                'help_quickstart': 'SCHNELLSTART:',
                'help_formats': 'FORMATE:',
                'help_features': 'FUNKTIONEN:',
                
                'conversion_started': 'KONVERTIERUNG GESTARTET',
                'conversion_completed': 'KONVERTIERUNG ABGESCHLOSSEN',
                'parsing_cabrillo': 'Cabrillo-Datei wird analysiert',
                'generating_adif': 'ADIF wird generiert',
                'saving_file': 'Datei wird gespeichert',
                'qsos_converted': 'QSOs konvertiert',
                'duration': 'Dauer',
                'adif_preview': 'ADIF-VORSCHAU',
                
                'bands_hf': 'KW-Bänder',
                'bands_vhf_uhf': 'VHF/UHF-Bänder',
                
                'close': 'Schließen',
                'ok': 'OK',
                'cancel': 'Abbrechen',
                'yes': 'Ja',
                'no': 'Nein',
                'unknown': 'Unbekannt',
                'seconds': 'Sekunden'
            }
        }
        
        self.current_language = 'en'
    
    def set_language(self, language_code):
        """Set current language"""
        if language_code in self.translations:
            self.current_language = language_code
        else:
            self.current_language = 'en'
    
    def get(self, key, *args):
        """Get translated text"""
        try:
            text = self.translations[self.current_language].get(key, key)
            if args:
                return text.format(*args)
            return text
        except:
            try:
                text = self.translations['en'].get(key, key)
                if args:
                    return text.format(*args)
                return text
            except:
                return key

translator = Translations()

def _(key, *args):
    """Translation shorthand"""
    return translator.get(key, *args)