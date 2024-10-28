import argparse
import subprocess
import os
import shutil
import datetime

def build_fasta_index(fasta, gene):
    cmd = "bowtie2-build "
    cmd += f"-f {fasta} "
    cmd += f"{gene}"

    return cmd

def extract_umis(umi_len, R1, R2, read1umi, read2umi):
    umi = "N" * umi_len
    cmd = "umi_tools extract "
    cmd += f"-p {umi} "
    cmd += f"-I {R1} "
    cmd += f"--read2-in={R2} "
    cmd += f"-S {read1umi} "
    cmd += f"--read2-out={read2umi}"

    return cmd

def align_reads(gene_name, p, R1, R2, output):
    cmd = "bowtie2 "
    cmd += f"-p {p} "
    cmd += "--local "
    cmd += "--sensitive-local "
    cmd += "--mp 3,1 "
    cmd += "--rdg 5,1 "
    cmd += "--rfg 5,1 "
    cmd += "--dpad 30 "
    cmd += "--maxins 800 "
    cmd += "--ignore-quals "
    cmd += "--no-unal "
    cmd += f"-x {gene_name} "
    cmd += f"-1 {R1} "
    cmd += f"-2 {R2} "
    cmd += f"-S {output}"

    return cmd

def sam_to_bam(sam, bam):
    cmd = "samtools "
    cmd += "view -b "
    cmd += f"{sam} "
    cmd += "> "
    cmd += f"{bam}"

    return cmd

def sort_bam(inp, out, by_name=False):
    cmd = "samtools "    
    cmd += "sort "
    cmd += f"{inp} "
    cmd += f"-o {out}"
    if by_name:
        cmd +=  " -n"

    return cmd


def index_bam(bam):
    cmd = "samtools "
    cmd += "index "
    cmd += f"{bam}"

    return cmd

def collapse_umi(bam, dedup):
    cmd = "umicollapse "
    cmd += "bam "
    cmd += "-p .05 "
    cmd += f"-i {bam} "
    cmd += f"-o {dedup} "
    cmd += "--paired"

    return cmd

def bam_to_fastq(bam, fastq):
    cmd = "samtools "
    cmd += f"fastq {bam} "
    cmd += "> "
    cmd += f"{fastq}"

    return cmd

def deinterleave_fastq(interleaved, R1, R2):
    cmd = "python "
    cmd += "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/" + "deinterleaver.py "
    cmd += f"{interleaved} "
    cmd += f"{R1} "
    cmd += f"{R2}"

    return cmd

def trim_header(fastq_in, fastq_out):
    cmd = "python "
    cmd += "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/" + "strip_fastq_headers.py "
    cmd += f"{fastq_in} "
    cmd += f"{fastq_out}"

    return cmd

def copy(f, dest):
    cmd = "cp "
    cmd += f"{f} "
    cmd += f"{dest}"

    return cmd

def run_commands(cmds):
    # for output in cmd 
    for cmd in cmds:
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}---', flush = True)
        print(f"Running {cmd}", flush = True)

        try:
            completed_process = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
        except Exception as e: # Catch error thrown by subprocess module
            handle_exception(e)
        if completed_process.returncode != 0: # Catch error thrown by SHELL
            handle_exception(completed_process)

        else: # Print stout and stderr to stdout and stderr of user
            print(completed_process.stdout.decode('utf-8'), flush=True)
            print(completed_process.stderr.decode('utf-8'), flush=True)

def handle_exception(error):

    if isinstance(error, FileNotFoundError):
        raise FileNotFoundError("Please ensure that all dependencies are installed. ") from error

    elif isinstance(error, Exception):
        raise error

    else: # If not exception, error is a CompletedProcess object housing a stderr attribute

        if "does not exist or is not a Bowtie 2 index" in str(error.stderr) or "Could not locate a Bowtie index" in str(error.stderr):
            raise FileNotFoundError("Fasta file index not found. Ensure the fasta file is bowtie indexed in place. (Can rerun script with --index_fasta)")

        elif "command not found" in str(error.stderr):
            raise FileNotFoundError(f"{error.stderr.decode('utf-8').rstrip()}\nPlease ensure that all dependencies are installed. ")

        else:
            raise Exception(str(error.stderr))

def main(R1, R2, fasta, umi_len, output_prefix, temp, keep_temp, p, index_fasta, disable_header_correction):
    # Ensure R1, R2, fasta exist
    for fl in (R1, R2, fasta):
        if not os.path.exists(fl):
            raise ValueError(f"File: {fl} not found.")

    # Ensure temp file doesn't exist
    try:
        os.mkdir(temp)
    except FileExistsError:
        raise FileExistsError(f"Filename: {temp} already exists. Please either delete this file or submit a different temp file name via --temp.")

    # Naming all temp files
    prefix = temp + "/" + output_prefix
    #gene_name = fasta.split(".")[0].split("/")[-1]
    gene_name = fasta.split(".")[0]

    bowtie_sam = prefix + ".sam"
    bowtie_bam = prefix + ".bam"
    bowtie_bam2 = prefix + "sortedsample.bam"
    dedup = prefix + "sortedsamplededup.bam"
    dedup_by_name = prefix + "sortedsamplebynamededup.bam"
    interleaved = prefix + "_dedup.fastq"
    read1umi = prefix + "_umi_R1.fastq"
    read2umi = prefix + "_umi_R2.fastq"

    pre_final_out_1 = prefix + "_nonstripped_R1.fastq" # Both of the pre files must have headers edited
    pre_final_out_2 = prefix + "_nonstripped_R2.fastq"

    final_out_1 = output_prefix + "_R1.fastq"
    final_out_2 = output_prefix + "_R2.fastq"

    # Generate all commands to run
    cmds = []
    if index_fasta:
        if fasta_index_present(gene_name):
            print("Fasta index already present, skipping indexing.", flush = True)    
        else:
            cmds += [build_fasta_index(fasta, gene_name)]

    cmds += [extract_umis(umi_len, R1, R2, read1umi, read2umi)]
    cmds += [align_reads(gene_name, p, read1umi, read2umi, bowtie_sam)]
    cmds += [sam_to_bam(bowtie_sam, bowtie_bam)]
    cmds += [sort_bam(bowtie_bam, bowtie_bam2)]
    cmds += [index_bam(bowtie_bam2)] 
    cmds += [collapse_umi(bowtie_bam2, dedup)]
    cmds += [sort_bam(dedup, dedup_by_name, by_name = True)]
    cmds += [bam_to_fastq(dedup_by_name, interleaved)]
    cmds += [deinterleave_fastq(interleaved, pre_final_out_1, pre_final_out_2)]

    # Prevent header trimming fix.
    # Necessary to reproduce old results
    # produced prior to patch.
    if disable_header_correction:
        cmds += [copy(pre_final_out_1, final_out_1)]
        cmds += [copy(pre_final_out_2, final_out_2)]

    else:
        cmds += [trim_header(pre_final_out_1, final_out_1)]
        cmds += [trim_header(pre_final_out_2, final_out_2)]

    # Run all cmds
    run_commands(cmds)

    
    if not keep_temp:
        print("Pipeline completed. Deleting temp folder. Use --keep_temp argument to preserve temp folder.")
        shutil.rmtree(temp)

def file_is_index(f, gene_name):
    if f.startswith(gene_name) and f.endswith("bt2"):
        return True

def fasta_index_present(gene):
    spl_gene = gene.split("/")
    if len(spl_gene) > 1: # If gene in a sub directory
        for f in os.listdir(spl_gene[:-1]):
            if file_is_index(f, spl_gene[-1]):
                return True
    else: # If gene in current working directory
        for f in os.listdir("."):
            if file_is_index(f, spl_gene[-1]):
                return True
    

    return False


if __name__ == "__main__":
    # Parse all arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--R1", help = "Read 1 fastq. Contains umis. (Required)", required = True)
    ap.add_argument("--R2", help = "Read 2 fastq. (Required)", required = True)
    ap.add_argument("--fasta", help = "Fasta for aligning reads. Must be bowtie indexed. (Required)", required = True)
    ap.add_argument("--umi_len", type = int, default = 12, help = "Umi length. (default = 12)")
    ap.add_argument("--output_prefix", default="dedup", help = "Name of the output file. (default = dedup)")
    ap.add_argument("--index_fasta", action="store_true", default = False, help = "Index the fasta file. An indexed fasta is required for this script. (Default = False)" )
    ap.add_argument("--temp", default = "temp", help = "Name of temp directory. (default = temp)")
    ap.add_argument("--keep_temp", default=False, action="store_true", help = "Keep the temp files. (Default = False)")
    ap.add_argument("--disable_header_correction", default=False, action="store_true", help = "Disable removal of \1 and \2 suffix from read headers. Necessary to reproduce deduplication / ShapeMapper results produced prior to introduction of header correction (Default = False)")
    ap.add_argument("-p", default = 8, type = int, help = "Number of processors to align with. (Default = 8)")
    pa = ap.parse_args()

    main(pa.R1, pa.R2, pa.fasta, pa.umi_len, pa.output_prefix, pa.temp, pa.keep_temp, pa.p, pa.index_fasta, pa.disable_header_correction)
