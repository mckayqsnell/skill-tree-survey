variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-2"
}

variable "environment" {
  description = "Deployment environment (only prod exists today)"
  type        = string
  default     = "prod"

  validation {
    condition     = contains(["prod", "test"], var.environment)
    error_message = "Environment must be 'prod' or 'test'."
  }
}

variable "project_name" {
  description = "Project name, used for resource naming and tags"
  type        = string
  default     = "skill-tree-survey"
}

# -----------------------------------------------------------------------------
# EC2 configuration
# -----------------------------------------------------------------------------

variable "instance_type" {
  description = "EC2 instance type (Graviton/arm64)"
  type        = string
  default     = "t4g.medium"
}

variable "root_volume_size" {
  description = "Root EBS volume size in GB"
  type        = number
  default     = 30
}

variable "key_pair_name" {
  description = "Name of the existing EC2 key pair for SSH access"
  type        = string
  default     = "skill-tree-keypair"
}

# -----------------------------------------------------------------------------
# Networking — the box lives in the account's default VPC. Set explicitly (not
# looked up) so the AZ/subnet are deterministic across applies.
# -----------------------------------------------------------------------------

variable "vpc_id" {
  description = "VPC ID the instance and security group live in (the default VPC)"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID for the instance (determines the AZ)"
  type        = string
}

# -----------------------------------------------------------------------------
# Access control
# -----------------------------------------------------------------------------

variable "ssh_allowed_cidrs" {
  description = "CIDR blocks allowed to SSH in. The app itself is served via Cloudflare Tunnel (outbound-only), so 22 is the ONLY inbound port. No default on purpose — set SSH_ALLOWED_CIDRS in the SKILL-TREE-INFRA vault (task tf:gen) and restrict it where you can."
  type        = list(string)

  validation {
    condition     = length(var.ssh_allowed_cidrs) > 0
    error_message = "ssh_allowed_cidrs must list at least one CIDR (e.g. [\"1.2.3.4/32\"])."
  }
}
