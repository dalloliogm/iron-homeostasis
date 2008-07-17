
clean:
	mysql -u root -e 'use iron_omeostasis; drop table if exists database_entity, database_gene, database_protein, database_geneontologyterm;' -p
