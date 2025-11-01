#!/bin/bash
# Convert an existing git repository to a bare + worktree structure

set -e

usage() {
    echo "Usage: $0 <repo-path> [default-branch]"
    echo "Example: $0 ./my-repo main"
    echo ""
    echo "This will convert an existing cloned repository to use a bare"
    echo "repository with worktrees structure."
    exit 1
}

if [ "$#" -lt 1 ]; then
    usage
fi

REPO_PATH="$1"
DEFAULT_BRANCH="${2:-main}"

if [ ! -d "$REPO_PATH/.git" ]; then
    echo "❌ Error: $REPO_PATH is not a git repository"
    exit 1
fi

echo "🔄 Converting to headless worktree structure..."
echo "   Repository: $REPO_PATH"
echo "   Current branch: $(cd "$REPO_PATH" && git branch --show-current)"
echo ""

# Get the absolute path
REPO_PATH=$(cd "$REPO_PATH" && pwd)
PARENT_DIR=$(dirname "$REPO_PATH")
REPO_NAME=$(basename "$REPO_PATH")
TEMP_BARE="${PARENT_DIR}/.${REPO_NAME}_bare_temp"

# Create backup warning
echo "⚠️  This will restructure your repository."
echo "   Make sure all changes are committed or stashed."
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Clone as bare to temporary location
echo "📦 Creating bare repository..."
cd "$PARENT_DIR"
git clone --bare "$REPO_PATH" "$TEMP_BARE"

# Move the bare repo into the original location
echo "🔧 Restructuring..."
cd "$REPO_PATH"
rm -rf .git
mkdir -p .bare
mv "$TEMP_BARE"/* .bare/
mv "$TEMP_BARE"/.git* .bare/ 2>/dev/null || true
rmdir "$TEMP_BARE"

# Configure the bare repository
cd .bare
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"

# Create .git file pointing to bare repo
cd "$REPO_PATH"
echo "gitdir: ./.bare" > .git

# Create worktree for the default branch
echo "🌳 Creating worktree for $DEFAULT_BRANCH..."
git worktree add "$DEFAULT_BRANCH"

# Clean up the now-empty working directory files (they're in the worktree now)
# Keep only .bare, .git, and worktree directories
find . -maxdepth 1 -type f -delete
find . -maxdepth 1 -type d ! -name "." ! -name ".bare" ! -name "$DEFAULT_BRANCH" ! -name ".git*" -exec rm -rf {} + 2>/dev/null || true

echo ""
echo "✅ Conversion complete!"
echo ""
echo "Your repository structure:"
echo "  $REPO_PATH/"
echo "    ├── .bare/           (bare repository)"
echo "    ├── .git             (pointer to .bare)"
echo "    └── $DEFAULT_BRANCH/ (worktree)"
echo ""
echo "To add more worktrees:"
echo "  cd $REPO_PATH"
echo "  git worktree add <branch-name>"
