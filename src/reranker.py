from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L6-v2"


class SemanticReranker:

    def __init__(self):
        self.model = CrossEncoder(
            MODEL_NAME
        )

    def rerank(
        self,
        question,
        candidates
    ):
        if not candidates:
            return []

        pairs = [
            [
                question,
                candidate["document"]
            ]
            for candidate in candidates
        ]

        scores = self.model.predict(
            pairs
        )

        ranked_candidates = []

        for candidate, score in zip(
            candidates,
            scores
        ):
            ranked_candidate = dict(
                candidate
            )

            ranked_candidate[
                "rerank_score"
            ] = float(score)

            ranked_candidates.append(
                ranked_candidate
            )

        ranked_candidates.sort(
            key=lambda item:
            item["rerank_score"],
            reverse=True
        )

        return ranked_candidates