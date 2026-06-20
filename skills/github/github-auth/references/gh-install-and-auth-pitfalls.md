# gh CLI Installation and Auth Pitfalls

## Installing gh CLI from scratch

When `gh` is not installed and you need it (richer GitHub API, better git integration):

```bash
# Debian/Ubuntu — requires sudo
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] \
  https://cli.github.com/packages stable main" \
  | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
apt-get update -qq && apt-get install -y -qq gh
```

## Pitfall: `gh auth login --with-token` fails when GITHUB_TOKEN is set

When the `GITHUB_TOKEN` environment variable is already exported, `gh auth login --with-token` refuses to work and prints:

```
The value of the GITHUB_TOKEN environment variable is being used for authentication.
To have GitHub CLI store credentials instead, first clear the value from the environment.
```

**Fix:** Unset the env var before piping the token:

```bash
# WRONG — will fail if GITHUB_TOKEN is already set:
echo "$GITHUB_TOKEN" | gh auth login --with-token

# CORRECT — clear the env var first:
GITHUB_TOKEN="" gh auth login --with-token
# OR:
unset GITHUB_TOKEN && echo "$TOKEN" | gh auth login --with-token
```

## Hermes-specific: token location

In Hermes Agent setups, the GitHub token is typically stored in `/hermes-home/.env` (not `~/.hermes/.env`):

```bash
# Read from Hermes-specific location
token=$(grep GITHUB_TOKEN /hermes-home/.env 2>/dev/null | cut -d= -f2-)
GITHUB_TOKEN="" echo "$token" | gh auth login --with-token
```

## Setting up a GitHub repo as Hermes skills source

After cloning a private repo, configure it as a skills external_dir:

```yaml
# In config.yaml
skills:
  external_dirs:
    - /path/to/cloned/repo/skills-dir
```

Then restart the session (`/reset` in chat, or new session) for Hermes to detect the new skills.
