# Terraform Module
Content: https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/terraform

## Concepts and Overview
https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/terraform/1_terraform_overview.md
- Is an infrastructure as code tool that lets you define both cloud and on-prem resources in human-readable configuration files that you can version, reuse, and share. 
- With that it is possible to use a consistent workflow to provision and manage all of your infrastructure throughout its lifecycle.
- Basically infrastructure as code -> main take-home

### Advantages
- Makes it simple to track infrastructure
- Allows easier collaboration between peers
- Reproducibility

### What doesn't do
- Does not manage and update code on infrastructure
- Does not give you the ability to change immutable resources
	- Example is wanting to change the type of a virtual machine. It does not allow that, the only way to do it is to destroy the virtual machine and recreate it with the desired type.
	- The same would apply to moving the storage on GCP from one location to another. This would require copying the data out, destroying the older bucket and creating a new bucket on the desired location
- Manage resources not defined on the terraform files.


### Core
- Terraform is a software that can be installed on the local machine.
- It will be managing the resources being consumed on a given provider. 
	- With the code defined on terraform files, it will allow it to communicate with the provider resources, thus allowing to manage those being consumed by the user.
- Some providers are:
	- Cloud Services
		- GCP
		- Azure
		- AWS
		- Oracle Cloud Infrastructure
	- Kubernetes
	- VSphere (This is the one used in CGPP)
	- Active Directory (also used in CGPP)
	- For the full list of providers
		- https://registry.terraform.io/browse/providers

## Key Terraform Commands
- Init -> Get me the providers I need
	- Once the provider is defined on the interface and the command is executed, terraform will pull the code from its repository that allows it to communicate with the providers resources
		- These codes were developed by the own company or by the community.
- plan -> Makes terraform indicate what it's about to do
	- It's going to show the resources that will be created
- apply -> Indicates to terraform execute what it's defined on the .tf files
	- Build the infrastructure and do what I defined on the code.
- destroy -> removes everything defined on .tf files.

## Basics
- First thing first was to choose the provider to which terraform will be managing resources. For this course it was selected the Google Cloud Platform (GCP).
The initial content of this video concerns the GCP configuration :https://www.youtube.com/watch?v=Y2ux7gq3Z0o&t=540s
- By following the above video a service account was created on GCP, whose purpose is for the latter identify that you is you, and you have permission to create and manage resources.
    - The credentials were saved on a specific folder.

### Terraform Installation
- Since the GitHub codespaces is a Ubuntu VM, terraform was installed by running the commands indicated for Ubuntu/Debian.

### Creating main.tf file
- Since we are going to use GCP, it's important to obtain the Google provider config from Terraform docs: https://registry.terraform.io/providers/hashicorp/google/latest
- Once the main.tf file was defined with basic GCP provider config, to fix the file internal format, terraform has the following command:
`terraform fmt`
This will adjust all lines to be in the correct indentation, for every .tf file within the folder where it was executed.

### Avoiding defining credentials on main.tf file
- Another approach is to use gcloud but it would be using the user account, thus the account with all the permisions.
- Another way is to define the path to the credentials JSON file to the GOOGLE CLOUD environment variables, it can be done through the following command:
```
export GOOGLE_CREDENTIALS='path/to/creds'
``` 
To test whether the modification was succesfull, simply echo the env variable (e.g. $GOOGLE_CREDENTIALS)

### Initializing terraform connection
- Executing terraform init, and with the main.tf file ready and creds to GCP, terraform will stablish connection with it.

## Creating a Storage Bucket on GCP with terraform
- First thing is to get the terraform settings to build the google storage, which can be found here: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
- To better undestand the configuration files variables, reading the docs is the best way to get the meaning of each field.