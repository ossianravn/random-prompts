# Research Basis and Design Decisions

Accessed: 2026-07-19

This reference explains why the skill uses its defaults. It is not a diagnostic guide. Neurodivergent people are heterogeneous, and the most reliable accessibility rule is to respect individual preferences and observed feedback.

## Evidence-to-rule map

| Evidence or guidance | Design implication in this skill |
|---|---|
| W3C cognitive accessibility guidance emphasizes clear purpose, understandable language, short blocks, separated instructions, focus, orientation, memory support, and personalization. | Lead with the answer or action; chunk content; number sequences; show progress and state; keep one primary path. |
| W3C's clear-step pattern recommends showing completed, current, pending, and important choices so a distracted user can reorient without restarting. | Maintain a compact multi-turn state ledger and distinguish done, now, next, and blocked. |
| National Autistic Society guidance says communication preferences vary and some autistic people benefit from direct language, broken-down instructions, patience, and processing time. | Use literal, explicit wording; one action per step; avoid stacked questions and implied meaning. |
| NHS England says the best accessible format depends on the person; shorter is not always better, pictures may distract some autistic people, and some people need detail. | Preserve technical depth, avoid forced “easy read,” keep visuals optional, and let user preference override defaults. |
| CDC notes that adults with ADHD may have difficulty managing attention, completing lengthy tasks, and staying organized. | Put the next action first, reduce choice overload, externalize progress, and make completion criteria visible. |
| Reviews of adult ADHD research report differences in time perception, with substantial variation across tasks and people. | Make time visible, but use ranges and assumptions rather than claiming a universal “time blindness” profile or false precision. |
| A 2021 study of 245 autistic adults found that communication-mode preferences varied by context; written modes often ranked highly and phone calls were often disliked. | Exploit written chat's strengths: editable steps, exact wording, visible state, and resumability; never claim one mode suits everyone. |
| Autism communication research and advocacy increasingly frame mismatch as two-way rather than a one-sided deficit. | Avoid deficit framing, blame, forced masking, and “normalizing” language; adapt the agent's communication too. |

## Ideas retained

- **Action-first:** lowers the cost of finding where to begin.
- **One recommended path:** reduces avoidable decision load without withholding alternatives.
- **Visible state:** supports recovery after distraction, interruption, or context switching.
- **Concrete time ranges:** makes effort schedulable while preserving uncertainty.
- **Factual wins:** shows progress and verification without gamification.
- **Progressive disclosure:** keeps the first screen usable while preserving optional depth.
- **Literal, explicit references:** reduces ambiguity in instructions, code, and decisions.
- **Proportional structure:** applies the skill to every message without turning casual conversation into a checklist.

## Ideas rejected or softened

- **Always be brief:** rejected. Some readers need detail; the better rule is answer first, then layered depth.
- **Always use pictures or emoji:** rejected. Visuals can help some people and distract others.
- **Always show a state block:** softened. State is valuable for complex or multi-turn work and clutter for trivial exchanges.
- **Always give a single exact duration:** rejected. Specific ranges plus assumptions are more honest and useful.
- **Always ask one question only:** softened. Ask one at a time by default, but group a small numbered set when all answers are genuinely required.
- **Use childlike or “easy” language:** rejected. Use clear adult language and retain domain vocabulary that carries meaning.
- **Treat autism and ADHD as one profile:** rejected. The skill uses broadly useful defaults and personalizes from user feedback.

## Source priorities

1. Accessibility standards and public-health guidance.
2. Autistic-led or autism-specialist guidance that acknowledges preference diversity.
3. Peer-reviewed research, especially work that asks neurodivergent adults about their own preferences.
4. Lived-experience material as design input, not as universal evidence.

## Sources

- W3C, *Making Content Usable for People with Cognitive and Learning Disabilities*: https://www.w3.org/TR/coga-usable/
- W3C, *Make Each Step Clear*: https://www.w3.org/WAI/WCAG2/supplemental/patterns/o1p04-clear-steps/
- W3C, *Use Clear and Understandable Content*: https://www.w3.org/WAI/WCAG2/supplemental/objectives/o3-clear-content/
- National Autistic Society, *Autism and communication*: https://www.autism.org.uk/advice-and-guidance/about-autism/autism-and-communication
- NHS England, *Making information and the words we use accessible*: https://www.england.nhs.uk/learning-disabilities/about/get-involved/involving-people/making-information-and-the-words-we-use-accessible/
- CDC, *ADHD in Adults*: https://www.cdc.gov/adhd/about/adhd-in-adults.html
- Mette et al. (2023), *Time Perception in Adult ADHD: Findings from a Decade—A Review*: https://pmc.ncbi.nlm.nih.gov/articles/PMC9962130/
- Howard and Sedgewick (2021), *Anything but the phone! Communication mode preferences in the autism community*: https://doi.org/10.1177/13623613211014995
- Crompton et al. (2020), *Autistic peer-to-peer information transfer is highly effective*: https://pmc.ncbi.nlm.nih.gov/articles/PMC7545656/
