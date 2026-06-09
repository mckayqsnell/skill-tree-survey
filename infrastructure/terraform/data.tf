# Latest Amazon Linux 2023 ARM64 AMI (for the Graviton t4g instance).
#
# Resolves the newest AL2023 arm64 AMI for the instance. `ignore_changes = [ami]`
# in ec2.tf pins whatever actually booted, so a newer AMI landing here later
# never triggers a replacement of the running box.
data "aws_ami" "amazon_linux_arm" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-kernel-*-arm64"]
  }

  filter {
    name   = "architecture"
    values = ["arm64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

# Current account / region — handy for outputs and sanity checks.
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
