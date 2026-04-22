from pipeline import EntrepreneurshipAssistant


def main() -> None:
    assistant = EntrepreneurshipAssistant(base_dir=".")
    questions = [
        "How should I validate market demand before opening a small cafe?",
        "How do I write an executable business plan in the early stage?",
        "With a limited budget, which marketing channels should I prioritize first?",
        "How can I tell whether my product has PMF?",
        "What are the most common first-year failure reasons for startups?",
    ]

    print("=== 5-Question Functional Check ===")
    functional_pass = True

    for i, q in enumerate(questions, 1):
        result = assistant.answer_query(q, top_k=5)
        evidence_n = len(result.get("evidence", []))
        next_n = len(result.get("next_questions", []))
        ans_len = len(result.get("answer", ""))
        ok = evidence_n >= 2 and next_n == 3 and ans_len > 0
        functional_pass = functional_pass and ok
        print(
            f"Q{i}: topic={result.get('topic')} conf={result.get('confidence')} "
            f"evidence={evidence_n} next_q={next_n} answer_len={ans_len} ok={ok}"
        )

    print("=== 10-Round Stability Check ===")
    stable = True
    try:
        for _ in range(2):
            for q in questions:
                _ = assistant.answer_query(q, top_k=5)
        print("PASS_10_ROUNDS")
    except Exception as exc:
        stable = False
        print(f"FAIL_10_ROUNDS: {exc}")

    print(
        "SUMMARY "
        f"functional={'PASS' if functional_pass else 'FAIL'} "
        f"stability={'PASS' if stable else 'FAIL'}"
    )


if __name__ == "__main__":
    main()
