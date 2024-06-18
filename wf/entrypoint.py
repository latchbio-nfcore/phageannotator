from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], run_viromeqc: typing.Optional[bool], run_reference_containment: typing.Optional[bool], reference_virus_fasta: typing.Optional[LatchFile], reference_virus_sketch: typing.Optional[LatchFile], save_reference_virus_sketch: typing.Optional[bool], mash_screen_winner_take_all: typing.Optional[bool], skip_genomad: typing.Optional[bool], genomad_db: typing.Optional[LatchDir], save_genomad_db: typing.Optional[bool], run_cobra: typing.Optional[bool], cobra_assembler: typing.Optional[str], cobra_mink: typing.Optional[str], cobra_maxk: typing.Optional[str], skip_checkv: typing.Optional[bool], checkv_db: typing.Optional[str], save_checkv_db: typing.Optional[bool], checkv_remove_proviruses: typing.Optional[bool], checkv_remove_warnings: typing.Optional[bool], skip_virus_clustering: typing.Optional[bool], skip_read_alignment: typing.Optional[bool], run_genomad_taxonomy: typing.Optional[bool], run_iphop: typing.Optional[bool], iphop_db: typing.Optional[str], save_iphop_db: typing.Optional[bool], run_bacphlip: typing.Optional[bool], run_pharokka: typing.Optional[bool], pharokka_db: typing.Optional[str], skip_instrain: typing.Optional[bool], instrain_min_ani: typing.Optional[float], instrain_min_mapq: typing.Optional[int], instrain_min_variant_cov: typing.Optional[int], instrain_min_snp_freq: typing.Optional[float], instrain_max_snp_fdr: typing.Optional[int], instrain_min_genome_cov: typing.Optional[float], instrain_popani_thresh: typing.Optional[float], instrain_min_genome_comp: typing.Optional[float], instrain_min_genome_breadth: typing.Optional[float], multiqc_methods_description: typing.Optional[str], assembly_min_length: typing.Optional[int], mash_screen_min_score: typing.Optional[float], genomad_min_score: typing.Optional[float], genomad_max_fdr: typing.Optional[float], genomad_splits: typing.Optional[int], checkv_min_length: typing.Optional[int], checkv_min_completeness: typing.Optional[int], blast_min_percent_identity: typing.Optional[int], blast_max_num_seqs: typing.Optional[int], anicluster_min_ani: typing.Optional[int], anicluster_min_qcov: typing.Optional[int], anicluster_min_tcov: typing.Optional[int], coverm_min_read_alignment: typing.Optional[int], coverm_min_percent_identity: typing.Optional[int], coverm_min_percent_read_aligned: typing.Optional[int], coverm_metrics: typing.Optional[str], iphop_min_score: typing.Optional[int], logo: typing.Optional[bool]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('assembly_min_length', assembly_min_length),
                *get_flag('run_viromeqc', run_viromeqc),
                *get_flag('run_reference_containment', run_reference_containment),
                *get_flag('reference_virus_fasta', reference_virus_fasta),
                *get_flag('reference_virus_sketch', reference_virus_sketch),
                *get_flag('save_reference_virus_sketch', save_reference_virus_sketch),
                *get_flag('mash_screen_min_score', mash_screen_min_score),
                *get_flag('mash_screen_winner_take_all', mash_screen_winner_take_all),
                *get_flag('skip_genomad', skip_genomad),
                *get_flag('genomad_db', genomad_db),
                *get_flag('save_genomad_db', save_genomad_db),
                *get_flag('genomad_min_score', genomad_min_score),
                *get_flag('genomad_max_fdr', genomad_max_fdr),
                *get_flag('genomad_splits', genomad_splits),
                *get_flag('run_cobra', run_cobra),
                *get_flag('cobra_assembler', cobra_assembler),
                *get_flag('cobra_mink', cobra_mink),
                *get_flag('cobra_maxk', cobra_maxk),
                *get_flag('skip_checkv', skip_checkv),
                *get_flag('checkv_db', checkv_db),
                *get_flag('save_checkv_db', save_checkv_db),
                *get_flag('checkv_min_length', checkv_min_length),
                *get_flag('checkv_min_completeness', checkv_min_completeness),
                *get_flag('checkv_remove_proviruses', checkv_remove_proviruses),
                *get_flag('checkv_remove_warnings', checkv_remove_warnings),
                *get_flag('skip_virus_clustering', skip_virus_clustering),
                *get_flag('blast_min_percent_identity', blast_min_percent_identity),
                *get_flag('blast_max_num_seqs', blast_max_num_seqs),
                *get_flag('anicluster_min_ani', anicluster_min_ani),
                *get_flag('anicluster_min_qcov', anicluster_min_qcov),
                *get_flag('anicluster_min_tcov', anicluster_min_tcov),
                *get_flag('skip_read_alignment', skip_read_alignment),
                *get_flag('coverm_min_read_alignment', coverm_min_read_alignment),
                *get_flag('coverm_min_percent_identity', coverm_min_percent_identity),
                *get_flag('coverm_min_percent_read_aligned', coverm_min_percent_read_aligned),
                *get_flag('coverm_metrics', coverm_metrics),
                *get_flag('run_genomad_taxonomy', run_genomad_taxonomy),
                *get_flag('run_iphop', run_iphop),
                *get_flag('iphop_db', iphop_db),
                *get_flag('save_iphop_db', save_iphop_db),
                *get_flag('iphop_min_score', iphop_min_score),
                *get_flag('run_bacphlip', run_bacphlip),
                *get_flag('run_pharokka', run_pharokka),
                *get_flag('pharokka_db', pharokka_db),
                *get_flag('skip_instrain', skip_instrain),
                *get_flag('instrain_min_ani', instrain_min_ani),
                *get_flag('instrain_min_mapq', instrain_min_mapq),
                *get_flag('instrain_min_variant_cov', instrain_min_variant_cov),
                *get_flag('instrain_min_snp_freq', instrain_min_snp_freq),
                *get_flag('instrain_max_snp_fdr', instrain_max_snp_fdr),
                *get_flag('instrain_min_genome_cov', instrain_min_genome_cov),
                *get_flag('instrain_popani_thresh', instrain_popani_thresh),
                *get_flag('instrain_min_genome_comp', instrain_min_genome_comp),
                *get_flag('instrain_min_genome_breadth', instrain_min_genome_breadth),
                *get_flag('multiqc_methods_description', multiqc_methods_description),
                *get_flag('logo', logo)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_phageannotator", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_phageannotator(input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], run_viromeqc: typing.Optional[bool], run_reference_containment: typing.Optional[bool], reference_virus_fasta: typing.Optional[LatchFile], reference_virus_sketch: typing.Optional[LatchFile], save_reference_virus_sketch: typing.Optional[bool], mash_screen_winner_take_all: typing.Optional[bool], skip_genomad: typing.Optional[bool], genomad_db: typing.Optional[LatchDir], save_genomad_db: typing.Optional[bool], run_cobra: typing.Optional[bool], cobra_assembler: typing.Optional[str], cobra_mink: typing.Optional[str], cobra_maxk: typing.Optional[str], skip_checkv: typing.Optional[bool], checkv_db: typing.Optional[str], save_checkv_db: typing.Optional[bool], checkv_remove_proviruses: typing.Optional[bool], checkv_remove_warnings: typing.Optional[bool], skip_virus_clustering: typing.Optional[bool], skip_read_alignment: typing.Optional[bool], run_genomad_taxonomy: typing.Optional[bool], run_iphop: typing.Optional[bool], iphop_db: typing.Optional[str], save_iphop_db: typing.Optional[bool], run_bacphlip: typing.Optional[bool], run_pharokka: typing.Optional[bool], pharokka_db: typing.Optional[str], skip_instrain: typing.Optional[bool], instrain_min_ani: typing.Optional[float], instrain_min_mapq: typing.Optional[int], instrain_min_variant_cov: typing.Optional[int], instrain_min_snp_freq: typing.Optional[float], instrain_max_snp_fdr: typing.Optional[int], instrain_min_genome_cov: typing.Optional[float], instrain_popani_thresh: typing.Optional[float], instrain_min_genome_comp: typing.Optional[float], instrain_min_genome_breadth: typing.Optional[float], multiqc_methods_description: typing.Optional[str], assembly_min_length: typing.Optional[int] = 1000, mash_screen_min_score: typing.Optional[float] = 0.95, genomad_min_score: typing.Optional[float] = 0.7, genomad_max_fdr: typing.Optional[float] = 0.1, genomad_splits: typing.Optional[int] = 5, checkv_min_length: typing.Optional[int] = 3000, checkv_min_completeness: typing.Optional[int] = 50, blast_min_percent_identity: typing.Optional[int] = 90, blast_max_num_seqs: typing.Optional[int] = 25000, anicluster_min_ani: typing.Optional[int] = 95, anicluster_min_qcov: typing.Optional[int] = 0, anicluster_min_tcov: typing.Optional[int] = 85, coverm_min_read_alignment: typing.Optional[int] = 0, coverm_min_percent_identity: typing.Optional[int] = 0, coverm_min_percent_read_aligned: typing.Optional[int] = 0, coverm_metrics: typing.Optional[str] = 'mean', iphop_min_score: typing.Optional[int] = 90, logo: typing.Optional[bool] = True) -> None:
    """
    nf-core/phageannotator

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, email=email, multiqc_title=multiqc_title, assembly_min_length=assembly_min_length, run_viromeqc=run_viromeqc, run_reference_containment=run_reference_containment, reference_virus_fasta=reference_virus_fasta, reference_virus_sketch=reference_virus_sketch, save_reference_virus_sketch=save_reference_virus_sketch, mash_screen_min_score=mash_screen_min_score, mash_screen_winner_take_all=mash_screen_winner_take_all, skip_genomad=skip_genomad, genomad_db=genomad_db, save_genomad_db=save_genomad_db, genomad_min_score=genomad_min_score, genomad_max_fdr=genomad_max_fdr, genomad_splits=genomad_splits, run_cobra=run_cobra, cobra_assembler=cobra_assembler, cobra_mink=cobra_mink, cobra_maxk=cobra_maxk, skip_checkv=skip_checkv, checkv_db=checkv_db, save_checkv_db=save_checkv_db, checkv_min_length=checkv_min_length, checkv_min_completeness=checkv_min_completeness, checkv_remove_proviruses=checkv_remove_proviruses, checkv_remove_warnings=checkv_remove_warnings, skip_virus_clustering=skip_virus_clustering, blast_min_percent_identity=blast_min_percent_identity, blast_max_num_seqs=blast_max_num_seqs, anicluster_min_ani=anicluster_min_ani, anicluster_min_qcov=anicluster_min_qcov, anicluster_min_tcov=anicluster_min_tcov, skip_read_alignment=skip_read_alignment, coverm_min_read_alignment=coverm_min_read_alignment, coverm_min_percent_identity=coverm_min_percent_identity, coverm_min_percent_read_aligned=coverm_min_percent_read_aligned, coverm_metrics=coverm_metrics, run_genomad_taxonomy=run_genomad_taxonomy, run_iphop=run_iphop, iphop_db=iphop_db, save_iphop_db=save_iphop_db, iphop_min_score=iphop_min_score, run_bacphlip=run_bacphlip, run_pharokka=run_pharokka, pharokka_db=pharokka_db, skip_instrain=skip_instrain, instrain_min_ani=instrain_min_ani, instrain_min_mapq=instrain_min_mapq, instrain_min_variant_cov=instrain_min_variant_cov, instrain_min_snp_freq=instrain_min_snp_freq, instrain_max_snp_fdr=instrain_max_snp_fdr, instrain_min_genome_cov=instrain_min_genome_cov, instrain_popani_thresh=instrain_popani_thresh, instrain_min_genome_comp=instrain_min_genome_comp, instrain_min_genome_breadth=instrain_min_genome_breadth, multiqc_methods_description=multiqc_methods_description, logo=logo)

