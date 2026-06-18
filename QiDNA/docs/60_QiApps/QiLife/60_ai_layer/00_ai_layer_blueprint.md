# QiLife AI Layer Blueprint

## Principle

AI should be directly connected to the life ledger, not floating beside it as a detached chatbot.

AI should read, summarize, classify, retrieve, and eventually help update:

- QiBits
- timeline projections
- buckets
- threads
- actions
- people
- transactions
- obligations
- documents
- knowledge items
- note-type QiBits
- reflection-type QiBits

## V1 AI Behavior

V1 may use mock responses, but the service boundaries should exist from the start.

## AI Service Functions

```text
interpret_qibit
extract_related_entities
suggest_actions
generate_action_steps
find_relevant_knowledge
suggest_future_slot
summarize_day
summarize_thread
extract_transaction_from_text
extract_obligation_from_text
answer_life_query
generate_reflection_prompt
```

## Human Review Rule

AI should suggest. Cody approves.

For v1, AI should not silently create or modify important records without a review step.

## Ask QiLife Example Questions

- What happened today?
- What matters right now?
- What am I waiting on?
- Who owes me money?
- What tasks involve Zai?
- What legal items are open?
- What is the next action on the surplus check?
- What did I spend on gas this week?
- Turn this rant into QiBits, actions, and note-type QiBits.
- What is real, what is noise, and what do I do next?

## AI Response Shape

```text
answer
supporting_records
suggested_actions
related_people
related_threads
confidence
save_options
```

## Save Options

AI output should be savable as:

- QiBit
- action
- knowledge item
- thread summary
- reflection
- daily summary draft
