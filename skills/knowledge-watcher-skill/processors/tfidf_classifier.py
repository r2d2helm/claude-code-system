#!/usr/bin/env python3
"""Classificateur TF-IDF pour Knowledge Watcher.

Remplace/augmente le classifieur rule-based (Classifier.ps1) avec une
approche statistique entrainee sur les notes existantes du vault.

Pipeline:
1. Entraine sur les notes vault (frontmatter type = label)
2. Classe les nouveaux fichiers par similarite cosinus
3. Fallback vers rules.json si confiance < seuil

Usage CLI:
    python tfidf_classifier.py train                    # Entraine le modele
    python tfidf_classifier.py classify <fichier>       # Classe un fichier
    python tfidf_classifier.py classify <fichier> --json # Sortie JSON

Usage Python:
    from tfidf_classifier import TfidfClassifier
    clf = TfidfClassifier()
    clf.load_model()  # ou clf.train(vault_path)
    result = clf.classify("contenu du fichier")
"""

import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ============================================================
# Configuration
# ============================================================

_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_DIR = _SCRIPT_DIR.parent
_DATA_DIR = _SKILL_DIR / "data"
_CONFIG_DIR = _SKILL_DIR / "config"

MODEL_PATH = _DATA_DIR / "tfidf-model.json"
RULES_PATH = _CONFIG_DIR / "rules.json"

# Categories valides (doivent correspondre aux types frontmatter)
VALID_CATEGORIES = {
    "conversation", "code", "concept", "troubleshooting",
    "project", "reference", "formation", "daily", "note",
}

# Seuil de confiance minimum pour accepter la prediction TF-IDF
CONFIDENCE_THRESHOLD = 0.08

# Max termes par centroid categorie (evite les centroids enormes)
MAX_CENTROID_TERMS = 500

# Min document frequency pour inclure un terme dans IDF
MIN_DOC_FREQ = 3

# Stopwords compacts (FR + EN essentiels)
STOPWORDS = {
    # FR
    "le", "la", "les", "de", "du", "des", "un", "une", "et", "en",
    "est", "que", "qui", "dans", "pour", "pas", "sur", "avec", "ce",
    "cette", "il", "elle", "je", "nous", "vous", "sont", "mais", "ou",
    "donc", "ni", "car", "par", "plus", "tout", "fait", "etre", "avoir",
    "faire", "comme", "aussi",
    # EN
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "have",
    "has", "had", "do", "does", "did", "will", "would", "could", "should",
    "can", "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "and", "but", "or", "not", "no", "if", "then", "so",
    "than", "too", "very", "just", "about", "this", "that", "these",
    "those", "it", "its", "me", "my", "we", "our", "you", "your",
    "he", "she", "they", "them", "their", "what", "which", "who",
    "when", "where", "how", "all", "each", "every", "both", "few",
    "more", "most", "other", "some", "such", "only", "own", "same",
    "here", "there", "file", "use", "using", "used", "need", "now",
    "get", "got", "make", "made", "let", "want",
}


# ============================================================
# Tokenizer
# ============================================================

_TOKEN_RE = re.compile(r"[^\W\d_]{3,}", re.UNICODE)


def tokenize(text: str) -> list[str]:
    """Tokenize: mots unicode >= 3 chars, lowercased, sans stopwords."""
    return [
        w.lower()
        for w in _TOKEN_RE.findall(text)
        if w.lower() not in STOPWORDS and len(w) >= 3
    ]


# ============================================================
# TF-IDF Classifier
# ============================================================

class TfidfClassifier:
    """Classificateur TF-IDF leger, zero-dependance externe."""

    def __init__(self, model_path: str | Path | None = None):
        self.model_path = Path(model_path) if model_path else MODEL_PATH
        self.idf: dict[str, float] = {}
        self.centroids: dict[str, dict[str, float]] = {}
        self.categories: list[str] = []
        self.doc_counts: dict[str, int] = {}
        self.trained = False

    # --- Training ---

    def train(self, vault_path: str | Path) -> dict:
        """Entraine le modele sur les notes du vault.

        Returns:
            dict avec stats d'entrainement (categories, docs, terms)
        """
        vault = Path(vault_path)
        if not vault.exists():
            return {"error": "Vault path not found", "trained": False}

        docs_by_cat: dict[str, list[list[str]]] = defaultdict(list)

        for md_file in vault.rglob("*.md"):
            # Skip systeme
            rel = md_file.relative_to(vault)
            parts = rel.parts
            if any(p.startswith((".", "_")) for p in parts):
                continue

            note_type, content = self._extract_type_and_content(md_file)
            if not note_type or not content:
                continue
            if note_type not in VALID_CATEGORIES:
                continue

            tokens = tokenize(content)
            if len(tokens) < 10:  # Trop court pour etre significatif
                continue

            docs_by_cat[note_type].append(tokens)

        if not docs_by_cat:
            return {"error": "No valid training documents found", "trained": False}

        # Compute IDF
        all_doc_tokens: list[set[str]] = []
        for cat_docs in docs_by_cat.values():
            for tokens in cat_docs:
                all_doc_tokens.append(set(tokens))

        total_docs = len(all_doc_tokens)
        term_doc_count: Counter = Counter()
        for doc_set in all_doc_tokens:
            for term in doc_set:
                term_doc_count[term] += 1

        # IDF = log(N / (1 + df)) - garder termes presents dans >= MIN_DOC_FREQ docs
        self.idf = {}
        for term, df in term_doc_count.items():
            if df >= MIN_DOC_FREQ:
                self.idf[term] = math.log(total_docs / (1 + df))

        # Compute centroids (average TF-IDF per category)
        # Limiter chaque centroid a ses top MAX_CENTROID_TERMS termes
        self.centroids = {}
        self.doc_counts = {}
        for cat, cat_docs in docs_by_cat.items():
            centroid: dict[str, float] = defaultdict(float)
            for tokens in cat_docs:
                tf = self._compute_tf(tokens)
                for term, tf_val in tf.items():
                    if term in self.idf:
                        centroid[term] += tf_val * self.idf[term]

            n = len(cat_docs)
            scored = {
                term: score / n
                for term, score in centroid.items()
                if score / n > 0.0005
            }

            # Keep top N terms per centroid
            if len(scored) > MAX_CENTROID_TERMS:
                top = sorted(scored.items(), key=lambda x: -x[1])[:MAX_CENTROID_TERMS]
                scored = dict(top)

            self.centroids[cat] = scored
            self.doc_counts[cat] = n

        self.categories = sorted(docs_by_cat.keys())
        self.trained = True

        stats = {
            "trained": True,
            "total_docs": total_docs,
            "categories": {cat: len(docs) for cat, docs in docs_by_cat.items()},
            "vocabulary_size": len(self.idf),
            "model_path": str(self.model_path),
        }

        self.save_model()
        return stats

    # --- Classification ---

    def classify(self, content: str, source_path: str = "") -> dict:
        """Classe un contenu texte.

        Returns:
            {"type": str, "confidence": float, "method": str, "scores": dict}
        """
        # TF-IDF prediction
        tfidf_result = self._classify_tfidf(content) if self.trained else None

        # Rules-based fallback
        rules_result = self._classify_rules(content, source_path)

        # Decision: TF-IDF si confiance suffisante, sinon rules
        if tfidf_result and tfidf_result["confidence"] >= CONFIDENCE_THRESHOLD:
            result = tfidf_result
            result["method"] = "tfidf"
            result["rules_type"] = rules_result.get("type", "note")
        else:
            result = rules_result
            result["method"] = "rules"
            if tfidf_result:
                result["tfidf_type"] = tfidf_result.get("type", "?")
                result["tfidf_confidence"] = tfidf_result.get("confidence", 0)

        # Auto-tags (toujours appliques)
        result["auto_tags"] = self._compute_auto_tags(content)

        return result

    def _classify_tfidf(self, content: str) -> dict | None:
        """Classification TF-IDF pure."""
        if not self.trained or not self.centroids:
            return None

        tokens = tokenize(content)
        if len(tokens) < 5:
            return None

        tf = self._compute_tf(tokens)
        doc_tfidf = {
            term: tf_val * self.idf.get(term, 0)
            for term, tf_val in tf.items()
            if term in self.idf
        }

        if not doc_tfidf:
            return None

        scores = {}
        for cat, centroid in self.centroids.items():
            scores[cat] = self._cosine_similarity(doc_tfidf, centroid)

        if not scores:
            return None

        best_type = max(scores, key=scores.get)
        return {
            "type": best_type,
            "confidence": round(scores[best_type], 4),
            "scores": {
                k: round(v, 4)
                for k, v in sorted(scores.items(), key=lambda x: -x[1])
            },
        }

    def _classify_rules(self, content: str, source_path: str = "") -> dict:
        """Classification rule-based (fallback, lit rules.json)."""
        try:
            if not RULES_PATH.exists():
                return self._default_result()

            rules_data = json.loads(RULES_PATH.read_text(encoding="utf-8"))
            rules = rules_data.get("classification", {}).get("rules", [])

            content_lower = content.lower()
            ext = Path(source_path).suffix.lower() if source_path else ""

            for rule in sorted(rules, key=lambda r: -r.get("priority", 0)):
                conditions = rule.get("conditions", {})

                if conditions.get("always"):
                    return self._rule_output(rule)

                any_conds = conditions.get("any", [])
                for cond in any_conds:
                    field = cond.get("field", "")
                    if field == "source" and cond.get("contains", "") in source_path:
                        return self._rule_output(rule)
                    if field == "content":
                        if "contains" in cond and cond["contains"].lower() in content_lower:
                            return self._rule_output(rule)
                        if "containsAny" in cond:
                            if any(kw.lower() in content_lower for kw in cond["containsAny"]):
                                return self._rule_output(rule)
                    if field == "extension" and cond.get("equals", "") == ext:
                        return self._rule_output(rule)
                    if field == "path":
                        if cond.get("contains", "") in source_path:
                            return self._rule_output(rule)

        except Exception:
            pass

        return self._default_result()

    # --- Auto-tagging ---

    def _compute_auto_tags(self, content: str) -> list[str]:
        """Calcule les auto-tags depuis rules.json."""
        tags = []
        try:
            if not RULES_PATH.exists():
                return tags
            rules_data = json.loads(RULES_PATH.read_text(encoding="utf-8"))
            auto_tags = rules_data.get("tagging", {}).get("autoTags", [])

            content_lower = content.lower()
            for tag_rule in auto_tags:
                pattern = tag_rule.get("pattern", "")
                if pattern and re.search(pattern, content_lower):
                    tags.append(tag_rule["tag"])
        except Exception:
            pass
        return tags

    # --- Model persistence ---

    def save_model(self, path: str | Path | None = None) -> bool:
        """Sauvegarde le modele en JSON."""
        target = Path(path) if path else self.model_path
        if not self.trained:
            return False

        try:
            # Only store IDF terms that appear in at least one centroid
            used_terms = set()
            for centroid in self.centroids.values():
                used_terms.update(centroid.keys())
            compact_idf = {t: v for t, v in self.idf.items() if t in used_terms}

            data = {
                "version": "1.1",
                "categories": self.categories,
                "doc_counts": self.doc_counts,
                "idf_size": len(self.idf),
                "idf_stored": len(compact_idf),
                "idf": compact_idf,
                "centroids": self.centroids,
            }
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            return True
        except Exception:
            return False

    def load_model(self, path: str | Path | None = None) -> bool:
        """Charge un modele pre-entraine."""
        target = Path(path) if path else self.model_path
        if not target.exists():
            return False

        try:
            data = json.loads(target.read_text(encoding="utf-8"))
            self.categories = data["categories"]
            self.doc_counts = data.get("doc_counts", {})
            self.idf = data["idf"]
            self.centroids = data["centroids"]
            self.trained = True
            return True
        except Exception:
            return False

    # --- Helpers ---

    @staticmethod
    def _compute_tf(tokens: list[str]) -> dict[str, float]:
        """Term Frequency: count / total."""
        counts = Counter(tokens)
        total = sum(counts.values())
        if total == 0:
            return {}
        return {t: c / total for t, c in counts.items()}

    @staticmethod
    def _cosine_similarity(vec_a: dict, vec_b: dict) -> float:
        """Cosine similarity entre deux vecteurs sparse."""
        common = set(vec_a.keys()) & set(vec_b.keys())
        if not common:
            return 0.0

        dot = sum(vec_a[t] * vec_b[t] for t in common)
        norm_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
        norm_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))

        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    @staticmethod
    def _extract_type_and_content(md_file: Path) -> tuple[str | None, str | None]:
        """Extrait le type (frontmatter) et le contenu d'une note."""
        try:
            text = md_file.read_text(encoding="utf-8", errors="replace")
            if not text.startswith("---"):
                return None, None

            end = text.find("---", 3)
            if end < 0:
                return None, None

            frontmatter = text[3:end]
            content = text[end + 3:]

            note_type = None
            for line in frontmatter.split("\n"):
                stripped = line.strip()
                if stripped.startswith("type:"):
                    val = stripped.split(":", 1)[1].strip().strip("\"'")
                    note_type = val
                    break

            return note_type, content.strip() if content.strip() else None
        except Exception:
            return None, None

    @staticmethod
    def _rule_output(rule: dict) -> dict:
        """Convertit un rule match en resultat standardise."""
        output = rule.get("output", {})
        return {
            "type": output.get("type", "note"),
            "confidence": 1.0,
            "folder": output.get("folder", "_Inbox"),
            "prefix": output.get("prefix", "{date}_"),
            "template": output.get("template"),
            "tags": output.get("tags", []),
        }

    @staticmethod
    def _default_result() -> dict:
        return {
            "type": "note",
            "confidence": 0.0,
            "folder": "_Inbox",
            "prefix": "{date}_",
            "template": None,
            "tags": ["inbox"],
        }


# ============================================================
# Folder resolution (replaces Classifier.ps1 folder logic)
# ============================================================

def resolve_folder(classification: dict, source_path: str = "") -> dict:
    """Resout le dossier cible et le prefix a partir de la classification.

    Enrichit le dict classification avec folder et prefix resolus.
    """
    from datetime import datetime

    note_type = classification.get("type", "note")
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Mapping type -> folder (defaut)
    type_folders = {
        "conversation": "Conversations",
        "code": "Code",
        "concept": "Concepts",
        "troubleshooting": "Références/Troubleshooting",
        "project": "Projets",
        "reference": "Références",
        "formation": "Formations",
        "daily": "_Daily",
        "note": "_Inbox",
    }

    # Prefix mapping
    type_prefixes = {
        "conversation": f"{date_str}_Conv_",
        "code": f"{date_str}_",
        "concept": "C_",
        "troubleshooting": f"{date_str}_Fix_",
        "project": f"{date_str}_",
        "reference": f"{date_str}_",
        "formation": f"{date_str}_",
        "daily": "",
        "note": f"{date_str}_",
    }

    folder = classification.get("folder", type_folders.get(note_type, "_Inbox"))
    prefix = classification.get("prefix", type_prefixes.get(note_type, f"{date_str}_"))

    # Resolve template variables
    folder = folder.replace("{date}", date_str)
    prefix = prefix.replace("{date}", date_str)

    # Project name extraction
    if "{projectName}" in folder:
        project_name = "Unknown"
        for part in Path(source_path).parts:
            if part not in (".", "..", "Projets", "Projects"):
                project_name = part
                break
        folder = folder.replace("{projectName}", project_name)

    classification["folder"] = folder
    classification["prefix"] = prefix
    return classification


# ============================================================
# CLI
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tfidf_classifier.py train [vault_path]")
        print("  python tfidf_classifier.py classify <file> [--json]")
        print("  python tfidf_classifier.py info")
        sys.exit(1)

    command = sys.argv[1]
    clf = TfidfClassifier()

    if command == "train":
        # Vault path from arg or config
        vault_path = sys.argv[2] if len(sys.argv) > 2 else None
        if not vault_path:
            try:
                config = json.loads(
                    (_CONFIG_DIR / "config.json").read_text(encoding="utf-8")
                )
                vault_path = config.get("paths", {}).get("obsidianVault", "")
            except Exception:
                pass

        if not vault_path:
            print("ERROR: No vault path. Usage: train <vault_path>")
            sys.exit(1)

        print(f"Training on: {vault_path}")
        stats = clf.train(vault_path)
        if stats.get("trained"):
            print(f"Model trained successfully:")
            print(f"  Documents: {stats['total_docs']}")
            print(f"  Categories: {stats['categories']}")
            print(f"  Vocabulary: {stats['vocabulary_size']} terms")
            print(f"  Saved to: {stats['model_path']}")
        else:
            print(f"Training failed: {stats.get('error', 'unknown')}")
            sys.exit(1)

    elif command == "classify":
        if len(sys.argv) < 3:
            print("Usage: classify <file> [--json]")
            sys.exit(1)

        file_path = sys.argv[2]
        json_output = "--json" in sys.argv

        # Load model (or classify rules-only)
        clf.load_model()

        try:
            content = Path(file_path).read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"ERROR: Cannot read file: {e}")
            sys.exit(1)

        result = clf.classify(content, source_path=file_path)
        result = resolve_folder(result, source_path=file_path)

        if json_output:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Type:       {result['type']}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Method:     {result['method']}")
            print(f"Folder:     {result['folder']}")
            print(f"Tags:       {', '.join(result.get('tags', []) + result.get('auto_tags', []))}")
            if result.get("scores"):
                print("Scores:")
                for cat, score in list(result["scores"].items())[:5]:
                    bar = "#" * int(score * 40)
                    print(f"  {cat:.<20} {score:.4f} {bar}")

    elif command == "info":
        if clf.load_model():
            print(f"Model loaded: {clf.model_path}")
            print(f"Categories: {clf.categories}")
            print(f"Documents: {clf.doc_counts}")
            print(f"Vocabulary: {len(clf.idf)} terms")
        else:
            print("No trained model found.")
            print(f"Expected at: {MODEL_PATH}")
            print("Run: python tfidf_classifier.py train")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
