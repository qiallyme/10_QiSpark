# Supabase Database Full ERD Map

## Summary
- Schemas: `21`
- Tables: `144`
- Fields: `1455`

## Schema: auth

### auth.audit_log_entries
- Estimated rows: `-1`
- Comment: Auth: Audit trail for user actions.
- Fields
  - instance_id : `uuid`
  - id : `uuid` 🔑 PK NOT NULL
  - payload : `json`
  - created_at : `timestamptz`
  - ip_address : `varchar` NOT NULL DEFAULT `''::character varying`

### auth.custom_oauth_providers
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - provider_type : `text` NOT NULL
  - identifier : `text` NOT NULL
  - name : `text` NOT NULL
  - client_id : `text` NOT NULL
  - client_secret : `text` NOT NULL
  - acceptable_client_ids : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - scopes : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - pkce_enabled : `bool` NOT NULL DEFAULT `true`
  - attribute_mapping : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - authorization_params : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - enabled : `bool` NOT NULL DEFAULT `true`
  - email_optional : `bool` NOT NULL DEFAULT `false`
  - issuer : `text`
  - discovery_url : `text`
  - skip_nonce_check : `bool` NOT NULL DEFAULT `false`
  - cached_discovery : `jsonb`
  - discovery_cached_at : `timestamptz`
  - authorization_url : `text`
  - token_url : `text`
  - userinfo_url : `text`
  - jwks_uri : `text`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### auth.flow_state
- Estimated rows: `-1`
- Comment: Stores metadata for all OAuth/SSO login flows
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - user_id : `uuid`
  - auth_code : `text`
  - code_challenge_method : `code_challenge_method`
  - code_challenge : `text`
  - provider_type : `text` NOT NULL
  - provider_access_token : `text`
  - provider_refresh_token : `text`
  - created_at : `timestamptz`
  - updated_at : `timestamptz`
  - authentication_method : `text` NOT NULL
  - auth_code_issued_at : `timestamptz`
  - invite_token : `text`
  - referrer : `text`
  - oauth_client_state_id : `uuid`
  - linking_target_id : `uuid`
  - email_optional : `bool` NOT NULL DEFAULT `false`

### auth.identities
- Estimated rows: `-1`
- Comment: Auth: Stores identities associated to a user.
- Fields
  - provider_id : `text` NOT NULL
  - user_id : `uuid` NOT NULL
  - identity_data : `jsonb` NOT NULL
  - provider : `text` NOT NULL
  - last_sign_in_at : `timestamptz`
  - created_at : `timestamptz`
  - updated_at : `timestamptz`
  - email : `text`
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`

### auth.instances
- Estimated rows: `-1`
- Comment: Auth: Manages users across multiple sites.
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - uuid : `uuid`
  - raw_base_config : `text`
  - created_at : `timestamptz`
  - updated_at : `timestamptz`

### auth.mfa_amr_claims
- Estimated rows: `-1`
- Comment: auth: stores authenticator method reference claims for multi factor authentication
- Fields
  - session_id : `uuid` NOT NULL
  - created_at : `timestamptz` NOT NULL
  - updated_at : `timestamptz` NOT NULL
  - authentication_method : `text` NOT NULL
  - id : `uuid` 🔑 PK NOT NULL

### auth.mfa_challenges
- Estimated rows: `-1`
- Comment: auth: stores metadata about challenge requests made
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - factor_id : `uuid` NOT NULL
  - created_at : `timestamptz` NOT NULL
  - verified_at : `timestamptz`
  - ip_address : `inet` NOT NULL
  - otp_code : `text`
  - web_authn_session_data : `jsonb`

### auth.mfa_factors
- Estimated rows: `-1`
- Comment: auth: stores metadata about factors
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - user_id : `uuid` NOT NULL
  - friendly_name : `text`
  - factor_type : `factor_type` NOT NULL
  - status : `factor_status` NOT NULL
  - created_at : `timestamptz` NOT NULL
  - updated_at : `timestamptz` NOT NULL
  - secret : `text`
  - phone : `text`
  - last_challenged_at : `timestamptz`
  - web_authn_credential : `jsonb`
  - web_authn_aaguid : `uuid`
  - last_webauthn_challenge_data : `jsonb`

### auth.oauth_authorizations
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - authorization_id : `text` NOT NULL
  - client_id : `uuid` NOT NULL
  - user_id : `uuid`
  - redirect_uri : `text` NOT NULL
  - scope : `text` NOT NULL
  - state : `text`
  - resource : `text`
  - code_challenge : `text`
  - code_challenge_method : `code_challenge_method`
  - response_type : `oauth_response_type` NOT NULL DEFAULT `'code'::auth.oauth_response_type`
  - status : `oauth_authorization_status` NOT NULL DEFAULT `'pending'::auth.oauth_authorization_status`
  - authorization_code : `text`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - expires_at : `timestamptz` NOT NULL DEFAULT `(now() + '00:03:00'::interval)`
  - approved_at : `timestamptz`
  - nonce : `text`

### auth.oauth_client_states
- Estimated rows: `-1`
- Comment: Stores OAuth states for third-party provider authentication flows where Supabase acts as the OAuth client.
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - provider_type : `text` NOT NULL
  - code_verifier : `text`
  - created_at : `timestamptz` NOT NULL

### auth.oauth_clients
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - client_secret_hash : `text`
  - registration_type : `oauth_registration_type` NOT NULL
  - redirect_uris : `text` NOT NULL
  - grant_types : `text` NOT NULL
  - client_name : `text`
  - client_uri : `text`
  - logo_uri : `text`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`
  - deleted_at : `timestamptz`
  - client_type : `oauth_client_type` NOT NULL DEFAULT `'confidential'::auth.oauth_client_type`
  - token_endpoint_auth_method : `text` NOT NULL

### auth.oauth_consents
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - user_id : `uuid` NOT NULL
  - client_id : `uuid` NOT NULL
  - scopes : `text` NOT NULL
  - granted_at : `timestamptz` NOT NULL DEFAULT `now()`
  - revoked_at : `timestamptz`

### auth.one_time_tokens
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - user_id : `uuid` NOT NULL
  - token_type : `one_time_token_type` NOT NULL
  - token_hash : `text` NOT NULL
  - relates_to : `text` NOT NULL
  - created_at : `timestamp` NOT NULL DEFAULT `now()`
  - updated_at : `timestamp` NOT NULL DEFAULT `now()`

### auth.refresh_tokens
- Estimated rows: `-1`
- Comment: Auth: Store of tokens used to refresh JWT tokens once they expire.
- Fields
  - instance_id : `uuid`
  - id : `int8` 🔑 PK NOT NULL DEFAULT `nextval('auth.refresh_tokens_id_seq'::regclass)`
  - token : `varchar`
  - user_id : `varchar`
  - revoked : `bool`
  - created_at : `timestamptz`
  - updated_at : `timestamptz`
  - parent : `varchar`
  - session_id : `uuid`

### auth.saml_providers
- Estimated rows: `-1`
- Comment: Auth: Manages SAML Identity Provider connections.
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - sso_provider_id : `uuid` NOT NULL
  - entity_id : `text` NOT NULL
  - metadata_xml : `text` NOT NULL
  - metadata_url : `text`
  - attribute_mapping : `jsonb`
  - created_at : `timestamptz`
  - updated_at : `timestamptz`
  - name_id_format : `text`

### auth.saml_relay_states
- Estimated rows: `-1`
- Comment: Auth: Contains SAML Relay State information for each Service Provider initiated login.
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - sso_provider_id : `uuid` NOT NULL
  - request_id : `text` NOT NULL
  - for_email : `text`
  - redirect_to : `text`
  - created_at : `timestamptz`
  - updated_at : `timestamptz`
  - flow_state_id : `uuid`

### auth.schema_migrations
- Estimated rows: `76`
- Comment: Auth: Manages updates to the auth system.
- Fields
  - version : `varchar` NOT NULL

### auth.sessions
- Estimated rows: `-1`
- Comment: Auth: Stores session data associated to a user.
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - user_id : `uuid` NOT NULL
  - created_at : `timestamptz`
  - updated_at : `timestamptz`
  - factor_id : `uuid`
  - aal : `aal_level`
  - not_after : `timestamptz`
  - refreshed_at : `timestamp`
  - user_agent : `text`
  - ip : `inet`
  - tag : `text`
  - oauth_client_id : `uuid`
  - refresh_token_hmac_key : `text`
  - refresh_token_counter : `int8`
  - scopes : `text`

### auth.sso_domains
- Estimated rows: `-1`
- Comment: Auth: Manages SSO email address domain mapping to an SSO Identity Provider.
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - sso_provider_id : `uuid` NOT NULL
  - domain : `text` NOT NULL
  - created_at : `timestamptz`
  - updated_at : `timestamptz`

### auth.sso_providers
- Estimated rows: `-1`
- Comment: Auth: Manages SSO identity provider information; see saml_providers for SAML.
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - resource_id : `text`
  - created_at : `timestamptz`
  - updated_at : `timestamptz`
  - disabled : `bool`

### auth.users
- Estimated rows: `-1`
- Comment: Auth: Stores user login data within a secure schema.
- Fields
  - instance_id : `uuid`
  - id : `uuid` 🔑 PK NOT NULL
  - aud : `varchar`
  - role : `varchar`
  - email : `varchar`
  - encrypted_password : `varchar`
  - email_confirmed_at : `timestamptz`
  - invited_at : `timestamptz`
  - confirmation_token : `varchar`
  - confirmation_sent_at : `timestamptz`
  - recovery_token : `varchar`
  - recovery_sent_at : `timestamptz`
  - email_change_token_new : `varchar`
  - email_change : `varchar`
  - email_change_sent_at : `timestamptz`
  - last_sign_in_at : `timestamptz`
  - raw_app_meta_data : `jsonb`
  - raw_user_meta_data : `jsonb`
  - is_super_admin : `bool`
  - created_at : `timestamptz`
  - updated_at : `timestamptz`
  - phone : `text` DEFAULT `NULL::character varying`
  - phone_confirmed_at : `timestamptz`
  - phone_change : `text` DEFAULT `''::character varying`
  - phone_change_token : `varchar` DEFAULT `''::character varying`
  - phone_change_sent_at : `timestamptz`
  - confirmed_at : `timestamptz`
  - email_change_token_current : `varchar` DEFAULT `''::character varying`
  - email_change_confirm_status : `int2` DEFAULT `0`
  - banned_until : `timestamptz`
  - reauthentication_token : `varchar` DEFAULT `''::character varying`
  - reauthentication_sent_at : `timestamptz`
  - is_sso_user : `bool` NOT NULL DEFAULT `false`
  - deleted_at : `timestamptz`
  - is_anonymous : `bool` NOT NULL DEFAULT `false`

### auth.webauthn_challenges
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - user_id : `uuid`
  - challenge_type : `text` NOT NULL
  - session_data : `jsonb` NOT NULL
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - expires_at : `timestamptz` NOT NULL

### auth.webauthn_credentials
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - user_id : `uuid` NOT NULL
  - credential_id : `bytea` NOT NULL
  - public_key : `bytea` NOT NULL
  - attestation_type : `text` NOT NULL DEFAULT `''::text`
  - aaguid : `uuid`
  - sign_count : `int8` NOT NULL DEFAULT `0`
  - transports : `jsonb` NOT NULL DEFAULT `'[]'::jsonb`
  - backup_eligible : `bool` NOT NULL DEFAULT `false`
  - backed_up : `bool` NOT NULL DEFAULT `false`
  - friendly_name : `text` NOT NULL DEFAULT `''::text`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`
  - last_used_at : `timestamptz`

## Schema: care

### care.attachments
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - encounter_id : `uuid` 🔗 FK → care.encounters.id
  - file_name : `text`
  - file_type : `text`
  - storage_path : `text`
  - attachment_kind : `text`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - uploaded_at : `timestamptz` NOT NULL DEFAULT `now()`
  - discharge_document_id : `uuid` 🔗 FK → care.discharge_documents.id
  - care_plan_id : `uuid` 🔗 FK → care.care_plans.id

### care.care_daily_notes
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - household_id : `uuid`
  - caregiver_id : `uuid`
  - note_date : `date` NOT NULL
  - caregiver_name : `text`
  - sleep_last_night : `text`
  - overall_day : `text`
  - o2_range : `text`
  - heart_rate : `text`
  - blood_pressure : `text`
  - temperature : `text`
  - breathing_quality : `text`
  - symptoms : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - last_morphine_time : `text`
  - last_norco_time : `text`
  - nebulizers_completed : `bool`
  - prednisone_taken : `bool`
  - blood_sugar_checked : `bool`
  - medication_notes : `text`
  - transfer_status : `text`
  - bathroom_status : `text`
  - walking_standing : `text`
  - mental_state : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - key_notes_events : `text`
  - red_flags : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - urgent_followup : `bool` NOT NULL DEFAULT `false`
  - is_printed : `bool` NOT NULL DEFAULT `false`
  - printed_at : `timestamptz`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`
  - deleted_at : `timestamptz`

### care.care_events
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - event_type : `text` NOT NULL
  - event_category : `text`
  - title : `text` NOT NULL
  - description : `text`
  - severity : `text`
  - occurred_at : `timestamptz` NOT NULL DEFAULT `now()`
  - related_table : `text`
  - related_id : `uuid`
  - caregiver_name : `text`
  - followup_needed : `bool` NOT NULL DEFAULT `false`
  - followup_status : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.care_locations
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - name : `text` NOT NULL
  - location_type : `text`
  - parent_location_id : `uuid` 🔗 FK → care.care_locations.id
  - notes : `text`
  - active : `bool` NOT NULL DEFAULT `true`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.care_plan_items
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - care_plan_id : `uuid` 🔗 FK → care.care_plans.id NOT NULL
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - category : `text`
  - item_text : `text` NOT NULL
  - frequency : `text`
  - status : `text`
  - target_metric : `text`
  - target_value : `numeric`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.care_plans
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - title : `text` NOT NULL
  - status : `text`
  - start_date : `date`
  - end_date : `date`
  - created_by : `text`
  - source_type : `text`
  - summary : `text`
  - precautions : `text`
  - escalation_rules : `text`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.conditions
- Estimated rows: `5`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - category : `text`
  - summary : `text`
  - risks : `text`
  - actions : `text`
  - status : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`
  - condition_name : `text`
  - medical_code : `text`
  - code_system : `text`
  - watch_fors : `text`
  - interaction_summary : `text`
  - compounding_risks : `text`

### care.device_profiles
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - device_type : `text` NOT NULL
  - manufacturer : `text`
  - model : `text`
  - serial_number : `text`
  - active : `bool` NOT NULL DEFAULT `true`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.device_readings
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - device_profile_id : `uuid` 🔗 FK → care.device_profiles.id NOT NULL
  - reading_type : `text`
  - reading_name : `text` NOT NULL
  - reading_value : `numeric`
  - reading_unit : `text`
  - recorded_at : `timestamptz` NOT NULL DEFAULT `now()`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.discharge_actions
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - discharge_document_id : `uuid` 🔗 FK → care.discharge_documents.id NOT NULL
  - action_type : `text`
  - action_text : `text` NOT NULL
  - due_date : `date`
  - status : `text`
  - completed_at : `timestamptz`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.discharge_documents
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - encounter_id : `uuid` 🔗 FK → care.encounters.id
  - document_title : `text`
  - discharge_date : `date`
  - facility : `text`
  - provider_name : `text`
  - summary : `text`
  - medication_changes_text : `text`
  - follow_up_text : `text`
  - warning_signs_text : `text`
  - raw_text : `text`
  - status : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.encounters
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - encounter_type : `text`
  - provider_name : `text`
  - facility : `text`
  - status : `text`
  - occurred_at : `timestamptz`
  - summary : `text`
  - med_changes : `text`
  - follow_up_needed : `text`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.interactions
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - med1 : `text`
  - med2 : `text`
  - severity : `text`
  - description : `text`
  - recommendation : `text`
  - source_notes : `text`
  - metadata_json : `jsonb` DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` DEFAULT `now()`

### care.kb_sections
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - title : `text` NOT NULL
  - category : `text`
  - section_key : `text`
  - summary : `text`
  - content : `text` NOT NULL
  - content_format : `text` NOT NULL DEFAULT `'markdown'::text`
  - source_type : `text`
  - source_path : `text`
  - source_title : `text`
  - tags : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - ai_retrievable : `bool` NOT NULL DEFAULT `true`
  - review_status : `text` NOT NULL DEFAULT `'active'::text`
  - sort_order : `int4` NOT NULL DEFAULT `0`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.medication_events
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - medication_id : `uuid` 🔗 FK → care.medications.id
  - encounter_id : `uuid` 🔗 FK → care.encounters.id
  - action : `text` NOT NULL
  - dose_taken : `text`
  - quantity_change : `numeric`
  - reason : `text`
  - notes : `text`
  - source_type : `text`
  - occurred_at : `timestamptz` NOT NULL DEFAULT `now()`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - discharge_document_id : `uuid` 🔗 FK → care.discharge_documents.id

### care.medications
- Estimated rows: `50`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - medication_name : `text` NOT NULL
  - strength : `text`
  - form : `text`
  - prescriber : `text`
  - dosage_instructions : `text`
  - frequency : `text`
  - quantity_prescribed : `numeric`
  - quantity_remaining : `numeric`
  - active : `bool` NOT NULL DEFAULT `true`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`
  - expiration_date : `date`
  - refills_allowed : `int4`
  - prescribed_date : `date`
  - prescription_notes : `text`
  - medication_image_url : `text`
  - barcode : `text`
  - strength_value : `numeric`
  - strength_unit : `text`
  - route : `text`
  - unit_type : `text`
  - low_supply_threshold : `numeric`
  - pharmacy_source : `text`
  - cost : `numeric`
  - medication_status : `text` NOT NULL DEFAULT `'active'::text`
  - hold_reason : `text`
  - hold_started_at : `timestamptz`
  - hold_requested_by : `text`
  - hold_notes : `text`
  - clinician_review_needed : `bool` NOT NULL DEFAULT `false`
  - review_reason : `text`

### care.milestones
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - name : `text` NOT NULL
  - metric : `text`
  - value : `numeric`
  - baseline_value : `numeric`
  - target_value : `numeric`
  - unit : `text`
  - notes : `text`
  - recorded_at : `timestamptz` NOT NULL DEFAULT `now()`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - care_plan_id : `uuid` 🔗 FK → care.care_plans.id

### care.observations
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - encounter_id : `uuid` 🔗 FK → care.encounters.id
  - category : `text`
  - subtype : `text`
  - severity : `int4`
  - body_area : `text`
  - notes : `text`
  - recorded_at : `timestamptz` NOT NULL DEFAULT `now()`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - care_plan_id : `uuid` 🔗 FK → care.care_plans.id

### care.oxygen_tank_types
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - type_code : `text` NOT NULL
  - display_name : `text` NOT NULL
  - standard_capacity_liters : `numeric`
  - standard_full_pressure_psi : `numeric`
  - reserve_pressure_psi : `numeric`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.oxygen_tanks
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - tank_label : `text`
  - tank_type : `text`
  - capacity_liters : `numeric`
  - current_status : `text`
  - last_pressure_psi : `numeric`
  - last_checked_at : `timestamptz`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`
  - tank_type_id : `uuid` 🔗 FK → care.oxygen_tank_types.id

### care.oxygen_tanks_with_runtime
- Estimated rows: `0`
- Fields
  - id : `uuid`
  - patient_id : `uuid`
  - tank_label : `text`
  - tank_type : `text`
  - tank_type_id : `uuid`
  - type_code : `text`
  - tank_type_name : `text`
  - standard_capacity_liters : `numeric`
  - standard_full_pressure_psi : `numeric`
  - reserve_pressure_psi : `numeric`
  - current_status : `text`
  - last_pressure_psi : `numeric`
  - last_checked_at : `timestamptz`
  - flow_rate_lpm : `numeric`
  - estimated_liters_remaining : `numeric`
  - estimated_runtime_minutes : `numeric`
  - estimated_runtime_hours : `numeric`
  - calculated_pressure_status : `text`
  - notes : `text`
  - metadata_json : `jsonb`
  - created_at : `timestamptz`
  - updated_at : `timestamptz`

### care.oxygen_usage_sessions
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - oxygen_tank_id : `uuid` 🔗 FK → care.oxygen_tanks.id NOT NULL
  - started_at : `timestamptz`
  - ended_at : `timestamptz`
  - flow_rate_lpm : `numeric`
  - starting_pressure_psi : `numeric`
  - ending_pressure_psi : `numeric`
  - estimated_empty_at : `timestamptz`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.patients
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - full_name : `text`
  - dob : `date`
  - baseline_notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.regimen_events
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - regimen_id : `uuid` 🔗 FK → care.regimens.id NOT NULL
  - status : `text` NOT NULL
  - performed_at : `timestamptz` NOT NULL DEFAULT `now()`
  - notes : `text`
  - source_type : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`

### care.regimens
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - regimen_type : `text` NOT NULL
  - title : `text` NOT NULL
  - linked_medication_id : `uuid` 🔗 FK → care.medications.id
  - instructions : `text`
  - with_food : `bool`
  - food_instruction_text : `text`
  - is_prn : `bool` NOT NULL DEFAULT `false`
  - min_interval_minutes : `int4`
  - schedule_type : `text` NOT NULL
  - schedule_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - active : `bool` NOT NULL DEFAULT `true`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.station_requirements
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - location_id : `uuid` 🔗 FK → care.care_locations.id NOT NULL
  - supply_item_id : `uuid` 🔗 FK → care.supply_items.id NOT NULL
  - par_level : `numeric`
  - minimum_level : `numeric`
  - required : `bool` NOT NULL DEFAULT `true`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.supply_events
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - supply_item_id : `uuid` 🔗 FK → care.supply_items.id NOT NULL
  - event_type : `text` NOT NULL
  - quantity_change : `numeric` NOT NULL
  - occurred_at : `timestamptz` NOT NULL DEFAULT `now()`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.supply_inventory
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - supply_item_id : `uuid` 🔗 FK → care.supply_items.id NOT NULL
  - quantity_on_hand : `numeric` NOT NULL DEFAULT `0`
  - quantity_reserved : `numeric` NOT NULL DEFAULT `0`
  - last_counted_at : `timestamptz`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.supply_items
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - name : `text` NOT NULL
  - category : `text`
  - unit : `text`
  - reorder_threshold : `numeric`
  - target_stock_level : `numeric`
  - notes : `text`
  - active : `bool` NOT NULL DEFAULT `true`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`
  - location : `text`
  - status : `text`
  - cost : `numeric`

### care.supply_order_items
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - order_id : `uuid` 🔗 FK → care.supply_orders.id NOT NULL
  - supply_item_id : `uuid` 🔗 FK → care.supply_items.id NOT NULL
  - quantity_ordered : `numeric` NOT NULL DEFAULT `0`
  - quantity_received : `numeric` NOT NULL DEFAULT `0`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.supply_orders
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - vendor_contact_id : `uuid`
  - status : `text`
  - ordered_at : `timestamptz`
  - expected_at : `timestamptz`
  - received_at : `timestamptz`
  - notes : `text`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### care.vitals
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - patient_id : `uuid` 🔗 FK → care.patients.id NOT NULL
  - encounter_id : `uuid` 🔗 FK → care.encounters.id
  - systolic : `int4`
  - diastolic : `int4`
  - pulse : `int4`
  - oxygen : `int4`
  - temp : `numeric`
  - context : `text`
  - notes : `text`
  - recorded_at : `timestamptz` NOT NULL DEFAULT `now()`
  - metadata_json : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - glucose : `numeric`
  - ketones : `numeric`
  - weight : `numeric`
  - respiratory_rate : `int4`

## Schema: cron

### cron.job
- Estimated rows: `-1`
- Fields
  - jobid : `int8` NOT NULL DEFAULT `nextval('cron.jobid_seq'::regclass)`
  - schedule : `text` NOT NULL
  - command : `text` NOT NULL
  - nodename : `text` NOT NULL DEFAULT `'localhost'::text`
  - nodeport : `int4` NOT NULL DEFAULT `inet_server_port()`
  - database : `text` NOT NULL DEFAULT `current_database()`
  - username : `text` NOT NULL DEFAULT `CURRENT_USER`
  - active : `bool` NOT NULL DEFAULT `true`
  - jobname : `text`

### cron.job_run_details
- Estimated rows: `-1`
- Fields
  - jobid : `int8`
  - runid : `int8` 🔑 PK NOT NULL DEFAULT `nextval('cron.runid_seq'::regclass)`
  - job_pid : `int4`
  - database : `text`
  - username : `text`
  - command : `text`
  - status : `text`
  - return_message : `text`
  - start_time : `timestamptz`
  - end_time : `timestamptz`

## Schema: notion

### notion.blocks
- Estimated rows: `0`
- Fields
  - id : `text`
  - page_id : `text`
  - type : `text`
  - created_time : `timestamp`
  - last_edited_time : `timestamp`
  - archived : `bool`
  - attrs : `jsonb`

### notion.databases
- Estimated rows: `0`
- Fields
  - id : `text`
  - url : `text`
  - created_time : `timestamp`
  - last_edited_time : `timestamp`
  - archived : `bool`
  - attrs : `jsonb`

### notion.pages
- Estimated rows: `0`
- Fields
  - id : `text`
  - url : `text`
  - created_time : `timestamp`
  - last_edited_time : `timestamp`
  - archived : `bool`
  - attrs : `jsonb`

### notion.users
- Estimated rows: `0`
- Fields
  - id : `text`
  - name : `text`
  - type : `text`
  - avatar_url : `text`
  - attrs : `jsonb`

## Schema: public

### public.chat_messages
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - room_id : `uuid` 🔗 FK → public.chat_rooms.id NOT NULL
  - sender_id : `uuid` 🔗 FK → public.profiles.id NOT NULL
  - client_message_id : `uuid` NOT NULL
  - body : `text` NOT NULL
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - deleted_at : `timestamptz`

### public.chat_room_members
- Estimated rows: `-1`
- Fields
  - room_id : `uuid` 🔑 PK 🔗 FK → public.chat_rooms.id NOT NULL
  - user_id : `uuid` 🔑 PK 🔗 FK → public.profiles.id NOT NULL
  - joined_at : `timestamptz` NOT NULL DEFAULT `now()`
  - left_at : `timestamptz`

### public.chat_rooms
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - name : `text` NOT NULL
  - created_by : `uuid` 🔗 FK → public.profiles.id NOT NULL
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### public.dev_history
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - owner_id : `uuid` NOT NULL
  - session_id : `text` NOT NULL
  - record_type : `text` NOT NULL DEFAULT `'dev_session'::text`
  - schema_version : `text` NOT NULL DEFAULT `'1.0'::text`
  - session_date : `date` NOT NULL DEFAULT `CURRENT_DATE`
  - title : `text` NOT NULL
  - project : `text`
  - repo : `text`
  - branch : `text`
  - feature_area : `text`
  - session_type : `text`
  - status : `text` NOT NULL DEFAULT `'draft'::text`
  - summary : `text`
  - purpose : `text`
  - context : `text`
  - final_outcome : `text`
  - restart_prompt : `text`
  - decisions : `jsonb` NOT NULL DEFAULT `'[]'::jsonb`
  - files_affected : `jsonb` NOT NULL DEFAULT `'[]'::jsonb`
  - folders_affected : `jsonb` NOT NULL DEFAULT `'[]'::jsonb`
  - database_notes : `jsonb` NOT NULL DEFAULT `'[]'::jsonb`
  - implementation_plan : `jsonb` NOT NULL DEFAULT `'[]'::jsonb`
  - code_artifacts : `jsonb` NOT NULL DEFAULT `'[]'::jsonb`
  - prompts : `jsonb` NOT NULL DEFAULT `'[]'::jsonb`
  - risks : `jsonb` NOT NULL DEFAULT `'[]'::jsonb`
  - validation_checklist : `jsonb` NOT NULL DEFAULT `'[]'::jsonb`
  - next_actions : `jsonb` NOT NULL DEFAULT `'[]'::jsonb`
  - markdown_body : `text`
  - tags : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - related_files : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - related_tables : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - related_tools : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - artifact_paths : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - artifact_urls : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - source : `text` NOT NULL DEFAULT `'qiaccess_capture'::text`
  - created_by : `text`
  - metadata : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### public.ingestion_queue
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - file_path : `text` NOT NULL
  - slug : `text` NOT NULL
  - qid : `text`
  - realm : `text`
  - realm_guess : `text`
  - realm_slug : `text`
  - mime_type : `text`
  - file_ext : `text`
  - content_hash : `text`
  - extracted_text : `text`
  - route_confidence : `numeric` DEFAULT `0`
  - status : `text` NOT NULL DEFAULT `'pending'::text`
  - meta : `jsonb` DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` DEFAULT `now()`
  - updated_at : `timestamptz` DEFAULT `now()`

### public.manual_blocks
- Estimated rows: `144`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - node_id : `uuid` 🔗 FK → public.manual_nodes.id NOT NULL
  - block_kind : `manual_block_kind` NOT NULL
  - sort_order : `int4` NOT NULL DEFAULT `0`
  - content : `text` NOT NULL
  - metadata : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_by : `uuid` DEFAULT `auth.uid()`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### public.manual_chunks
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - manual_id : `uuid` 🔗 FK → public.manuals.id NOT NULL
  - node_id : `uuid` 🔗 FK → public.manual_nodes.id NOT NULL
  - block_id : `uuid` 🔗 FK → public.manual_blocks.id
  - chunk_index : `int4` NOT NULL DEFAULT `0`
  - chunk_text : `text` NOT NULL
  - source_hash : `text`
  - metadata : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - embedding : `vector`
  - embedding_model : `text`
  - embedding_updated_at : `timestamptz`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### public.manual_edges
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - manual_id : `uuid` 🔗 FK → public.manuals.id NOT NULL
  - from_node_id : `uuid` 🔗 FK → public.manual_nodes.id NOT NULL
  - to_node_id : `uuid` 🔗 FK → public.manual_nodes.id NOT NULL
  - edge_type : `text` NOT NULL
  - note : `text`
  - weight : `numeric` NOT NULL DEFAULT `1.00`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### public.manual_nodes
- Estimated rows: `88`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - manual_id : `uuid` 🔗 FK → public.manuals.id NOT NULL
  - parent_id : `uuid` 🔗 FK → public.manual_nodes.id
  - node_kind : `manual_node_kind` NOT NULL
  - title : `text` NOT NULL
  - slug : `text` NOT NULL
  - sort_order : `int4` NOT NULL DEFAULT `0`
  - depth : `int4` NOT NULL DEFAULT `0`
  - summary : `text`
  - metadata : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### public.manuals
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - owner_id : `uuid` NOT NULL DEFAULT `auth.uid()`
  - slug : `text` NOT NULL
  - title : `text` NOT NULL
  - description : `text`
  - status : `text` NOT NULL DEFAULT `'draft'::text`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### public.nods_page
- Estimated rows: `-1`
- Fields
  - id : `int8` 🔑 PK NOT NULL DEFAULT `nextval('nods_page_id_seq'::regclass)`
  - parent_page_id : `int8` 🔗 FK → public.nods_page.id
  - path : `text` NOT NULL
  - checksum : `text`
  - meta : `jsonb`
  - type : `text`
  - source : `text`

### public.nods_page_section
- Estimated rows: `-1`
- Fields
  - id : `int8` 🔑 PK NOT NULL DEFAULT `nextval('nods_page_section_id_seq'::regclass)`
  - page_id : `int8` 🔗 FK → public.nods_page.id NOT NULL
  - content : `text`
  - token_count : `int4`
  - embedding : `vector`
  - slug : `text`
  - heading : `text`

### public.profiles
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - updated_at : `timestamptz`
  - username : `text`
  - full_name : `text`
  - avatar_url : `text`
  - website : `text`
  - display_name : `text` NOT NULL DEFAULT `'User'::text`
  - created_at : `timestamptz` DEFAULT `now()`
  - role : `text`

### public.quick_notes
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - owner_id : `uuid` NOT NULL
  - title : `text`
  - body_md : `text` NOT NULL DEFAULT `''::text`
  - capture_type : `text` NOT NULL DEFAULT `'general'::text`
  - target_area : `text`
  - tags : `_text` NOT NULL DEFAULT `'{}'::text[]`
  - source : `text` NOT NULL DEFAULT `'quick_capture'::text`
  - is_pinned : `bool` NOT NULL DEFAULT `false`
  - is_archived : `bool` NOT NULL DEFAULT `false`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### public.todos
- Estimated rows: `-1`
- Fields
  - id : `int8` 🔑 PK NOT NULL
  - user_id : `uuid` NOT NULL
  - task : `text`
  - is_complete : `bool` DEFAULT `false`
  - inserted_at : `timestamptz` NOT NULL DEFAULT `timezone('utc'::text, now())`

## Schema: qially

### qially.memory_embeddings
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - message_id : `uuid` 🔗 FK → qially.messages.id NOT NULL
  - embedding : `vector`
  - chunk_text : `text` NOT NULL
  - chunk_index : `int4` NOT NULL DEFAULT `0`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qially.messages
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - session_id : `uuid` 🔗 FK → qially.sessions.id NOT NULL
  - sender_type : `text` NOT NULL
  - sender_id : `uuid` 🔗 FK → qione.users.id
  - content : `text` NOT NULL
  - tokens_consumed : `int4` DEFAULT `0`
  - meta : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qially.sessions
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - title : `text`
  - session_type : `text` NOT NULL DEFAULT `'ai_chat'::text`
  - is_active : `bool` NOT NULL DEFAULT `true`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

## Schema: qiarchive

### qiarchive.archive_chunks
- Estimated rows: `-1`
- Fields
  - chunk_id : `int8` 🔑 PK NOT NULL DEFAULT `nextval('qiarchive.archive_chunks_chunk_id_seq'::regclass)`
  - archive_id : `text` 🔗 FK → qiarchive.archive_files.archive_id NOT NULL
  - chunk_index : `int4` NOT NULL
  - text : `text` NOT NULL
  - embedding : `vector`
  - embedding_model : `text`
  - metadata : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qiarchive.archive_files
- Estimated rows: `-1`
- Fields
  - archive_id : `text` 🔑 PK NOT NULL
  - domain_prefix : `text` 🔗 FK → qiarchive.prefix_registry.domain_prefix
  - short_code : `text` NOT NULL
  - original_filename : `text` NOT NULL
  - normalized_filename : `text` NOT NULL
  - sha256 : `text` NOT NULL
  - mime_type : `text`
  - file_ext : `text`
  - source_type : `text`
  - storage_path : `text`
  - file_size : `int8`
  - status : `text` NOT NULL DEFAULT `'registered'::text`
  - route_confidence : `float4` DEFAULT `0`
  - extracted_text : `text`
  - metadata : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### qiarchive.file_history
- Estimated rows: `-1`
- Fields
  - id : `int8` 🔑 PK NOT NULL DEFAULT `nextval('qiarchive.file_history_id_seq'::regclass)`
  - archive_id : `text` 🔗 FK → qiarchive.archive_files.archive_id NOT NULL
  - event_type : `text` NOT NULL
  - actor : `text` NOT NULL
  - old_values : `jsonb`
  - new_values : `jsonb`
  - metadata : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qiarchive.ingest_jobs
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - archive_id : `text` 🔗 FK → qiarchive.archive_files.archive_id
  - job_type : `text` NOT NULL
  - status : `text` NOT NULL DEFAULT `'pending'::text`
  - worker_id : `text`
  - error_message : `text`
  - started_at : `timestamptz`
  - completed_at : `timestamptz`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qiarchive.prefix_registry
- Estimated rows: `-1`
- Fields
  - domain_prefix : `text` 🔑 PK NOT NULL
  - entity_type : `text` NOT NULL
  - entity_id : `text` NOT NULL
  - display_name : `text` NOT NULL
  - is_active : `bool` NOT NULL DEFAULT `true`
  - notes : `text`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

## Schema: qicase

### qicase.case_documents
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - phase_id : `uuid` 🔗 FK → qicase.phases.id NOT NULL
  - archive_id : `text` 🔗 FK → qiarchive.archive_files.archive_id NOT NULL
  - doc_type : `text` NOT NULL
  - proof_type : `text` NOT NULL
  - lane : `text`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qicase.cases
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - qid : `text` 🔗 FK → qigraph.master_index.qid
  - case_name : `text` NOT NULL
  - case_number : `text`
  - court : `text`
  - judge : `text`
  - opposing_counsel : `text`
  - status : `text` DEFAULT `'Active'::text`
  - description : `text`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### qicase.deadlines
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - phase_id : `uuid` 🔗 FK → qicase.phases.id NOT NULL
  - chronicle_event_id : `uuid` 🔗 FK → qichronicle.events.id
  - trigger : `text` NOT NULL
  - clock_type : `text` NOT NULL
  - due_date : `timestamptz` NOT NULL
  - consequence : `text` NOT NULL
  - status : `text` NOT NULL
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qicase.document_issues
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - case_document_id : `uuid` 🔗 FK → qicase.case_documents.id NOT NULL
  - issue_id : `uuid` 🔗 FK → qicase.issues.id NOT NULL
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qicase.issues
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - phase_id : `uuid` 🔗 FK → qicase.phases.id NOT NULL
  - issue_title : `text` NOT NULL
  - issue_statement : `text` NOT NULL
  - elements_to_prove : `_text`
  - strength : `int4`
  - status : `text` NOT NULL
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qicase.phases
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - case_id : `uuid` 🔗 FK → qicase.cases.id NOT NULL
  - phase_name : `text` NOT NULL
  - status : `text` NOT NULL
  - purpose : `text` NOT NULL
  - phase_order : `int4` NOT NULL
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

## Schema: qichronicle

### qichronicle.calendar_feeds
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - name : `text` NOT NULL
  - secret_key : `uuid` NOT NULL DEFAULT `uuid_generate_v4()`
  - filters : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qichronicle.events
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - qid : `text` 🔗 FK → qigraph.master_index.qid
  - title : `text` NOT NULL
  - description : `text`
  - event_type : `text` NOT NULL DEFAULT `'event'::text`
  - status : `text` NOT NULL DEFAULT `'confirmed'::text`
  - start_at : `timestamptz` NOT NULL
  - end_at : `timestamptz`
  - is_all_day : `bool` NOT NULL DEFAULT `false`
  - location : `text`
  - owner_id : `uuid` 🔗 FK → qione.users.id
  - meta : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

## Schema: qicms

### qicms.posts
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - qid : `text` 🔗 FK → qigraph.master_index.qid
  - title : `text` NOT NULL
  - slug : `text` NOT NULL
  - status : `text` NOT NULL DEFAULT `'draft'::text`
  - content_md : `text` NOT NULL
  - excerpt : `text`
  - featured_image_archive_id : `text` 🔗 FK → qiarchive.archive_files.archive_id
  - author_id : `uuid` 🔗 FK → qione.users.id
  - published_at : `timestamptz`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

## Schema: qigraph

### qigraph.edges
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - from_qid : `text` 🔗 FK → qigraph.master_index.qid NOT NULL
  - to_qid : `text` 🔗 FK → qigraph.master_index.qid NOT NULL
  - link_type : `text` NOT NULL
  - meta : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qigraph.master_index
- Estimated rows: `-1`
- Fields
  - qid : `text` 🔑 PK NOT NULL
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - entity_type : `text` NOT NULL
  - object_id : `uuid` NOT NULL
  - table_reference : `text` NOT NULL
  - title : `text` NOT NULL
  - route_url : `text`
  - tags : `_text` DEFAULT `'{}'::text[]`
  - is_active : `bool` NOT NULL DEFAULT `true`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

## Schema: qihealth

### qihealth.care_events
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - owner_id : `uuid` NOT NULL DEFAULT `auth.uid()`
  - patient_id : `text`
  - household_id : `text`
  - type : `text`
  - category : `text`
  - label : `text`
  - details : `jsonb`
  - dose : `text`
  - route : `text`
  - note : `text`
  - input_method : `text`
  - created_by : `text`
  - created_at : `timestamptz` DEFAULT `now()`
  - synced : `bool` DEFAULT `true`

### qihealth.patients
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - owner_id : `uuid` NOT NULL DEFAULT `auth.uid()`
  - household_id : `text`
  - name : `text`
  - age : `int4`
  - photo_url : `text`
  - conditions : `jsonb` DEFAULT `'[]'::jsonb`
  - allergies : `jsonb` DEFAULT `'[]'::jsonb`
  - baseline_medications : `jsonb` DEFAULT `'[]'::jsonb`
  - prn_medications : `jsonb` DEFAULT `'[]'::jsonb`
  - emergency_contacts : `jsonb` DEFAULT `'[]'::jsonb`
  - doctor_contacts : `jsonb` DEFAULT `'[]'::jsonb`
  - notes : `text`
  - created_at : `timestamptz` DEFAULT `now()`
  - updated_at : `timestamptz` DEFAULT `now()`

## Schema: qihome

### qihome.categories
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - name : `text` NOT NULL
  - is_active : `bool` NOT NULL DEFAULT `true`

### qihome.chore_assignments
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - chore_id : `uuid` 🔗 FK → qihome.chores.id NOT NULL
  - user_id : `uuid` 🔗 FK → qione.users.id NOT NULL
  - due_date : `date` NOT NULL
  - status : `text` NOT NULL DEFAULT `'open'::text`
  - done_at : `timestamptz`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - related_user_id : `uuid` 🔗 FK → public.profiles.id

### qihome.chores
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - title : `text` NOT NULL
  - frequency : `text` NOT NULL DEFAULT `'weekly'::text`
  - points : `int4` NOT NULL DEFAULT `1`
  - is_active : `bool` NOT NULL DEFAULT `true`
  - description : `text`
  - wiki-link : `text`
  - category : `uuid` 🔗 FK → qihome.categories.id

### qihome.expense_shares
- Estimated rows: `-1`
- Fields
  - expense_id : `uuid` 🔑 PK 🔗 FK → qihome.expenses.id NOT NULL
  - user_id : `uuid` 🔑 PK 🔗 FK → qione.users.id NOT NULL
  - share_cents : `int4` NOT NULL

### qihome.expenses
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - date : `date` NOT NULL DEFAULT `CURRENT_DATE`
  - amount_cents : `int4` NOT NULL
  - category_id : `uuid` 🔗 FK → qihome.categories.id
  - paid_by_user_id : `uuid` 🔗 FK → qione.users.id NOT NULL
  - memo : `text`
  - archive_id : `text` 🔗 FK → qiarchive.archive_files.archive_id
  - created_by : `uuid` 🔗 FK → qione.users.id NOT NULL
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### qihome.ledger_entries
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - user_id : `uuid`
  - reference_id : `uuid`
  - entry_type : `text`
  - amount : `numeric` NOT NULL
  - description : `text`
  - tenant_id : `uuid` NOT NULL
  - created_at : `timestamptz` DEFAULT `now()`

### qihome.settlements
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - date : `date` NOT NULL DEFAULT `CURRENT_DATE`
  - from_user_id : `uuid` 🔗 FK → qione.users.id NOT NULL
  - to_user_id : `uuid` 🔗 FK → qione.users.id NOT NULL
  - amount_cents : `int4` NOT NULL
  - memo : `text`
  - created_by : `uuid` 🔗 FK → qione.users.id NOT NULL
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qihome.v_user_balances
- Estimated rows: `0`
- Fields
  - user_id : `uuid`
  - username : `text`
  - avatar_url : `text`
  - tenant_id : `uuid`
  - balance : `numeric`

## Schema: qiknowledge

### qiknowledge.notes
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - qid : `text` 🔗 FK → qigraph.master_index.qid NOT NULL
  - title : `text` NOT NULL
  - slug : `text` NOT NULL
  - content_md : `text`
  - content_html : `text`
  - sensitivity : `text` NOT NULL DEFAULT `'internal'::text`
  - author_id : `uuid` 🔗 FK → qione.users.id
  - meta : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

## Schema: qione

### qione.app_module_registry
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - slug : `text` NOT NULL
  - name : `text` NOT NULL
  - icon : `text`
  - description : `text`
  - default_enabled : `bool` DEFAULT `true`
  - order_int : `int4` NOT NULL DEFAULT `nextval('qione.app_module_registry_order_int_seq'::regclass)`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qione.member_roles
- Estimated rows: `-1`
- Fields
  - tenant_id : `uuid` 🔑 PK 🔗 FK → qione.tenants.id NOT NULL
  - user_id : `uuid` 🔑 PK 🔗 FK → qione.users.id NOT NULL
  - role_id : `uuid` 🔑 PK 🔗 FK → qione.roles.id NOT NULL

### qione.module_role_access
- Estimated rows: `-1`
- Fields
  - tenant_id : `uuid` 🔑 PK 🔗 FK → qione.tenants.id NOT NULL
  - module_key : `text` 🔑 PK 🔗 FK → qione.modules.key NOT NULL
  - role_id : `uuid` 🔑 PK 🔗 FK → qione.roles.id NOT NULL
  - access_level : `text` NOT NULL

### qione.modules
- Estimated rows: `-1`
- Fields
  - key : `text` 🔑 PK NOT NULL
  - name : `text` NOT NULL
  - description : `text`
  - icon : `text`
  - route : `text` NOT NULL
  - is_active : `bool` NOT NULL DEFAULT `true`

### qione.profiles
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL
  - role : `text` NOT NULL DEFAULT `'user'::text`
  - full_name : `text`
  - avatar_url : `text`
  - metadata : `jsonb` DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`
  - username : `text`
  - household_id : `uuid`

### qione.roles
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - name : `text` NOT NULL
  - rank : `int4` NOT NULL DEFAULT `100`

### qione.tenant_members
- Estimated rows: `2`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - user_id : `uuid` 🔗 FK → qione.users.id NOT NULL
  - status : `text` NOT NULL DEFAULT `'active'::text`
  - joined_at : `timestamptz` NOT NULL DEFAULT `now()`
  - display_name : `text`

### qione.tenant_modules
- Estimated rows: `-1`
- Fields
  - tenant_id : `uuid` 🔑 PK 🔗 FK → qione.tenants.id NOT NULL
  - module_key : `text` 🔑 PK 🔗 FK → qione.modules.key NOT NULL
  - is_enabled : `bool` NOT NULL DEFAULT `true`
  - settings : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`

### qione.tenants
- Estimated rows: `1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - name : `text` NOT NULL
  - slug : `text` NOT NULL
  - type : `text` NOT NULL
  - metadata : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_by : `uuid` 🔗 FK → qione.users.id
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### qione.user_module_settings
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - user_id : `uuid` 🔗 FK → qione.profiles.id NOT NULL
  - module_id : `uuid` 🔗 FK → qione.app_module_registry.id NOT NULL
  - is_enabled : `bool` DEFAULT `true`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qione.users
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - email : `text` NOT NULL
  - display_name : `text`
  - avatar_url : `text`
  - is_active : `bool` DEFAULT `true`
  - is_super_admin : `bool` DEFAULT `false`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

## Schema: qisys

### qisys.integration_tokens
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - provider : `text` NOT NULL
  - access_token : `text` NOT NULL
  - refresh_token : `text`
  - expires_at : `timestamptz`
  - meta : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - is_active : `bool` NOT NULL DEFAULT `true`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### qisys.jobs
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id
  - job_type : `text` NOT NULL
  - status : `text` NOT NULL DEFAULT `'pending'::text`
  - params : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - result : `jsonb`
  - worker_id : `text`
  - error_message : `text`
  - started_at : `timestamptz`
  - completed_at : `timestamptz`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qisys.system_events
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id
  - event_type : `text` NOT NULL
  - severity : `text` NOT NULL DEFAULT `'info'::text`
  - message : `text` NOT NULL
  - actor : `text`
  - meta : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qisys.worker_status
- Estimated rows: `-1`
- Fields
  - worker_id : `text` 🔑 PK NOT NULL
  - worker_name : `text` NOT NULL
  - worker_type : `text` NOT NULL
  - status : `text` NOT NULL DEFAULT `'idle'::text`
  - last_heartbeat : `timestamptz` NOT NULL DEFAULT `now()`
  - current_job_id : `uuid` 🔗 FK → qisys.jobs.id
  - meta : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`

## Schema: qitax

### qitax.return_files
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - return_id : `uuid` 🔗 FK → qitax.returns.id NOT NULL
  - archive_id : `text` 🔗 FK → qiarchive.archive_files.archive_id NOT NULL
  - role : `text` NOT NULL
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### qitax.returns
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - tax_year : `int4` NOT NULL
  - return_type : `text` NOT NULL
  - filing_kind : `text` NOT NULL
  - status : `text` NOT NULL DEFAULT `'intake'::text`
  - version : `int4` NOT NULL DEFAULT `1`
  - canonical_archive_id : `text` 🔗 FK → qiarchive.archive_files.archive_id
  - summary : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - notes : `text`
  - created_by : `uuid` 🔗 FK → qione.users.id
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

## Schema: qivault

### qivault.documents
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `uuid_generate_v4()`
  - tenant_id : `uuid` 🔗 FK → qione.tenants.id NOT NULL
  - qid : `text` 🔗 FK → qigraph.master_index.qid
  - archive_id : `text` 🔗 FK → qiarchive.archive_files.archive_id NOT NULL
  - doc_type : `text` NOT NULL
  - status : `text` NOT NULL DEFAULT `'draft'::text`
  - form_data : `jsonb` DEFAULT `'{}'::jsonb`
  - signed_at : `timestamptz`
  - expires_at : `timestamptz`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

## Schema: realtime

### realtime.messages
- Estimated rows: `-1`
- Fields
  - topic : `text` NOT NULL
  - extension : `text` NOT NULL
  - payload : `jsonb`
  - event : `text`
  - private : `bool` DEFAULT `false`
  - updated_at : `timestamp` NOT NULL DEFAULT `now()`
  - inserted_at : `timestamp` 🔑 PK NOT NULL DEFAULT `now()`
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`

### realtime.messages_2026_05_14
- Estimated rows: `-1`
- Fields
  - topic : `text` NOT NULL
  - extension : `text` NOT NULL
  - payload : `jsonb`
  - event : `text`
  - private : `bool` DEFAULT `false`
  - updated_at : `timestamp` NOT NULL DEFAULT `now()`
  - inserted_at : `timestamp` 🔑 PK NOT NULL DEFAULT `now()`
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`

### realtime.messages_2026_05_15
- Estimated rows: `-1`
- Fields
  - topic : `text` NOT NULL
  - extension : `text` NOT NULL
  - payload : `jsonb`
  - event : `text`
  - private : `bool` DEFAULT `false`
  - updated_at : `timestamp` NOT NULL DEFAULT `now()`
  - inserted_at : `timestamp` 🔑 PK NOT NULL DEFAULT `now()`
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`

### realtime.messages_2026_05_16
- Estimated rows: `-1`
- Fields
  - topic : `text` NOT NULL
  - extension : `text` NOT NULL
  - payload : `jsonb`
  - event : `text`
  - private : `bool` DEFAULT `false`
  - updated_at : `timestamp` NOT NULL DEFAULT `now()`
  - inserted_at : `timestamp` 🔑 PK NOT NULL DEFAULT `now()`
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`

### realtime.messages_2026_05_17
- Estimated rows: `-1`
- Fields
  - topic : `text` NOT NULL
  - extension : `text` NOT NULL
  - payload : `jsonb`
  - event : `text`
  - private : `bool` DEFAULT `false`
  - updated_at : `timestamp` NOT NULL DEFAULT `now()`
  - inserted_at : `timestamp` 🔑 PK NOT NULL DEFAULT `now()`
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`

### realtime.messages_2026_05_18
- Estimated rows: `-1`
- Fields
  - topic : `text` NOT NULL
  - extension : `text` NOT NULL
  - payload : `jsonb`
  - event : `text`
  - private : `bool` DEFAULT `false`
  - updated_at : `timestamp` NOT NULL DEFAULT `now()`
  - inserted_at : `timestamp` 🔑 PK NOT NULL DEFAULT `now()`
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`

### realtime.messages_2026_05_19
- Estimated rows: `-1`
- Fields
  - topic : `text` NOT NULL
  - extension : `text` NOT NULL
  - payload : `jsonb`
  - event : `text`
  - private : `bool` DEFAULT `false`
  - updated_at : `timestamp` NOT NULL DEFAULT `now()`
  - inserted_at : `timestamp` 🔑 PK NOT NULL DEFAULT `now()`
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`

### realtime.messages_2026_05_20
- Estimated rows: `-1`
- Fields
  - topic : `text` NOT NULL
  - extension : `text` NOT NULL
  - payload : `jsonb`
  - event : `text`
  - private : `bool` DEFAULT `false`
  - updated_at : `timestamp` NOT NULL DEFAULT `now()`
  - inserted_at : `timestamp` 🔑 PK NOT NULL DEFAULT `now()`
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`

### realtime.schema_migrations
- Estimated rows: `68`
- Fields
  - version : `int8` 🔑 PK NOT NULL
  - inserted_at : `timestamp`

### realtime.subscription
- Estimated rows: `-1`
- Fields
  - id : `int8` 🔑 PK NOT NULL
  - subscription_id : `uuid` NOT NULL
  - entity : `regclass` NOT NULL
  - filters : `_user_defined_filter` NOT NULL DEFAULT `'{}'::realtime.user_defined_filter[]`
  - claims : `jsonb` NOT NULL
  - claims_role : `regrole` NOT NULL
  - created_at : `timestamp` NOT NULL DEFAULT `timezone('utc'::text, now())`
  - action_filter : `text` DEFAULT `'*'::text`

## Schema: registry

### registry.namespace_allocations
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - namespace_code : `text` NOT NULL
  - namespace_class : `text` NOT NULL
  - owner_type : `text` NOT NULL
  - owner_id : `uuid` NOT NULL
  - band_start : `int4` NOT NULL
  - band_label : `text` NOT NULL
  - status : `text` NOT NULL DEFAULT `'active'::text`
  - display_name : `text`
  - notes : `text`
  - metadata : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### registry.namespace_bands
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - band_start : `int4` NOT NULL
  - band_end : `int4` NOT NULL
  - band_label : `text` NOT NULL
  - canonical_name : `text` NOT NULL
  - status : `text` NOT NULL DEFAULT `'active'::text`
  - allocation_mode : `text` NOT NULL DEFAULT `'manual'::text`
  - metadata : `jsonb` NOT NULL DEFAULT `'{}'::jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

## Schema: storage

### storage.buckets
- Estimated rows: `-1`
- Fields
  - id : `text` 🔑 PK NOT NULL
  - name : `text` NOT NULL
  - owner : `uuid`
  - created_at : `timestamptz` DEFAULT `now()`
  - updated_at : `timestamptz` DEFAULT `now()`
  - public : `bool` DEFAULT `false`
  - avif_autodetection : `bool` DEFAULT `false`
  - file_size_limit : `int8`
  - allowed_mime_types : `_text`
  - owner_id : `text`
  - type : `buckettype` NOT NULL DEFAULT `'STANDARD'::storage.buckettype`

### storage.buckets_analytics
- Estimated rows: `-1`
- Fields
  - name : `text` NOT NULL
  - type : `buckettype` NOT NULL DEFAULT `'ANALYTICS'::storage.buckettype`
  - format : `text` NOT NULL DEFAULT `'ICEBERG'::text`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - deleted_at : `timestamptz`

### storage.buckets_vectors
- Estimated rows: `-1`
- Fields
  - id : `text` NOT NULL
  - type : `buckettype` NOT NULL DEFAULT `'VECTOR'::storage.buckettype`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

### storage.migrations
- Estimated rows: `57`
- Fields
  - id : `int4` NOT NULL
  - name : `varchar` NOT NULL
  - hash : `varchar` NOT NULL
  - executed_at : `timestamp` DEFAULT `CURRENT_TIMESTAMP`

### storage.objects
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - bucket_id : `text`
  - name : `text`
  - owner : `uuid`
  - created_at : `timestamptz` DEFAULT `now()`
  - updated_at : `timestamptz` DEFAULT `now()`
  - last_accessed_at : `timestamptz` DEFAULT `now()`
  - metadata : `jsonb`
  - path_tokens : `_text`
  - version : `text`
  - owner_id : `text`
  - user_metadata : `jsonb`

### storage.s3_multipart_uploads
- Estimated rows: `-1`
- Fields
  - id : `text` 🔑 PK NOT NULL
  - in_progress_size : `int8` NOT NULL DEFAULT `0`
  - upload_signature : `text` NOT NULL
  - bucket_id : `text` NOT NULL
  - key : `text` NOT NULL
  - version : `text` NOT NULL
  - owner_id : `text`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - user_metadata : `jsonb`
  - metadata : `jsonb`

### storage.s3_multipart_uploads_parts
- Estimated rows: `-1`
- Fields
  - id : `uuid` 🔑 PK NOT NULL DEFAULT `gen_random_uuid()`
  - upload_id : `text` NOT NULL
  - size : `int8` NOT NULL DEFAULT `0`
  - part_number : `int4` NOT NULL
  - bucket_id : `text` NOT NULL
  - key : `text` NOT NULL
  - etag : `text` NOT NULL
  - owner_id : `text`
  - version : `text` NOT NULL
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`

### storage.vector_indexes
- Estimated rows: `-1`
- Fields
  - id : `text` NOT NULL DEFAULT `gen_random_uuid()`
  - name : `text` NOT NULL
  - bucket_id : `text` NOT NULL
  - data_type : `text` NOT NULL
  - dimension : `int4` NOT NULL
  - distance_metric : `text` NOT NULL
  - metadata_configuration : `jsonb`
  - created_at : `timestamptz` NOT NULL DEFAULT `now()`
  - updated_at : `timestamptz` NOT NULL DEFAULT `now()`

## Relationships
- care.attachments.care_plan_id → care.care_plans.id
- care.attachments.discharge_document_id → care.discharge_documents.id
- care.attachments.encounter_id → care.encounters.id
- care.attachments.patient_id → care.patients.id
- care.care_daily_notes.patient_id → care.patients.id
- care.care_events.patient_id → care.patients.id
- care.care_locations.parent_location_id → care.care_locations.id
- care.care_locations.patient_id → care.patients.id
- care.care_plan_items.care_plan_id → care.care_plans.id
- care.care_plan_items.patient_id → care.patients.id
- care.care_plans.patient_id → care.patients.id
- care.conditions.patient_id → care.patients.id
- care.device_profiles.patient_id → care.patients.id
- care.device_readings.device_profile_id → care.device_profiles.id
- care.device_readings.patient_id → care.patients.id
- care.discharge_actions.discharge_document_id → care.discharge_documents.id
- care.discharge_actions.patient_id → care.patients.id
- care.discharge_documents.encounter_id → care.encounters.id
- care.discharge_documents.patient_id → care.patients.id
- care.encounters.patient_id → care.patients.id
- care.kb_sections.patient_id → care.patients.id
- care.medication_events.discharge_document_id → care.discharge_documents.id
- care.medication_events.encounter_id → care.encounters.id
- care.medication_events.medication_id → care.medications.id
- care.medication_events.patient_id → care.patients.id
- care.medications.patient_id → care.patients.id
- care.milestones.care_plan_id → care.care_plans.id
- care.milestones.patient_id → care.patients.id
- care.observations.care_plan_id → care.care_plans.id
- care.observations.encounter_id → care.encounters.id
- care.observations.patient_id → care.patients.id
- care.oxygen_tanks.patient_id → care.patients.id
- care.oxygen_tanks.tank_type_id → care.oxygen_tank_types.id
- care.oxygen_usage_sessions.oxygen_tank_id → care.oxygen_tanks.id
- care.oxygen_usage_sessions.patient_id → care.patients.id
- care.regimen_events.patient_id → care.patients.id
- care.regimen_events.regimen_id → care.regimens.id
- care.regimens.linked_medication_id → care.medications.id
- care.regimens.patient_id → care.patients.id
- care.station_requirements.location_id → care.care_locations.id
- care.station_requirements.patient_id → care.patients.id
- care.station_requirements.supply_item_id → care.supply_items.id
- care.supply_events.patient_id → care.patients.id
- care.supply_events.supply_item_id → care.supply_items.id
- care.supply_inventory.patient_id → care.patients.id
- care.supply_inventory.supply_item_id → care.supply_items.id
- care.supply_items.patient_id → care.patients.id
- care.supply_order_items.order_id → care.supply_orders.id
- care.supply_order_items.supply_item_id → care.supply_items.id
- care.supply_orders.patient_id → care.patients.id
- care.vitals.encounter_id → care.encounters.id
- care.vitals.patient_id → care.patients.id
- public.chat_messages.room_id → public.chat_rooms.id
- public.chat_messages.sender_id → public.profiles.id
- public.chat_room_members.room_id → public.chat_rooms.id
- public.chat_room_members.user_id → public.profiles.id
- public.chat_rooms.created_by → public.profiles.id
- public.manual_blocks.node_id → public.manual_nodes.id
- public.manual_chunks.block_id → public.manual_blocks.id
- public.manual_chunks.manual_id → public.manuals.id
- public.manual_chunks.node_id → public.manual_nodes.id
- public.manual_edges.from_node_id → public.manual_nodes.id
- public.manual_edges.manual_id → public.manuals.id
- public.manual_edges.to_node_id → public.manual_nodes.id
- public.manual_nodes.manual_id → public.manuals.id
- public.manual_nodes.parent_id → public.manual_nodes.id
- public.nods_page.parent_page_id → public.nods_page.id
- public.nods_page_section.page_id → public.nods_page.id
- qially.memory_embeddings.message_id → qially.messages.id
- qially.messages.sender_id → qione.users.id
- qially.messages.session_id → qially.sessions.id
- qially.sessions.tenant_id → qione.tenants.id
- qiarchive.archive_chunks.archive_id → qiarchive.archive_files.archive_id
- qiarchive.archive_files.domain_prefix → qiarchive.prefix_registry.domain_prefix
- qiarchive.file_history.archive_id → qiarchive.archive_files.archive_id
- qiarchive.ingest_jobs.archive_id → qiarchive.archive_files.archive_id
- qicase.case_documents.archive_id → qiarchive.archive_files.archive_id
- qicase.case_documents.phase_id → qicase.phases.id
- qicase.cases.qid → qigraph.master_index.qid
- qicase.cases.tenant_id → qione.tenants.id
- qicase.deadlines.chronicle_event_id → qichronicle.events.id
- qicase.deadlines.phase_id → qicase.phases.id
- qicase.document_issues.case_document_id → qicase.case_documents.id
- qicase.document_issues.issue_id → qicase.issues.id
- qicase.issues.phase_id → qicase.phases.id
- qicase.phases.case_id → qicase.cases.id
- qichronicle.calendar_feeds.tenant_id → qione.tenants.id
- qichronicle.events.owner_id → qione.users.id
- qichronicle.events.qid → qigraph.master_index.qid
- qichronicle.events.tenant_id → qione.tenants.id
- qicms.posts.author_id → qione.users.id
- qicms.posts.featured_image_archive_id → qiarchive.archive_files.archive_id
- qicms.posts.qid → qigraph.master_index.qid
- qicms.posts.tenant_id → qione.tenants.id
- qigraph.edges.from_qid → qigraph.master_index.qid
- qigraph.edges.tenant_id → qione.tenants.id
- qigraph.edges.to_qid → qigraph.master_index.qid
- qigraph.master_index.tenant_id → qione.tenants.id
- qihome.categories.tenant_id → qione.tenants.id
- qihome.chore_assignments.chore_id → qihome.chores.id
- qihome.chore_assignments.related_user_id → public.profiles.id
- qihome.chore_assignments.tenant_id → qione.tenants.id
- qihome.chore_assignments.user_id → qione.users.id
- qihome.chores.category → qihome.categories.id
- qihome.chores.tenant_id → qione.tenants.id
- qihome.expense_shares.expense_id → qihome.expenses.id
- qihome.expense_shares.user_id → qione.users.id
- qihome.expenses.archive_id → qiarchive.archive_files.archive_id
- qihome.expenses.category_id → qihome.categories.id
- qihome.expenses.created_by → qione.users.id
- qihome.expenses.paid_by_user_id → qione.users.id
- qihome.expenses.tenant_id → qione.tenants.id
- qihome.settlements.created_by → qione.users.id
- qihome.settlements.from_user_id → qione.users.id
- qihome.settlements.tenant_id → qione.tenants.id
- qihome.settlements.to_user_id → qione.users.id
- qiknowledge.notes.author_id → qione.users.id
- qiknowledge.notes.qid → qigraph.master_index.qid
- qiknowledge.notes.tenant_id → qione.tenants.id
- qione.member_roles.role_id → qione.roles.id
- qione.member_roles.tenant_id → qione.tenants.id
- qione.member_roles.user_id → qione.users.id
- qione.module_role_access.module_key → qione.modules.key
- qione.module_role_access.role_id → qione.roles.id
- qione.module_role_access.tenant_id → qione.tenants.id
- qione.roles.tenant_id → qione.tenants.id
- qione.tenant_members.tenant_id → qione.tenants.id
- qione.tenant_members.user_id → qione.users.id
- qione.tenant_modules.module_key → qione.modules.key
- qione.tenant_modules.tenant_id → qione.tenants.id
- qione.tenants.created_by → qione.users.id
- qione.user_module_settings.module_id → qione.app_module_registry.id
- qione.user_module_settings.user_id → qione.profiles.id
- qisys.integration_tokens.tenant_id → qione.tenants.id
- qisys.jobs.tenant_id → qione.tenants.id
- qisys.system_events.tenant_id → qione.tenants.id
- qisys.worker_status.current_job_id → qisys.jobs.id
- qitax.return_files.archive_id → qiarchive.archive_files.archive_id
- qitax.return_files.return_id → qitax.returns.id
- qitax.returns.canonical_archive_id → qiarchive.archive_files.archive_id
- qitax.returns.created_by → qione.users.id
- qitax.returns.tenant_id → qione.tenants.id
- qivault.documents.archive_id → qiarchive.archive_files.archive_id
- qivault.documents.qid → qigraph.master_index.qid
- qivault.documents.tenant_id → qione.tenants.id