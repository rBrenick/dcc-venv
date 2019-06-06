import os
import sys

NORMAL_REQUIREMENTS_PATH = os.path.abspath(sys.argv[1])
DEV_REQUIREMENTS_PATH = NORMAL_REQUIREMENTS_PATH.replace(".txt", "_DEV.txt")

print("#"*50)
print("Creating DEV Requirements from: {}\n".format(NORMAL_REQUIREMENTS_PATH))
print("-"*50)

with open(NORMAL_REQUIREMENTS_PATH, 'r') as src:  
    with open(DEV_REQUIREMENTS_PATH, 'w') as dest:
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
            
            print(output_line)
            dest.write('{}\n'.format(output_line))
            

print("-"*50)
print("Created: {}".format(DEV_REQUIREMENTS_PATH))
print("#"*50)
