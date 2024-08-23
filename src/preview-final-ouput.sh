#!/usr/bin/env bash
ls final_output/*.txt | fzf --preview 'mdless {} 2>/dev/null'
