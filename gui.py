#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern GUI for Cabrillo2ADIF Converter
Date: 2025-09-02 19:37:45
User: ertig3
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import webbrowser
import logging
from datetime import datetime
from pathlib import Path

from translations import translator, _
from cabrillo_parser import CabrilloParser
from adif_generator import ADIFGenerator

class ModernTheme:
    """Dark theme configuration"""
    
    DARK_BG = "#1e1e1e"
    DARK_FG = "#ffffff"
    ACCENT_BLUE = "#0078d4"
    ACCENT_GREEN = "#107c10"
    ACCENT_RED = "#d13438"
    ACCENT_ORANGE = "#ff8c00"
    
    PANEL_BG = "#2d2d30"
    INPUT_BG = "#3c3c3c"
    BUTTON_BG = "#404040"
    HOVER_BG = "#4a4a4a"
    
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#cccccc"
    TEXT_MUTED = "#999999"
    
    BORDER_COLOR = "#505050"

class Cabrillo2ADIFConverterGUI:
    """Main application GUI class"""
    
    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        self.theme = ModernTheme()
        
        self.root = tk.Tk()
        self.root.title(_('app_title') + " " + _('version'))
        self.root.configure(bg=self.theme.DARK_BG)
        
        geometry = self.settings.get('window_geometry', '1200x900')
        self.root.geometry(geometry)
        self.root.minsize(1000, 700)
        
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.status_text = tk.StringVar(value=_('status_ready'))
        self.qso_count = tk.StringVar(value="0 QSOs")
        
        self.default_output_dir = Path(settings.get_output_directory())
        
        self.setup_styling()
        self.setup_menu()
        self.setup_gui()
        
        self.logger.info("GUI initialized - ertig3")
        
    def setup_styling(self):
        """Configure dark theme styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('.',
                       background=self.theme.DARK_BG,
                       foreground=self.theme.TEXT_PRIMARY,
                       fieldbackground=self.theme.INPUT_BG,
                       bordercolor=self.theme.BORDER_COLOR)
        
        style.configure('Title.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       foreground=self.theme.ACCENT_BLUE,
                       background=self.theme.DARK_BG)
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12),
                       foreground=self.theme.TEXT_SECONDARY,
                       background=self.theme.DARK_BG)
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       foreground=self.theme.TEXT_PRIMARY,
                       background=self.theme.DARK_BG)
        
        style.configure('Modern.TButton',
                       font=('Segoe UI', 11),
                       foreground=self.theme.TEXT_PRIMARY,
                       background=self.theme.BUTTON_BG,
                       borderwidth=1,
                       focuscolor='none')
        
        style.map('Modern.TButton',
                 background=[('active', self.theme.HOVER_BG),
                            ('pressed', self.theme.ACCENT_BLUE)])
        
        style.configure('Accent.TButton',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.theme.TEXT_PRIMARY,
                       background=self.theme.ACCENT_BLUE,
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Accent.TButton',
                 background=[('active', '#106ebe'),
                            ('pressed', '#005a9e')])
        
        style.configure('Modern.TLabelframe',
                       background=self.theme.PANEL_BG,
                       bordercolor=self.theme.BORDER_COLOR,
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Modern.TLabelframe.Label',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.theme.ACCENT_BLUE,
                       background=self.theme.PANEL_BG)
        
        style.configure('Modern.TEntry',
                       font=('Consolas', 10),
                       foreground=self.theme.TEXT_PRIMARY,
                       fieldbackground=self.theme.INPUT_BG,
                       bordercolor=self.theme.BORDER_COLOR,
                       insertcolor=self.theme.TEXT_PRIMARY)
        
        style.configure('Modern.Horizontal.TProgressbar',
                       background=self.theme.ACCENT_BLUE,
                       troughcolor=self.theme.INPUT_BG,
                       borderwidth=0)
        
    def setup_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root, 
                         bg=self.theme.PANEL_BG,
                         fg=self.theme.TEXT_PRIMARY,
                         activebackground=self.theme.HOVER_BG)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0,
                           bg=self.theme.PANEL_BG,
                           fg=self.theme.TEXT_PRIMARY,
                           activebackground=self.theme.ACCENT_BLUE)
        menubar.add_cascade(label=_('menu_file'), menu=file_menu)
        file_menu.add_command(label=_('menu_open'), command=self.browse_input, accelerator="Ctrl+O")
        file_menu.add_command(label=_('menu_save'), command=self.browse_output, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label=_('menu_open_folder'), command=self.open_output_folder)
        file_menu.add_separator()
        file_menu.add_command(label=_('menu_exit'), command=self.root.quit, accelerator="Ctrl+Q")
        
        edit_menu = tk.Menu(menubar, tearoff=0,
                           bg=self.theme.PANEL_BG,
                           fg=self.theme.TEXT_PRIMARY,
                           activebackground=self.theme.ACCENT_BLUE)
        menubar.add_cascade(label=_('menu_edit'), menu=edit_menu)
        edit_menu.add_command(label=_('menu_clear'), command=self.clear_preview)
        edit_menu.add_command(label=_('menu_reset'), command=self.reset_all)
        
        tools_menu = tk.Menu(menubar, tearoff=0,
                            bg=self.theme.PANEL_BG,
                            fg=self.theme.TEXT_PRIMARY,
                            activebackground=self.theme.ACCENT_BLUE)
        menubar.add_cascade(label=_('menu_tools'), menu=tools_menu)
        
        language_menu = tk.Menu(tools_menu, tearoff=0,
                               bg=self.theme.PANEL_BG,
                               fg=self.theme.TEXT_PRIMARY,
                               activebackground=self.theme.ACCENT_BLUE)
        tools_menu.add_cascade(label=_('menu_language'), menu=language_menu)
        language_menu.add_command(label="English", command=lambda: self.change_language('en'))
        language_menu.add_command(label="Deutsch", command=lambda: self.change_language('de'))
        
        help_menu = tk.Menu(menubar, tearoff=0,
                           bg=self.theme.PANEL_BG,
                           fg=self.theme.TEXT_PRIMARY,
                           activebackground=self.theme.ACCENT_BLUE)
        menubar.add_cascade(label=_('menu_help'), menu=help_menu)
        help_menu.add_command(label=_('menu_about'), command=self.show_about)
        help_menu.add_command(label=_('menu_help_content'), command=self.show_help)
        
        self.root.bind('<Control-o>', lambda e: self.browse_input())
        self.root.bind('<Control-s>', lambda e: self.browse_output())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F1>', lambda e: self.show_help())
        
    def setup_gui(self):
        """Build main interface"""
        main_frame = tk.Frame(self.root, bg=self.theme.DARK_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_header(main_frame)
        self.create_file_section(main_frame) 
        self.create_conversion_section(main_frame)
        self.create_preview_section(main_frame)
        self.create_status_section(main_frame)
        
    def create_header(self, parent):
        """Application header"""
        header_frame = tk.Frame(parent, bg=self.theme.DARK_BG)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_frame = tk.Frame(header_frame, bg=self.theme.DARK_BG)
        title_frame.pack(side=tk.LEFT)
        
        title_label = ttk.Label(title_frame, text=_('app_title'), style='Title.TLabel')
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(title_frame, text=_('app_subtitle'), style='Subtitle.TLabel')
        subtitle_label.pack(anchor=tk.W)
        
        info_frame = tk.Frame(header_frame, bg=self.theme.DARK_BG)
        info_frame.pack(side=tk.RIGHT)
        
        version_label = tk.Label(info_frame, text=f"{_('version')} - Modern",
                                font=('Segoe UI', 10, 'bold'),
                                fg=self.theme.ACCENT_BLUE,
                                bg=self.theme.DARK_BG)
        version_label.pack(anchor=tk.E)
        
        time_label = tk.Label(info_frame, text="github.com/ertig3 | 2025-09-02 19:37:45 UTC",
                             font=('Segoe UI', 9),
                             fg=self.theme.ACCENT_BLUE,
                             bg=self.theme.DARK_BG,
                             cursor="hand2")
        time_label.pack(anchor=tk.E)
        time_label.bind("<Button-1>", lambda e: self.open_github())
        
    def open_github(self):
        """Open GitHub profile in browser"""
        try:
            webbrowser.open("https://github.com/ertig3")
        except Exception as e:
            self.logger.error(f"Error opening GitHub: {e}")
        
    def create_file_section(self, parent):
        """File selection section"""
        file_frame = ttk.LabelFrame(parent, text=_('files_section'), 
                                   style='Modern.TLabelframe', padding=20)
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        input_label = tk.Label(file_frame, text=_('input_file_label'),
                              font=('Segoe UI', 11, 'bold'),
                              fg=self.theme.TEXT_PRIMARY,
                              bg=self.theme.PANEL_BG)
        input_label.pack(anchor=tk.W, pady=(0, 8))
        
        input_container = tk.Frame(file_frame, bg=self.theme.PANEL_BG)
        input_container.pack(fill=tk.X, pady=(0, 20))
        
        self.input_entry = ttk.Entry(input_container, textvariable=self.input_file,
                                    style='Modern.TEntry', width=80)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        input_btn = ttk.Button(input_container, text=_('browse_button'),
                              command=self.browse_input, style='Modern.TButton',
                              width=12)
        input_btn.pack(side=tk.RIGHT)
        
        output_label = tk.Label(file_frame, text=_('output_file_label'),
                               font=('Segoe UI', 11, 'bold'),
                               fg=self.theme.TEXT_PRIMARY,
                               bg=self.theme.PANEL_BG)
        output_label.pack(anchor=tk.W, pady=(0, 8))
        
        output_container = tk.Frame(file_frame, bg=self.theme.PANEL_BG)
        output_container.pack(fill=tk.X)
        
        self.output_entry = ttk.Entry(output_container, textvariable=self.output_file,
                                     style='Modern.TEntry', width=80)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        output_btn = ttk.Button(output_container, text=_('save_as_button'),
                               command=self.browse_output, style='Modern.TButton',
                               width=12)
        output_btn.pack(side=tk.RIGHT)
        
    def create_conversion_section(self, parent):
        """Conversion control section"""
        conv_frame = ttk.LabelFrame(parent, text=_('conversion_section'),
                                   style='Modern.TLabelframe', padding=20)
        conv_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_container = tk.Frame(conv_frame, bg=self.theme.PANEL_BG)
        info_container.pack(fill=tk.X, pady=(0, 20))
        
        qso_frame = tk.Frame(info_container, bg=self.theme.PANEL_BG)
        qso_frame.pack(side=tk.LEFT)
        
        qso_label = tk.Label(qso_frame, text=_('qso_count'),
                            font=('Segoe UI', 10),
                            fg=self.theme.TEXT_SECONDARY,
                            bg=self.theme.PANEL_BG)
        qso_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.qso_display = tk.Label(qso_frame, textvariable=self.qso_count,
                                   font=('Segoe UI', 10, 'bold'),
                                   fg=self.theme.ACCENT_BLUE,
                                   bg=self.theme.PANEL_BG)
        self.qso_display.pack(side=tk.LEFT)
        
        status_frame = tk.Frame(info_container, bg=self.theme.PANEL_BG)
        status_frame.pack(side=tk.RIGHT)
        
        status_label = tk.Label(status_frame, text=_('status_label'),
                               font=('Segoe UI', 10),
                               fg=self.theme.TEXT_SECONDARY,
                               bg=self.theme.PANEL_BG)
        status_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.status_display = tk.Label(status_frame, text=_('status_ready'),
                                      font=('Segoe UI', 10, 'bold'),
                                      fg=self.theme.ACCENT_GREEN,
                                      bg=self.theme.PANEL_BG)
        self.status_display.pack(side=tk.LEFT)
        
        button_container = tk.Frame(conv_frame, bg=self.theme.PANEL_BG)
        button_container.pack(fill=tk.X, pady=(10, 0))
        
        self.convert_button = ttk.Button(button_container, text=_('convert_button'),
                                        command=self.start_conversion,
                                        style='Accent.TButton')
        self.convert_button.pack(pady=10, ipadx=30, ipady=8)
        
        self.progress = ttk.Progressbar(button_container, mode='indeterminate',
                                       style='Modern.Horizontal.TProgressbar',
                                       length=400)
        self.progress.pack(pady=(10, 0))
        
    def create_preview_section(self, parent):
        """Preview section"""
        preview_frame = ttk.LabelFrame(parent, text=_('preview_section'),
                                      style='Modern.TLabelframe', padding=15)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        toolbar = tk.Frame(preview_frame, bg=self.theme.PANEL_BG)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text=_('clear_button'), 
                  command=self.clear_preview, style='Modern.TButton',
                  width=12).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(toolbar, text=_('save_button'), 
                  command=self.save_preview, style='Modern.TButton',
                  width=12).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(toolbar, text=_('copy_button'), 
                  command=self.copy_preview, style='Modern.TButton',
                  width=12).pack(side=tk.LEFT)
        
        info_label = tk.Label(toolbar, text=_('preview_info'),
                             font=('Segoe UI', 9),
                             fg=self.theme.TEXT_MUTED,
                             bg=self.theme.PANEL_BG)
        info_label.pack(side=tk.RIGHT)
        
        text_container = tk.Frame(preview_frame, bg=self.theme.PANEL_BG)
        text_container.pack(fill=tk.BOTH, expand=True)
        
        self.preview_text = scrolledtext.ScrolledText(
            text_container,
            height=25,
            width=120,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg=self.theme.INPUT_BG,
            fg=self.theme.TEXT_PRIMARY,
            insertbackground=self.theme.TEXT_PRIMARY,
            selectbackground=self.theme.ACCENT_BLUE,
            selectforeground=self.theme.TEXT_PRIMARY,
            relief='flat',
            borderwidth=1
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        self.preview_text.vbar.configure(
            bg=self.theme.PANEL_BG,
            troughcolor=self.theme.INPUT_BG,
            activebackground=self.theme.HOVER_BG
        )
        
        self.show_welcome_text()
        
    def create_status_section(self, parent):
        """Status bar"""
        status_frame = tk.Frame(parent, bg=self.theme.DARK_BG, height=30)
        status_frame.pack(fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, textvariable=self.status_text,
                                    font=('Segoe UI', 10),
                                    fg=self.theme.TEXT_SECONDARY,
                                    bg=self.theme.DARK_BG)
        self.status_label.pack(side=tk.LEFT, pady=5)
        
        self.time_label = tk.Label(status_frame, text="",
                                  font=('Segoe UI', 9),
                                  fg=self.theme.TEXT_MUTED,
                                  bg=self.theme.DARK_BG)
        self.time_label.pack(side=tk.RIGHT, pady=5)
        
        self.update_timestamp()
        
    def show_welcome_text(self):
        """Display welcome information"""
        current_lang = self.settings.get('language', 'en')
        
        welcome_text = f"""{_('welcome_title')}
{'='*80}
{_('welcome_intro')}

{_('welcome_instructions')}
- {_('welcome_step1')}
- {_('welcome_step2')}
- {_('welcome_step3')}
- {_('welcome_step4')}

{_('welcome_features')}
- ADIF 3.1.4 output
- Modern dark theme
- Multi-language support
- Real-time preview
- Error handling

{_('welcome_bands')}
{_('bands_hf')}: 160M, 80M, 60M, 40M, 30M, 20M, 17M, 15M, 12M, 10M
{_('bands_vhf_uhf')}: 6M, 4M, 2M, 70CM, 23CM, 13CM, 9CM, 6CM, 3CM
LF: 2200M, 630M

{_('welcome_shortcuts')}
Ctrl+O: {_('menu_open')}
Ctrl+S: {_('menu_save')}
F1: {_('menu_help_content')}
Ctrl+Q: {_('menu_exit')}

SETTINGS:
Language: {current_lang.upper()}
Theme: Dark Modern
Output: {self.default_output_dir}
GitHub: github.com/ertig3 | 2025-09-02 19:37:45 UTC

{_('welcome_ready')}
{'='*80}
"""
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, welcome_text)
        
    def update_timestamp(self):
        """Update timestamp display"""
        current_time = datetime.utcnow().strftime("Updated: %Y-%m-%d %H:%M:%S UTC")
        self.time_label.config(text=current_time)
        self.root.after(30000, self.update_timestamp)
        
    def browse_input(self):
        """Select input Cabrillo file"""
        filename = filedialog.askopenfilename(
            title=_('select_cabrillo'),
            filetypes=[
                ("Cabrillo files", "*.cbr *.log *.txt"),
                ("Contest files", "*.cbr"),
                ("Log files", "*.log"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            initialdir=self.settings.get('last_input_dir', str(Path.home()))
        )
        
        if filename:
            self.input_file.set(filename)
            self.settings.set('last_input_dir', str(Path(filename).parent))
            
            base_name = Path(filename).stem
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            output_path = self.default_output_dir / f"{base_name}_converted_{timestamp}.adi"
            self.output_file.set(str(output_path))
            
            self.status_text.set(_('status_file_loaded') + f": {Path(filename).name}")
            self.status_display.config(text="File loaded", fg=self.theme.ACCENT_BLUE)
            self.preview_file_info()
            
            self.logger.info(f"Input file selected: {filename}")
            
    def browse_output(self):
        """Select output ADIF file"""
        initial_dir = self.settings.get('last_output_dir', str(self.default_output_dir))
        
        if self.input_file.get():
            base_name = Path(self.input_file.get()).stem
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            initial_filename = f"{base_name}_converted_{timestamp}.adi"
        else:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            initial_filename = f"cabrillo_converted_{timestamp}.adi"
            
        filename = filedialog.asksaveasfilename(
            title=_('save_adif'),
            filetypes=[
                ("ADIF files", "*.adi"),
                ("All files", "*.*")
            ],
            defaultextension=".adi",
            initialdir=initial_dir,
            initialfile=initial_filename
        )
        
        if filename:
            self.output_file.set(filename)
            self.settings.set('last_output_dir', str(Path(filename).parent))
            self.status_text.set(f"{_('save_adif')}: {Path(filename).name}")
            self.logger.info(f"Output file set: {filename}")
            
    def preview_file_info(self):
        """Preview Cabrillo file information"""
        if not self.input_file.get() or not Path(self.input_file.get()).exists():
            return
            
        try:
            file_path = Path(self.input_file.get())
            file_size = file_path.stat().st_size
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000)
                
            qso_lines = [line for line in content.split('\n') if line.strip().startswith('QSO:')]
            estimated_qsos = len(qso_lines)
            
            contest_lines = [line for line in content.split('\n') if line.strip().startswith('CONTEST:')]
            contest_name = contest_lines[0].split(':', 1)[1].strip() if contest_lines else _('unknown')
            
            callsign_lines = [line for line in content.split('\n') if line.strip().startswith('CALLSIGN:')]
            callsign = callsign_lines[0].split(':', 1)[1].strip() if callsign_lines else _('unknown')
            
            info_text = f"""FILE ANALYSIS - Cabrillo2ADIF Converter v0.9
{'='*80}
File: {file_path.name}
Path: {file_path}
Size: {file_size:,} bytes ({file_size/1024:.1f} KB)
Estimated QSOs: {estimated_qsos}
Contest: {contest_name}
Station: {callsign}
Analyzed: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
GitHub: github.com/ertig3

FILE CONTENT PREVIEW:
{'='*80}
{content}

{'='*80}
[Preview of first 2000 characters]

Ready for conversion!
"""
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, info_text)
            self.qso_count.set(f"~{estimated_qsos} QSOs")
            
        except Exception as e:
            error_text = f"""ERROR READING FILE
{'='*60}
Error: {str(e)}
File: {self.input_file.get()}
Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
GitHub: github.com/ertig3

Check file accessibility and format.
"""
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, error_text)
            self.logger.error(f"Error reading input file: {e}")
            
    def start_conversion(self):
        """Start conversion process"""
        if not self.input_file.get():
            messagebox.showerror(_('error_title'), _('error_no_input'))
            return
            
        if not Path(self.input_file.get()).exists():
            messagebox.showerror(_('error_title'), _('error_file_not_found'))
            return
            
        if not self.output_file.get():
            messagebox.showerror(_('error_title'), _('error_no_output'))
            return
        
        self.convert_file()
        
    def convert_file(self):
        """Perform file conversion"""
        self.progress.start(10)
        self.convert_button.config(state='disabled', text=_('converting_button'))
        self.status_text.set(_('status_converting'))
        self.status_display.config(text="Converting...", fg=self.theme.ACCENT_ORANGE)
        self.root.update()
        
        start_time = datetime.utcnow()
        
        try:
            log_text = f"""{_('conversion_started')} - Cabrillo2ADIF Converter v0.9
{'='*80}
Start: {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}
Input: {Path(self.input_file.get()).name}
Output: {Path(self.output_file.get()).name}
GitHub: github.com/ertig3

"""
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, log_text)
            self.root.update()
            
            self.status_text.set(_('parsing_cabrillo'))
            self.root.update()
            
            parser = CabrilloParser()
            qsos = parser.parse_file(self.input_file.get())
            contest_info = parser.get_contest_info()
            
            log_text += f"[1/3] {len(qsos)} QSOs parsed successfully\n"
            if contest_info:
                log_text += f"Contest: {contest_info.get('contest', _('unknown'))}\n"
                log_text += f"Station: {contest_info.get('callsign', _('unknown'))}\n"
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, log_text)
            self.root.update()
            
            if len(qsos) == 0:
                raise Exception(_('error_no_qsos'))
            
            self.qso_count.set(f"{len(qsos)} QSOs")
            
            self.status_text.set(_('generating_adif'))
            self.root.update()
            
            generator = ADIFGenerator()
            adif_content = generator.generate(qsos, contest_info)
            
            stats = generator.get_conversion_stats()
            
            log_text += f"[2/3] ADIF 3.1.4 format generated ({len(adif_content)} characters)\n"
            log_text += f"QSOs processed: {stats.get('total_qsos', len(qsos))}\n"
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, log_text)
            self.root.update()
            
            self.status_text.set(_('saving_file'))
            self.root.update()
            
            output_path = Path(self.output_file.get())
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(adif_content)
            
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            log_text += f"[3/3] ADIF file saved: {output_path.name}\n\n"
            log_text += f"{_('conversion_completed')}!\n"
            log_text += f"{_('duration')}: {duration:.2f} {_('seconds')}\n"
            log_text += f"Output size: {len(adif_content):,} characters\n"
            log_text += f"GitHub: github.com/ertig3\n\n"
            
            log_text += f"{_('adif_preview')}:\n"
            log_text += "="*80 + "\n"
            log_text += adif_content[:2000]
            if len(adif_content) > 2000:
                log_text += f"\n\n[...{len(adif_content)-2000} more characters...]\n"
            log_text += "\n" + "="*80
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, log_text)
            
            self.status_text.set(_('status_success'))
            self.status_display.config(text="Success!", fg=self.theme.ACCENT_GREEN)
            self.progress.stop()
            self.convert_button.config(state='normal', text=_('convert_button'))
            
            messagebox.showinfo(_('success_title'), 
                              f"{_('success_conversion')}\n\n"
                              f"QSOs: {len(qsos)}\n"
                              f"Duration: {duration:.2f}s\n"
                              f"File: {output_path.name}")
            
            self.logger.info(f"Conversion completed - {len(qsos)} QSOs")
            
        except Exception as e:
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            error_text = f"""CONVERSION ERROR
{'='*60}
Error: {str(e)}
Time: {end_time.strftime('%Y-%m-%d %H:%M:%S UTC')}
Duration: {duration:.2f} seconds
GitHub: github.com/ertig3

Input File: {self.input_file.get()}
Output File: {self.output_file.get()}

Check file format and permissions.
"""
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, error_text)
            
            self.status_text.set(_('status_error'))
            self.status_display.config(text="Error!", fg=self.theme.ACCENT_RED)
            self.progress.stop()
            self.convert_button.config(state='normal', text=_('convert_button'))
            
            messagebox.showerror(_('error_title'), f"{_('error_conversion')}\n\n{str(e)}")
            self.logger.error(f"Conversion failed: {e}")
    
    def clear_preview(self):
        """Clear preview area"""
        self.show_welcome_text()
        self.status_text.set(_('status_cleared'))
        self.status_display.config(text=_('status_ready'), fg=self.theme.ACCENT_GREEN)
        self.qso_count.set("0 QSOs")
        self.logger.info("Preview cleared")
    
    def reset_all(self):
        """Reset all input fields"""
        self.input_file.set("")
        self.output_file.set("")
        self.show_welcome_text()
        self.status_text.set(_('status_reset'))
        self.status_display.config(text=_('status_ready'), fg=self.theme.ACCENT_GREEN)
        self.qso_count.set("0 QSOs")
        self.logger.info("All fields reset")
    
    def save_preview(self):
        """Save preview content to file"""
        try:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            default_filename = f"conversion_log_{timestamp}.txt"
            
            filename = filedialog.asksaveasfilename(
                title=_('save_log'),
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialdir=str(self.default_output_dir),
                initialfile=default_filename
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.preview_text.get(1.0, tk.END))
                
                self.status_text.set(_('success_saved'))
                messagebox.showinfo(_('success_title'), f"{_('success_saved')}")
                self.logger.info(f"Preview saved: {filename}")
        except Exception as e:
            messagebox.showerror(_('error_title'), f"Error saving file: {e}")
            self.logger.error(f"Error saving preview: {e}")
    
    def copy_preview(self):
        """Copy preview content to clipboard"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.preview_text.get(1.0, tk.END))
            self.root.update()
            
            self.status_text.set(_('success_copied'))
            messagebox.showinfo(_('success_title'), f"{_('success_copied')}")
            self.logger.info("Preview copied to clipboard")
        except Exception as e:
            messagebox.showerror(_('error_title'), f"Error copying to clipboard: {e}")
            self.logger.error(f"Error copying preview: {e}")
    
    def open_output_folder(self):
        """Open output directory"""
        try:
            output_dir = self.default_output_dir
            if self.output_file.get():
                output_dir = Path(self.output_file.get()).parent
            
            if sys.platform == "win32":
                os.startfile(output_dir)
            elif sys.platform == "darwin":
                os.system(f"open '{output_dir}'")
            else:
                os.system(f"xdg-open '{output_dir}'")
                
            self.logger.info(f"Output folder opened: {output_dir}")
        except Exception as e:
            messagebox.showerror(_('error_title'), f"Error opening folder: {e}")
            self.logger.error(f"Error opening output folder: {e}")
    
    def change_language(self, language_code):
        """Change application language"""
        self.settings.set('language', language_code)
        translator.set_language(language_code)
        
        self.root.title(_('app_title') + " " + _('version'))
        
        messagebox.showinfo(
            _('info_title'),
            "Language changed! Some elements update immediately.\n"
            "For complete change, restart the application."
        )
        
        self.show_welcome_text()
        self.logger.info(f"Language changed to: {language_code}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = f"""{_('about_title')}

{_('about_version')} - Modern Edition
{_('about_created')}
{_('about_purpose')}

GitHub: github.com/ertig3
Date: 2025-09-02 19:37:45 UTC

FEATURES:
- ADIF 3.1.4 output
- Multi-language support
- Modern dark theme
- Real-time preview
- Error handling

SUPPORTED FORMATS:
- Input: Cabrillo (.cbr, .log, .txt)
- Output: ADIF 3.1.4 (.adi)

SUPPORTED BANDS:
- HF: 160M-10M
- VHF/UHF: 6M-3CM
- LF: 2200M-630M

For amateur radio community
"""
        messagebox.showinfo(_('about_title'), about_text)
    
    def show_help(self):
        """Show help dialog"""
        help_text = f"""{_('help_title')}

{_('help_quickstart')}
1. Select Cabrillo file
2. Choose ADIF output location
3. Click START CONVERSION
4. Review results

{_('help_formats')}
- Cabrillo: .cbr, .log, .txt
- ADIF: .adi (version 3.1.4)

{_('help_features')}
- File selection
- Live preview
- Multi-language
- Dark theme
- Error handling

TROUBLESHOOTING:
- Check file format
- Verify permissions
- Use test file
- Check error messages
- Ensure disk space

GitHub: github.com/ertig3 | {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
        messagebox.showinfo(_('help_title'), help_text)
    
    def run(self):
        """Start the application"""
        self.logger.info("Starting Cabrillo2ADIF GUI v0.9")
        self.root.mainloop()
        
        try:
            geometry = self.root.geometry()
            self.settings.set('window_geometry', geometry)
            self.logger.info(f"Window geometry saved: {geometry}")
        except:
            pass