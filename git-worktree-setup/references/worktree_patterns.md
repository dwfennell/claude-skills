# Git Worktree Patterns and Best Practices

## What is a Headless/Bare Worktree Setup?

A headless worktree setup uses a bare git repository (`.bare/`) as the source of truth, with each branch checked out as a separate directory (worktree). This approach offers several advantages over traditional git workflows.

## Directory Structure

```
my-project/
├── .bare/              # Bare repository (git database)
├── .git                # Pointer file: "gitdir: ./.bare"
├── main/               # Worktree for main branch
├── feature-a/          # Worktree for feature-a branch
└── feature-b/          # Worktree for feature-b branch
```

## Benefits

### 1. Multiple Branches Simultaneously
Work on multiple branches without switching contexts or stashing changes:
- Run tests on `main` while developing in `feature-branch`
- Compare implementations side-by-side
- Run a dev server on one branch while coding on another

### 2. Clean Branch Isolation
Each worktree is a separate directory with its own:
- Working files
- Node modules / dependencies
- Build artifacts
- IDE state

No more stashing, no more `node_modules` reinstalls when switching branches.

### 3. Simplified CI/CD Testing
Test branches locally exactly as CI would see them:
- Fresh checkout in dedicated directory
- No working directory contamination
- Easy to script parallel testing

### 4. Better IDE Integration
Modern IDEs work better with worktrees:
- Open multiple worktrees in separate windows
- Each has its own language server instance
- No confusion about which branch files belong to

## Common Workflows

### Starting Fresh with a GitHub Repo

Use when cloning a new project:
```bash
setup_bare_repo.sh https://github.com/user/repo my-project main
cd my-project
```

### Converting an Existing Repo

Use when you have an existing cloned repository:
```bash
convert_to_worktree.sh ./existing-repo main
cd existing-repo
```

### Adding Branches

When starting new work:
```bash
# Create new branch from main
add_worktree.sh feature/new-api main

# Checkout existing remote branch
add_worktree.sh bugfix/urgent-fix

# Add any branch
add_worktree.sh experimental
```

### Removing Worktrees

When done with a branch:
```bash
git worktree remove feature/completed
git branch -d feature/completed  # optional: delete the branch
```

List all worktrees:
```bash
git worktree list
```

## Edge Cases and Gotchas

### Submodules
Submodules work but each worktree maintains its own submodule checkouts. Run `git submodule update --init` in each worktree.

### Hooks
Git hooks in `.bare/hooks/` apply to all worktrees. Worktree-specific hooks aren't supported.

### Lock Files
Package manager lock files (`package-lock.json`, `Gemfile.lock`, etc.) are per-worktree. This is usually desirable but can cause confusion during merges.

### Disk Space
Each worktree is a full working directory. Projects with large `node_modules/` or build artifacts will consume more disk space. The git objects are still shared in `.bare/` though.

## When NOT to Use Worktrees

- **Small, simple projects** - Overhead isn't worth it
- **Rarely switch branches** - Traditional git flow is simpler
- **Disk space constrained** - Multiple working directories consume space
- **Team doesn't use worktrees** - Consistency with team practices matters

## Pro Tips

### Use Descriptive Names
Instead of branch names like `fix-123`, use the actual branch name so the directory name is meaningful:
```bash
git worktree add feature/user-authentication
```

### Consistent Base Directory
Always work from the root (where `.bare/` lives) when running git commands that affect the repository as a whole.

### Prune Stale Worktrees
Occasionally clean up worktree records for deleted directories:
```bash
git worktree prune
```

### Gitignore the Worktrees
If the worktree directories bother you, add them to `.git/info/exclude`:
```
main/
feature-*/
bugfix-*/
```
