# Independent Spec review

**Verdict: APPROVE the bounded D21 presentation delta; zero Spec findings. Operational narrow interaction remains FAIL on candidate and baseline, not waived.**

Fixed range: `58586f786bc507c1b8e1d933974e1e4eb7c46bf6...1c364b8128c1b6dca476f41b13cb28a177dc7e8b`. Product8e15852. Reviewed range diff/log and necessary regression paths. D21 supersedes old overview-display requirements.

- D21: “移除整個可見文件概覽與其英文警告”. `frontend/src/DocumentPane.tsx:10` removes the entire summary render/placeholder/expansion path; upload/progress/Ready/reconnect remain. No backend or event schema delta.
- D16 follow-up: “僅移除快捷題群組的可見標題，保留五題、無障礙名稱與既有送出／disabled／focus／其他文件過濾”. `Shortcuts.tsx:21` uses accessible-only aria-label with unchanged five questions/filter/click guard. Composer IME/submit handlers are unchanged.
- D21: “此表格的行列結構辨識不完整，相關數字請核對原文。” `SourceContent.tsx:5,30` and `AnswerProcess.tsx:149` show exactly this text only for unreconstructed Table Chunks, beside raw sources. Reliable grid/text paths retain their content. `SourcePane.tsx:29` keeps summary-source provenance; ReadyEvent retains document_summary.

Dist index/bundle include the updated presentation. Reviewed build/type/source/event provenance and raw ordinary-suite result327passed/3deselected/zeroSKIP. Reviewed retained failed browser runs and corrected390batch7PASS, without relabeling failed full batches. Prior label evidence covers filtering/click/disabled/focus; synthetic IME evidence applies to unchanged handlers, not physical IME proof. LLM-format/prompt teaching N/A: static UI only.

Independent390 check, including rawCDP, reproduces reconstructedC2→Escape browser unresponsiveness on BOTH candidate and exact baseline; neither reaches q3 typing/submission. See `narrow-transition.md`, exact commands, screenshots, hashes and cleanup. This is not demonstrated regression from this diff or a full operational PASS; Main owns disposition.

Inspected: AGENTS.md, CONTEXT.md, issue12, Main D21/D20/D16 and approved-overview note; frontend/src/{DocumentPane,Shortcuts,SourceContent,AnswerProcess,SourcePane,Composer,App,events,Answer}; frontend/review/{scripted-events,checks,followup}; source-content test; dist index/JS; overview README/build/runtime/fullpytest/three failed browser logs/narrow-final; label README/continuation report/checks/DOM provenance.

Runtime: native session01a13822-11fd-7f11-bf7c-dd5c1992df7e, turn_context line8: gpt-6.1-sol medium/workspace-write/on-request. No children, tests/builds/provider/server changes. Only assigned reports/evidence written. Owned browser closed; servers untouched.
