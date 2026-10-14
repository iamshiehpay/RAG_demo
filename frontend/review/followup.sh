#!/bin/zsh
# D16 follow-up interaction checks (real mouse and keyboard through agent-browser; scripted /api, no model calls).
# Usage: review/followup.sh <base-url> [session] [out-dir]   e.g. review/followup.sh http://127.0.0.1:8121 nova-uifix
# Needs: a server serving frontend/dist (the API is replaced by review/scripted-events.js). Exit code 1 on any FAIL.
BASE=${1:?base url}; SESSION=${2:-nova-uifix}
AB() { agent-browser --session "$SESSION" "$@"; }
DIR=${0:A:h}; FAILS=0
OUT=${3:-$DIR/../../docs/verification/ticket-12/followup}; OUT=${OUT:A}; mkdir -p $OUT/checks
cd $DIR/..
# ONLY='tight unmount' runs just those sections (names: drag unmount shortcuts drag920 narrow tight checks)
want() { [[ -z "$ONLY" || " $ONLY " == *" $1 "* ]]; }
FRAME_BASE=$(mktemp -t followup-frame)
FRAME=$FRAME_BASE.png
trap 'rm -f "$FRAME" "$FRAME_BASE"' EXIT
# A headless page only re-evaluates media queries when a frame is produced; force one after a viewport change.
frame() { AB screenshot "$FRAME" >/dev/null; sleep .3; }
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILS=$((FAILS+1)); }
# run NAME 'js expression that evaluates to true'
run() { local out; out=$(AB eval "$2" 2>&1); if [[ "$out" == "true" ]]; then pass "$1"; else fail "$1 (got: $out)"; fi }
boot() { # width height [documentName] : fresh page, empty storage, fixture installed, upload (scripted) unless NOUPLOAD
  AB set viewport $1 $2 >/dev/null
  AB open $BASE >/dev/null
  AB eval 'try{localStorage.clear()}catch(e){}; location.reload()' >/dev/null; sleep 1.5
  AB eval --stdin < review/scripted-events.js >/dev/null
  [[ -n "$3" ]] && AB eval "window.__t09.documentName='$3'" >/dev/null
  if [[ -z "$NOUPLOAD" ]]; then AB upload '#document' ../data/lightrag.pdf >/dev/null; sleep 1.5; fi
}
ask() { AB eval "window.__t09.scenario='$1'" >/dev/null; AB fill '#question' "${2:-測試問題}" >/dev/null; AB click 'button[type=submit]' >/dev/null; sleep 1.5; }
sepw() { AB eval 'document.querySelector("[role=separator]").getAttribute("aria-valuenow")' | tr -d '"'; }
sepxy() { AB eval '(()=>{const r=document.querySelector("[role=separator]").getBoundingClientRect(); return `${Math.round(r.left+r.width/2)} ${Math.round(r.top+r.height/2)}`})()' | tr -d '"'; }
INBOUNDS='(()=>{const s=document.querySelector("[role=separator]"),n=+s.getAttribute("aria-valuenow"),lo=+s.getAttribute("aria-valuemin"),hi=+s.getAttribute("aria-valuemax");const p=document.querySelector(".pane-right").getBoundingClientRect().width,c=document.querySelector(".chat").getBoundingClientRect().width;return lo<=n&&n<=hi&&Math.abs(p-n)<=1&&c>=360&&document.documentElement.scrollWidth<=innerWidth})()'
drag() { local x y; read x y <<< "$(sepxy)"; AB mouse move $x $y >/dev/null; AB mouse down >/dev/null; AB mouse move $(($x+$1)) $y >/dev/null; [[ -n "$2" ]] && return; AB mouse up >/dev/null; }

if want drag; then
echo "== 1440: separator, drag, keyboard =="
boot 1440 900; ask q3 "Performance of ablated versions of LightRAG."
AB eval 'document.querySelector(".inline-citation").click()' >/dev/null; sleep 1
run "source pane open with separator and in-bounds width" "$INBOUNDS"
W0=$(sepw)
drag -100; sleep .3; W1=$(sepw)
run "dragging left by 100px widens the pane by 100px (was $W0, now $W1)" "$W1 - $W0 === 100"
drag 60; sleep .3; W2=$(sepw)
run "dragging right by 60px narrows it by 60px (now $W2)" "$W1 - $W2 === 60"
run "no stuck drag state after pointer up" '!document.querySelector("[role=separator]").hasAttribute("data-dragging")'
drag -2000; sleep .3; run "extreme drag left clamps to aria-valuemax" "+document.querySelector('[role=separator]').getAttribute('aria-valuenow') === +document.querySelector('[role=separator]').getAttribute('aria-valuemax') && $INBOUNDS"
drag 3000; sleep .3; run "extreme drag right clamps to aria-valuemin" "+document.querySelector('[role=separator]').getAttribute('aria-valuenow') === +document.querySelector('[role=separator]').getAttribute('aria-valuemin') && $INBOUNDS"
# release outside the separator and the window area: capture must still deliver pointerup
read X Y <<< "$(sepxy)"; W3=$(sepw); AB mouse move $X $Y >/dev/null; AB mouse down >/dev/null; AB mouse move $(($X-80)) 300 >/dev/null
run "dragging flag is set during the drag" 'document.querySelector("[role=separator]").hasAttribute("data-dragging")'
AB mouse move 5 5 >/dev/null; AB mouse up >/dev/null; sleep .3; W4=$(sepw)
run "releasing far outside the separator ends the drag" '!document.querySelector("[role=separator]").hasAttribute("data-dragging")'
AB mouse move $(($X-300)) 400 >/dev/null; sleep .2; run "moving after that release does not resize" "$(sepw) === $W4"
# pointercancel mid-drag
read X Y <<< "$(sepxy)"; AB mouse move $X $Y >/dev/null; AB mouse down >/dev/null; AB mouse move $(($X-40)) $Y >/dev/null
AB eval 'document.querySelector("[role=separator]").dispatchEvent(new PointerEvent("pointercancel",{bubbles:true,pointerId:1}))' >/dev/null; sleep .2
W5=$(sepw); run "pointercancel ends the drag" '!document.querySelector("[role=separator]").hasAttribute("data-dragging")'
AB mouse move $(($X-200)) $Y >/dev/null; sleep .2; run "moves after pointercancel do not resize" "$(sepw) === $W5"; AB mouse up >/dev/null
# keyboard
AB eval 'document.querySelector("[role=separator]").focus()' >/dev/null; AB press ArrowRight >/dev/null; AB press ArrowLeft >/dev/null; sleep .2; Wk=$(sepw)
AB press Home >/dev/null; sleep .2; run "Home goes to the minimum" "$(sepw) === +document.querySelector('[role=separator]').getAttribute('aria-valuemin')"
Wm=$(sepw); AB press ArrowLeft >/dev/null; sleep .2; run "ArrowLeft widens by 16 (from $Wm)" "$(sepw) - $Wm === 16"
Wm=$(sepw); AB press ArrowRight >/dev/null; sleep .2; run "ArrowRight narrows by 16" "$Wm - $(sepw) === 16"
AB press End >/dev/null; sleep .2; run "End goes to the maximum and stays in bounds" "+document.querySelector('[role=separator]').getAttribute('aria-valuenow') === +document.querySelector('[role=separator]').getAttribute('aria-valuemax') && $INBOUNDS"
AB press ArrowLeft >/dev/null; sleep .2; run "ArrowLeft at the maximum does not exceed it" "$INBOUNDS"
AB press Home >/dev/null; AB press ArrowRight >/dev/null; sleep .2; run "ArrowRight at the minimum does not go below it" "$INBOUNDS"
AB eval 'document.activeElement.blur()' >/dev/null; AB press Tab >/dev/null
AB eval 'document.querySelector("[role=separator]").focus()' >/dev/null; AB press ArrowLeft >/dev/null
run "separator shows a visible focus ring from the keyboard" 'document.activeElement.matches("[role=separator]") && getComputedStyle(document.activeElement).outlineStyle !== "none" && parseFloat(getComputedStyle(document.activeElement).outlineWidth) >= 2'
AB press End >/dev/null
# window resize and collapse/expand
AB set viewport 1000 800 >/dev/null; frame
run "shrinking the window re-clamps the pane (max is now 382)" "$INBOUNDS && +document.querySelector('[role=separator]').getAttribute('aria-valuemax') <= 382"
AB set viewport 1440 900 >/dev/null; frame; run "growing the window again stays in bounds" "$INBOUNDS"
AB click 'button[aria-label="收合文件欄"]' >/dev/null; sleep .3; run "collapsing the document column keeps the pane in bounds" "$INBOUNDS"
AB click 'button[aria-label="展開文件欄"]' >/dev/null; sleep .3; run "expanding it again keeps the pane in bounds" "$INBOUNDS"
AB click 'button[aria-label="收合來源欄"]' >/dev/null; sleep .3
run "collapsed source rail is 64px wide with a readable label" 'document.querySelector(".rail-right").getBoundingClientRect().width === 64 && document.querySelector(".rail-right .rail-label").textContent === "來源" && !document.querySelector("[role=separator]")'
AB click 'button[aria-label="展開來源欄"]' >/dev/null; sleep .3; run "re-expanding the source pane restores a bounded separator" "$INBOUNDS"
# persistence survives reload but is re-clamped
AB eval 'localStorage.setItem("chat-document.source-width","99999"); location.reload()' >/dev/null; sleep 1.5
AB eval --stdin < review/scripted-events.js >/dev/null; AB upload '#document' ../data/lightrag.pdf >/dev/null; sleep 1.5
run "an absurd stored width is clamped on load" "$INBOUNDS"

asks() { AB eval 'window.__t09.asks.length' | tr -d '"'; }
fi
if want unmount; then
echo "== separator unmounted mid-drag (crossing the 900px breakpoint) =="
boot 1440 900; ask q3 "Performance of ablated versions of LightRAG."; AB eval 'document.querySelector(".inline-citation").click()' >/dev/null; sleep 1
Wd=$(sepw); read X Y <<< "$(sepxy)"; AB mouse move $X $Y >/dev/null; AB mouse down >/dev/null; AB mouse move $(($X-60)) $Y >/dev/null
run "a drag is in progress (workspace is resizing)" 'document.querySelector(".workspace").classList.contains("resizing")'
AB set viewport 800 800 >/dev/null; frame
run "the separator is unmounted at 800px while the button is still held" '!document.querySelector("[role=separator]")'
AB mouse up >/dev/null; AB set viewport 1440 900 >/dev/null; frame
run "after returning to 1440 no resizing state is left behind" '!document.querySelector(".workspace").classList.contains("resizing") && !document.querySelector("[role=separator]")?.hasAttribute("data-dragging")'
AB eval '(() => { if (!document.querySelector(".pane-right")) document.querySelector("button[aria-label=\"展開來源欄\"]")?.click(); return true; })()' >/dev/null; sleep .4
Wb=$(sepw); read X Y <<< "$(sepxy)"; AB mouse move $(($X+40)) $Y >/dev/null; AB mouse move $(($X-90)) $(($Y+30)) >/dev/null; sleep .3
run "hovering without a pressed button does not resize the pane (width $Wb)" "$(sepw) === $Wb"
run "text can be selected again (user-select is not none)" 'getComputedStyle(document.querySelector(".workspace")).userSelect !== "none"'

fi
if want shortcuts; then
echo "== 1440: shortcuts and composer =="
boot 1440 900
run "all five LightRAG questions are shown and enabled when a Document is Ready" 'document.querySelectorAll(".shortcut").length === 5 && [...document.querySelectorAll(".shortcut")].every(b => b.getAttribute("aria-disabled") !== "true")'
AB eval 'window.__t09.scenario="provisional"' >/dev/null
AB fill '#question' "我先寫的草稿" >/dev/null
AB click '.shortcut:nth-child(2)' >/dev/null; sleep 1.2
run "one click sends exactly one ask with the exact text" 'window.__t09.asks.length === 1 && window.__t09.asks[0] === "Compare LightRAG with GraphRAG."'
run "the typed draft is kept when a shortcut is used" 'document.querySelector("#question").value === "我先寫的草稿"'
run "while generating, every shortcut, the textarea and 送出 are disabled" '[...document.querySelectorAll(".shortcut")].every(b => b.getAttribute("aria-disabled") === "true") && document.querySelector("#question").disabled && document.querySelector(".send-button").disabled'
run "keyboard focus stays on the activated shortcut while generating" 'document.activeElement === document.querySelector(".shortcut:nth-child(2)") && !document.activeElement.disabled'
AB eval 'document.querySelectorAll(".shortcut").forEach(b => b.click()); document.querySelector("#question").dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}))' >/dev/null; sleep .4
run "clicking disabled shortcuts while generating sends nothing" 'window.__t09.asks.length === 1'
AB eval 'window.__t09.release()' >/dev/null; sleep 1.2
run "after the answer is final the shortcuts are enabled again" '[...document.querySelectorAll(".shortcut")].every(b => b.getAttribute("aria-disabled") !== "true") && document.querySelector(".turn .provisional-text") === null'
AB eval 'window.__t09.scenario="q3"' >/dev/null
AB dblclick '.shortcut:nth-child(3)' >/dev/null; sleep 1.5
run "a real double click sends exactly one more ask" 'window.__t09.asks.length === 2 && window.__t09.asks[1] === "Performance of ablated versions of LightRAG."'
AB eval 'const b=document.querySelector(".shortcut:nth-child(4)"); b.click(); b.click(); b.click()' >/dev/null; sleep 1.5
run "three clicks in the same tick send exactly one ask" 'window.__t09.asks.length === 3 && window.__t09.asks[2] === "這篇論文有什麼限制？"'
AB fill '#question' "typed A" >/dev/null; AB focus '#question' >/dev/null; AB press Shift+Enter >/dev/null; sleep .2
run "Shift+Enter inserts a newline and sends nothing" 'window.__t09.asks.length === 3 && document.querySelector("#question").value.includes("\n")'
AB press Enter >/dev/null; sleep 1.5
run "Enter sends the typed question through the same path (one ask)" 'window.__t09.asks.length === 4 && window.__t09.asks[3].startsWith("typed A")'
AB eval 'window.__t09.scenario="error"' >/dev/null; AB click '.shortcut:nth-child(5)' >/dev/null; sleep 1.5
run "an error answer shows 重試 and the shortcuts are usable again" 'window.__t09.asks.length === 5 && !!document.querySelector(".error-state button") && [...document.querySelectorAll(".shortcut")].every(b => b.getAttribute("aria-disabled") !== "true")'
AB screenshot "$OUT/10-shortcuts-error-state-1440.png" >/dev/null

fi
if want shortcuts; then
echo "== shortcuts: no Document, uploading, other Documents =="
NOUPLOAD=1 boot 1440 900
run "no Document: five shortcuts shown but disabled, composer disabled" 'document.querySelectorAll(".shortcut").length === 5 && [...document.querySelectorAll(".shortcut")].every(b => b.getAttribute("aria-disabled") === "true") && document.querySelector("#question").disabled'
AB screenshot "$OUT/08-shortcuts-disabled-no-document-1440.png" >/dev/null
AB eval 'window.__t09.uploadHold=true' >/dev/null; AB upload '#document' ../data/lightrag.pdf >/dev/null; sleep 1
run "while the Document is processing the shortcuts stay disabled" '[...document.querySelectorAll(".shortcut")].every(b => b.getAttribute("aria-disabled") === "true") && document.querySelector("#question").disabled'
AB screenshot "$OUT/09-shortcuts-disabled-uploading-1440.png" >/dev/null
AB eval 'window.__t09.release()' >/dev/null; sleep 1.2
run "once Ready they are enabled" '[...document.querySelectorAll(".shortcut")].every(b => b.getAttribute("aria-disabled") !== "true")'
boot 1440 900 industrial-robotics.pdf
run "another Document gets only the general question, no visible heading, neutral accessible name" 'document.querySelectorAll(".shortcut").length === 1 && document.querySelector(".shortcut").textContent === "Summary this document." && document.querySelector(".shortcuts").getAttribute("aria-label") === "範例問題" && document.querySelector(".shortcuts").textContent === "Summary this document." && !document.querySelector(".shortcuts").textContent.includes("LightRAG")'
AB click '.shortcut' >/dev/null; sleep 1.2
run "that general shortcut sends once" 'window.__t09.asks.length === 1 && window.__t09.asks[0] === "Summary this document."'
AB screenshot "$OUT/11-other-document-shortcuts-1440.png" >/dev/null

fi
if want drag920; then
echo "== 920: separator =="
boot 920 800; ask q3 "Performance of ablated versions of LightRAG."; AB eval 'document.querySelector(".inline-citation").click()' >/dev/null; sleep 1
run "920: separator present and in bounds (max 302)" "$INBOUNDS && +document.querySelector('[role=separator]').getAttribute('aria-valuemax') === 302"
drag -400; sleep .3; run "920: dragging far left clamps and keeps the conversation >= 360" "$INBOUNDS"
AB screenshot "$OUT/04-drag-max-920.png" >/dev/null

fi
if want narrow; then
echo "== 390: overlay, focus, Escape =="
boot 390 844; ask q3 "Performance of ablated versions of LightRAG."
run "390: no separator, shortcut row scrolls inside itself, no page overflow" '!document.querySelector("[role=separator]") && document.documentElement.scrollWidth <= innerWidth && getComputedStyle(document.querySelector(".shortcut-list")).overflowX === "auto"'
AB eval 'document.querySelector(".inline-citation").focus()' >/dev/null; AB press Enter >/dev/null; sleep 1
run "390: opening a Citation opens the source overlay and moves focus into it" 'document.querySelector(".pane-right")?.contains(document.activeElement)'
AB screenshot "$OUT/05-source-overlay-390.png" >/dev/null
AB press Escape >/dev/null; sleep .3
run "390: Escape closes the overlay and returns focus to the Citation" '!document.querySelector(".pane-right") && document.activeElement.classList.contains("inline-citation")'
AB eval 'window.__t09.overlayExpected=null; document.activeElement.blur()' >/dev/null
for i in 1 2 3 4 5 6; do AB press Tab >/dev/null; done
run "keyboard focus on a Citation or shortcut shows a visible ring" 'parseFloat(getComputedStyle(document.activeElement).outlineWidth) >= 2 && getComputedStyle(document.activeElement).outlineStyle !== "none"'

fi
if want tight; then
echo "== tight list inline spaces =="
boot 1440 900; ask tightlist "tight list"
run "tight list items keep their inline spaces in the rendered text" 'JSON.stringify([...document.querySelectorAll(".turn:last-child .answer-text li")].map(li => li.textContent)) === JSON.stringify(["see this and that now C1","run npm i now","A B","link x here","中文 粗體 文字","引用 C1 之後","two alpha beta gamma"])'
fi
if want overview; then
echo "== D21: overview removed, uncertainty beside related source =="
for W in 1440 920 390; do
  [[ -n "$OVERVIEW_WIDTH" && $W != $OVERVIEW_WIDTH ]] && continue
  H=900; [[ $W == 390 ]] && H=844; [[ $W == 920 ]] && H=800
  boot $W $H
  run "Ready @ $W: overview, controls and embedded English warning absent" '!document.querySelector(".document-overview, .overview-text") && !document.body.innerText.includes("English extraction warning") && !document.querySelector(".document-pane")?.textContent.includes("文件概覽") && document.querySelectorAll(".shortcut").length === 5 && !document.querySelector("#question").disabled'
  AB screenshot "$OUT/ready-$W.png" >/dev/null
  ask uncertain-table "uncertain source"
  AB click '.turn:last-child .inline-citation' >/dev/null
  frame
  run "uncertain table @ $W: exact Chinese warning beside raw citation source" 'document.querySelector(".pane-right .table-limitation").textContent === "此表格的行列結構辨識不完整，相關數字請核對原文。" && document.querySelector(".pane-right .source-text").textContent === "Review raw table text: alpha 12 beta 34" && !document.querySelector(".pane-right .source-table")'
  AB screenshot "$OUT/uncertain-$W.png" >/dev/null
  AB eval 'document.querySelector(".turn:last-child .answer-process").open = true; document.querySelector(".turn:last-child .found-chunk").open = true' >/dev/null
  run "uncertain table @ $W: retrieved source also keeps exact warning" '[...document.querySelectorAll(".turn:last-child .table-limitation")].some(el => el.textContent === "此表格的行列結構辨識不完整，相關數字請核對原文。")'
  boot $W $H
  ask compare "reconstructed source"
  AB eval 'document.querySelectorAll(".turn:last-child .inline-citation")[1].click()' >/dev/null
  frame
  run "reconstructed table @ $W: grid retained, uncertainty note absent" '!!document.querySelector(".pane-right .source-table") && !document.querySelector(".pane-right .table-limitation")'
  boot $W $H
  ask q3 "text source"
  AB click '.turn:last-child .inline-citation' >/dev/null
  frame
  run "text source @ $W: no table uncertainty warning" '!document.querySelector(".pane-right .table-limitation")'
  boot $W $H
  ask global "summary provenance"
  AB click '.turn:last-child .inline-citation' >/dev/null
  frame
  run "Global @ $W: summary citation and provenance retained" 'document.querySelector(".pane-right .source-text").textContent.includes("Review fixture summary") && !document.querySelector(".document-overview")'
  [[ $W == 390 ]] && AB press Escape >/dev/null
  frame
  AB eval --stdin < review/checks.js > "$OUT/checks/global-$W.json" && pass "D21 common assertions @ $W" || fail "D21 common assertions @ $W"
done
fi
if want checks; then
echo "== checks.js across widths and scenarios =="
for W in 1440 920 390; do
  H=900; [[ $W == 390 ]] && H=844; [[ $W == 920 ]] && H=800
  boot $W $H
  for SC in replay-cost replay-q3 spacing tightlist compare unverified error; do
    ask $SC "scenario $SC"
    AB eval --stdin < review/checks.js > "$OUT/checks/$SC-$W.json" 2>"$OUT/checks/$SC-$W.err" && pass "checks.js $SC @ $W ($(grep -c PASS "$OUT/checks/$SC-$W.json") assertions)" || fail "checks.js $SC @ $W: $(head -c 300 "$OUT/checks/$SC-$W.err")"
    rm -f "$OUT/checks/$SC-$W.err"
    case $SC in replay-cost|replay-q3) AB screenshot "$OUT/replay-${SC#replay-}-$W.png" >/dev/null;; esac
  done
done
fi
echo "FAILS=$FAILS"; exit $((FAILS>0))
