---

title: QiLabs Full Tree
section: qilabs/10_qispark/01_nav
access_level: L1
visibility: private
ai_ingest: true
status: final_candidate
last_updated: 2026-06-20
mindmap-plugin: basic
---------------------


------

NEED TO REVIEW 

---
mindmap-plugin: basic
---

# 10_blueprint

## 10_governance/
- 01_principles.md
- 02_agent_rules.md
- 03_standards.md
- 04_registry.md
- 05_policies.md
- 06_decisions.md
- _index.md

## 20_architecture/
- 01_identity.md
- 02_component_map.md
- 03_system_model.md
- 04_device_model.md
- 05_runtime_zones.md
- 06_service_boundaries.md
- 07_data_flow.md
- _index.md

## 30_data/
- 01_infrastructure_layout.md
- 02_bands.md
- 03_domains.md
- 04_subdomains.md
- 05_namespace_registry.md
- 06_directory_tree.md
- 07_object_model.md
- 08_objects.md
- 09_placement_rules.md
- 10_schema.md
- 11_front_matter.md
- 12_metadata.md
- 13_storage.md
- 14_exports.md
- 15_qievidence.md
- 16_structure.md
- _index.md

## 40_compute/
- 01_apis.md
- 02_workers.md
- 03_pipelines.md
- 04_integrations.md
- 05_runtime.md
- 06_qiserver_runtime_profile.md
- 07_tech_stack.md
- _index.md

## 50_applications/
- 01_portal.md
- 02_admin.md
- 03_tools.md
- 04_interfaces.md
- _index.md

## 60_operations/
- 01_cases.md
- 02_templates.md
- _index.md

## 70_appendices/
- 07_superseded_sources/
    - QiAccess_Start_Blueprint.md
    - README.md
    - qi_os_home_blueprint.md
    - tech_stack_markmind.md
- 01_changelog.md
- 02_glossary.md
- 03_migration_notes.md
- 04_legacy_csv_migration_plan.md
- 05_legacy_salvage.md
- 06_qiaccess_start_legacy_quarantine.md

## adr/
- ADR-0000_template.md
- ADR-0001_blueprint_scope.md
- ADR-0002_single_domain_rule.md
- ADR-0003_band_model.md
- ADR-0004_single_account_modular_mode.md
- ADR-0005_fleet_orchestration.md
- ADR-0006_narrative_and_knowledge_consolidation.md
- ADR-0007_unified_front_matter_and_progressive_doc_topology.md
- ADR-0008_qilabs_root.md
- ADR-0009_backup_server_control_plane_and_public_edge_pattern.md
- adr.md

## assets/
- diagrams/
    - diagrams.md
    - markmind-data.json
- images/
    - images.md
- assets.md

## registry/
- band_registry.yaml
- deprecation_registry.yaml
- domain_registry.yaml
- folder_registry.yaml
- infrastructure_registry.yaml
- realms_registry.yaml
- sensitivity_classification.yaml
- subdomain_registry.yaml
- workspace_realms.yaml

## schemas/
- band_registry.schema.json

## scripts/

## standards/
- content_metadata_profile.yaml
- metadata_rules.yaml
- naming_rules.yaml
- pdf_standards.yaml
- repo_rules.yaml

## templates/
- README.md
- _index.md
- adr_template.md
- appendix_template.md
- artifact_template.md
- note_template.md
- operational_template.md
- page_template.md
- registry_reference_template.md
- section_index_template.md
- standard_template.md
- templates.md

## README.md

## _index.md

## file-index.json

## vizvibe.mmd

## Sub title

## Sub title

## Sub title

## Sub title

## Sub title

---------------

# qilabs

## 00_qilabs.workspace

### _root

* why.qilabs_workspace.md
* readme.qilabs_workspace.md
* quickstart.qilabs_workspace.md
* changelog.qilabs_workspace.md
* qilabs.code-workspace
* justfile

### .github

#### issue_template

* architecture_change.md
* bug_report.md
* feature_request.md

#### workflows

* ci.yml
* docs.yml
* lint.yml
* migrations.yml
* release.yml
* test.yml

#### root

* codeowners.github
* pull_request_template.md

### .qios

* docs_compiler.config.json

### .vscode

* settings.json

### 20_manifests

* apps.manifest.json
* connectors.manifest.json
* domains.manifest.json
* repos.manifest.json
* services.manifest.json
* storage.manifest.json

### 30_configs

* .editorconfig
* .gitignore
* repo.rules.json
* tsconfig.root.json
* eslint.config.mjs
* tailwind.config.ts
* postcss.config.js
* env.workspace.example.env

### 50_toolkit

* bootstrap_workspace.ps1
* check_root_clean.ps1
* export_file_inventory.ps1
* generate_tree.ps1
* tree_snapshot.ps1
* verify_env.ps1

### 99_quarantine

* hold_only_until_sorted

## 10_qispark

### _root

* why.qispark.md
* readme.qispark_root.md
* codex.qispark_ai.md
* changelog.qispark.md

### 00_obsidian

#### _root

* why.qispark_obsidian.md
* guide.qispark_obsidian.md

#### .obsidian

* app.json
* appearance.json
* core-plugins.json
* community-plugins.json
* hotkeys.json
* workspace.json

#### plugins

* plugins.qispark_obsidian.md
* plugins.qispark_required.md
* plugins.qispark_optional.md

#### attachments

* rules.qispark_attachments.md
* inbox.attachments_qispark.md

#### canvas

* map.qispark_canvas_index.md
* canvas.qilabs_spine.canvas
* canvas.qispark_nav.canvas

#### cadence

* why.qispark_cadence.md
* cadence.qispark_index.md
* cadence.qispark_daily.md
* cadence.qispark_weekly.md
* cadence.qispark_monthly.md
* cadence.qispark_review.md

### 01_nav

* why.qispark_nav.md
* map.qispark_nav.md

  * mirror_nav
  * public_nav
  * private_nav
  * archive_nav
* map.qispark_tree.md

  * current_tree
  * target_tree
  * move_map
  * rename_map
* registry.qispark_nav.csv
* registry.qispark_routes.csv
* audit.qispark_nav.md

  * bad_names
  * duplicate_nodes
  * stale_routes
  * empty_placeholders

### 10_qilabs.workspace

* why.qispark_mirror_workspace.md
* map.qilabs_workspace_current.md
* map.qilabs_workspace_target.md
* audit.qilabs_workspace_current_tree.md

  * keep
  * move
  * delete
  * quarantine
* plan.qilabs_workspace_cleanup.md

  * scripts_to_move
  * configs_to_keep
  * manifests_to_check
  * quarantine_to_sort
* rules.qilabs_workspace_scope.md

  * setup_only
  * configs
  * extensions
  * workspace_toolkit
  * not_source_truth
  * not_runtime
  * not_kb
* notes.qilabs_workspace_configs.md

  * github
  * qios
  * vscode
  * manifests
  * repo_rules
  * docs_compiler

### 20_qispark

#### core

* why.qispark_kb.md
* guide.qispark_start.md

  * what_this_is
  * how_to_use_it
  * what_lives_here
  * what_does_not_live_here
  * current_state
  * next_moves
* kb.qispark_context.md

  * qilabs
  * workspace
  * qispark
  * qiserver
  * qidrive
  * qiapps
  * terms
  * boundaries
* kb.qispark_current_state.md

  * locked
  * changed
  * still_fluid
  * parked
* kb.qispark_source_map.md

  * what_counts
  * what_does_not_count
  * where_truth_lives
  * where_records_live
  * where_runtime_lives

#### life_stream

* why.qispark_life_stream.md
* timeline.qispark_life.md

  * childhood
  * resets
  * housing
  * work
  * caregiving
  * health
  * relationships
  * faith
  * systems
* events.qispark_life.md

  * dated_events
  * turning_points
  * incidents
  * wins
  * losses
  * unresolved
* journal.qispark_current.md

  * today
  * this_week
  * active_processing
  * open_loops
* journal.qispark_archive.md

  * older_entries
  * finished_threads
  * raw_but_keep

#### creative

* why.qispark_creative.md
* creative.qispark_index.md

  * sermons
  * essays
  * posts
  * scripts
  * fragments
  * titles
* sermons.qispark_drafts.md

  * jesus_savage
  * flip_the_table
  * modern_parables
  * faith_without_fluff
* writing.qispark_fragments.md

  * lines
  * hooks
  * analogies
  * voice_notes
  * unfinished
* posts.qispark_social.md

  * facebook
  * linkedin
  * captions
  * drafts

#### symbols

* why.qispark_symbols.md
* symbols.qispark_713.md

  * meaning
  * appearances
  * patterns
  * caution_notes
  * writing_uses
* symbols.qispark_mirror.md

  * mirror
  * reflection
  * reversal
  * self_other
  * perception
* symbols.qispark_onions.md

  * layers
  * peeling
  * hidden_core
  * emotional_logic
* symbols.qispark_lexicon.md

  * recurring_words
  * personal_terms
  * metaphors
  * phrases
  * shorthand

#### narrative

* why.qispark_narrative.md
* narrative.qispark_identity.md

  * who_i_am
  * what_i_am_building
  * what_i_refuse
  * what_i_keep_learning
* narrative.qispark_themes.md

  * survival
  * systems
  * faith
  * betrayal
  * repair
  * agency
  * legacy
* narrative.qispark_arcs.md

  * origin_arc
  * reset_arc
  * builder_arc
  * caregiver_arc
  * liberation_arc

### 30_qiserver

* why.qispark_mirror_qiserver.md
* map.qiserver_current.md
* map.qiserver_target.md
* plan.qiserver_from_workspace_scripts.md

  * ai
  * apps
  * db
  * deploy
  * dev
  * flow
  * inbox
  * ingest
  * pdf
  * process
  * sync
  * tools
* audit.qiserver_script_routes.md

  * keep_in_workspace
  * move_to_qiserver
  * merge
  * delete
  * quarantine
* notes.qiserver_runtime.md

  * fastapi
  * ollama
  * aider
  * lancedb
  * tmux
  * ports
  * env
* map.qiserver_services.md

  * qiconnect
  * qimemory
  * qiapi
  * qillm
  * qivector
* map.qimemory_pipeline.md

  * capture
  * ingest
  * summarize
  * embed
  * classify
  * route
  * recall

### 40_qidrive

* why.qispark_mirror_qidrive.md
* map.qidrive_current.md
* map.qidrive_target.md
* plan.qidrive_from_qivault.md

  * current_40_qivault
  * target_30_qidrive
  * rename_plan
  * path_risks
  * links_to_update
* notes.qidrive_records.md

  * identity
  * legal
  * money
  * medical
  * housing
  * taxes
  * benefits
* notes.qidrive_evidence.md

  * exhibits
  * screenshots
  * messages
  * pdfs
  * scans
  * photos
  * audio
  * video
* rules.qidrive_evidence.md

  * evidence_lives_here
  * docs_point_here
  * do_not_duplicate_in_qispark
  * redact_before_public

### 50_qiapps

* why.qispark_mirror_qiapps.md
* map.qiapps_current.md
* map.qiapps_target.md
* plan.qiapps_from_60_qiapps.md

  * current_60_qiapps
  * target_40_qiapps
  * rename_plan
  * app_boundaries
  * links_to_update
* spec.qiapps_qilife.md

  * dashboard
  * routines
  * tasks
  * money
  * health
  * legal
  * gigi
* spec.qiapps_qiconnect.md

  * contacts
  * messages
  * clients
  * vendors
  * crm
  * outreach
* spec.qiapps_qinexus.md

  * search
  * retrieval
  * records
  * evidence
  * semantic_index
* spec.qiapps_qidna.md

  * identity
  * rules
  * preferences
  * memory
  * ai_alignment
* spec.qiapps_qiaccess.md

  * accounts
  * devices
  * permissions
  * recovery
  * security

### 60_rules

* why.qispark_rules.md
* rules.qispark_core.md

  * truth
  * leverage
  * naming
  * modularity
  * ai_use
  * human_override
* rules.qispark_docs.md

  * filenames
  * folders
  * markdown
  * frontmatter
  * links
  * archive
* rules.qispark_boundaries.md

  * qispark_not_workspace
  * qispark_not_server
  * qispark_not_drive
  * qispark_not_apps
  * docs_not_evidence
  * maps_not_runtime
* rules.qispark_access.md

  * access_level
  * visibility
  * ai_ingest
  * status
  * sensitive_info
  * public_private

### 70_prompts

* prompts.qispark_build.md

  * nav_cleanup
  * folder_reconcile
  * docs_generate
  * frontmatter_audit
* prompts.qispark_extract.md

  * extract_nav
  * extract_decisions
  * extract_tasks
  * find_contradictions
  * check_privacy
* prompts.qispark_write.md

  * clean_doc
  * compress_notes
  * make_timeline
  * make_plan
  * make_message

### 80_ops

* ops.qispark_maintenance.md

  * add_page
  * update_nav
  * deprecate_page
  * archive_content
  * audit
  * reconcile_names
* ops.qispark_publish.md

  * route_check
  * private_check
  * broken_links
  * export_review
  * handoff_to_qiserver

### 90_runtime

* why.qispark_runtime.md
* runtime.qispark_obsidian.md

  * vault_open
  * plugin_state
  * cadence_state
  * active_file
  * workspace_layout
* runtime.qispark_ai.md

  * active_prompt
  * active_context
  * ingest_ready
  * export_ready
* runtime.qispark_publish.md

  * docs_compile
  * route_check
  * private_check
  * output_handoff

### 91_ref

* ref.qispark_tables.md

  * glossary
  * canonical_names
  * root_index
  * route_index
  * access_values
  * visibility_values
  * ingest_values
  * status_values
* ref.qispark_legacy_names.md

  * qivault_to_qidrive
  * qiapps_old_60
  * qicapture_to_qimemory
  * cloudflare_not_root
  * old_99_system_removed

### 98_archive

* archive.qispark_legacy.md

  * old_nav
  * old_names
  * deprecated_pages
  * removed_routes
  * legacy_qios

## 20_qiserver

### _root

* why.qiserver.md
* readme.qiserver_root.md
* codex.qiserver_ai.md
* changelog.qiserver.md
* env.qiserver.example.env
* justfile

### 00_config

* config.qiserver_runtime.json
* config.qiserver_paths.json
* config.qiserver_ports.json
* config.qiserver_services.json
* config.qiserver_secrets.example.json

### 10_runtime

#### local

* run.qiserver_dev.ps1
* run.qiserver_dev.sh
* run.qiserver_agent.ps1
* run.qiserver_workers.ps1
* check.qiserver_env.ps1
* check.qiserver_env.sh

#### api

* app.qiserver_fastapi.py
* routes.qiserver_health.py
* routes.qiserver_services.py
* routes.qiserver_webhooks.py

#### process

* runner.qiserver_command.py
* runner.qiserver_service.py
* runner.qiserver_worker.py
* scheduler.qiserver_windows_task.xml
* scheduler.qiserver_install.ps1

### 20_data

#### sqlite

* schema.qiserver_sqlite.md
* migrate.qiserver_sqlite.ps1
* seed.qiserver_sqlite.ps1
* reset.qiserver_sqlite.ps1
* start.qiserver_sqlite.ps1
* stop.qiserver_sqlite.ps1

#### supabase

* schema.qiserver_supabase.md
* migrate.qiserver_supabase.ps1
* validate.qiserver_supabase.py
* log.qiserver_supabase_error.py

#### csv

* pipeline.qiserver_csv_import.md
* convert.qiserver_csv_to_md.py
* validate.qiserver_csv.py
* compare.qiserver_csv_md.py

#### vectors

* schema.qiserver_vectors.md
* build.qiserver_vector_index.py
* search.qiserver_vectors.py
* sync.qiserver_vectors.py

### 30_services

#### qiapi

* why.qiapi.md
* service.qiapi.md
* routes.qiapi.py
* auth.qiapi_check.ps1
* health.qiapi.py

#### qillm

* why.qillm.md
* service.qillm.md
* models.qillm.py
* prompts.qillm.py
* rag.qillm_core.py

#### qivector

* why.qivector.md
* service.qivector.md
* index.qivector_build.py
* search.qivector_docs.py
* sync.qivector_index.py

#### qimemory

* why.qimemory.md
* service.qimemory.md

##### capture

* capture.qimemory_audio.py
* capture.qimemory_files.py
* capture.qimemory_web.py
* capture.qimemory_screenshots.py

##### inbox

* audit.qimemory_inbox.ts
* normalize.qimemory_inbox.ts
* dedup.qimemory_inbox.ts
* rename.qimemory_inbox.py
* run.qimemory_inbox.ts

##### ingest

* ingest.qimemory_audio.py
* ingest.qimemory_files.py
* ingest.qimemory_pdf.ts
* ingest.qimemory_video.py
* ingest.qimemory_web.py

##### process

* process.qimemory_clean.py
* process.qimemory_normalize.py
* process.qimemory_summarize.py
* process.qimemory_classify.py
* process.qimemory_route.py
* process.qimemory_embed.py

##### recall

* recall.qimemory_search.py
* recall.qimemory_context.py
* recall.qimemory_profile.py

#### qiconnect

* why.qiconnect_server.md
* service.qiconnect.md

##### contacts

* service.qiconnect_contacts.py
* sync.qiconnect_contacts.py

##### mail

* service.qiconnect_mail.py
* get.qiconnect_mail_recent.py
* send.qiconnect_mail.py

##### calendar

* service.qiconnect_calendar.py
* get.qiconnect_calendar_upcoming.py
* create.qiconnect_calendar_event.py

##### sms

* service.qiconnect_sms.py
* send.qiconnect_sms.py

##### web

* service.qiconnect_web.py
* get.qiconnect_web.py
* search.qiconnect_web.py

##### cloudflare

* why.qiconnect_cloudflare.md
* service.qiconnect_cloudflare.md
* deploy.qiconnect_cloudflare.ps1
* deploy.qiconnect_workers.ps1
* get.qiconnect_worker_urls.ps1
* routes.qiconnect_cloudflare.json
* redirects.qiconnect_cloudflare.json

### 40_apps_runtime

#### qilife

* service.qilife_runtime.md
* routes.qilife_api.py
* jobs.qilife_sync.py

#### qinexus

* service.qinexus_runtime.md
* routes.qinexus_search.py
* jobs.qinexus_index.py

#### qidna

* service.qidna_runtime.md
* routes.qidna_profile.py
* jobs.qidna_sync.py

#### qiaccess

* service.qiaccess_runtime.md
* routes.qiaccess_auth.py
* jobs.qiaccess_check.py

### 50_jobs

#### sync

* job.qiserver_sync.py
* sync.qiserver_git.py
* sync.qiserver_gdrive.py
* sync.qiserver_index.ts

#### backup

* job.qiserver_backup.py
* backup.qiserver_data.ps1
* restore.qiserver_data.ps1

#### ingest

* job.qiserver_ingest.py
* queue.qiserver_ingest.py

#### cleanup

* job.qiserver_cleanup.py
* clean.qiserver_storage.py
* clean.qiserver_duplicates.py

#### deploy

* job.qiserver_deploy.py
* deploy.qiserver_all.ps1
* deploy.qiserver_critical.ps1

### 60_tools

#### repo

* validate.qiserver_paths.py
* lint.qiserver_tree.py
* enforce.qiserver_structure.py
* print.qiserver_tree.py

#### frontmatter

* add.qiserver_frontmatter.py
* validate.qiserver_frontmatter.ts
* enforce.qiserver_frontmatter.py

#### maps

* map.qiserver_tree.py
* map.qiserver_slugs.py

#### debug

* debug.qiserver_maps.py
* test.qiserver_pipeline.ps1
* verify.qiserver_env.ps1
* verify.qiserver_env.sh

### 70_logs

* logs.qiserver.md

  * runtime
  * errors
  * deploy
  * ingest
  * memory
  * sync

### 80_ops

* ops.qiserver_maintenance.md

  * setup
  * start
  * stop
  * restart
  * backup
  * restore
  * troubleshoot
* ops.qiserver_deploy.md

  * local
  * cloudflare
  * rollback
  * env_check
* ops.qiserver_migration_from_workspace.md

  * scripts_to_move
  * scripts_to_merge
  * scripts_to_delete
  * scripts_to_quarantine

### 90_rules

* rules.qiserver_scope.md

  * runtime_lives_here
  * services_live_here
  * secrets_never_public
  * qiserver_not_kb
  * qiserver_not_drive
  * qiserver_not_workspace
  * logs_not_docs
  * do_not_put_here

## 30_qidrive

<!-- currently: 40_qivault -->

### _root

* why.qidrive.md
* readme.qidrive_root.md
* changelog.qidrive.md
* rules.qidrive_scope.md

### 00_index

* index.qidrive_records.md
* index.qidrive_evidence.md
* index.qidrive_exports.md
* index.qidrive_mirrors.md

### 10_records

#### identity

* why.identity.md
* ids
* licenses
* social_security
* immigration

#### legal

* why.legal.md
* claims
* notices
* filings
* court
* contracts

#### money

* why.money.md
* income
* bills
* taxes
* disputes
* receipts

#### medical

* why.medical.md
* visits
* prescriptions
* insurance
* hospital
* care

#### housing

* why.housing.md
* lease
* utilities
* repairs
* notices
* photos

### 20_evidence

#### exhibits

* why.exhibits.md
* active
* final
* sent
* archived

#### screenshots

* why.screenshots.md
* messages
* websites
* apps
* receipts
* errors

#### messages

* why.messages.md
* sms
* email
* messenger
* whatsapp
* transcripts

#### pdfs

* why.pdfs.md
* forms
* letters
* notices
* records
* packets

#### media

* why.media.md
* photos
* audio
* video
* scans

### 30_drive_mirror

#### google_drive

* why.google_drive.md
* my_drive
* shared_with_me
* exports
* upload_queue

#### local_mirror

* why.local_mirror.md
* active_sync
* offline_cache
* restore_points

#### archive_mirror

* why.archive_mirror.md
* cold_storage
* old_exports
* deprecated_sets

### 40_exports

#### packets

* why.packets.md
* legal_packets
* exhibit_packets
* client_packets
* admin_packets

#### machine_exports

* why.machine_exports.md
* csv
* json
* markdown
* zip

### 50_pointers

* pointers.qidrive_files.csv
* pointers.qidrive_evidence.csv
* pointers.qidrive_records.csv

### 90_rules

* rules.qidrive_access.md

  * private_by_default
  * redact_before_public
  * qidrive_holds_blobs
  * qispark_holds_meaning
  * qiserver_indexes_and_processes
  * qiapps_request_through_qiserver

## 40_qiapps

<!-- currently: 60_qiapps -->

### _root

* why.qiapps.md
* readme.qiapps_root.md
* changelog.qiapps.md
* rules.qiapps_scope.md

### 00_shared

#### ui

* why.shared_ui.md
* components
* layouts
* themes
* icons

#### config

* config.qiapps_shared.json
* config.qiapps_routes.json

#### patterns

* patterns.qiapps_navigation.md
* patterns.qiapps_cards.md
* patterns.qiapps_forms.md

### 10_qilife

* why.qilife.md
* spec.qilife_app.md
* map.qilife_flows.md
* backlog.qilife.md

#### ui

* dashboard
* routines
* tasks
* money
* health
* legal
* gigi

#### config

* config.qilife_routes.json
* config.qilife_views.json

### 20_qiconnect

* why.qiconnect.md
* spec.qiconnect_app.md
* map.qiconnect_flows.md
* backlog.qiconnect.md

#### ui

* contacts
* messages
* clients
* vendors
* crm
* outreach

#### config

* config.qiconnect_routes.json
* config.qiconnect_views.json

### 30_qinexus

* why.qinexus.md
* spec.qinexus_app.md
* map.qinexus_flows.md
* backlog.qinexus.md

#### ui

* search
* retrieval
* records
* evidence
* semantic_index

#### config

* config.qinexus_routes.json
* config.qinexus_views.json

### 40_qidna

* why.qidna.md
* spec.qidna_app.md
* map.qidna_flows.md
* backlog.qidna.md

#### ui

* identity
* rules
* preferences
* memory
* ai_alignment

#### config

* config.qidna_routes.json
* config.qidna_views.json

### 50_qiaccess

* why.qiaccess.md
* spec.qiaccess_app.md
* map.qiaccess_flows.md
* backlog.qiaccess.md

#### ui

* accounts
* devices
* permissions
* recovery
* security

#### config

* config.qiaccess_routes.json
* config.qiaccess_views.json

### 90_rules

* rules.qiapps_boundaries.md

  * apps_not_server_runtime
  * apps_not_drive_storage
  * apps_not_kb
  * api_calls_go_to_qiserver
  * files_come_from_qidrive_pointers
  * docs_live_in_qispark
