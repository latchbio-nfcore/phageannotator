
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'assembly_min_length': NextflowParameter(
        type=typing.Optional[int],
        default=1000,
        section_title='Assembly filtering options',
        description='Minimum assembly length',
    ),
    'run_viromeqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Virus enrichment options',
        description='Run ViromeQC to estimate viral enrichment',
    ),
    'run_reference_containment': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Reference virus containment options',
        description='Run MASH screen to identify external viruses contained in reads',
    ),
    'reference_virus_fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to FASTA file containing reference virus sequences',
    ),
    'reference_virus_sketch': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to mash sketch file for reference virus sequences',
    ),
    'save_reference_virus_sketch': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save reference virus sketch, if it was created.',
    ),
    'mash_screen_min_score': NextflowParameter(
        type=typing.Optional[float],
        default=0.95,
        section_title=None,
        description='Minimum mash screen score to consider a genome contained',
    ),
    'mash_screen_winner_take_all': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Hashes present in multiple references are assigned only to top sequence',
    ),
    'skip_genomad': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Virus classification options',
        description='Skip running geNomad to classify viral/non-viral sequences',
    ),
    'genomad_db': NextflowParameter(
        type=typing.Optional[LatchDir],
        default=None,
        section_title=None,
        description="Path to directory containing geNomad's database",
    ),
    'save_genomad_db': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description="Save geNomad's database, if it was downloaded.",
    ),
    'genomad_min_score': NextflowParameter(
        type=typing.Optional[float],
        default=0.7,
        section_title=None,
        description='Minimum virus score for a sequence to be considered viral',
    ),
    'genomad_max_fdr': NextflowParameter(
        type=typing.Optional[float],
        default=0.1,
        section_title=None,
        description='Maximum FDR for a sequence to be considered viral (will include --enable-score-calibration)',
    ),
    'genomad_splits': NextflowParameter(
        type=typing.Optional[int],
        default=5,
        section_title=None,
        description='Number of splits for running geNomad (more splits lowers memory requirements)',
    ),
    'run_cobra': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Viral contig extension',
        description='Run COBRA to extend viral contigs',
    ),
    'cobra_assembler': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='The assembler that was used to assemble viral contigs',
    ),
    'cobra_mink': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Minimum kmer value used during assembly',
    ),
    'cobra_maxk': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Maximum kmer value used during assembly',
    ),
    'skip_checkv': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Virus quality options',
        description='Skip running CheckV to assess virus quality and filter sequences',
    ),
    'checkv_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to directory containing CheckV database',
    ),
    'save_checkv_db': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description="Save CheckV's database, if it was downloaded",
    ),
    'checkv_min_length': NextflowParameter(
        type=typing.Optional[int],
        default=3000,
        section_title=None,
        description='Minimum virus length to pass filtering',
    ),
    'checkv_min_completeness': NextflowParameter(
        type=typing.Optional[int],
        default=50,
        section_title=None,
        description='Minimum CheckV completeness to pass filtering',
    ),
    'checkv_remove_proviruses': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Remove viruses labeled as provirus by geNomad or CheckV',
    ),
    'checkv_remove_warnings': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Remove viruses with CheckV warnings',
    ),
    'skip_virus_clustering': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Genome clustering options',
        description='Skip ANI-based virus clustering',
    ),
    'blast_min_percent_identity': NextflowParameter(
        type=typing.Optional[int],
        default=90,
        section_title=None,
        description='Minimum precent identity for BLAST hits',
    ),
    'blast_max_num_seqs': NextflowParameter(
        type=typing.Optional[int],
        default=25000,
        section_title=None,
        description='Maximum number of BLAST hits to record for each sequence',
    ),
    'anicluster_min_ani': NextflowParameter(
        type=typing.Optional[int],
        default=95,
        section_title=None,
        description='Minimum average nucleotide identity (ANI) for sequences to be clustered together',
    ),
    'anicluster_min_qcov': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description='Minimum query coverage for sequences to be clustered together',
    ),
    'anicluster_min_tcov': NextflowParameter(
        type=typing.Optional[int],
        default=85,
        section_title=None,
        description='Minimum test coverage for sequences to be clustered together',
    ),
    'skip_read_alignment': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Virus abundance options',
        description='Skip read alignment to viral sequences',
    ),
    'coverm_min_read_alignment': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description='Minimum length of reads aligned to references',
    ),
    'coverm_min_percent_identity': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description='Minimum percent identity of aligned reads',
    ),
    'coverm_min_percent_read_aligned': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description='Minimum percent of read aligned to references',
    ),
    'coverm_metrics': NextflowParameter(
        type=typing.Optional[str],
        default='mean',
        section_title=None,
        description='Abundance calculation metrics',
    ),
    'run_genomad_taxonomy': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Virus taxonomy options',
        description=None,
    ),
    'run_iphop': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Phage host options',
        description='Run iPHoP to predict phage hosts',
    ),
    'iphop_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to locally iPHoP database',
    ),
    'save_iphop_db': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save downloaded iPHoP database',
    ),
    'iphop_min_score': NextflowParameter(
        type=typing.Optional[int],
        default=90,
        section_title=None,
        description='Minimum confidence score to provide host prediction',
    ),
    'run_bacphlip': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Virus lifestyle options',
        description='Run BACPHLIP to predict virus lifestyle',
    ),
    'run_pharokka': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Virus function options',
        description='Run pharokka to predict and annotate phage ORFs',
    ),
    'pharokka_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to predownloaded pharokka db',
    ),
    'skip_instrain': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Virus microdiversity options',
        description='Bypass microdiversity analysis with inStrain',
    ),
    'instrain_min_ani': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='Minimum identity for read alignment to be considered',
    ),
    'instrain_min_mapq': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Minimum MAPQ for a read to be considered',
    ),
    'instrain_min_variant_cov': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Minimum coverage for a variant to be considered',
    ),
    'instrain_min_snp_freq': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='Minimum allele frequency for an SNP to be considered',
    ),
    'instrain_max_snp_fdr': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Maximum FDR for a SNP to be considered',
    ),
    'instrain_min_genome_cov': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='Minimum number of reads mapping to a genome to consider profiling',
    ),
    'instrain_popani_thresh': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='Minimum identity for genomes to be considered in the same strain',
    ),
    'instrain_min_genome_comp': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='Minimum percent of genomes compared for comparison to be considered',
    ),
    'instrain_min_genome_breadth': NextflowParameter(
        type=typing.Optional[float],
        default=None,
        section_title=None,
        description='Minimum breadth of coverage for a genome to be considered present',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
    'logo': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Use logo in initialise subworkflow',
    ),
}

