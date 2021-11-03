                
## to remove
import pysam
from sinto import utils


bam="./A.bam"
chrom = utils.get_chromosomes(bam, keep_contigs="^chr")

getFragments(
    interval=('chr20', 1000000),
    bam=bam
)