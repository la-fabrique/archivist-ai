#!/bin/bash
# Fires at end of Claude session — reminds to run simplify + harness-cleaner
# when on a feature branch (superpowers dev cycle in progress or just finished).
branch=$(git branch --show-current 2>/dev/null)
if [ -n "$branch" ] && [ "$branch" != "main" ]; then
    echo '{"systemMessage": "Dev cycle reminder: invoke /simplify on changed code, then launch the harness-cleaner agent to archive plans and harvest learnings."}'
fi
