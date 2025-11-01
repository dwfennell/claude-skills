#!/bin/bash
# Add a new worktree to an existing bare repository setup

set -e

usage() {
    echo "Usage: $0 <branch-name> [base-branch]"
    echo "Example: $0 feature/new-api main"
    echo ""
    echo "Creates a new worktree for the specified branch."
    echo "If base-branch is provided, creates a new branch from it."
    exit 1
}

if [ "$#" -lt 1 ]; then
    usage
fi

BRANCH_NAME="$1"
BASE_BRANCH="$2"

# Check if we're in a bare repo setup
if [ ! -f ".git" ] || ! grep -q "gitdir: ./.bare" .git 2>/dev/null; then
    echo "❌ Error: Not in a bare repository setup"
    echo "   Run this from the root of your worktree-structured repository"
    exit 1
fi

echo "🌳 Creating worktree for branch: $BRANCH_NAME"

if [ -n "$BASE_BRANCH" ]; then
    echo "   Base branch: $BASE_BRANCH"
    git worktree add -b "$BRANCH_NAME" "$BRANCH_NAME" "$BASE_BRANCH"
else
    # Try to add existing branch or create new one from current HEAD
    if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
        echo "   Using existing branch"
        git worktree add "$BRANCH_NAME"
    elif git show-ref --verify --quiet "refs/remotes/origin/$BRANCH_NAME"; then
        echo "   Checking out remote branch"
        git worktree add "$BRANCH_NAME" "origin/$BRANCH_NAME"
    else
        echo "   Creating new branch"
        git worktree add -b "$BRANCH_NAME" "$BRANCH_NAME"
    fi
fi

echo ""
echo "✅ Worktree created!"
echo "   Location: ./$BRANCH_NAME"
echo ""
echo "To start working:"
echo "  cd $BRANCH_NAME"
