"""Tests pour prompt_analyzer.py — classify_message, skill/keyword detection."""

import re

import pytest

from prompt_analyzer import (
    SKILL_COMMAND_RE,
    TECHNICAL_KEYWORDS,
    QUESTION_STARTERS,
    classify_message,
)


class TestClassifyMessage:
    # --- Commands ---
    def test_command_slash(self):
        assert classify_message("/dk-status") == "command"

    def test_command_with_args(self):
        assert classify_message("/know-save mon concept") == "command"

    # --- Questions ---
    def test_question_mark(self):
        assert classify_message("What is Docker?") == "question"

    def test_question_fr_comment(self):
        assert classify_message("comment configurer Proxmox") == "question"

    def test_question_fr_pourquoi(self):
        assert classify_message("pourquoi le service crash") == "question"

    def test_question_en_how(self):
        assert classify_message("how to deploy containers") == "question"

    # --- Debug ---
    def test_debug_fix(self):
        assert classify_message("fix the import error") == "debug"

    def test_debug_traceback(self):
        assert classify_message("I see a traceback in the logs") == "debug"

    def test_debug_error_keyword(self):
        assert classify_message("there is an error in path_guard") == "debug"

    def test_debug_bug(self):
        assert classify_message("found a bug in the router") == "debug"

    # --- Instruction (default) ---
    def test_instruction_simple(self):
        assert classify_message("create a new skill for networking") == "instruction"

    def test_instruction_imperative(self):
        assert classify_message("deploy the container to production") == "instruction"

    # --- Edge cases ---
    def test_empty_message(self):
        assert classify_message("") == "instruction"

    def test_whitespace_only(self):
        assert classify_message("   ") == "instruction"


class TestSkillDetection:
    def test_single_skill(self):
        matches = SKILL_COMMAND_RE.findall("/dk-status")
        assert "dk-status" in matches

    def test_multiple_skills(self):
        matches = SKILL_COMMAND_RE.findall("/know-save and /obs-health")
        assert "know-save" in matches
        assert "obs-health" in matches

    def test_no_skill(self):
        matches = SKILL_COMMAND_RE.findall("just a normal sentence")
        assert matches == []

    def test_skill_in_sentence(self):
        matches = SKILL_COMMAND_RE.findall("run /guardian-fix on the vault")
        assert "guardian-fix" in matches


class TestKeywordDetection:
    def test_docker_detected(self):
        msg = "deploy the docker container"
        keywords = [kw for kw in TECHNICAL_KEYWORDS if kw in msg.lower()]
        assert "docker" in keywords
        assert "deploy" in keywords
        assert "container" in keywords

    def test_no_keywords(self):
        msg = "hello world"
        keywords = [kw for kw in TECHNICAL_KEYWORDS if kw in msg.lower()]
        assert keywords == []

    def test_proxmox_cluster(self):
        msg = "configure the proxmox cluster with ceph"
        keywords = [kw for kw in TECHNICAL_KEYWORDS if kw in msg.lower()]
        assert "proxmox" in keywords
        assert "cluster" in keywords
        assert "ceph" in keywords
