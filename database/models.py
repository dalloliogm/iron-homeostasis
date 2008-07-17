from django.db import models

# Create your models here.

class GeneOntologyTerm(models.Model):
	"""
	A Gene Ontology Term

	>>> 
	"""
	go_id = models.CharField(max_length=20, unique=True, verbose_name="gene ontology id", help_text="Enter a Gene Ontology Id")
	description = models.TextField(help_text="Enter a description for Gene Ontology Term")
	ontology = models.CharField(max_length = 2, choices = (("cc", "Cellular Component"), ("bp", "Biological Process"), ("mf", "Molecular Function")), null = True)

	def __unicode__(self):
		return "%s (%s)" % (self.go_id, self.description)

	class Admin: pass


class Organism(models.Model):
	"""
	An Organism
	"""
	binary_name = models.CharField(max_length = 30, unique = True)
	short_name = models.CharField(max_length = 20)
	
	def __unicode__(self):
		return "%s" % self.short_name

	class Admin: pass

class Pdb(models.Model):
	"""
	A pdb structure from the pdb.org database.

	Many-To-Many relationship to Protein, because a pdb file can contain multiple proteins and a protein can have multiple structures.
	"""
	pdb_id = models.CharField(max_length = 5)

	def __unicode__(self):
		return self.pdb_id

	class Admin: pass

class Entity(models.Model):
	"""
	Base class for Genes and Proteins. 
	Don't use it directly.
	"""
	test = ''
	organism = models.ForeignKey(Organism, blank = True)
	ensemblId = models.CharField(max_length = 15, unique=True)
	display_name = models.CharField(max_length = 30)
	sequence = models.TextField(max_length = 3000, blank = True, null = True)

	go_Cellular_component = models.ManyToManyField(GeneOntologyTerm, limit_choices_to = {'ontology' : 'cc'}, related_name = "%(class)s_cellular_component", null = True, blank = True)
	go_Biological_process = models.ManyToManyField(GeneOntologyTerm, limit_choices_to = {'ontology' : 'bp'}, related_name = "%(class)s_biological_process", null = True, blank = True)
	go_Molecular_function = models.ManyToManyField(GeneOntologyTerm, limit_choices_to = {'ontology' : 'mf'}, related_name = "%(class)s_molecular_function", null = True, blank = True)
	interactions = models.ManyToManyField("self", null = True, blank = True)

	homologues = models.ManyToManyField("self", null = True, blank = True)

	def __unicode__(self):
		return self.display_name + '_' + str(self.organism)

	class Meta:
		abstract = True
	
	class Admin:
		pass

class Gene(Entity):

	"""
	A Gene
	One-to-Many relationship to a Protein

	"""
	class Admin: 
		list_display = ('display_name', 'ensemblId')

class Protein(Entity):
	"""
	A Protein. 
	Many-to-One relationship to Gene.

	>>> dmt1 = Protein()

	"""
	uniprot_entry_name = models.CharField(max_length = 20, blank = True)
	protein_name = models.CharField(max_length = 50, blank = True)
	gene = models.ForeignKey(Gene)
	is_canonical_isoform = models.BooleanField(help_text = "if True, this protein is the favorite isoform of the gene")
	uniprot_id = models.CharField(max_length = 20)
	pdb_id = models.ManyToManyField(Pdb, null=True, blank=True)		# pdb is a ManyToMany relationship

	class Admin: 
		list_display = ('display_name', 'organism', 'ensemblId', 'uniprot_id', )
		list_filter = ('gene', 'organism')


	

