# =============================================================================
# EC2 instance for skill-tree-survey (backend + cloudflared + watchtower).
#
# We PROVISION A FRESH instance and cut over to it. The old hand-built box
# (1Password → SKILL-TREE-INFRA → OLD_INSTANCE_ID) is NOT in Terraform state
# and is terminated manually after cutover. See README.md → "Provision the production instance".
#
# prevent_destroy is intentionally FALSE for the initial stand-up so the first
# apply can create cleanly and be re-run freely.
#   ⚠️ TODO: after the first successful deploy + verify, set prevent_destroy = true
#      (and re-apply) so prod can't be destroyed by accident.
#
# ignore_changes = [ami] only: the AMI data source is most_recent=true, so
# pinning it here stops a newly-released AL2023 AMI from forcing a replacement on
# every apply. user_data and the root volume ARE managed (this is a fresh box).
# =============================================================================

# Elastic IP — gives the box a stable public address that survives stop/start.
# (Serving doesn't depend on it; the Cloudflare Tunnel is outbound. It only
#  matters for SSH — point your `skill-tree` SSH host at this IP after apply.)
resource "aws_eip" "api" {
  domain = "vpc"

  tags = {
    Name        = "${var.project_name}-eip-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_instance" "api" {
  ami                         = data.aws_ami.amazon_linux_arm.id
  instance_type               = var.instance_type
  key_name                    = var.key_pair_name
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.ec2.id]
  associate_public_ip_address = true

  # Enforce IMDSv2 (mitigates SSRF against the metadata service). In-place change.
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  # First-boot bootstrap: installs Docker + Compose and preps the app dir.
  # Managed (this is a fresh box) — changing it later forces a replacement.
  user_data = templatefile("${path.module}/scripts/user_data.sh", {
    project_name = var.project_name
    environment  = var.environment
  })

  root_block_device {
    volume_size           = var.root_volume_size
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}"
    Environment = var.environment
  }

  lifecycle {
    # ⚠️ TODO: flip to true after the first successful deploy + verify (see README).
    prevent_destroy = false
    ignore_changes  = [ami]
  }
}

# Bind the Elastic IP to the instance.
resource "aws_eip_association" "api" {
  instance_id   = aws_instance.api.id
  allocation_id = aws_eip.api.id
}
