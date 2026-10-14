# #03 independent-review corrections and rebase acceptance

Levi review request #4830: changes requested. Original reviewed head was 8d91fc0
on base 3a15958. The branch is rebased onto main d56e092 (includes #04 at 4eee3d2);
review-fix checkpoint is bd8f0f7. This report records correction acceptance,
not independent approval. No main merge, push, cloud eval or Q3 prompt tuning.

## Finding coverage

All parser regressions use authored PDF bytes through Application.upload_document,
real local bge-m3, and the guarded recording ScriptedLLM.

| Review item | Final change | Upload/test evidence |
|---|---|---|
| 1: centred caption drops Table 4 row labels | Bounds use caption's column/text region. Rectangular grids require consistent left/centre/right column alignment, numeric data, and nonnumeric row labels. | `test_centred_caption_keeps_row_labels_in_aligned_table`; `test_lightrag_table4_preserves_statistics_and_row_labels`; `test_equal_cell_counts_require_column_alignment` |
| 2: caption-below swallows prose; columns become fake grids | Body prose stops a candidate region. When below has no grid evidence, scan upward under the same rules. Caption column excludes opposite prose, using the actual gutter rather than clipping at page midpoint. Physical first source line is the insertion anchor. | `test_caption_below_grid_preserves_table_and_following_body_prose`; `test_two_column_caption_pairs_do_not_turn_body_prose_into_a_table` (Table and Figure); `test_column_table_uses_the_text_gutter_instead_of_clipping_at_page_midpoint` |
| 3: limitation assertion checks only system prompt | Checks the actual raw Table Chunk in the answer's user message. Frontend static rendering checks the note and escaped raw text, with no invented table. | `test_uncertain_table_retains_source_text_and_answer_limitation_rule`; `npm run test:source --prefix frontend` |
| 4: math underscore cleanup caption-specific | Shared cleanup applies to raw text and reconstructed cells; identifier underscores remain. | `test_math_italic_artifact_is_cleaned_in_table_cells_without_changing_identifiers`; existing Figure 2 cost-grid test |
| 5: variant header disagrees with Table 1 meaning | Multiple baseline comparisons use baseline/candidate headers, consistent with meaning. | `test_table1_preserves_every_labelled_cell_and_cost_grid_removes_noise` checks headers and all 128 numbers |
| 6: Synthesis size bound too loose | Retrieved IDs must be a subset of selected primary/Sub-query seeds and those seeds' links. | `test_q2_sub_queries_cover_cost_and_incremental_update_in_document_order` in test_router_synthesis.py |
| 7: uncertain physical line can exceed 2K | Split oversized raw lines at character-preserving token bounds; every part repeats caption and limitation. | `test_oversized_unreconstructed_physical_line_is_split_without_losing_text` preserves all 1,100 numeric values, every Chunk ≤2K |
| Optional: defaults, constant reuse, repeated labels | Chunk reconstruction defaults false; answer prompt uses LIMITATION constant; virtual Table metadata comes directly from current Chunk fields. Exact known raw prefix is removed once, without splitting on arbitrary marker occurrences or selecting by label. | `test_virtual_sections_keep_duplicate_labels_attached_to_their_own_source`; existing large heading-free/uncertain tests |
| Required #04 cache integration | Added tables.py and embedder.py to PIPELINE_SOURCES, keeping ingestion-v2 format and configuration identity. | `test_table_and_embedder_source_changes_invalidate_upload_cache` proves a cache hit preserves typed fields, then modifying either source fingerprint causes parsing on re-upload |

Original Table 1/2 cell, Figure 2 cost, Lookup ordering/link/neighbor, budget-drop,
Q2 collective-coverage, Context Budget and row-split tests remain in the full suite.
Source-labelled prose cells such as LightRAG Table 3 remain raw Table evidence;
ordinary body prose outside a grid stays in Section paragraphs.

## Final verification

Final full suite output: `pytest.txt`: **208 passed, 2 deselected**, 184.59s (default excludes the two cloud eval tests).
Previous rebased run before the additional gutter regression: `pytest-before-gutter.txt`
(**207 passed**, 2 deselected, 216.32s).

Passing checks:

```sh
uv run pytest -q
uv run ruff check src tests scripts/generate_event_types.py scripts/measure_table_reading.py
uv run ruff format --check src tests scripts/generate_event_types.py scripts/measure_table_reading.py
uv run python scripts/generate_event_types.py --check
npm run build --prefix frontend
npm run test:source --prefix frontend
```

The build includes TypeScript checking and regenerates committed frontend/dist.
The independent reviewer must still approve these corrections.

## Browser acceptance after the final geometry correction

Fresh backend on 127.0.0.1:8130, rebased committed dist, real parser/local bge-m3,
scripted answer selecting the actual parsed Table 2 Citation. No cloud model call.
Upload receives HTTP 202 and follows background progress to Ready; question enabled
only then. Clicking [C11] opens p.8 §4.3 with 16 rows × 6 columns, caption, source
comparison meaning and typed cells. DOM assertions verify labelled -Low/Overall/Mix
and -Origin/Overall/Agriculture values. At 1440×900, page width remains 1440 and
Table region is focusable. Close source removes the source region. No page or
console errors. Browser session and backend process stopped afterward.

Evidence: `table2-browser.json`, `table2-rebased.png` (visually inspected).
Frontend static rendering also verifies the raw fallback limitation note.
Original narrow-screen and fallback screenshots remain in ../ui/.

## Remaining scope

Q3 numeric exceptions and forbidden-claim failures remain deferred to #11 under
Levi #4532/#4830. Retained reports are the original N=3, one authorized generic
follow-up N=3, and one correct held-out Table 1 answer. There was no additional
live quality measurement or prompt tuning in these corrections.
