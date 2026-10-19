"""acq: shared engine for evidence-first client acquisition playbooks.

Deterministic, standard-library only. It makes no LLM calls: writing messages and building samples is done
by the Antigravity agent following the acq* SKILL.md files, and the engine validates the results.
"""

__version__ = "0.1.0"
