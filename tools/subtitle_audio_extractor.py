# -*- coding: utf-8 -*-
"""
Breaking Bad Subtitle Audio Extractor v2.0
功能和 v1.0 相同, 但添加了预览和合并导出功能
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os, re, subprocess, json, sys, tempfile, threading
from datetime import datetime

class Tool:
    def __init__(self, root):
        self.root = root
        self.root.title("Breaking Bad Subtitle Audio Extractor v2.0")
        self.root.geometry("1100x800")
        self.subtitle_files, self.search_results, self.ffmpeg_path = [], [], self._find_ffmpeg()
        self.recent_outputs, self.playing_item, self.temp_files = [], None, []
        self._build_ui()
        self._load_last_session()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        cfg = ttk.LabelFrame(self.root, text=" Config ", padding=8)
        cfg.pack(fill='x', padx=10, pady=(10, 5))
        ttk.Label(cfg, text="FFmpeg:").grid(row=0, column=0, sticky='w', padx=5)
        self.ffmpeg_entry = ttk.Entry(cfg, width=55)
        self.ffmpeg_entry.insert(0, self.ffmpeg_path or "")
        self.ffmpeg_entry.grid(row=0, column=1, padx=5, sticky='ew')
        ttk.Button(cfg, text="Browse", command=self._browse_ffmpeg, width=6).grid(row=0, column=2, padx=2)
        ttk.Button(cfg, text="Auto Find", command=self._auto_find_ffmpeg, width=8).grid(row=0, column=3, padx=2)
        ttk.Label(cfg, text="Subtitle Dir:").grid(row=1, column=0, sticky='w', padx=5, pady=(5,0))
        self.subtitle_dir_entry = ttk.Entry(cfg, width=55)
        self.subtitle_dir_entry.insert(0, r"E:\moive\Breaking Bad 01")
        self.subtitle_dir_entry.grid(row=1, column=1, padx=5, pady=(5,0), sticky='ew')
        ttk.Button(cfg, text="Browse", command=self._browse_subtitle_dir, width=6).grid(row=1, column=2, pady=(5,0))
        ttk.Label(cfg, text="Video Dir:").grid(row=2, column=0, sticky='w', padx=5, pady=(5,0))
        self.video_dir_entry = ttk.Entry(cfg, width=55)
        self.video_dir_entry.insert(0, r"E:\moive\Breaking Bad 01")
        self.video_dir_entry.grid(row=2, column=1, padx=5, pady=(5,0), sticky='ew')
        ttk.Button(cfg, text="Browse", command=self._browse_video_dir, width=6).grid(row=2, column=2, pady=(5,0))
        ttk.Label(cfg, text="Output Dir:").grid(row=3, column=0, sticky='w', padx=5, pady=(5,0))
        self.output_dir_entry = ttk.Entry(cfg, width=55)
        self.output_dir_entry.insert(0, r"D:\EnglishPracticeMiniProgram\assets\audio\breaking_bad\clips")
        self.output_dir_entry.grid(row=3, column=1, padx=5, pady=(5,0), sticky='ew')
        ttk.Button(cfg, text="Browse", command=self._browse_output_dir, width=6).grid(row=3, column=2, pady=(5,0))
        ttk.Button(cfg, text="Load Subtitles", command=self._load_subtitles, width=12, style='Accent.TButton').grid(row=3, column=3, padx=2, pady=(5,0))
        cfg.columnconfigure(1, weight=1)
        sf = ttk.LabelFrame(self.root, text=" Search ", padding=8)
        sf.pack(fill='x', padx=10, pady=5)
        ttk.Label(sf, text="Quick:").grid(row=0, column=0, sticky='w', padx=5)
        scenes = [("Greeting", "hello|hi|hey|yo|how are you|nice to meet|goodbye|bye|later"),
            ("Directions", "where|turn|left|right|straight|corner|block|street|address|direction|lost"),
            ("Restaurant", "order|menu|food|eat|steak|chicken|drink|waiter|delicious|table|beer"),
            ("Hospital", "doctor|hospital|sick|medicine|prescription|cancer|nurse|health"),
            ("Family", "family|wife|son|home|love|dinner|birthday|kids|children"),
            ("Negotiation", "deal|money|business|price|agreement|partner|offer|contract|pay"),
            ("Chemistry", "chemistry|hydrogen|oxygen|carbon|element|percent|science|formula|lab"),
            ("Emotion", "love|hate|happy|sad|angry|scared|worried|excited|proud|sorry"),
            ("Question", "what|why|how|where|who|when|can you|could you|would you"),
            ("Insurance", "insurance|HMO|deposit|pension|money|bank|afford")]
        for i, (n, k) in enumerate(scenes):
            ttk.Button(sf, text=n, width=8, command=lambda n=n, k=k: self._quick_search(n, k)).grid(row=0, column=1+i, padx=1)
        ttk.Label(sf, text="Keyword:").grid(row=1, column=0, sticky='w', padx=5, pady=(8,0))
        self.search_entry = ttk.Entry(sf, width=65, font=('Consolas', 11))
        self.search_entry.grid(row=1, column=1, columnspan=7, padx=5, pady=(8,0), sticky='ew')
        self.search_entry.bind('<Return>', lambda e: self._do_search())
        ttk.Button(sf, text="  Search  ", command=self._do_search, width=10).grid(row=1, column=8, padx=5, pady=(8,0))
        ttk.Button(sf, text="  Clear  ", command=self._clear_results, width=10).grid(row=1, column=9, pady=(8,0))
        sf.columnconfigure(1, weight=1)
        cf = ttk.Frame(self.root)
        cf.pack(fill='both', expand=True, padx=10, pady=5)
        left = ttk.LabelFrame(cf, text=" Results ", padding=5)
        left.pack(side='left', fill='both', expand=True)
        self.stats_label = ttk.Label(left, text="0 results | 0 selected", font=('Microsoft YaHei', 9), foreground='#555')
        self.stats_label.pack(anchor='w', padx=5, pady=(0,3))
        cols = ('play', 'check', 'episode', 'start', 'dur', 'text')
        self.tree = ttk.Treeview(left, columns=cols, show='headings', height=18, selectmode='extended')
        for h, w in [('play', 50), ('check', 30), ('episode', 80), ('start', 70), ('dur', 50), ('text', 1)]:
            self.tree.heading(h, text=h.capitalize())
            self.tree.column(h, width=w, anchor='center' if h != 'text' else 'w')
        vsb = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)
        self.tree.bind('<Button-1>', self._on_tree_click)
        self.tree.bind('<Double-Button-1>', self._on_tree_double_click)
        bf = ttk.Frame(left)
        bf.pack(fill='x', pady=5)
        ttk.Button(bf, text=" Select All ", command=self._select_all).pack(side='left', padx=2)
        ttk.Button(bf, text=" Deselect ", command=self._deselect_all).pack(side='left', padx=2)
        ttk.Button(bf, text=" Invert ", command=self._invert_selection).pack(side='left', padx=2)
        right = ttk.LabelFrame(cf, text=" Extract Settings ", padding=10, width=350)
        right.pack(side='right', fill='both', padx=(10, 0))
        right.pack_propagate(False)
        ttk.Label(right, text="Clip Mode:", font=('', 10, 'bold')).pack(anchor='w')
        self.clip_mode = tk.StringVar(value='expand')
        for v, t in [('sentence', 'Sentence only'), ('expand', 'Expand (N sec)'), ('fixed', 'Fixed length')]:
            ttk.Radiobutton(right, text=t, variable=self.clip_mode, value=v).pack(anchor='w', padx=15)
        ef = ttk.Frame(right); ef.pack(fill='x', pady=3)
        ttk.Label(ef, text="Expand (sec):").pack(side='left')
        self.expand_secs = tk.IntVar(value=2)
        ttk.Spinbox(ef, from_=0, to=30, width=5, textvariable=self.expand_secs).pack(side='left', padx=5)
        ff = ttk.Frame(right); ff.pack(fill='x', pady=3)
        ttk.Label(ff, text="Fixed (sec):").pack(side='left')
        self.fixed_secs = tk.IntVar(value=10)
        ttk.Spinbox(ff, from_=1, to=300, width=5, textvariable=self.fixed_secs).pack(side='left', padx=5)
        ttk.Separator(right, orient='horizontal').pack(fill='x', pady=8)
        ttk.Label(right, text="Filename Template:", font=('', 10, 'bold')).pack(anchor='w')
        self.filename_entry = ttk.Entry(right, font=('Consolas', 10))
        self.filename_entry.insert(0, "{index:03d}_{episode}_{timestamp}")
        self.filename_entry.pack(fill='x', pady=3)
        ttk.Separator(right, orient='horizontal').pack(fill='x', pady=8)
        ttk.Label(right, text="Audio Settings:", font=('', 10, 'bold')).pack(anchor='w')
        br_f = ttk.Frame(right); br_f.pack(fill='x')
        ttk.Label(br_f, text="Bitrate:").pack(side='left')
        self.bitrate_var = tk.StringVar(value='64k')
        for br in ['32k', '48k', '64k', '96k', '128k']:
            ttk.Radiobutton(br_f, text=br, variable=self.bitrate_var, value=br).pack(side='left', padx=3)
        ttk.Checkbutton(right, text="Mono (voice optimized)", variable=tk.BooleanVar(value=True)).pack(anchor='w', pady=2)
        ttk.Separator(right, orient='horizontal').pack(fill='x', pady=8)
        ttk.Label(right, text="Preview:", font=('', 10, 'bold')).pack(anchor='w')
        self.preview_text = scrolledtext.ScrolledText(right, height=6, font=('Consolas', 9), wrap='word', relief='solid', borderwidth=1)
        self.preview_text.pack(fill='both', expand=True, pady=3)
        self.preview_text.config(state='disabled')
        self.extract_btn = ttk.Button(right, text="  Extract Selected  ", command=self._extract_selected, style='Accent.TButton')
        self.extract_btn.pack(fill='x', pady=(5, 2))
        mf = ttk.Frame(right); mf.pack(fill='x', pady=2)
        self.merge_name_entry = ttk.Entry(mf, font=('Consolas', 10))
        self.merge_name_entry.insert(0, "merged_output")
        self.merge_name_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        ttk.Button(mf, text="  Merge Export  ", command=self._merge_export, width=12).pack(side='left')
        ttk.Button(right, text="  Batch Extract All  ", command=self._extract_all).pack(fill='x', pady=2)
        self.status_bar = ttk.Label(self.root, text="Ready", relief='sunken', anchor='w', font=('Microsoft YaHei', 9))
        self.status_bar.pack(fill='x', padx=10, pady=(0, 5))
        self.play_indicator = ttk.Label(self.status_bar, text="", foreground='#228B22')
        self.play_indicator.pack(side='right', padx=10)

    def _find_ffmpeg(self):
        for p in [r'D:\tools\ffmpeg\bin\ffmpeg.exe', r'C:\tools\ffmpeg\bin\ffmpeg.exe', r'C:\ffmpeg\bin\ffmpeg.exe', r'D:\ffmpeg\bin\ffmpeg.exe']:
            if os.path.exists(p): return p
        try:
            r = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True, timeout=5, shell=True)
            if r.returncode == 0: return r.stdout.strip().split('\n')[0]
        except: pass
        return ''
    def _auto_find_ffmpeg(self):
        p = self._find_ffmpeg()
        if p:
            self.ffmpeg_entry.delete(0, tk.END); self.ffmpeg_entry.insert(0, p); self.ffmpeg_path = p
            self._set_status(f"FFmpeg found: {p}")
        else:
            messagebox.showwarning("FFmpeg not found", "Download from https://ffmpeg.org"); self._set_status("FFmpeg not found")
    def _browse_ffmpeg(self):
        p = filedialog.askopenfilename(title="Select FFmpeg", filetypes=[("FFmpeg", "ffmpeg.exe"), ("All", "*.*")])
        if p: self.ffmpeg_entry.delete(0, tk.END); self.ffmpeg_entry.insert(0, p); self.ffmpeg_path = p
    def _browse_subtitle_dir(self):
        p = filedialog.askdirectory(title="Select Subtitle Directory")
        if p: self.subtitle_dir_entry.delete(0, tk.END); self.subtitle_dir_entry.insert(0, p)
    def _browse_video_dir(self):
        p = filedialog.askdirectory(title="Select Video Directory")
        if p: self.video_dir_entry.delete(0, tk.END); self.video_dir_entry.insert(0, p)
    def _browse_output_dir(self):
        p = filedialog.askdirectory(title="Select Output Directory")
        if p: self.output_dir_entry.delete(0, tk.END); self.output_dir_entry.insert(0, p)
    def _load_subtitles(self):
        srt_dir = self.subtitle_dir_entry.get().strip()
        video_dir = self.video_dir_entry.get().strip()
        if not os.path.isdir(srt_dir): messagebox.showerror("Error", f"Subtitle dir not exist:\n{srt_dir}"); return
        self.subtitle_files = []
        srt_files = sorted([f for f in os.listdir(srt_dir) if f.lower().endswith('.srt')])
        if not srt_files: messagebox.showwarning("No subtitles", f"No .srt files:\n{srt_dir}"); return
        for srt_file in srt_files:
            srt_path = os.path.join(srt_dir, srt_file)
            base_name = os.path.splitext(srt_file)[0]
            ep = re.sub(r' 720p\.BRrip\.Sujaidr|720p|BRrip|Sujaidr', '', base_name).replace('Breaking Bad', '').strip()
            if 's01e' in ep.lower():
                parts = re.split(r'[sSeE]', ep)
                if len(parts) >= 2: ep = f"S{parts[1].zfill(2)}E{parts[2].zfill(2) if len(parts) > 2 else '01'}"
            video_path = None
            for ext in ['.mkv', '.mp4', '.avi', '.mov']:
                cp = os.path.join(video_dir, base_name + ext)
                if os.path.exists(cp): video_path = cp; break
            self.subtitle_files.append((srt_path, video_path, ep, base_name))
        with_video = sum(1 for f in self.subtitle_files if f[1])
        self._set_status(f"Loaded {len(self.subtitle_files)} subtitles, {with_video} with video"); self._do_search()
    def _parse_srt(self, srt_path):
        entries = []
        for enc in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
            try:
                with open(srt_path, 'r', encoding=enc) as f: content = f.read(); break
            except: continue
        for block in re.split(r'\n\s*\n', content):
            lines = block.strip().split('\n')
            if len(lines) < 2: continue
            idx = -1
            for i, ln in enumerate(lines):
                if '-->' in ln: idx = i; break
            if idx == -1: continue
            try:
                ts = lines[idx]; ss, es = ts.split('-->')
                ss = ss.strip().replace(',', '.'); es = es.strip().replace(',', '.')
                text = ' '.join(lines[idx+1:]).strip()
                if not text: continue
                entries.append({'start': self._parse_time(ss), 'end': self._parse_time(es), 'text': text, 'srt_path': srt_path})
            except: continue
        return entries
    def _parse_time(self, s):
        try:
            p = s.strip().split(':'); h, m, sec = p; sec, ms = (sec.split('.') if '.' in sec else (sec, '0'))[:2]
            return int(h)*3600 + int(m)*60 + int(sec) + int(ms.ljust(3, '0')[:3])/1000
        except: return 0
    def _format_time(self, sec):
        h = int(sec // 3600); m = int((sec % 3600) // 60); s = int(sec % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    def _quick_search(self, name, kw):
        self.search_entry.delete(0, tk.END); self.search_entry.insert(0, kw)
        self._set_status(f"Quick search: {name}"); self._do_search()
    def _do_search(self):
        kw = self.search_entry.get().strip()
        if not kw: return
        if not self.subtitle_files: self._load_subtitles()
        if not self.subtitle_files: return
        self.search_results = []
        try: pat = re.compile(kw, re.IGNORECASE)
        except re.error as e: messagebox.showerror("Regex Error", f"Invalid keyword:\n{e}"); return
        for srt_path, video_path, ep, base_name in self.subtitle_files:
            for entry in self._parse_srt(srt_path):
                if pat.search(entry['text']):
                    r = entry.copy(); r['episode'] = ep; r['video_path'] = video_path; r['base_name'] = base_name; r['selected'] = False
                    self.search_results.append(r)
        self.search_results.sort(key=lambda x: (x.get('srt_path', ''), x['start']))
        self._render_tree(); self._set_status(f"Found {len(self.search_results)} results")
    def _render_tree(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for i, r in enumerate(self.search_results):
            dur = r['end'] - r['start']
            chk = '[x]' if r['selected'] else '[ ]'
            play_btn = '||' if self.playing_item == i else '>'
            self.tree.insert('', 'end', iid=i, values=(play_btn, chk, r['episode'], self._format_time(r['start']), f"{dur:.1f}s", r['text'][:80] + ('...' if len(r['text']) > 80 else '')))
            if r['selected']: self.tree.selection_add(i)
        self._update_stats()
    def _on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == 'cell':
            col = self.tree.identify_column(event.x); iid = self.tree.identify_row(event.y)
            if iid:
                idx = int(iid)
                if col == '#1': self._preview_clip(idx)
                elif col == '#2':
                    self.search_results[idx]['selected'] = not self.search_results[idx]['selected']
                    self._render_tree(); self._update_preview()
    def _on_tree_double_click(self, event):
        iid = self.tree.identify_row(event.y)
        if iid: self._preview_clip(int(iid))
    def _on_tree_select(self, event=None):
        sel = set(int(i) for i in self.tree.selection())
        for i, r in enumerate(self.search_results):
            if r['selected'] != (i in sel):
                r['selected'] = (i in sel); self._render_tree(); break
        self._update_preview(); self._update_stats()
    def _update_stats(self):
        total = len(self.search_results); sel = sum(1 for r in self.search_results if r['selected'])
        self.stats_label.config(text=f"{total} results | {sel} selected")
        self.extract_btn.config(text=f"  Extract ({sel})  " if sel else "  Extract Selected  ")
    def _update_preview(self):
        sel = [r for r in self.search_results if r['selected']]
        self.preview_text.config(state='normal'); self.preview_text.delete('1.0', tk.END)
        if not sel: self.preview_text.insert('1.0', "(Click > to preview, [] to select)")
        else:
            total_dur = 0
            for i, r in enumerate(sel[:20], 1):
                cs, ce = self._get_clip_range(r); cd = ce - cs; total_dur += cd
                self.preview_text.insert(tk.END, f"[{i}] {r['episode']} @ {self._format_time(r['start'])} ({cd:.1f}s)\n{chr(32)*4}{r['text']}\n\n")
            if len(sel) > 20: self.preview_text.insert(tk.END, f"... {len(sel)-20} more\n")
            self.preview_text.insert(tk.END, f"\nTotal: {len(sel)} clips, ~{total_dur:.0f} sec")
        self.preview_text.config(state='disabled')
    def _select_all(self):
        for r in self.search_results: r['selected'] = True
        self._render_tree(); self._update_preview()
    def _deselect_all(self):
        for r in self.search_results: r['selected'] = False
        self._render_tree(); self._update_preview()
    def _invert_selection(self):
        for r in self.search_results: r['selected'] = not r['selected']
        self._render_tree(); self._update_preview()
    def _clear_results(self):
        self.search_results = []; self._render_tree()
        self.preview_text.config(state='normal'); self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', "(Click > to preview, [] to select)"); self.preview_text.config(state='disabled')
        self._update_stats()
    def _get_clip_range(self, result):
        mode = self.clip_mode.get(); start, end = result['start'], result['end']
        if mode == 'expand':
            exp = self.expand_secs.get(); start = max(0, start - exp); end = end + exp
        elif mode == 'fixed':
            f = self.fixed_secs.get(); mid = (start + end) / 2; start = max(0, mid - f/2); end = mid + f/2
        return start, end
# ---- Preview ----
    def _preview_clip(self, idx):
        if idx < 0 or idx >= len(self.search_results): return
        r = self.search_results[idx]
        if not r.get('video_path') or not os.path.exists(r['video_path']):
            messagebox.showwarning('No video', 'No corresponding video file'); return
        ffmpeg = self.ffmpeg_entry.get().strip()
        if not ffmpeg or not os.path.exists(ffmpeg): messagebox.showerror('Error', 'FFmpeg not configured'); return
        if self.playing_item == idx: self._stop_preview(); return
        self._stop_preview()
        start, end = self._get_clip_range(r)
        preview_dur = min(5, max(0.5, end - start))
        temp_dir = tempfile.gettempdir()
        temp_mp3 = os.path.join(temp_dir, 'preview_' + str(idx) + '.mp3')
        cmd = '"' + ffmpeg + '" -i "' + r["video_path"] + '" -ss ' + str(start) + ' -t ' + str(preview_dur) + ' -vn -ar 22050 -b:a 32k -ac 1 -y "' + temp_mp3 + '"'
        self._set_status('Generating preview...')
        def do_extract():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, shell=True)
                if result.returncode == 0 and os.path.exists(temp_mp3):
                    self.root.after(0, lambda: self._play_preview(idx, temp_mp3))
                else:
                    self.root.after(0, lambda: messagebox.showerror('Preview failed', 'Cannot extract audio'))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror('Preview failed', str(e)))
        threading.Thread(target=do_extract, daemon=True).start()

    def _play_preview(self, idx, mp3_path):
        self.playing_item = idx; self._render_tree()
        txt = self.search_results[idx]['text'][:30]
        self.play_indicator.config(text='Playing: ' + txt + '...')
        self.temp_files.append(mp3_path)
        try:
            os.startfile(mp3_path)
            self._set_status('Preview playing (5 sec)')
            def reset():
                import time; time.sleep(6); self.root.after(0, self._reset_play_indicator)
            threading.Thread(target=reset, daemon=True).start()
        except Exception as e:
            messagebox.showerror('Playback failed', str(e)); self._reset_play_indicator()

    def _stop_preview(self):
        if self.playing_item is not None: self.playing_item = None; self._reset_play_indicator()

    def _reset_play_indicator(self):
        self.playing_item = None; self.play_indicator.config(text=''); self._render_tree(); self._set_status('Ready')

    # ---- Extract ----
    def _extract_selected(self):
        sel = [r for r in self.search_results if r['selected']]
        if not sel: messagebox.showinfo('Tip', 'Select clips first'); return
        self._extract_clips(sel)

    def _extract_all(self):
        if not self.search_results: messagebox.showwarning('No results', 'Nothing to extract'); return
        if messagebox.askyesno('Confirm', 'Extract all ' + str(len(self.search_results)) + ' clips?'): self._extract_clips(self.search_results)

    def _extract_clips(self, clips):
        ffmpeg = self.ffmpeg_entry.get().strip()
        out_dir = self.output_dir_entry.get().strip()
        template = self.filename_entry.get().strip() or '{index:03d}'
        bitrate = self.bitrate_var.get()
        if not ffmpeg or not os.path.exists(ffmpeg): messagebox.showerror('Error', 'FFmpeg not found'); return
        if not out_dir: messagebox.showwarning('Error', 'Specify output directory'); return
        try: os.makedirs(out_dir, exist_ok=True)
        except Exception as e: messagebox.showerror('Error', 'Cannot create output dir: ' + str(e)); return
        grouped = {}
        for clip in clips:
            vp = clip.get('video_path') or ''
            if vp not in grouped: grouped[vp] = []
            grouped[vp].append(clip)
        total = len(clips); completed = 0; errors = 0
        pw = tk.Toplevel(self.root); pw.title('Extract Progress'); pw.geometry('580x220'); pw.transient(self.root); pw.grab_set()
        ttk.Label(pw, text='Extracting 0/' + str(total) + '...', font=('', 11)).pack(pady=8)
        pbar = ttk.Progressbar(pw, length=480, mode='determinate'); pbar.pack(pady=5)
        log_t = scrolledtext.ScrolledText(pw, height=7, font=('Consolas', 9)); log_t.pack(fill='both', expand=True, padx=10, pady=(0, 5))
        def log(msg): log_t.insert(tk.END, msg + '\n'); log_t.see(tk.END); pw.update()
        def do_work():
            nonlocal completed, errors
            for video_path, vclips in grouped.items():
                if not video_path or not os.path.exists(video_path):
                    for c in vclips:
                        self.root.after(0, lambda c=c: log('SKIP: ' + c['text'][:50])); completed += 1; self.root.after(0, lambda: pbar.config(value=completed/float(total)*100))
                    continue
                for c in vclips:
                    start, end = self._get_clip_range(c); dur = end - start
                    if dur < 1.0:
                        self.root.after(0, lambda c=c: log('SKIP (short): ' + c['text'][:40])); completed += 1; self.root.after(0, lambda: pbar.config(value=completed/float(total)*100)); continue
                    ts = self._format_time(c['start']).replace(':', ''); txt_clean = re.sub(r'[^\w\s]', '', c['text'])[:15].strip().replace(' ', '_')
                    ep = c.get('episode', 'S00').replace(' ', '')
                    filename = template.replace('{index}', str(completed+1).zfill(3)).replace('{episode}', ep).replace('{timestamp}', ts).replace('{text}', txt_clean)
                    filename = re.sub(r'[<>:"/\\|?*]', '_', filename) + '.mp3'
                    out_path = os.path.join(out_dir, filename)
                    self.root.after(0, lambda fn=filename: log('[' + str(completed+1) + '/' + str(total) + '] ' + fn))
                    try:
                        cmd = '"' + ffmpeg + '" -i "' + video_path + '" -ss ' + str(start) + ' -t ' + str(dur) + ' -vn -ar 44100 -b:a ' + bitrate + ' -ac 1 -y "' + out_path + '"'
                        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120, shell=True)
                        if res.returncode == 0 and os.path.exists(out_path):
                            sz = os.path.getsize(out_path) / 1024; self.root.after(0, lambda s=sz, e=ep, t=self._format_time(c['start']): log('   OK ' + str(int(s)) + 'KB | ' + e + ' ' + t))
                        else:
                            err = (res.stderr or 'unknown')[-80:]; self.root.after(0, lambda e=err: log('   FAIL: ' + e[-60:])); errors += 1
                    except subprocess.TimeoutExpired: self.root.after(0, lambda: log('   TIMEOUT')); errors += 1
                    except Exception as e: self.root.after(0, lambda e=str(e): log('   ERROR: ' + e)); errors += 1
                    completed += 1; self.root.after(0, lambda: pbar.config(value=completed/float(total)*100))
            self.root.after(0, pw.destroy)
            self.root.after(0, lambda: (self._set_status('Done! ' + str(total-errors) + '/' + str(total) + ' success, ' + str(errors) + ' failed'), self._save_session(), messagebox.showinfo('Done', 'Success: ' + str(total-errors) + '\nFailed: ' + str(errors) + '\n\nOutput: ' + out_dir)))
        threading.Thread(target=do_work, daemon=True).start()

    # ---- Merge Export ----
    def _merge_export(self):
        sel = [r for r in self.search_results if r['selected']]
        if len(sel) < 2: messagebox.showinfo('Tip', 'Need at least 2 clips to merge'); return
        ffmpeg = self.ffmpeg_entry.get().strip()
        out_dir = self.output_dir_entry.get().strip()
        merge_name = self.merge_name_entry.get().strip() or 'merged'
        bitrate = self.bitrate_var.get()
        if not ffmpeg or not os.path.exists(ffmpeg): messagebox.showerror('Error', 'FFmpeg not found'); return
        try: os.makedirs(out_dir, exist_ok=True)
        except Exception as e: messagebox.showerror('Error', 'Cannot create output dir: ' + str(e)); return
        total_dur = sum(self._get_clip_range(c)[1] - self._get_clip_range(c)[0] for c in sel)
        if not messagebox.askyesno('Confirm Merge', 'Merge ' + str(len(sel)) + ' clips\nTotal duration: ~' + str(int(total_dur)) + ' sec (' + str(int(total_dur/60)) + ' min)\nOutput: ' + merge_name + '.mp3'): return
        pw = tk.Toplevel(self.root); pw.title('Merging'); pw.geometry('580x280'); pw.transient(self.root); pw.grab_set()
        ttk.Label(pw, text='Merging ' + str(len(sel)) + ' clips...', font=('', 11)).pack(pady=8)
        pbar = ttk.Progressbar(pw, length=480, mode='determinate'); pbar.pack(pady=5)
        log_t = scrolledtext.ScrolledText(pw, height=8, font=('Consolas', 9)); log_t.pack(fill='both', expand=True, padx=10, pady=(0, 5))
        def log(msg): log_t.insert(tk.END, msg + '\n'); log_t.see(tk.END); pw.update()
        def do_merge():
            try:
                temp_dir = tempfile.gettempdir()
                temp_files = []
                for idx, c in enumerate(sel):
                    start, end = self._get_clip_range(c); dur = end - start
                    if not c.get('video_path') or not os.path.exists(c['video_path']): self.root.after(0, lambda c=c: log('SKIP: ' + c['text'][:40])); continue
                    temp_mp3 = os.path.join(temp_dir, 'merge_' + str(idx).zfill(3) + '.mp3')
                    temp_files.append(temp_mp3)
                    self.root.after(0, lambda i=idx, t=len(sel): log('Extracting [' + str(i+1) + '/' + str(t) + ']...'))
                    cmd = '"' + ffmpeg + '" -i "' + c["video_path"] + '" -ss ' + str(start) + ' -t ' + str(dur) + ' -vn -ar 44100 -b:a ' + bitrate + ' -ac 1 -y "' + temp_mp3 + '"'
                    res = subprocess.run(cmd, capture_output=True, text=True, timeout=120, shell=True)
                    if res.returncode == 0 and os.path.exists(temp_mp3):
                        sz = os.path.getsize(temp_mp3) / 1024; self.root.after(0, lambda s=sz: log('   OK (' + str(int(s)) + 'KB)'))
                    else: self.root.after(0, lambda: log('   FAIL'))
                    self.root.after(0, lambda p=(idx+1)/float(len(sel))*40: pbar.config(value=p))
                valid_files = [f for f in temp_files if os.path.exists(f)]
                if not valid_files: self.root.after(0, lambda: log('No valid clips')); self.root.after(0, pw.destroy); return
                self.root.after(0, lambda: log('Merging ' + str(len(valid_files)) + ' clips...'))
                list_file = os.path.join(temp_dir, 'merge_list.txt')
                with open(list_file, 'w', encoding='utf-8') as f:
                    for tf in valid_files: f.write("file '" + tf + "'\n")
                output_file = os.path.join(out_dir, merge_name + '.mp3')
                output_file = re.sub(r'[<>:"/\\|?*]', '_', output_file)
                merge_cmd = '"' + ffmpeg + '" -f concat -safe 0 -i "' + list_file + '" -c copy -y "' + output_file + '"'
                self.root.after(0, lambda: pbar.config(value=50))
                merge_res = subprocess.run(merge_cmd, capture_output=True, text=True, timeout=300, shell=True)
                if merge_res.returncode == 0 and os.path.exists(output_file):
                    sz = os.path.getsize(output_file) / 1024 / 1024
                    for tf in temp_files:
                        try: os.remove(tf)
                        except: pass
                    try: os.remove(list_file)
                    except: pass
                    self.root.after(0, lambda: log('\nDone!\nFile: ' + output_file + '\nSize: ' + str(round(sz, 2)) + ' MB\nClips: ' + str(len(valid_files))))
                    self.root.after(0, lambda: pbar.config(value=100))
                    self.root.after(500, lambda: os.startfile(out_dir))
                else:
                    self.root.after(0, lambda: log('Merge failed: ' + (merge_res.stderr or '')[:100]))
            except Exception as e:
                self.root.after(0, lambda: log('Error: ' + str(e)))
        threading.Thread(target=do_merge, daemon=True).start()

    # ---- Config ----
    def _get_cfg_path(self):
        base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, 'subtitle_tool_config.json')

    def _save_session(self):
        cfg = {'subtitle_dir': self.subtitle_dir_entry.get(), 'video_dir': self.video_dir_entry.get(), 'output_dir': self.output_dir_entry.get(), 'ffmpeg': self.ffmpeg_entry.get()}
        try:
            with open(self._get_cfg_path(), 'w', encoding='utf-8') as f: json.dump(cfg, f, ensure_ascii=False, indent=2)
        except: pass

    def _load_last_session(self):
        try:
            path = self._get_cfg_path()
            if os.path.exists(path):
                cfg = json.load(open(path, 'r', encoding='utf-8'))
                def set_if(entry, val):
                    if val: entry.delete(0, tk.END); entry.insert(0, val)
                set_if(self.subtitle_dir_entry, cfg.get('subtitle_dir', ''))
                set_if(self.video_dir_entry, cfg.get('video_dir', ''))
                set_if(self.output_dir_entry, cfg.get('output_dir', ''))
                set_if(self.ffmpeg_entry, cfg.get('ffmpeg', ''))
        except: pass

    def _set_status(self, msg):
        self.status_bar.config(text='  ' + datetime.now().strftime('%H:%M:%S') + '  ' + msg)
        self.root.update_idletasks()

    def _on_close(self):
        for f in self.temp_files:
            try:
                if os.path.exists(f): os.remove(f)
            except: pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    try:
        s = ttk.Style()
        for th in ['clam', 'vista', 'xpnative']:
            if th in s.theme_names(): s.theme_use(th); break
    except: pass
    Tool(root)
    root.mainloop()
