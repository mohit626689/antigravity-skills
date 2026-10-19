#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# AI Restaurant Team — Claude Code Skill Installer
# Installs the AI-powered restaurant marketing & operations tool
# ============================================================

REPO_URL="https://github.com/mohit626689/ai-restaurant-claude.git"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"
INSTALL_DIR="${SKILLS_DIR}/restaurant"
TEMP_DIR=$(mktemp -d)

INTERACTIVE=true
if [ ! -t 0 ]; then
    INTERACTIVE=false
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${RED}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║   AI Restaurant Team — Installer              ║${NC}"
    echo -e "${RED}║   AI-Powered Restaurant Marketing & Audit     ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
print_error()   { echo -e "${RED}✗ $1${NC}"; }
print_info()    { echo -e "${BLUE}→ $1${NC}"; }

cleanup() { rm -rf "$TEMP_DIR"; }
trap cleanup EXIT

main() {
    print_header

    # ---- Check Prerequisites ----
    print_info "Checking prerequisites..."

    if ! command -v git &> /dev/null; then
        print_error "Git is required but not installed."
        echo "  Install: https://git-scm.com/downloads"
        exit 1
    fi
    print_success "Git found: $(git --version)"

    PYTHON_CMD=""
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        if [ -n "$PYTHON_VERSION" ]; then
            MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
            MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
            if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 8 ]; then
                PYTHON_CMD="python"
            fi
        fi
    fi

    if [ -z "$PYTHON_CMD" ]; then
        print_error "Python 3.8+ is required but not found."
        exit 1
    fi
    print_success "Python found: $($PYTHON_CMD --version)"

    if $PYTHON_CMD -c "import reportlab" 2>/dev/null; then
        print_success "reportlab found"
    else
        print_warning "reportlab not found — will attempt to install"
    fi

    if ! command -v claude &> /dev/null; then
        print_warning "Claude Code CLI not found in PATH."
        echo "  Install: npm install -g @anthropic-ai/claude-code"
        echo ""
        if [ "$INTERACTIVE" = true ]; then
            read -p "Continue installation anyway? (y/n): " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        else
            print_info "Non-interactive mode — continuing anyway..."
        fi
    else
        print_success "Claude Code CLI found"
    fi

    # ---- Create Directories ----
    print_info "Creating directories..."
    mkdir -p "$SKILLS_DIR" "$AGENTS_DIR" "$INSTALL_DIR" "$INSTALL_DIR/scripts"
    print_success "Directory structure created"

    # ---- Clone or Copy Repository ----
    print_info "Fetching AI Restaurant Team files..."

    SCRIPT_DIR=""
    if [ -n "${BASH_SOURCE[0]:-}" ] && [ "${BASH_SOURCE[0]}" != "bash" ]; then
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)" || true
    fi

    if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/restaurant/SKILL.md" ]; then
        print_info "Installing from local directory..."
        SOURCE_DIR="$SCRIPT_DIR"
    else
        print_info "Cloning from repository..."
        git clone --depth 1 "$REPO_URL" "$TEMP_DIR/repo" || {
            print_error "Failed to clone repository. Check your internet connection."
            exit 1
        }
        SOURCE_DIR="${TEMP_DIR}/repo"
    fi

    # ---- Install Main Skill ----
    print_info "Installing main orchestrator..."
    cp -r "$SOURCE_DIR/restaurant/"* "$INSTALL_DIR/"
    print_success "Main skill installed → ${INSTALL_DIR}/"

    # ---- Install Sub-Skills ----
    print_info "Installing sub-skills..."
    SKILL_COUNT=0
    for skill_dir in "$SOURCE_DIR/skills"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            target_dir="${SKILLS_DIR}/${skill_name}"
            mkdir -p "$target_dir"
            cp -r "$skill_dir"* "$target_dir/"
            SKILL_COUNT=$((SKILL_COUNT + 1))
            print_success "  ${skill_name}"
        fi
    done
    echo "  → ${SKILL_COUNT} sub-skills installed"

    # ---- Install Agents ----
    print_info "Installing subagents..."
    AGENT_COUNT=0
    for agent_file in "$SOURCE_DIR/agents/"*.md; do
        if [ -f "$agent_file" ]; then
            cp "$agent_file" "$AGENTS_DIR/"
            AGENT_COUNT=$((AGENT_COUNT + 1))
            print_success "  $(basename "$agent_file")"
        fi
    done
    echo "  → ${AGENT_COUNT} subagents installed"

    # ---- Install Scripts ----
    print_info "Installing utility scripts..."
    if [ -d "$SOURCE_DIR/scripts" ]; then
        cp -r "$SOURCE_DIR/scripts/"* "$INSTALL_DIR/scripts/"
        chmod +x "$INSTALL_DIR/scripts/"*.py 2>/dev/null || true
        print_success "Scripts installed → ${INSTALL_DIR}/scripts/"
    fi

    # ---- Install Python Dependencies ----
    print_info "Installing Python dependencies..."
    if [ -f "$SOURCE_DIR/requirements.txt" ]; then
        $PYTHON_CMD -m pip install -r "$SOURCE_DIR/requirements.txt" --quiet 2>/dev/null && {
            print_success "Python dependencies installed (reportlab)"
        } || {
            print_warning "Some Python dependencies failed to install."
            echo "  Run manually: $PYTHON_CMD -m pip install reportlab"
            cp "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/"
        }
    fi

    # ---- Verify Installation ----
    echo ""
    print_info "Verifying installation..."

    [ -f "$INSTALL_DIR/SKILL.md" ] && print_success "Main skill file" || print_error "Main skill file missing"
    [ -d "$SKILLS_DIR/restaurant-audit" ] && print_success "Sub-skills directory" || print_error "Sub-skills missing"
    [ "$(ls "$AGENTS_DIR"/restaurant-*.md 2>/dev/null | wc -l)" -gt 0 ] && print_success "Agent files" || print_warning "No agent files found"
    [ -d "$INSTALL_DIR/scripts" ] && print_success "Utility scripts" || print_error "Scripts missing"

    if $PYTHON_CMD -c "import reportlab" 2>/dev/null; then
        print_success "reportlab available for PDF generation"
    else
        print_warning "reportlab not available — PDF reports won't work until installed"
        echo "  Install: $PYTHON_CMD -m pip install reportlab"
    fi

    # ---- Summary ----
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║          Installation Complete!               ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
    echo ""
    echo "  Installed to: ${INSTALL_DIR}"
    echo "  Skills:       ${SKILL_COUNT} sub-skills"
    echo "  Agents:       ${AGENT_COUNT} subagents"
    echo ""
    echo -e "${CYAN}Quick Start:${NC}"
    echo "  Open Claude Code and try:"
    echo ""
    echo "    /restaurant audit Bella Italia Trattoria"
    echo "    /restaurant quick The French Laundry"
    echo "    /restaurant reviews Joe's Pizza"
    echo ""
    echo -e "${CYAN}Command Reference:${NC}"
    echo "    /restaurant audit <name>         Full audit (5 parallel agents)"
    echo "    /restaurant quick <name>         60-second snapshot"
    echo "    /restaurant reviews <name>       Multi-platform review analysis"
    echo "    /restaurant respond <name>       Generate review responses"
    echo "    /restaurant menu <url>           Menu engineering analysis"
    echo "    /restaurant pricing <name>       Competitive pricing analysis"
    echo "    /restaurant online <name>        Online presence audit"
    echo "    /restaurant photos <name>        Food photography audit"
    echo "    /restaurant social <name>        30-day social calendar"
    echo "    /restaurant local-seo <name>     Local SEO audit"
    echo "    /restaurant ads <name>           Facebook/Instagram ad copy"
    echo "    /restaurant email <name>         Email & SMS sequences"
    echo "    /restaurant competitors <name>   Top 5 competitor analysis"
    echo "    /restaurant report-pdf           Generate PDF report"
    echo ""
    echo "  Documentation: https://github.com/mohit626689/ai-restaurant-claude"
    echo ""
}

main "$@"
