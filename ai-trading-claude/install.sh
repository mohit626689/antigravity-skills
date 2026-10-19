#!/bin/bash
# ============================================================================
# AI Trading Analyst — Claude Code Skills Installer
# 16 Skills · 5 Agents · Options · PDF Reports · Stock Screening
# ============================================================================
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}║${NC}   ${CYAN}AI Trading Analyst — Claude Code Skills${NC}                   ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}   ${GREEN}16 Skills · 5 Agents · Options · PDF Reports${NC}              ${BLUE}║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}  NOTE: This is a RESEARCH tool, not a trading bot.${NC}"
echo -e "${YELLOW}  It does NOT execute trades or provide financial advice.${NC}"
echo ""

# ---------------------------------------------------------------------------
# Detect script directory (handle both local and curl | bash)
# ---------------------------------------------------------------------------
GITHUB_REPO="mohit626689/ai-trading-claude"
TEMP_DIR=""

if [ -n "${BASH_SOURCE[0]}" ] && [ "${BASH_SOURCE[0]}" != "bash" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/install.sh" ] && [ -d "$SCRIPT_DIR/skills" ]; then
        SOURCE_DIR="$SCRIPT_DIR"
        echo -e "${GREEN}Installing from local directory:${NC} $SOURCE_DIR"
    else
        SCRIPT_DIR=""
    fi
fi

if [ -z "${SCRIPT_DIR:-}" ] || [ ! -d "${SOURCE_DIR:-}" ]; then
    echo -e "${YELLOW}Cloning from GitHub...${NC}"
    TEMP_DIR=$(mktemp -d)
    if command -v git &>/dev/null; then
        git clone --depth 1 "https://github.com/$GITHUB_REPO.git" "$TEMP_DIR/repo" 2>/dev/null
        SOURCE_DIR="$TEMP_DIR/repo"
    else
        echo -e "${RED}Error: git is required for remote installation.${NC}"
        echo "Install git or run install.sh from a local clone."
        exit 1
    fi
    echo -e "${GREEN}Cloned successfully.${NC}"
fi

# ---------------------------------------------------------------------------
# Target directories
# ---------------------------------------------------------------------------
SKILLS_DIR="$HOME/.claude/skills"
AGENTS_DIR="$HOME/.claude/agents"

# ---------------------------------------------------------------------------
# Check for Claude Code
# ---------------------------------------------------------------------------
echo -e "${BLUE}Checking prerequisites...${NC}"
if command -v claude &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Claude Code found"
else
    echo -e "  ${YELLOW}⚠${NC} Claude Code CLI not found (skills will still be installed)"
fi

# ---------------------------------------------------------------------------
# Create directories
# ---------------------------------------------------------------------------
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p "$SKILLS_DIR/trade/scripts"
echo -e "  ${GREEN}✓${NC} Skills directory ready"

mkdir -p "$AGENTS_DIR"
echo -e "  ${GREEN}✓${NC} Agents directory ready"

# ---------------------------------------------------------------------------
# Install main skill orchestrator
# ---------------------------------------------------------------------------
echo -e "${BLUE}Installing skills...${NC}"

INSTALL_COUNT=0

if [ -f "$SOURCE_DIR/trade/SKILL.md" ]; then
    cp "$SOURCE_DIR/trade/SKILL.md" "$SKILLS_DIR/trade/SKILL.md"
    echo -e "  ${GREEN}✓${NC} trade (orchestrator)"
    INSTALL_COUNT=$((INSTALL_COUNT + 1))
fi

# ---------------------------------------------------------------------------
# Install 15 sub-skills
# ---------------------------------------------------------------------------
SKILLS=(
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
    if [ -f "$SOURCE_DIR/skills/$skill/SKILL.md" ]; then
        mkdir -p "$SKILLS_DIR/$skill"
        cp "$SOURCE_DIR/skills/$skill/SKILL.md" "$SKILLS_DIR/$skill/SKILL.md"
        echo -e "  ${GREEN}✓${NC} $skill"
        INSTALL_COUNT=$((INSTALL_COUNT + 1))
    else
        echo -e "  ${YELLOW}⚠${NC} $skill (not found in source)"
    fi
done

# ---------------------------------------------------------------------------
# Install 5 agents
# ---------------------------------------------------------------------------
echo -e "${BLUE}Installing agents...${NC}"

AGENT_COUNT=0
AGENTS=(
    trade-technical
    trade-fundamental
    trade-sentiment
    trade-risk
    trade-thesis
)

for agent in "${AGENTS[@]}"; do
    if [ -f "$SOURCE_DIR/agents/$agent.md" ]; then
        cp "$SOURCE_DIR/agents/$agent.md" "$AGENTS_DIR/$agent.md"
        echo -e "  ${GREEN}✓${NC} $agent"
        AGENT_COUNT=$((AGENT_COUNT + 1))
    else
        echo -e "  ${YELLOW}⚠${NC} $agent (not found in source)"
    fi
done

# ---------------------------------------------------------------------------
# Install Python scripts
# ---------------------------------------------------------------------------
echo -e "${BLUE}Installing scripts...${NC}"

SCRIPT_COUNT=0
for script in "$SOURCE_DIR"/scripts/*.py; do
    if [ -f "$script" ]; then
        cp "$script" "$SKILLS_DIR/trade/scripts/"
        echo -e "  ${GREEN}✓${NC} $(basename "$script")"
        SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
    fi
done

# ---------------------------------------------------------------------------
# Check Python dependencies
# ---------------------------------------------------------------------------
echo -e "${BLUE}Checking Python environment...${NC}"

if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 --version 2>&1)
    PY_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
    PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 8 ]; then
        echo -e "  ${GREEN}✓${NC} $PY_VERSION"
    else
        echo -e "  ${YELLOW}⚠${NC} $PY_VERSION (Python 3.8+ recommended)"
    fi
else
    echo -e "  ${RED}✗${NC} Python 3 not found — required for PDF reports"
fi

# Check reportlab
if python3 -c "import reportlab" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} reportlab installed"
else
    echo -e "  ${YELLOW}⚠${NC} reportlab not installed (needed for PDF reports)"
    echo -e "      Install with: ${CYAN}pip3 install reportlab${NC}"
fi

# ---------------------------------------------------------------------------
# Cleanup temp dir if used
# ---------------------------------------------------------------------------
if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
    echo -e "  ${GREEN}✓${NC} Cleaned up temporary files"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Installation Complete!                                      ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${CYAN}Skills:${NC}    $INSTALL_COUNT installed  →  $SKILLS_DIR"
echo -e "  ${CYAN}Agents:${NC}    $AGENT_COUNT installed  →  $AGENTS_DIR"
echo -e "  ${CYAN}Scripts:${NC}   $SCRIPT_COUNT installed  →  $SKILLS_DIR/trade/scripts"
echo ""

# ---------------------------------------------------------------------------
# Command reference
# ---------------------------------------------------------------------------
echo -e "${BLUE}Command Reference:${NC}"
echo ""
echo -e "  ${CYAN}/trade analyze <ticker>${NC}      Full stock analysis (5 parallel agents)"
echo -e "  ${CYAN}/trade quick <ticker>${NC}        60-second stock snapshot"
echo -e "  ${CYAN}/trade technical <ticker>${NC}    Technical analysis (price, indicators)"
echo -e "  ${CYAN}/trade fundamental <ticker>${NC}  Fundamental analysis (financials, moat)"
echo -e "  ${CYAN}/trade sentiment <ticker>${NC}    News & social sentiment"
echo -e "  ${CYAN}/trade sector <sector>${NC}       Sector rotation & momentum"
echo -e "  ${CYAN}/trade compare <t1> <t2>${NC}     Head-to-head stock comparison"
echo -e "  ${CYAN}/trade thesis <ticker>${NC}       Investment thesis with entry/exit"
echo -e "  ${CYAN}/trade options <ticker>${NC}      Options strategy recommendations"
echo -e "  ${CYAN}/trade portfolio${NC}             Portfolio analysis & rebalancing"
echo -e "  ${CYAN}/trade risk <ticker>${NC}         Risk assessment & position sizing"
echo -e "  ${CYAN}/trade screen <criteria>${NC}     Stock screener by strategy"
echo -e "  ${CYAN}/trade earnings <ticker>${NC}     Pre-earnings analysis"
echo -e "  ${CYAN}/trade watchlist${NC}             Build/update scored watchlist"
echo -e "  ${CYAN}/trade report-pdf${NC}            Professional PDF investment report"
echo ""
echo -e "  ${YELLOW}Tip:${NC} Start with ${CYAN}/trade analyze <ticker>${NC} for a full multi-agent analysis!"
echo ""
echo -e "  ${RED}DISCLAIMER:${NC} This tool is for educational and research purposes only."
echo -e "  It is NOT financial advice. It does NOT execute trades."
echo ""
