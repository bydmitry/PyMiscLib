import gffutils
from Bio import SeqIO

''' When providing TopHat with a known transcript annotation file (see -G/--GTF option),
a transcriptome sequence file (fasta) is built. Sequence annotations have to be modified to allow 
for further analysis with BitSeq. i) sequense ID must match transcript ID ii) sequence description
must contain gene name in the form of "gene:X...X". '''

### Beforehand: #####
## Import the GTF file into a sqlite3 database.
# db = gffutils.create_db("known.gff", dbfn='known.gtf.db')
## This only ever has to be one once. 


# Connect to the database:
db = gffutils.FeatureDB("known.gtf.db")

# Open fasta file:
record_iterator = SeqIO.parse(open("known.fa", "r"), "fasta")

updated_sequences = []
for record in record_iterator:
    # Split description string & extract transcript_id:
    descrLst      = record.description.split()
    transcriptID  = descrLst[1]
    
    # Check if transcript_id is available in the DB:
    try:
        dbItem    = db[transcriptID]
    except gffutils.exceptions.FeatureNotFoundError:
        print "Transcript NOT found: %s" % transcriptID
        continue

    # Extract gene_id for a given transcript_id:
    geneName      = dbItem.attributes['gene_id'][0]

    # Update sequence description:
    descrLst[0]   = str(transcriptID)
    descrLst[1]   = str("transcript_id:") + str(transcriptID)
    descrLst.append( str("gene:") + str(geneName) )

    # Update record:
    record.description  = " ".join(descrLst)
    record.id           = transcriptID

    updated_sequences.append(record)
 
# Save to a file: 
output_handle = open("updated_ref.fasta", "w")
SeqIO.write(updated_sequences, output_handle, "fasta")
output_handle.close()

###  DONE:  #####

# record = next(record_iterator)

## Note that gene and transcript have been inferred
# print list(db.featuretypes())
## ['CDS', 'exon', 'gene', 'start_codon', 'stop_codon', 'transcript']

