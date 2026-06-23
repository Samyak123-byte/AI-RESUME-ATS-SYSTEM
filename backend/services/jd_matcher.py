import logging
from typing import Dict, List

import numpy as np
import spacy
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer

from backend.utils.matching import (
    fuzzy_match_keywords,
    normalize_skill,
)

logger = logging.getLogger("ats_resume_scorer")


# ==========================================================
# Semantic Similarity
# ==========================================================

def calculate_semantic_similarity(
    resume_text: str,
    jd_text: str,
    embedder: SentenceTransformer,
) -> float:
    """
    Calculate cosine similarity between resume and job description.
    Returns a score between 0 and 1.
    """

    if not resume_text or not jd_text:
        return 0.0

    try:
        resume_emb = embedder.encode(
            resume_text[:5000],
            convert_to_tensor=False,
        )

        jd_emb = embedder.encode(
            jd_text[:5000],
            convert_to_tensor=False,
        )

        resume_norm = np.linalg.norm(resume_emb)
        jd_norm = np.linalg.norm(jd_emb)

        if resume_norm == 0 or jd_norm == 0:
            return 0.0

        similarity = np.dot(resume_emb, jd_emb) / (
            resume_norm * jd_norm
        )

        return float(np.clip(similarity, 0.0, 1.0))

    except Exception as e:
        logger.exception(
            f"Semantic similarity calculation failed: {e}"
        )
        return 0.0


# ==========================================================
# Keyword Matching
# ==========================================================

def identify_matched_keywords(
    resume_keywords: List[str],
    jd_keywords: List[str],
) -> List[str]:

    if not resume_keywords or not jd_keywords:
        return []

    try:
        result = fuzzy_match_keywords(
            resume_keywords,
            jd_keywords,
            threshold=80,
        )

        return result.get("matched", [])

    except Exception as e:
        logger.exception(
            f"Keyword matching failed: {e}"
        )
        return []


def identify_missing_keywords(
    resume_keywords: List[str],
    jd_keywords: List[str],
    top_n: int = 15,
) -> List[str]:

    if not jd_keywords:
        return []

    try:
        result = fuzzy_match_keywords(
            resume_keywords,
            jd_keywords,
            threshold=80,
        )

        return result.get("missing", [])[:top_n]

    except Exception as e:
        logger.exception(
            f"Missing keyword calculation failed: {e}"
        )
        return []


# ==========================================================
# Skills Gap Analysis
# ==========================================================

def analyze_skills_gap(
    resume_skills: List[str],
    jd_text: str,
    nlp: spacy.Language,
) -> List[str]:

    if not jd_text:
        return []

    try:
        doc = nlp(jd_text[:5000])

        jd_skills = set()

        # Named entities
        for ent in doc.ents:

            if ent.label_ in (
                "PRODUCT",
                "ORG",
                "LANGUAGE",
            ):
                jd_skills.add(
                    ent.text.lower().strip()
                )

        # Noun phrases
        for chunk in doc.noun_chunks:

            text = chunk.text.lower().strip()

            if 1 <= len(text.split()) <= 4:
                jd_skills.add(text)

        resume_normalized = {
            normalize_skill(skill)
            for skill in resume_skills
            if skill
        }

        gap = []

        for jd_skill in jd_skills:

            jd_norm = normalize_skill(jd_skill)

            # Exact canonical match
            if jd_norm in resume_normalized:
                continue

            # Fuzzy match
            best_score = max(
                (
                    fuzz.token_sort_ratio(
                        jd_norm,
                        resume_skill,
                    )
                    for resume_skill in resume_normalized
                ),
                default=0,
            )

            if best_score < 75:
                gap.append(jd_skill)

        return sorted(set(gap))[:20]

    except Exception as e:
        logger.exception(
            f"Skill gap analysis failed: {e}"
        )
        return []


# ==========================================================
# Match Percentage
# ==========================================================

def calculate_match_percentage(
    resume_keywords: List[str],
    jd_keywords: List[str],
    semantic_similarity: float,
) -> float:

    if not jd_keywords:
        return 0.0

    matched = identify_matched_keywords(
        resume_keywords,
        jd_keywords,
    )

    keyword_overlap = (
        len(matched) / len(jd_keywords)
    )

    match_pct = (
        keyword_overlap * 0.6 +
        semantic_similarity * 0.4
    ) * 100

    return float(
        np.clip(match_pct, 0.0, 100.0)
    )


# ==========================================================
# Full JD Comparison
# ==========================================================

def compare_resume_with_jd(
    resume_text: str,
    resume_keywords: List[str],
    resume_skills: List[str],
    jd_text: str,
    jd_keywords: List[str],
    embedder: SentenceTransformer,
    nlp: spacy.Language,
) -> Dict:

    try:

        semantic_similarity = (
            calculate_semantic_similarity(
                resume_text=resume_text,
                jd_text=jd_text,
                embedder=embedder,
            )
        )

        matched_keywords = (
            identify_matched_keywords(
                resume_keywords,
                jd_keywords,
            )
        )

        missing_keywords = (
            identify_missing_keywords(
                resume_keywords,
                jd_keywords,
            )
        )

        skills_gap = analyze_skills_gap(
            resume_skills,
            jd_text,
            nlp,
        )

        match_percentage = (
            calculate_match_percentage(
                resume_keywords,
                jd_keywords,
                semantic_similarity,
            )
        )

        return {
            "match_percentage": match_percentage,
            "semantic_similarity": semantic_similarity,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "skills_gap": skills_gap,
        }

    except Exception as e:

        logger.exception(
            f"JD comparison failed: {e}"
        )

        return {
            "match_percentage": 0.0,
            "semantic_similarity": 0.0,
            "matched_keywords": [],
            "missing_keywords": [],
            "skills_gap": [],
        }