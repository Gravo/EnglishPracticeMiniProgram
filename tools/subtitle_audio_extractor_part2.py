

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
