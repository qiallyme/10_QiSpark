# Device Model

Rather than architecting everything around a singular developer or operator machine, the system uses a scalable, fleet-managed node structure with cloud orchestration.

## Fleet Model Components

* **QiLabs**: The canonical local workstation root (`C:/QiLabs/`) on physical devices.
* **Device Node**: An enrolled machine in the fleet.
* **Local Agent**: The installed thin control service, reporting health and executing assigned jobs locally.
* **Local Runtime**: The machine-local execution layer for OCR, extraction, file chunking, and vectors.
* **Watch Assignment**: A configuration assigned from the hosted admin instructing a particular node to monitor specific directories or pipelines.
* **Drop Zone**: Specified ingress pathways (e.g. specialized folders) defined and assigned by the hosted admin.
* **Primary Dev Node**: A device node designated specifically for primary operator deployment, configuration, and structural adjustments.
* **Ingest Edge Node**: A specialized device node strictly responsible for watching paths/drop zones, reading local files, and ingesting them into the archive pipeline without administrative overhead.
* **Infrastructure Node**: A user-controlled server (e.g., `infra.backup_server`) providing local AI runtimes, secondary data services, and public application hosting under governed control.
* **Fleet Control Plane**: The hosted Admin platform authorizing and orchestrating action across the fleet of device nodes.
* **Trust/Auth Boundary**: Access control and credentials managed securely separating local worker execution from cross-tenant operations.
