#!/usr/bin/env bash
set -euo pipefail

# Generate a .env.<env> file from a 1Password vault.
#
# Convention:
#   - Each env var = one 1Password item.
#   - Item title    = ENV_VAR_NAME (UPPER_SNAKE_CASE, e.g. ADMIN_PASSWORD)
#   - Item value    = the `password` (or `credential`) field
#   - Vault per env = ${VAULT_PREFIX}-LOCAL, ${VAULT_PREFIX}-PROD
#
# Usage: scripts/generate-env.sh <env>
#   env: local | prod

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# Load project config (VAULT_PREFIX).
if [ -f .setup.config ]; then
    set -a; . ./.setup.config; set +a
fi
: "${VAULT_PREFIX:?VAULT_PREFIX not set — is .setup.config present?}"

ENV="${1:-local}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

case "$ENV" in
    local) VAULT="${VAULT_PREFIX}-LOCAL" ;;
    prod)  VAULT="${VAULT_PREFIX}-PROD" ;;
    *)     echo -e "${RED}Unknown env '$ENV' (use local|prod)${NC}"; exit 1 ;;
esac

OUTPUT_FILE=".env.${ENV}"

# Pin to a specific 1Password account when the same email is on multiple accounts
# (work + personal). Written by scripts/setup-1password.sh.
if [ -f .1password.yml ]; then
    ACCOUNT="$(grep '^account:' .1password.yml | awk '{print $2}' | head -1 || echo "")"
    [ -n "$ACCOUNT" ] && export OP_ACCOUNT="$ACCOUNT"
fi

echo -e "${CYAN}Generating ${OUTPUT_FILE}${NC} from 1Password vault ${CYAN}${VAULT}${NC}"

if ! op vault get "$VAULT" >/dev/null 2>&1; then
    echo -e "${RED}Vault '${VAULT}' not found (or not signed in).${NC}"
    echo "  Sign in:        op signin   (or: task env:setup)"
    echo "  Create vaults:  see README / docs (SKILL-TREE-LOCAL, SKILL-TREE-PROD)"
    exit 1
fi

ITEMS="$(op item list --vault="$VAULT" --format json 2>/dev/null | jq -r '.[].title')"
if [ -z "$ITEMS" ]; then
    echo -e "${YELLOW}  No items in vault '${VAULT}' — writing an empty ${OUTPUT_FILE} (app will use defaults).${NC}"
fi

cat > "$OUTPUT_FILE" << EOF
# ================================================
# Environment: ${ENV}
# Source: 1Password/${VAULT}
# Generated: $(date)
# DO NOT COMMIT THIS FILE — regenerate with: task env:generate ENV=${ENV}
# ================================================

EOF

# Read every item in parallel. Try the `credential` field (newer 1Password UI
# default) then fall back to `password`. Item titles are passed positionally to
# avoid shell injection.
if [ -n "$ITEMS" ]; then
    echo "$ITEMS" | xargs -P 10 -I {} sh -c '
        ITEM="$1"
        VAULT_NAME="'"$VAULT"'"
        VALUE=$(op read "op://${VAULT_NAME}/${ITEM}/credential" 2>/dev/null \
             || op read "op://${VAULT_NAME}/${ITEM}/password"   2>/dev/null \
             || true)
        if [ -z "$VALUE" ]; then
            echo "  ! Failed to read ${ITEM} (no credential/password field)" >&2
            exit 0
        fi
        printf "%s=%s\n" "${ITEM}" "${VALUE}"
    ' _ {} | grep -E "^[A-Z_][A-Z0-9_]*=" >> "$OUTPUT_FILE" || true
fi

VAR_COUNT="$(grep -cE '^[A-Z_][A-Z0-9_]*=' "$OUTPUT_FILE" 2>/dev/null || true)"
VAR_COUNT="${VAR_COUNT:-0}"
echo -e "${GREEN}Wrote ${VAR_COUNT} variable(s) to ${OUTPUT_FILE}${NC}"
