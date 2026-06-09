output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.api.id
}

output "public_ip" {
  description = "Auto-assigned public IP — point the `skill-tree` SSH host at this (no EIP: account quota is full; the IP changes if the box is stopped/started)"
  value       = aws_instance.api.public_ip
}

output "private_ip" {
  description = "Private IP within the VPC"
  value       = aws_instance.api.private_ip
}

output "ec2_security_group_id" {
  description = "Security group ID attached to the instance"
  value       = aws_security_group.ec2.id
}

output "ami_id" {
  description = "Latest AL2023 arm64 AMI the data source resolved (the running instance pins its own booted AMI via ignore_changes=[ami])"
  value       = data.aws_ami.amazon_linux_arm.id
}

output "ssh_command" {
  description = "Convenience SSH command"
  value       = "ssh -i ~/.ssh/${var.key_pair_name}.pem ec2-user@${aws_instance.api.public_ip}"
}
