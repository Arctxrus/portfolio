# DE-VIBE AUDIT (DRAFT, pending approval)

Status: DRAFT. The originally agreed checklist was not supplied in this
workspace, so this draft was written at stage 8 from CONCEPT.md's design
language and intent. It must be approved before the audit runs. Once approved,
remove this status note.

Purpose: catch anything that makes the site read as generic AI output or a
template, rather than a deliberate, specific piece of design. Run against the
built site before the final commit. Record PASS or FLAG per item in
PROGRESS.md. Tier 1 flags block shipping; Tier 2 flags are fixed or
consciously accepted with a note.

## Tier 1 (shipping blockers)

1. No em dashes anywhere in rendered copy, code or comments.
2. No fake content: no invented testimonials, no fabricated stats, no stock
   photography, no placeholder lorem text. Every factual claim on the page is
   true (player count, degree, live builds, prices).
3. No AI-slop tells: no emoji in UI copy, no "Elevate your business" style
   marketing filler, no exclamation marks doing the selling, no generic
   purple/indigo gradient aesthetic, no glassmorphism, no drop shadows.
4. Token discipline: every colour, radius and border width on the page comes
   from the CONCEPT 3.1 token set. Exactly two radii. One border width. Inset
   shadows only.
5. Type discipline: only Archivo and Martian Mono (plus the system-font
   expand glyph). No weight or size that is not in the 3.2 table.
6. Honest conversion path: no urgency tactics, no fake scarcity, no sticky
   CTA bars, no popups. One clear action.
7. Accessibility floor holds: keyboard-only journey works end to end,
   aria-live announces panel changes, reduced motion fully honoured, text
   contrast per section 10 (with the documented mobile/focus remediation).

## Tier 2 (fix or consciously accept)

8. Copy voice: UK English throughout, plain and specific, sentence case
   prose, no jargon a barber would not know, prices stated plainly.
9. Motion restraint: nothing loops or pulses for attention except the
   sanctioned CTA drift and light pass. No bounce or overshoot easing. No
   scale-on-press anywhere.
10. Density and negative space: the page reads in three seconds; nothing
    competes with the index and the CTA; the dot grid stays ambient (rest
    alpha 0.06), never decorative foreground.
11. Specificity of detail: the niche tags, captions and sub lines are about
    these actual businesses and builds, not swappable filler.
12. Performance truth: first load under 300KB excluding videos, no layout
    shift after load-in, videos lazy-load only on selection.
13. Screenshot test: a full-page screenshot at 1440x900 and at 390px could
    not be mistaken for a Tailwind template or a v0/Lovable default.

## Final check (answer in PROGRESS.md)

Name three distinctive, deliberate design choices in the shipped site and
say why each exists. If three cannot be named without reaching, the site has
a vibe problem regardless of the item results above.
