#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'priska'

'''
A script that enhances slot filling annotations with an additional 
field containing the source sentence these annotations refer to.
'''

import os
import logging

import pandas as pd

from IPython import embed

BASE_PATH           = "/mnt/hdfs/user/priska/tac/"
ANNOTATIONS_DIR     = "TAC_2011_KBP_English_Training_Regular_Slot_Filling_Annotation"
ANNOTATIONS_FILE    = "tac_2010_kbp_training_slot_filling_annotation.tab"
GIGAWORD_DIR        = "LDC2010E12/TAC_2010_KBP_Source_Data/data/2010/wb/"


def extract_and_augment():

    # make filenames
    input_file = os.path.join( BASE_PATH, ANNOTATIONS_DIR, "data", ANNOTATIONS_FILE )
    fname, ext = os.path.splitext( ANNOTATIONS_FILE )
    output_file = os.path.join( BASE_PATH, fname, "_augmented", ext )
    
    log.info( "read annotations from file" )
    annotations = pd.io.parsers.read_table( input_file )

    log.info( "extract sentences from corpus" )
    for idx, docid in enumerate( annotations.get('docid') ):
        corpus_file = os.path.join( BASE_PATH, GIGAWORD_DIR, docid )
        with open( corpus_file, 'r' ) as f:
            text = f.read().replace( "\n", "" )
            sentences.append( text[ annotations.get('start_char')[idx] : annotations.get('end_char')[idx] ])

    log.info( "write enhanced annotations to file" )
    annotations["sentence"] = pd.Series( sentences, index=annotations.index )
    annotations.to_csv( output_file, sep="\t" )

    # sample docIDs:
    # eng-WL-11-174592-12943032
    # NYT_ENG_20080515.0272.LDC2009T13


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    log = logging.getLogger(__name__)

    extract_and_augment()
