sudo docker run \
    -p 7474:7474 -p 7687:7687 \
    --user="$(id -u):$(id -g)" \
    --env NEO4J_AUTH=none\
    -v $PWD/import:/import -v $PWD/data:/data -v $PWD/plugins:/plugins \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.* \
    -e NEO4J_dbms_security_procedures_whitelist=apoc.*,gds.* \
    -e NEO4JLABS_PLUGINS='["apoc"]' \
    neo4j:4.4.16