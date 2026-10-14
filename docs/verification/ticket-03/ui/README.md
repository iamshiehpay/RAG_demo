# Ticket #03 Citation UI evidence

Browser integration acceptance against committed Vite dist served by FastAPI on
127.0.0.1:8130. Local real bge-m3 was used; a recording ScriptedLLM selected an
actual parsed Table Chunk Citation. This checks source rendering and source API
integration, not live answer quality (see the Q3 N=3 eval report).

- Table 2 Citation opens p.8 §4.3 with 16 rows × 6 columns, caption, comparison
  labels, dataset/metric headers, and explicit NaiveRAG / variant meaning.
- Desktop 1440×900: table/source readable, no page horizontal overflow.
- Narrow 390×844: page width 390px; the 721px table scrolls inside its 354px
  source region. Keyboard focus is available on that region.
- Authored missing-cell Table 7: source preserves the raw values and displays
  「結構未能可靠重建」 rather than showing an invented grid.
- Citation source closes successfully; no browser page errors or console errors.

Evidence: `table2.png`, `table2-mobile.png`, `uncertain-table.png`.
