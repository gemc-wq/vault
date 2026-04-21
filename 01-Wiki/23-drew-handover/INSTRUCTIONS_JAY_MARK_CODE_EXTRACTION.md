# Instructions for Jay Mark: Zero Codebase Extraction

**From:** Ava (on behalf of Cem)  
**To:** Jay Mark Catacutan  
**Date:** 2026-03-09  
**Priority:** HIGH — needed to understand and eventually replace the Zero system

---

## Goal

Copy the entire Zero PHP codebase from the PH server (192.168.20.57) to a private GitHub repository so Cem's team can analyze it remotely.

---

## What You Need

- Your PC (you're on the PH LAN, so you have access)
- Remote Desktop (RDP) or file share access to **192.168.20.57**
- Git (should be available via Claude Code on your PC)
- A GitHub account (use your personal or ask Cem for the org account)

---

## Step-by-Step

### Step 1: Access the Server

Connect to the web server where the Zero code lives:

**Option A — Remote Desktop (RDP):**
1. Open Remote Desktop Connection
2. Connect to: `192.168.20.57`
3. Username: `elcell`
4. Password: `yUpeMab9`

**Option B — Network share:**
1. Open File Explorer
2. Navigate to: `\\192.168.20.57\c$\xampp\htdocs\`
3. Use credentials above if prompted

### Step 2: Copy the Code to Your PC

1. Navigate to `C:\xampp\htdocs\` on the server
2. Copy the **entire htdocs folder** to your local PC
   - Right-click → Copy, then paste to your Desktop or a working folder
   - This may take a while depending on folder size
3. **Do NOT delete anything on the server** — we're only making a copy

### Step 3: Push to GitHub

Open a terminal (Command Prompt, PowerShell, or Git Bash) in the copied folder:

```bash
# Navigate to where you copied the files
cd C:\Users\JayMark\Desktop\htdocs   # adjust path as needed

# Initialize git
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial export of Zero PHP codebase from 192.168.20.57"

# Create private repo on GitHub (use Claude Code or GitHub.com)
# IMPORTANT: Make it PRIVATE — this contains business logic and credentials

# Add the remote and push
git remote add origin https://github.com/gemc-wq/zero-codebase.git
git push -u origin main
```

**If the folder is too large for one commit:**
```bash
# Check the total size first
dir /s   # on Windows shows total size

# If > 1GB, you may need Git LFS for large files, or exclude non-code files:
# Create a .gitignore to skip images/binaries
echo "*.jpg" >> .gitignore
echo "*.png" >> .gitignore
echo "*.tiff" >> .gitignore
echo "*.pdf" >> .gitignore
echo "*.zip" >> .gitignore
git add .
git commit -m "Initial export — code only, large binaries excluded"
git push -u origin main
```

### Step 4: Confirm

Once pushed, send Cem or Ava (via Slack) the repository URL. We'll take it from there.

---

## Key Files We're Especially Interested In

These were identified from Patrick's workflow documentation:

| File | Purpose |
|------|---------|
| `zero_POFiltering.php` | PO routing logic (~1300 lines, hardcoded warehouse rules) |
| `sage_generate_picking_list_split.php` | Picking list generation |
| `zero_generate_purchase_order_automated_phAMG1_wh.php` | Automated PO generation |
| Any files with `sage_` prefix | Sage integration layer |
| Any files with `zero_` prefix | Core Zero system logic |
| Database config files (e.g., `config.php`, `db.php`, `.env`) | Connection strings + credentials |

---

## Important Notes

1. **This is read-only** — don't change anything on the server
2. **Make the GitHub repo PRIVATE** — it contains credentials and business logic
3. **Don't worry about understanding the code** — just get it to GitHub, we'll analyze it
4. **If you hit permission issues**, try the network share approach (Option B) instead of RDP
5. **If the server is Windows**, the path is `C:\xampp\htdocs\`. If Linux, check `/var/www/html/` or `/opt/lampp/htdocs/`

---

## Troubleshooting

- **"Access denied" on RDP:** Try the network share approach, or ask IT (Chad/Patrick) to grant you access
- **Git not installed:** Download from https://git-scm.com/download/win or use Claude Code's terminal
- **Folder is massive (>5GB):** Focus on `.php`, `.js`, `.html`, `.css`, `.json`, `.sql` files only. Skip images, uploads, and temp folders.
- **GitHub push rejected:** Make sure the repo is initialized as private, and you're authenticated (`git config --global credential.helper store`)

---

*Questions? Message Ava on Slack or ask Cem directly.*
