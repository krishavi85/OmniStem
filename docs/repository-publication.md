# Publish this repository to GitHub

Create an empty GitHub repository named `omnistem-god-mode`, without adding a README, license, or `.gitignore`. Then run from the extracted project directory:

```bash
git remote add origin https://github.com/krishavi85/omnistem-god-mode.git
git branch -M main
git push -u origin main
```

Alternatively, clone the supplied Git bundle:

```bash
git clone omnistem-god-mode.git.bundle omnistem-god-mode
cd omnistem-god-mode
git remote set-url origin https://github.com/krishavi85/omnistem-god-mode.git
git push -u origin main
```
