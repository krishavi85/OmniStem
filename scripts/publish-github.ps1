param(
    [string]$RepositoryUrl = "https://github.com/krishavi85/omnistem-god-mode.git"
)
$ErrorActionPreference = "Stop"
git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    git remote add origin $RepositoryUrl
} else {
    git remote set-url origin $RepositoryUrl
}
git branch -M main
git push -u origin main
