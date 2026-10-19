#!/usr/bin/env bash
# AI Personal Finance Advisor - Installer
# Repo: mohit626689/ai-finance-claude
#
# Local install:  ./install.sh
# Remote install: curl -fsSL https://raw.githubusercontent.com/mohit626689/ai-finance-claude/main/install.sh | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

REPO="mohit626689/ai-finance-claude"
BRANCH="main"
RAW_BASE="https://raw.githubusercontent.com/${REPO}/${BRANCH}"
TARBALL_URL="https://github.com/${REPO}/archive/refs/heads/${BRANCH}.tar.gz"

CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"

# Detect local vs remote install
SCRIPT_PATH="${BASH_SOURCE[0]:-}"
IS_LOCAL=0
SOURCE_DIR=""

if [ -n "$SCRIPT_PATH" ] && [ -f "$SCRIPT_PATH" ]; then
  SOURCE_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
  if [ -d "${SOURCE_DIR}/skills" ] && [ -d "${SOURCE_DIR}/finance" ]; then
    IS_LOCAL=1
  fi
fi

print_banner() {
  echo ""
  echo -e "${BOLD}${YELLOW}╔══════════════════════════════════════════════════════════╗${NC}"
  echo -e "${BOLD}${YELLOW}║                                                          ║${NC}"
  echo -e "${BOLD}${YELLOW}║       AI PERSONAL FINANCE ADVISOR — Installer            ║${NC}"
  echo -e "${BOLD}${YELLOW}║       AI-Powered Financial Planning for Claude Code      ║${NC}"
  echo -e "${BOLD}${YELLOW}║                                                          ║${NC}"
  echo -e "${BOLD}${YELLOW}╚══════════════════════════════════════════════════════════╝${NC}"
  echo ""
}

err() {
  echo -e "${RED}✗ $1${NC}" >&2
}

ok() {
  echo -e "${GREEN}✓${NC} $1"
}

info() {
  echo -e "${BLUE}ℹ${NC} $1"
}

warn() {
  echo -e "${YELLOW}⚠${NC} $1"
}

check_python() {
  if ! command -v python3 >/dev/null 2>&1; then
    err "Python 3 not found. Please install Python 3.8 or later."
    return 1
  fi

  local pyver
  pyver=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
  local major minor
  major=$(echo "$pyver" | cut -d. -f1)
  minor=$(echo "$pyver" | cut -d. -f2)

  if [ "$major" -lt 3 ] || { [ "$major" -eq 3 ] && [ "$minor" -lt 8 ]; }; then
    err "Python 3.8+ required (found ${pyver})."
    return 1
  fi

  ok "Python ${pyver} detected"
  return 0
}

check_reportlab() {
  if python3 -c "import reportlab" >/dev/null 2>&1; then
    local rlver
    rlver=$(python3 -c "import reportlab; print(reportlab.Version)")
    ok "ReportLab ${rlver} detected"
    return 0
  fi

  warn "ReportLab not installed. Attempting to install..."
  if pip3 install --quiet --user "reportlab>=4.0.0" 2>/dev/null \
    || python3 -m pip install --quiet --user "reportlab>=4.0.0" 2>/dev/null; then
    ok "ReportLab installed"
    return 0
  fi

  warn "Could not auto-install ReportLab. Install manually with:"
  echo "    pip3 install 'reportlab>=4.0.0'"
  return 0
}

fetch_remote() {
  info "Downloading repo tarball..."
  local tmp
  tmp=$(mktemp -d)
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$TARBALL_URL" | tar -xz -C "$tmp"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO- "$TARBALL_URL" | tar -xz -C "$tmp"
  else
    err "Neither curl nor wget found."
    exit 1
  fi
  # archive name: ai-finance-claude-main
  SOURCE_DIR="${tmp}/ai-finance-claude-${BRANCH}"
  if [ ! -d "$SOURCE_DIR" ]; then
    err "Tarball extraction failed: ${SOURCE_DIR} not found."
    exit 1
  fi
  ok "Repo downloaded to ${SOURCE_DIR}"
}

install_orchestrator() {
  local src="${SOURCE_DIR}/finance"
  if [ ! -d "$src" ]; then
    warn "No orchestrator folder at ${src}, skipping."
    return
  fi
  mkdir -p "${SKILLS_DIR}/finance"
  cp -R "${src}/." "${SKILLS_DIR}/finance/"
  ok "Installed orchestrator → ~/.claude/skills/finance/"
}

install_skills() {
  local src="${SOURCE_DIR}/skills"
  if [ ! -d "$src" ]; then
    warn "No skills/ folder at ${src}, skipping."
    return
  fi
  local count=0
  for dir in "$src"/*/; do
    [ -d "$dir" ] || continue
    local name
    name=$(basename "$dir")
    mkdir -p "${SKILLS_DIR}/${name}"
    cp -R "${dir}." "${SKILLS_DIR}/${name}/"
    count=$((count + 1))
  done
  ok "Installed ${count} sub-skills → ~/.claude/skills/finance-*/"
}

install_agents() {
  local src="${SOURCE_DIR}/agents"
  if [ ! -d "$src" ]; then
    warn "No agents/ folder at ${src}, skipping."
    return
  fi
  mkdir -p "${AGENTS_DIR}"
  local count=0
  for file in "$src"/*.md; do
    [ -f "$file" ] || continue
    cp "$file" "${AGENTS_DIR}/"
    count=$((count + 1))
  done
  if [ "$count" -gt 0 ]; then
    ok "Installed ${count} agents → ~/.claude/agents/"
  else
    info "No agents to install."
  fi
}

install_scripts() {
  local src="${SOURCE_DIR}/scripts"
  if [ ! -d "$src" ]; then
    warn "No scripts/ folder at ${src}, skipping."
    return
  fi
  mkdir -p "${SKILLS_DIR}/finance/scripts"
  cp -R "${src}/." "${SKILLS_DIR}/finance/scripts/"
  chmod +x "${SKILLS_DIR}/finance/scripts/"*.py 2>/dev/null || true
  ok "Installed scripts → ~/.claude/skills/finance/scripts/"
}

print_summary() {
  local skill_count agent_count
  skill_count=$(find "${SKILLS_DIR}" -maxdepth 1 -type d -name "finance*" 2>/dev/null | wc -l | tr -d ' ')
  agent_count=$(find "${AGENTS_DIR}" -maxdepth 1 -type f -name "finance-*.md" 2>/dev/null | wc -l | tr -d ' ')

  echo ""
  echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
  echo -e "${BOLD}${GREEN}║              INSTALLATION COMPLETE                       ║${NC}"
  echo -e "${BOLD}${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
  echo ""
  echo -e "${BOLD}Installed:${NC}"
  echo -e "  ${GREEN}•${NC} ${skill_count} skill folder(s) under ~/.claude/skills/"
  echo -e "  ${GREEN}•${NC} ${agent_count} agent file(s) under ~/.claude/agents/"
  echo ""
  echo -e "${BOLD}${CYAN}Command Reference:${NC}"
  echo -e "  ${MAGENTA}/finance${NC}             — Main orchestrator (full plan + PDF)"
  echo -e "  ${MAGENTA}/finance-quick${NC}       — 60-second financial snapshot"
  echo -e "  ${MAGENTA}/finance-analyze${NC}     — Full multi-agent analysis"
  echo -e "  ${MAGENTA}/finance-budget${NC}      — Cash flow & budget analysis"
  echo -e "  ${MAGENTA}/finance-debt${NC}        — Debt payoff strategy (avalanche/snowball)"
  echo -e "  ${MAGENTA}/finance-emergency${NC}   — Emergency fund target & plan"
  echo -e "  ${MAGENTA}/finance-portfolio${NC}   — Investment allocation review"
  echo -e "  ${MAGENTA}/finance-retirement${NC}  — Retirement projections"
  echo -e "  ${MAGENTA}/finance-fire${NC}        — FIRE (Financial Independence) calculator"
  echo -e "  ${MAGENTA}/finance-taxes${NC}       — Tax optimization opportunities"
  echo -e "  ${MAGENTA}/finance-networth${NC}    — Net worth tracker"
  echo -e "  ${MAGENTA}/finance-goals${NC}       — Goal-based planning"
  echo -e "  ${MAGENTA}/finance-compare${NC}     — Compare scenarios side-by-side"
  echo -e "  ${MAGENTA}/finance-screen${NC}      — Financial product screener"
  echo -e "  ${MAGENTA}/finance-report-pdf${NC}  — Generate the PDF report"
  echo ""
  echo -e "${BOLD}${CYAN}Quick start:${NC} open Claude Code and type ${MAGENTA}/finance${NC}"
  echo ""
  echo -e "${YELLOW}⚠  This is NOT financial advice. Consult a licensed financial advisor.${NC}"
  echo ""
}

main() {
  print_banner

  info "Detecting environment..."
  if [ "$IS_LOCAL" -eq 1 ]; then
    ok "Local install detected (source: ${SOURCE_DIR})"
  else
    info "Remote install (curl | bash) detected"
    fetch_remote
  fi

  echo ""
  info "Checking prerequisites..."
  check_python || exit 1
  check_reportlab

  echo ""
  info "Creating Claude directories..."
  mkdir -p "${SKILLS_DIR}" "${AGENTS_DIR}"
  ok "~/.claude/skills/ and ~/.claude/agents/ ready"

  echo ""
  info "Installing components..."
  install_orchestrator
  install_skills
  install_agents
  install_scripts

  print_summary
}

main "$@"
