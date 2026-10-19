#!/bin/bash
# ============================================================================
# AI Reputation Manager — Claude Code Skills Installer
# 14 Skills · 5 Agents · PDF Reports
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
echo -e "${BLUE}║${NC}   ${CYAN}AI Reputation Manager — Claude Code Skills${NC}                ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}   ${GREEN}14 Skills · 5 Agents · PDF Reports${NC}                       ${BLUE}║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ---------------------------------------------------------------------------
# Detect script directory (handle both local and curl | bash)
# ---------------------------------------------------------------------------
GITHUB_REPO="mohit626689/ai-reputation-claude"
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
mkdir -p "$SKILLS_DIR/reputation/scripts"
echo -e "  ${GREEN}✓${NC} Skills directory ready"

mkdir -p "$AGENTS_DIR"
echo -e "  ${GREEN}✓${NC} Agents directory ready"

# ---------------------------------------------------------------------------
# Install main skill orchestrator
# ---------------------------------------------------------------------------
echo -e "${BLUE}Installing skills...${NC}"

INSTALL_COUNT=0

if [ -f "$SOURCE_DIR/reputation/SKILL.md" ]; then
    cp "$SOURCE_DIR/reputation/SKILL.md" "$SKILLS_DIR/reputation/SKILL.md"
    echo -e "  ${GREEN}✓${NC} reputation (orchestrator)"
    INSTALL_COUNT=$((INSTALL_COUNT + 1))
fi

# ---------------------------------------------------------------------------
# Install 13 sub-skills
# ---------------------------------------------------------------------------
SKILLS=(
    reputation-audit
    reputation-reviews
    reputation-sentiment
    reputation-trends
    reputation-competitors
    reputation-respond
    reputation-crisis
    reputation-recover
    reputation-request
    reputation-alerts
    reputation-social
    reputation-seo
    reputation-quick
    reputation-report-pdf
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
    reputation-reviews
    reputation-sentiment
    reputation-competitors
    reputation-response
    reputation-recommendations
)
# Note: actual agent files are reputation-reviews.md, reputation-sentiment.md,
# reputation-competitors.md, reputation-response.md, reputation-recommendations.md

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
        cp "$script" "$SKILLS_DIR/reputation/scripts/"
        echo -e "  ${GREEN}✓${NC} $(basename "$script")"
        SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
    fi
done

# ---------------------------------------------------------------------------
# Check Python dependencies
# ---------------------------------------------------------------------------
echo -e "${BLUE}Checking Python environment...${NC}"

if command -v python3 &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Python 3 found: $(python3 --version 2>&1)"
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
echo -e "  ${CYAN}Scripts:${NC}   $SCRIPT_COUNT installed  →  $SKILLS_DIR/reputation/scripts"
echo ""

# ---------------------------------------------------------------------------
# Command reference
# ---------------------------------------------------------------------------
echo -e "${BLUE}Command Reference:${NC}"
echo ""
echo -e "  ${CYAN}/reputation <business>${NC}            Full reputation audit (5 agents)"
echo -e "  ${CYAN}/reputation reviews <business>${NC}    Review analysis across platforms"
echo -e "  ${CYAN}/reputation sentiment <business>${NC}  Deep sentiment analysis"
echo -e "  ${CYAN}/reputation trends <business>${NC}     Reputation trajectory analysis"
echo -e "  ${CYAN}/reputation competitors <business>${NC} Competitor benchmarking"
echo -e "  ${CYAN}/reputation respond <business>${NC}    Generate review responses"
echo -e "  ${CYAN}/reputation crisis <situation>${NC}    Crisis response playbook"
echo -e "  ${CYAN}/reputation recover <review>${NC}      Review recovery strategy"
echo -e "  ${CYAN}/reputation request <business>${NC}    Review request campaigns"
echo -e "  ${CYAN}/reputation alerts <business>${NC}     Monitoring setup guide"
echo -e "  ${CYAN}/reputation social <business>${NC}     Social media reputation scan"
echo -e "  ${CYAN}/reputation seo <business>${NC}        Reputation SEO strategy"
echo -e "  ${CYAN}/reputation quick <business>${NC}      60-second scorecard"
echo -e "  ${CYAN}/reputation report-pdf${NC}            Professional PDF report"
echo ""
echo -e "  ${YELLOW}Tip:${NC} Start with ${CYAN}/reputation <business name>${NC} for a full reputation audit!"
echo ""
