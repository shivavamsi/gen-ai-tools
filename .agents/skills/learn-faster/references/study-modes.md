# Study modes and copyable prompts

Read only the mode needed for the current request. Use the topic or material from conversation in place of `[topic]`; placeholders in the examples are for the learner to fill. Any quiz uses the main skill's adaptive loop. Include its software guardrails when adapting a prompt for software study.

## 1. Explain simply, then test

Prompt: “Explain [topic] like I'm 10 using one everyday example. Keep the important facts accurate. Then ask me one question that checks understanding and wait for my answer.”

Explain one small concept in plain language, usually within 150 words. Define essential terminology instead of deleting necessary distinctions. Use a respectful tone; “like I'm 10” sets the explanation level, not an assumption about age. If using an analogy, name its most relevant limit. End with one teach-back or application task.

## 2. Eight visual sticky notes

Prompt: “Turn [topic/material] into exactly eight visual sticky notes. Give each one a short title, one key idea, and a tiny visual cue. Arrange them so I can see the connections. Then test me on one note at a time.”

Produce eight numbered cards, normally in a two-column, four-row grid; use eight separated text boxes when a grid is unreadable. Keep each to a short title, one sentence, and a simple visual cue such as an arrow or symbol. Use numbers or labels so color is not necessary to understand them. Connect cards by sequence, category, or dependency. Group a narrow topic into eight useful views without inventing facts. For source-limited material that cannot support eight nonredundant notes, explain the limitation rather than pad it. Follow with one recall question without copying that note's answer into the question.

## 3. The essential ideas

Prompt: “For my goal of [goal], identify the few ideas in [topic] that unlock the most useful understanding. Explain why they matter, then teach the first one and check my understanding before continuing.”

Choose roughly three to five foundational or frequently useful ideas, including prerequisites. Explain the selection briefly in terms of the stated goal. This is a shortlist followed by one lesson, not five simultaneous lessons. Do not omit safety-critical requirements or essential prerequisites to fit a percentage.

## 4. Visual concept map

Prompt: “Make a small visual map of [topic]. Label the connections to show how and why the key ideas relate. Then ask me to explain one connection without looking at the map.”

Prefer a diagram with about five to nine nodes and specific edge labels such as “requires,” “causes,” “contrasts with,” or “is an example of.” Distinguish association from causation. Use Mermaid where supported or an ASCII diagram otherwise. A list of boxes without relationships is not a concept map. Test one relationship, or ask the learner to reconstruct a small part from memory.

## 5. One-question quiz

Prompt: “Quiz me on [topic], one question at a time. Wait for each answer, give brief feedback, and use a new example to check whether I can apply the idea. Track what needs review and stop when I meet [success criterion].”

Start at the demonstrated level. With no prior evidence, use a small diagnostic task. With a complete beginner who needs instruction, give a short introduction before testing. Never display the answer key alongside a live question. If the user wants a printable quiz or question bank instead, honor that format.

## 6. Adapt to my answers

Prompt: “Use my last answer to choose the next study question about [topic]. If I have a gap, help me with that specific gap; if I understand, give me a harder application. Ask only one question and wait.”

Use actual answer evidence rather than self-reported confidence alone. If no answer is available, begin with one diagnostic question. A correct answer with a false explanation needs follow-up. A reasonable alternative method or phrasing is not wrong. Hinted answers demonstrate progress, not independent understanding.

## 7. Memorable story

Prompt: “Turn [topic] into a short, memorable story. Map the characters and events back to the real ideas, explain where the story stops being accurate, then test whether I remember the concept.”

Use a brief story, normally 150–250 words, with a meaningful causal sequence. Follow it with a compact mapping of story elements to concepts and the key limit. Label invented characters and events as fiction when they could be mistaken for history or facts. Test the underlying idea, not irrelevant plot details.

## 8. Beginner mistakes

Prompt: “Show me the most relevant beginner mistakes in [topic]. For each, explain why it fails and show a correction. Then give me one fresh example where I must spot a mistake myself.”

Choose three to five errors relevant to the learner's task or actual answers. Distinguish observed errors from plausible pitfalls; do not invent statistics about how common they are. Pair each error with its consequence and correction. End with one new error-spotting task rather than an example already solved above.

## 9. Three mental models

Prompt: “Give me three different mental models for [topic]. Explain what each helps me predict, show a small example, and state where each model breaks down. Then ask me to choose a model for one new situation.”

Choose genuinely different perspectives appropriate to the subject, such as a causal mechanism, a system of flows and constraints, and a tradeoff or decision model. Do not force those categories or merely rename the same analogy three times. Mark metaphorical models as simplifications. Prefer fewer accurate models if the material cannot support three; explain why rather than inventing a false one.

## 10. Seven-day plan with spaced repetition

Prompt: “Create a seven-day plan for [topic] and [goal], using [minutes] minutes per day. Schedule active recall of the same ideas across days, mix related practice, and adjust reviews when I struggle. Include a final unfamiliar application.”

Use the learner's actual time budget. If it is absent, explicitly label a 20-minute-per-day example as a provisional assumption. Specify a task and an observable check for each day. Scale or replace the concept groups below to fit the topic and deadline.

| Day | Main work | Retrieval and evidence |
| --- | --- | --- |
| 1 | Baseline check; learn core group A. | Explain or perform one A task without notes; record gaps. |
| 2 | Retrieve A; learn group B. | Check A after a day; attempt one B application. |
| 3 | Retrieve B; learn group C if ready. | Correct a B gap; recall the new C idea. |
| 4 | Retrieve A and C; compare related ideas. | Test A in a new context and check C after a day. |
| 5 | Retrieve B; mix A/B problem types. | Choose a method without being told the category. |
| 6 | Retrieve C; repair weak concepts. | Use fresh examples to verify corrections independently. |
| 7 | Cumulative retrieval and an unfamiliar application. | Compare with the baseline; identify gaps and next reviews. |

This revisits A on days 1, 2, 4, and 7: a usable example, not an experimentally optimal schedule for every learner. B and C also receive later checks; a list of seven different daily topics is not spaced repetition. Reserve review time before allocating new content, for example 5 minutes retrieval, 10 minutes focused study or practice, and 5 minutes checking on a 20-minute day. Reduce new content when due reviews fill the budget.

Adapt per concept: an independent correct response can justify a longer gap; a slow or hinted answer calls for an earlier check; a miss calls for feedback, a fresh attempt after another task, and review the next day. An immediate corrected answer does not erase the miss. If the learner misses a day, resume the overdue material and reduce new content rather than doubling the workload. Extend beyond the first week when retention matters, for example with further checks on days 14 and 30, adjusted to performance and the real deadline.

If asked why spacing helps, explain that returning after a delay creates opportunities to retrieve and strengthen access to the same knowledge. Spreading practice generally improves later retention compared with packing it together. Appropriate gaps depend on the content, learner, and desired retention period. No universal forgetting percentage or guaranteed multiplier is needed.
