#!/bin/bash
# ============================================================================
# AI Trading Analyst — Uninstaller
# ============================================================================
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SKILLS_DIR="$HOME/.claude/skills"
AGENTS_DIR="$HOME/.claude/agents"

echo ""
echo -e "${BLUE}Uninstalling AI Trading Analyst...${NC}"
echo ""

# Remove skills
SKILLS=(
    trade
    trade-analyze
    trade-technical
    trade-fundamental
    trade-sentiment
    trade-sector
    trade-compare
    trade-thesis
    trade-options
    trade-portfolio
    trade-risk
    trade-screen
    trade-earnings
    trade-watchlist
    trade-report-pdf
    trade-quick
)

for skill in "${SKILLS[@]}"; do
    if [ -d "$SKILLS_DIR/$skill" ]; then
        rm -rf "$SKILLS_DIR/$skill"
        echo -e "  ${GREEN}✓${NC} Removed $skill"
    fi
done

# Remove agents
AGENTS=(
    trade-technical
    trade-fundamental
    trade-sentiment
    trade-risk
    trade-thesis
)

for agent in "${AGENTS[@]}"; do
    if [ -f "$AGENTS_DIR/$agent.md" ]; then
        rm "$AGENTS_DIR/$agent.md"
        echo -e "  ${GREEN}✓${NC} Removed agent: $agent"
    fi
done

echo ""
echo -e "${GREEN}Uninstall complete.${NC} All AI Trading Analyst skills and agents have been removed."
echo -e "Your Claude Code installation is otherwise unchanged."
echo ""
