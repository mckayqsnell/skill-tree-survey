# Security group for the skill-tree-survey EC2 instance.
#
# The app is served entirely through a Cloudflare Tunnel, which the `cloudflared`
# container establishes as an OUTBOUND connection to Cloudflare's edge. Nothing
# ever connects inbound to the box on 80/443 — so the only inbound port we open
# is SSH (for `task prod:deploy` and admin). Everything outbound is allowed
# (GHCR image pulls, dnf updates, the Cloudflare Tunnel, Sentry, etc.).
resource "aws_security_group" "ec2" {
  name = "${var.project_name}-ec2-${var.environment}"
  # AWS SG descriptions must be ASCII-only.
  description = "skill-tree-survey EC2 - SSH in, all out (app traffic via Cloudflare Tunnel, outbound-only)"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.ssh_allowed_cidrs
    content {
      description = "SSH from allowed CIDRs"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = [ingress.value]
    }
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-ec2-${var.environment}"
    Environment = var.environment
  }

  # Renaming a security group forces a replacement; keep it stable across applies.
  lifecycle {
    create_before_destroy = true
  }
}
