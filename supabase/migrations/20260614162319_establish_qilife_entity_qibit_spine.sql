-- ADR-0018: minimal canonical QiLife Entity/QiBit spine.
-- This migration is local and has not been deployed.

create extension if not exists pgcrypto with schema extensions;

create schema if not exists qi_entities;
create schema if not exists qi_events;

revoke all on schema qi_entities from public, anon, authenticated;
revoke all on schema qi_events from public, anon, authenticated;

create table if not exists qi_entities.entities (
  id uuid primary key default gen_random_uuid(),
  entity_type text not null check (btrim(entity_type) <> ''),
  display_name text not null check (btrim(display_name) <> ''),
  attributes jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists qi_entities.relationships (
  id uuid primary key default gen_random_uuid(),
  source_entity_id uuid not null references qi_entities.entities(id) on update cascade on delete restrict,
  target_entity_id uuid not null references qi_entities.entities(id) on update cascade on delete restrict,
  relationship_type text not null check (btrim(relationship_type) <> ''),
  attributes jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint relationships_unique_direction unique (source_entity_id, target_entity_id, relationship_type)
);

create index if not exists relationships_target_entity_id_idx
  on qi_entities.relationships (target_entity_id);

create table if not exists qi_events.qibits (
  id uuid primary key default gen_random_uuid(),
  qibit_type text not null check (btrim(qibit_type) <> ''),
  title text not null check (btrim(title) <> ''),
  summary text,
  occurred_at timestamptz not null default now(),
  primary_entity_id uuid references qi_entities.entities(id) on update cascade on delete set null,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists qibits_primary_entity_id_idx
  on qi_events.qibits (primary_entity_id)
  where primary_entity_id is not null;

create index if not exists qibits_occurred_at_idx
  on qi_events.qibits (occurred_at desc);

alter table qi_entities.entities enable row level security;
alter table qi_entities.relationships enable row level security;
alter table qi_events.qibits enable row level security;
