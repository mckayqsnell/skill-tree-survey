#!/usr/bin/env bash
set -euo pipefail

# Generate infrastructure/terraform/environments/prod.tfvars from 1Password.
#
# Convention (mirrors scripts/generate-env.sh):
#   - Vault: ${VAULT_PREFIX}-INFRA  (e.g. SKILL-TREE-INFRA)
#   - Each Terraform input = one 1Password item tagged `tfvar`:
#       item title  = UPPER_SNAKE variable name (e.g. VPC_ID)
#       item value  = the `password` (or `credential`) field
#   - The title is lowercased into the tfvars key (VPC_ID -> vpc_id).
#   - Values starting with `[` or `{` are written raw (HCL list/map);
#     everything else is quoted as a string.
#   - Items WITHOUT the `tfvar` tag (e.g. AWS_ACCOUNT_ID) are reference-only
#     records and are not written to the file.
#
# All other Terraform inputs use their defaults in variables.tf; override them
# here only by adding a tagged item to the vault.
#
# Usage: scripts/generate-tfvars.sh   (or: task tf:gen)

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# Load project config (VAULT_PREFIX).
if [ -f .setup.config ]; then
    set -a; . ./.setup.config; set +a
fi
: "${VAULT_PREFIX:?VAULT_PREFIX not set — is .setup.config present?}"

VAULT="${VAULT_PREFIX}-INFRA"
OUTPUT_FILE="infrastructure/terraform/environments/prod.tfvars"

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'

# jq parses the `op item list` JSON below — fail fast with a clear message.
if ! command -v jq >/dev/null 2>&1; then
    echo -e "${RED}jq is required but not installed.${NC} Install it (e.g. brew install jq) and re-run."
    exit 1
fi

# Pin to a specific 1Password account when the same email is on multiple
# accounts (work + personal). Written by scripts/setup-1password.sh.
if [ -f .1password.yml ]; then
    ACCOUNT="$(grep '^account:' .1password.yml | awk '{print $2}' | head -1 || echo "")"
    [ -n "$ACCOUNT" ] && export OP_ACCOUNT="$ACCOUNT"
fi

echo -e "${CYAN}Generating ${OUTPUT_FILE}${NC} from 1Password vault ${CYAN}${VAULT}${NC}"

if ! op vault get "$VAULT" >/dev/null 2>&1; then
    echo -e "${RED}Vault '${VAULT}' not found (or not signed in).${NC}"
    echo "  Sign in:        op signin   (or: task env:setup)"
    echo "  Create vault:   op vault create ${VAULT}"
    exit 1
fi

ITEMS="$(op item list --vault="$VAULT" --tags tfvar --format json 2>/dev/null | jq -r '.[].title')"
if [ -z "$ITEMS" ]; then
    echo -e "${RED}No items tagged 'tfvar' in vault '${VAULT}' — refusing to write an empty tfvars.${NC}"
    exit 1
fi

cat > "$OUTPUT_FILE" << EOF
# ================================================
# Terraform inputs for prod
# Source: 1Password/${VAULT} (items tagged 'tfvar')
# Generated: $(date)
# DO NOT COMMIT THIS FILE — regenerate with: task tf:gen
# All other inputs use their defaults in variables.tf.
# ================================================

EOF

# Read every tagged item in parallel. Try the `credential` field (newer
# 1Password UI default) then fall back to `password`. Item titles are passed
# positionally to avoid shell injection.
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
    KEY="$(printf "%s" "$ITEM" | tr "[:upper:]" "[:lower:]")"
    case "$VALUE" in
        \[*|\{*) printf "%s = %s\n"     "$KEY" "$VALUE" ;;  # HCL list/map, raw
        *)       printf "%s = \"%s\"\n" "$KEY" "$VALUE" ;;  # string, quoted
    esac
' _ {} | grep -E '^[a-z_][a-z0-9_]* = ' | sort >> "$OUTPUT_FILE" || true

VAR_COUNT="$(grep -cE '^[a-z_][a-z0-9_]* = ' "$OUTPUT_FILE" 2>/dev/null || true)"
VAR_COUNT="${VAR_COUNT:-0}"
if [ "$VAR_COUNT" -eq 0 ]; then
    echo -e "${RED}Wrote 0 variables — check the vault items' fields.${NC}"
    exit 1
fi
echo -e "${GREEN}Wrote ${VAR_COUNT} variable(s) to ${OUTPUT_FILE}${NC}"
