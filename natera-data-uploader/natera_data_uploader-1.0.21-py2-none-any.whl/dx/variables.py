#!/usr/bin/env python


class Property(object):
    JOB_ID = "jobId"
    RUN_FOLDER = "runFolder"
    VERSION = "version"
    PRODUCT = "product"
    SAMPLE_REFERENCE = "uploadSampleReference"


class Type(object):
    UPLOAD_DATA = "UploadData"
    UPLOAD_SENTINEL = "UploadSentinel"
    UPLOAD_JOB = "UPLOAD"
    BAM = "bam"
    FASTQ = "fastq"
    CSV = "csv"
    PDF = "pdf"
    XLSX = "xlsx"
    WESQCREPORT = "WESQcReport"


class State(object):
    RUNNING = "running"
    WAITING = "waiting_on_input"
    TERMINATED = "terminated"
    DONE = "done"
    OPEN = "open"
    CLOSING = "closing"
    CLOSED = "closed"
