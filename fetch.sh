echo "This prints the current credential value from secret manager"
secret=$(aws secretsmanager get-secret-value --secret-id /poc/MySQL/secretmanager| jq .SecretString | jq fromjson)
user=$(echo $secret | jq -r .username)
password=$(echo $secret | jq -r .password)
endpoint=$(echo $secret | jq -r .host)
port=$(echo $secret | jq -r .port)
echo $password
