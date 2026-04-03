        tk.Label(btn_area, text="GIT INFO",
                 bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica", 8, "bold")).pack(anchor="w", pady=(0, 6))
        row1 = tk.Frame(btn_area, bg=BG_DARK)
        row1.pack(fill="x", pady=(0, 10))

        self._make_git_btn(
            row1, "git status",
            color="#1a2233", fg=BLUE,
            cmd=lambda: self._run_git(["git", "status"]),
        ).pack(side="left", padx=(0, 8))

        self._make_git_btn(
            row1, "git log",
            color="#1a2233", fg=BLUE,
            cmd=lambda: self._run_git(
                ["git", "log", "--oneline", "--graph", "--decorate", "-20"]),
        ).pack(side="left", padx=(0, 8))

        self._make_git_btn(
            row1, "git diff",
            color="#1a2233", fg=BLUE,
            cmd=lambda: self._run_git(["git", "diff", "--stat"]),
        ).pack(side="left")