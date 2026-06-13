# Endang Suwarna — CV

---

## Experience

### Pintu — Infrastructure / Platform Engineer

- **Managed multi-cloud infrastructure** — AWS for production services and Google Cloud for data team (BigQuery, data pipelines, research/playground environments). Ensured cost efficiency by right-sizing resources across both clouds.
- **Reduced AWS infrastructure costs** by identifying and removing orphaned/stale resources left from trial-and-error experiments — prior practice had no dedicated DevOps role, resulting in accumulated unused EC2 instances, load balancers, EBS volumes, and other billable assets. Performed full cleanup and established tagging/lifecycle policies to prevent regrowth.
- **Introduced containerization (Docker) to the engineering team** — migrated backend and frontend services from manual EC2 deployments to containerized workflows with Docker Compose, enabling consistent environments across dev/staging/production and reproducible builds.
- **Built monitoring and observability stack** with Grafana and Prometheus to replace default CloudWatch metrics — set up custom dashboards for application-level metrics, infrastructure health, and alerting across services, significantly improving incident response time and visibility into production systems.
- **Deployed Teleport** as a unified secure access gateway for SSH into servers and internal web applications, replacing ad-hoc VPN setups and providing audit logs for all access events.
- **Automated server management with Ansible** — wrote playbooks for configuration management, software provisioning, and repetitive maintenance tasks across the fleet, reducing manual toil and configuration drift.
- **Set up Consul** for service discovery and as a distributed key-value store for backend application configuration, enabling services to locate each other dynamically without hardcoded addresses.
- **Researched and rolled out container orchestration** — started with Nomad to onboard developers into container-based deployment with minimal cognitive overhead (simpler abstraction, single binary), then led the migration to Kubernetes once the team was comfortable with container concepts and needed more advanced scheduling, scaling, and ecosystem support.
- **Authored DevOps documentation and incident runbooks** — created standardized templates for infrastructure setup, deployment procedures, and incident response playbooks so recurring incidents could be resolved faster with consistent steps, reducing mean-time-to-resolution (MTTR) significantly.

---

*To be continued — more experience entries pending.*
