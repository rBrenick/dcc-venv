import os
import sys

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(" req_hand  ")


def create_requirements_dev(requirements_path):
    log.info("#"*50)
    log.info("Creating DEV Requirements from: {}\n".format(requirements_path))
    log.info("-"*50)
    
    requirements_dev_path = requirements_path.replace(".txt", "_DEV.txt")
    
    with open(requirements_path, 'r') as src:  
        with open(requirements_dev_path, 'w') as dest:
            DEV_Start = False
            
            prefix = '-e '  
            suffix = '#egg={}'
            
            for line in src:
                
                output_line = line.rstrip('\n')
                
                if DEV_Start: # Wait until we hit the # DEV line
                    package_name = line.split("/")[-1]
                    output_line = '{}{}{}'.format(prefix, output_line, suffix.format(package_name))
                    
                if line.startswith("# DEV"):
                    DEV_Start = True
                
                log.info(output_line)
                dest.write('{}\n'.format(output_line))
            
    log.info("-"*50)
    log.info("Created: {}".format(requirements_dev_path))
    log.info("#"*50)
    
    return requirements_dev_path
