# NLU Service Initialization
echo "Name of the service: python-fastapi-template"

copilot init -a "python-fastapi-template" -t "Load Balanced Web Service" -n "python-fastapi-template-$1-svc" -d ./Dockerfile

copilot env init -n $1 --profile default

copilot env deploy --name $1

# Deploying environment with addons
mkdir copilot/environments/addons

cp mysql_rds_template.yml copilot/environments/addons/mysql_rds_template.yml

copilot env deploy --name $1

SERVICE_MANIFEST_FILE_PATH=copilot/python-fastapi-template-$1-svc/manifest.yml

yq -i '.secrets.PYTHON_FASTAPI_TEMPLATE_CLUSTER_SECRET.from_cfn = "pythonFastApiTemplateclusterSecret"' $SERVICE_MANIFEST_FILE_PATH

copilot deploy --name "python-fastapi-template-$1-svc" -e $1
