---
name: digital_human_factory
description: Enterprise Digital Human Factory for OpenClaw v2026.7.1. Generates 1080p vertical TikTok/Reels promotional videos, educational courses, and automated Q&A dialogue using Gemini 3.6 & 768-dimensional RAG vector formulas.
---

# Enterprise Digital Human Factory Skill — OpenClaw v2026.7.1

## Overview
This skill implements the **IA.INFINITEX GLOBAL Enterprise Digital Human Factory** architecture. It trains a master digital human once and generates unlimited 1080p promotional and educational videos automatically.

## Quick Start Pipeline
1. Convert input prompt to 768-dimensional mathematical RAG vector.
2. Retrieve Q&A context from `qa_500_vector_formulas.json`.
3. Synthesize bilingual audio using Gemini 2.0 Flash Live.
4. Render 9:16 vertical video with -20dB background music ducking.
5. Execute auto-commit and cloud sync (`pipeline-cierre.ps1`).

## Command Reference
```bash
python agents/financial_rag_worker/qa_vectorizer_500.py
python agents/video_agent/avatar_viral_generator.py "Cadena Cubana Oro 14k"
powershell -ExecutionPolicy Bypass -File .\scripts\pipeline-cierre.ps1
```
