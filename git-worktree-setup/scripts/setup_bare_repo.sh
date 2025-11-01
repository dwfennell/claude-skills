#!/bin/bash
# Setup a bare git repository with worktree structure from a GitHub URL

set -e

usage() {
    echo "Usage: $0 <github-url> <target-dir> [default-branch]"
    echo "Example: $0 https://github.com/user/repo my-repo main"
    exit 1
}

if [ "$#" -lt 2 ]; then
    usage
fi

GITHUB_URL="$1"
TARGET_DIR="$2"
DEFAULT_BRANCH="${3:-main}"

# Extract repo name from URL if target dir not specified
REPO_NAME=$(basename "$GITHUB_URL" .git)
BARE_DIR="${TARGET_DIR}/.bare"

echo "🚀 Setting up headless worktree structure..."
echo "   Repository: $GITHUB_URL"
echo "   Target: $TARGET_DIR"
echo "   Default branch: $DEFAULT_BRANCH"
echo ""

# Create the main directory first
mkdir -p "$TARGET_DIR"

# Clone as bare repository
echo "📦 Cloning bare repository..."
git clone --bare "$GITHUB_URL" "$BARE_DIR"

# Configure the bare repository
cd "$BARE_DIR"
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"

# Create .git file pointing to bare repo
cd ..
echo "gitdir: ./.bare" > .git

# Add the default branch as first worktree
echo "🌳 Creating worktree for $DEFAULT_BRANCH..."
git worktree add "$DEFAULT_BRANCH"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Your repository structure:"
echo "  $TARGET_DIR/"
echo "    ├── .bare/           (bare repository)"
echo "    ├── .git             (pointer to .bare)"
echo "    └── $DEFAULT_BRANCH/ (worktree)"
echo ""
echo "To add more worktrees:"
echo "  cd $TARGET_DIR"
echo "  git worktree add <branch-name>"
