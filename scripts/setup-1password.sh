#!/usr/bin/env bash
set -euo pipefail

# One-time local setup: install the 1Password CLI + jq, sign in, and pin the
# 1Password account that owns the SKILL-TREE vaults to .1password.yml so
# generate-env.sh reads from the right account.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}1Password setup for skill-tree-survey${NC}"
echo "====================================="
echo ""

# Step 1: dependencies (macOS/Homebrew).
echo "Checking dependencies..."
if ! command -v brew >/dev/null 2>&1; then
    echo -e "${YELLOW}Homebrew not found. Install it from https://brew.sh, then re-run.${NC}"
    exit 1
fi
command -v op >/dev/null 2>&1 || { echo -e "${YELLOW}Installing 1Password CLI...${NC}"; brew install 1password-cli; }
command -v jq >/dev/null 2>&1 || { echo -e "${YELLOW}Installing jq...${NC}"; brew install jq; }
echo -e "${GREEN}  op, jq ready${NC}"
echo ""

# Step 2: sign in.
if ! op account list >/dev/null 2>&1; then
    echo -e "${YELLOW}Sign in to 1Password...${NC}"
    op signin
else
    echo -e "${GREEN}Already signed in to 1Password${NC}"
fi
echo ""

# Step 3: pick the account that owns the SKILL-TREE vaults.
echo -e "${CYAN}Select 1Password account${NC}"
ACCOUNTS="$(op account list --format json)"
COUNT="$(echo "$ACCOUNTS" | jq '. | length')"

if [ "$COUNT" -eq 0 ]; then
    echo -e "${RED}No 1Password accounts found${NC}"; exit 1
elif [ "$COUNT" -eq 1 ]; then
    SELECTED="$(echo "$ACCOUNTS" | jq -r '.[0].user_uuid')"
    echo -e "${GREEN}Using: $(echo "$ACCOUNTS" | jq -r '.[0].email')${NC}"
else
    echo "$ACCOUNTS" | jq -r 'to_entries | .[] | "  \(.key + 1)) \(.value.email)  (\(.value.url))"'
    echo ""
    while true; do
        printf "Select account number [1]: "
        read -r choice; choice="${choice:-1}"
        if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "$COUNT" ]; then
            SELECTED="$(echo "$ACCOUNTS" | jq -r ".[$((choice-1))].user_uuid")"
            echo -e "${GREEN}Using: $(echo "$ACCOUNTS" | jq -r ".[$((choice-1))].email")${NC}"
            break
        fi
        echo -e "${RED}Invalid selection${NC}"
    done
fi
echo ""

# Step 4: persist the account UUID.
cat > .1password.yml << EOF
# Pins which 1Password account generate-env.sh talks to (gitignored).
# Regenerate via: task env:setup
account: $SELECTED
EOF
chmod 600 .1password.yml
echo -e "${GREEN}Wrote .1password.yml${NC}"
echo ""
echo "Next steps:"
echo "  - Make sure vaults exist: op vault get ${VAULT_PREFIX:-SKILL-TREE}-LOCAL && op vault get ${VAULT_PREFIX:-SKILL-TREE}-PROD"
echo "  - Generate local env:     task env:generate ENV=local"
echo "  - Start the backend:      task start"
