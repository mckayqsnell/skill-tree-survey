# Remote state in the shared Heal state bucket, under this project's own key.
#
# The bucket (`heal-terraform-state`) and its native S3 locking are CREATED AND
# OWNED by heal-api's Terraform — we only consume them here with a distinct key,
# so the two projects never touch each other's state. There is a single prod
# environment, so the default workspace is used (no workspaces needed).
#
#   State path: s3://heal-terraform-state/skill-tree-survey/terraform.tfstate
#
terraform {
  backend "s3" {
    bucket       = "heal-terraform-state"
    key          = "skill-tree-survey/terraform.tfstate"
    region       = "us-east-2"
    encrypt      = true
    use_lockfile = true # S3 native locking (replaces the deprecated dynamodb_table)
  }
}
