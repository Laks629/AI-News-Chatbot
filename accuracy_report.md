# AI News Chatbot — Accuracy Report

---

## **Purpose**

This document summarizes the practical performance of the AI News Trend Chatbot prototype.  
It measures how well the semantic search matches user queries with **relevant headlines**.

---

## **Method**

- **10 queries** tested, covering:
  - Direct topical queries (`AI in India`, `AI ethics`)
  - Sector trends (`AI in farming`, `Gaming development with AI`)
  - Edge/ambiguous topics (`XAI`, `Smart toys`)
- For each, the **Top 5 results** were manually checked.
- Headlines were scored as:
  - `1` = Perfect match
  - `0.5` = Somewhat relevant
  - `0` = Not relevant

---

## **Key metric**

| Metric | Result |
|--------|--------|
| **Average relevance score** | `0.78` |
| **Precision@5** | `~0.8` |

- Low scores appear only on genuinely ambiguous edge cases (e.g. `XAI` vs `Explainable AI` vs Elon Musk’s `xAI`).

---

## **Supporting file**

Full details in [`accuracy_report.xlsx`](./accuracy_report.xlsx)

---

## **Observations**

- Cosine similarity via `FAISS` works well for short headlines, but adding more context (e.g., summaries/ date of articles) could improve accuracy and rank of providing latest articles of related topic.
- Short ambiguous headlines are not providing accurate results.
- For a lightweight prototype, ~0.78 average is acceptable for knowledge updates.

---
## **Future improvements**

- **User feedback & clicks:** In production, real user clicks can be logged and used to **re-weight or fine-tune the embeddings**, so the system learns what people actually consider relevant.
- **Fine-tuning:** A small domain-specific dataset (e.g., headlines with relevance labels) can help fine-tune the base `SentenceTransformer` or train a **custom re-ranker**.
**Key takeaway:** This prototype shows a strong baseline (~0.78 accuracy) which can be improved with real feedback loops in production.


## **Conclusion**

This score shows the prototype is a **valid proof-of-concept** for a **real-time AI news semantic search tool**.

---

**Last updated:** [07/06/2025]
