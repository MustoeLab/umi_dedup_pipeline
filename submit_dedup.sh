#!/usr/bin/bash

#. dedup.sh REP1-7SK-CF-LNA-MOD_S1_L001_R1_001.fastq.gz REP1-7SK-CF-LNA-MOD_S1_L001_R2_001.fastq.gz 7SK
. dedup.sh REP2-7SK-CF-LNA-MOD_S2_L001_R1_001.fastq.gz REP2-7SK-CF-LNA-MOD_S2_L001_R2_001.fastq.gz 7SK /storage/mustoe/home/u246626/concat_7sk_runs/irfana/CF_REP2/ Dedup_MOD_7SK_CF_IRFANA_REP2
. dedup.sh REP1-7SK-LNA1-ph9_S3_L001_R1_001.fastq.gz REP1-7SK-LNA1-ph9_S3_L001_R2_001.fastq.gz 7SK /storage/mustoe/home/u246626/concat_7sk_runs/irfana/IN_CELL/ Dedup_MOD_7SK_INCELL_IRFANA_REP1
. dedup.sh REP2-7SK-LNA1-ph9_S4_L001_R1_001.fastq.gz REP2-7SK-LNA1-ph9_S4_L001_R2_001.fastq.gz 7SK /storage/mustoe/home/u246626/concat_7sk_runs/irfana/IN_CELL_REP2/ Dedup_MOD_7SK_INCELL_IRFANA_REP2
#. dedup.sh REP1-7SK-CF-LNA-MOD_S1_L001_R1_001.fastq.gz REP1-7SK-CF-LNA-MOD_S1_L001_R2_001.fastq.gz 7SK path_to_run_location_including_final_/
