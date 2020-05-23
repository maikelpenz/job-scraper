Deploy terraform infrastructure
	- Update "cicd_infrastructure\terraform-backend.tfvars"
	- Update "cicd_infrastructure\terraform-deployment.tfvars"
	
	terraform init
		terraform init -backend-config="terraform-backend.tfvars"
	terraform apply
		terraform apply -var-file="terraform-deployment.tfvars"
			Inform the token
	terraform destroy
		terraform destroy -var-file="terraform-deployment.tfvars"
		