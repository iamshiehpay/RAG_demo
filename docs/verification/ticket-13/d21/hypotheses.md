# D21 feedback and ranked hypotheses

Baseline source: deployed backend 58586f7, unchanged compatible Main cache copied into isolated workspace. Original user history/source payload is unavailable.

Executed feedback command: `PYTHONPATH=src:. /Users/shiehpay/Desktop/resume/rag/.venv/bin/python docs/verification/ticket-13/d21/feedback.py --route Synthesis --output docs/verification/ticket-13/d21/live/baseline-standalone.json`.

Result: FAIL, `Unexpected fixed refusal`; actual Router chose Synthesis, unchanged question, three queries; final answer exactly `文件中未提及`. Two guarded calls, answer estimate 4,104 + 3,000 reservation, no truncation. Deterministic recorded-provider replay also FAILs in 0.35 seconds. Replay tests orchestration and the symptom, not a new model classification or semantic repair. Original Global observation is not reproduced by this standalone baseline.

Ranked falsifiable hypotheses:

1. **Answer scope/refusal interpretation.** The answer model treats absence of an explicit author limitations statement as total absence, even though supplied experimental/ablation evidence permits a qualified account of demonstrated scope/trade-offs. Prediction: a generic instruction to distinguish explicit limitations, evidence scope, and variant/other-system limits will produce a qualified supported answer on the same sources without inventing full-system limitations. Counter-test: absent facts still yield the exact refusal.
2. **History influences Router classification.** A previous overview may pull a limitation follow-up into Global despite the Synthesis contract. Prediction: realistic counterfactual overview histories yield Global while identical standalone wording yields Synthesis. Falsified if both consistently choose Synthesis; any reconstructed history cannot establish the original cause.
3. **Retrieval lacks method-specific evidence.** Broad generated queries retrieve limitations of existing systems and ablated variants, but omit supported constraints of the full method. Prediction: inspect retrieved versus original Chunks; method-specific queries materially add relevant evidence. No retrieval change justified if original Document lacks stronger relevant evidence.
4. **Source-warning attribution leaks across paths.** Chunk prompts embed processing warnings as excerpt content while summary prompt has an explicit attribution rule. Prediction: unrelated authored limitation plus an unreliable Table Chunk can yield a warning attributed to the authors through Synthesis. A generic provenance rule should preserve authored qualifiers and separate processing limitations.

Proceeding with one-variable probes under the released scope. No broad eval loop or additional critic calls.
